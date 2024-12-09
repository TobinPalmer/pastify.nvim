from .type import Config
from .validate import validate_config
from PIL import ImageGrab
from asyncio import create_task, create_subprocess_shell, subprocess
from codecs import encode, decode
from io import BytesIO
from json import loads
from os import makedirs, path
import time
from secrets import token_urlsafe
from typing import Literal
import vim  # type: ignore


class Pastify(object):
    def __init__(self) -> None:
        self.nonce: str = token_urlsafe()
        self.config: Config = vim.exec_lua('return require("pastify").getConfig()')

    def logger(self, msg: str, level: Literal["WARN", "INFO", "ERROR"]) -> None:
        vim.command(f'lua vim.notify("{msg}", vim.log.levels.{level or "INFO"})')

    def get_path(self, relative: bool = False):
        file_path = ""
        if relative:
            # image should be created in the same directory as the current file_path
            file_path = path.dirname(vim.exec_lua('return vim.fn.expand("%:p")'))
        else:
            file_path = path.normpath(vim.exec_lua("return vim.fn.getcwd()"))
        # Sanitize the path to guarantee absolute path and return
        return path.abspath(file_path)

    def get_image_path_name(self, relative: bool = False):
        image_path_name: str = vim.exec_lua(
            'return require("pastify").createImagePathName()'
        )
        return path.normpath("./" + image_path_name)

    def get_file_name(self):
        return vim.exec_lua('return require("pastify").getFileName()')

    def paste_text(self, after) -> None:
        img = ImageGrab.grabclipboard()
        # ImageGrab.grabclipboard returns either a: Image, List of file names or None (text)
        if img is None:
            # Get text from clipboard instead
            if after:
                vim.command('normal! "+p')
            else:
                vim.command('normal! "+P')
            return

        options = self.config["opts"]

        # Filetype should be run each time for each new buffer
        filetype: str = vim.exec_lua("return vim.bo.filetype")

        # The path should be re-run for each paste in case the buffer path changed
        if options["save"] == "local_file":
            local_path: str = self.get_path(True)
        else:
            local_path: str = self.get_path(False)

        if not validate_config(
            self.config,
            self.logger,
            filetype,
        ):
            return

        file_name = self.get_file_name()  # file name can be determined by lua

        if options["save"] in ["local", "local_file"]:
            if file_name == "":
                file_name = vim.exec_lua("return vim.fn.input('File Name? ', '')")

            file_name = path.basename(file_name)

            if file_name == "":
                self.logger("No file name provided.", "WARN")
                timestamp = int(time.time())
                file_name = f"image_{timestamp}"

            if path.exists(
                path.join(local_path, self.get_image_path_name(), f"{file_name}.png")
            ):
                self.logger("File already exists.", "WARN")
                return

        img_bytes = BytesIO()
        img.save(img_bytes, format="PNG")
        placeholder_text = ""
        if self.config["opts"]["save"] in ["local", "local_file"]:
            assets_path = path.abspath(
                path.join(local_path, self.get_image_path_name())
            )

            abs_img_path = path.join(assets_path, f"{file_name}.png")

            if not path.exists(assets_path):
                makedirs(assets_path)

            if not self.config["opts"]["absolute_path"]:
                self.logger("Assets path is: " + str(repr(assets_path)), "INFO")
                self.logger("Local path is: " + str(repr(local_path)), "INFO")
                current_file_path = path.dirname(
                    vim.exec_lua('return vim.fn.expand("%:p")')
                )
                assets_path = path.relpath(assets_path, current_file_path)
                self.logger("Relative path is: " + str(repr(assets_path)), "INFO")
            placeholder_text = path.join(assets_path, f"{file_name}.png")
            img.save(abs_img_path, "PNG")
        else:
            base64_data = encode(img_bytes.getvalue(), "base64")
            base64_text = decode(base64_data, "ascii")

            placeholder_text = f"Upload In Progress... {self.nonce}"
            create_task(self.get_image(base64_text, placeholder_text))

        if filetype not in self.config["ft"]:
            filetype = self.config["opts"]["default_ft"]
        pattern = (
            self.config["ft"][filetype]
            .replace("$IMG$", placeholder_text)
            .replace("$NAME$", file_name)
        )
        # check if we're in visual mode to run a different command
        if vim.eval("mode()") in ["v", "V", ""]:
            vim.command(f"normal! c{pattern}")
        else:
            if after:
                vim.command(f"normal! a{pattern}")
            else:
                vim.command(f"normal! i{pattern}")

    async def get_image(self, base64_text: str, placeholder_text: str) -> None:
        import re

        curl_command = f'curl --location --request POST \
                "https://api.imgbb.com/1/upload?key={self.config["opts"]["apikey"]}"\
                --form "image={base64_text}"'

        process = await create_subprocess_shell(
            curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        output, _ = await process.communicate()

        result = re.escape(loads(output.decode("utf-8"))["data"]["url"]).replace(
            "/", r"\/"
        )

        vim.command(f"%s/{placeholder_text}/{result}/g")
