from .type import Config
from .validate import validate_config
from PIL import ImageGrab
from asyncio import create_task, create_subprocess_shell, subprocess
from codecs import encode, decode
from io import BytesIO
from json import loads
from os import makedirs, path
from secrets import token_urlsafe
from typing import Literal
import vim  # type: ignore


class PasteImage(object):
    def __init__(self) -> None:
        self.nonce: str = token_urlsafe()
        self.config: Config = vim.exec_lua(
            'return require("paste-image").getConfig()')
        self.path: str = vim.exec_lua('return vim.fn.getcwd()')

    def logger(
            self, msg: str, level: Literal["WARN", "INFO", "ERROR"]
    ) -> None:
        vim.command(
            f'lua vim.notify("{msg}", vim.log.levels.{level or "INFO"})')

    def paste_text(self) -> None:
        options = self.config['options']
        img = ImageGrab.grabclipboard()
        if img is None:
            self.logger(
                "No image in clipboard.", "WARN")
            return
        if not validate_config(self.config, self.logger):
            self.logger(
                "Your config has an issue, please fix it.", "WARN")
            return

        file_name = ""

        if options['computer']:
            file_name = vim.exec_lua("return vim.fn.input('File Name? ', '')")
            if file_name == "":
                self.logger("No file name provided.", "WARN")
                return

            if file_name.endswith(".png"):
                file_name = file_name[:-4]

            if file_name.startswith("/"):
                file_name = file_name[1:]

            if path.exists(
                    f"{self.path}{options['local_path']}{file_name}.png"):
                self.logger("File already exists.", "WARN")
                return

        img_bytes = BytesIO()
        img.save(img_bytes, format="PNG")
        placeholder_text = ""
        if self.config['options']['computer']:
            assets_path = f"{self.path}{options['local_path']}"
            placeholder_text = f"{assets_path}{file_name}.png"
            if not path.exists(assets_path):
                makedirs(assets_path)
            img.save(placeholder_text, "PNG")
        else:
            base64_data = encode(img_bytes.getvalue(), 'base64')
            base64_text = decode(base64_data, 'ascii')

            placeholder_text = f"Upload In Progress... {self.nonce}"
            create_task(self.get_image(base64_text, placeholder_text))

        if options['markdown_image']:
            vim.command(f"normal! i<img src='{placeholder_text} />'")
        else:
            vim.command(f"normal! i![]({placeholder_text})")

    async def get_image(self, base64_text: str, placeholder_text: str) -> None:
        import re
        curl_command = f'curl --location --request POST \
                "https://api.imgbb.com/1/upload?key={self.config["options"]["apikey"]}"\
                --form "image={base64_text}"'

        process = await create_subprocess_shell(
            curl_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        output, _ = await process.communicate()
        result = re.escape(loads(output.decode('utf-8'))
                           ['data']['url']).replace('/', r'\/')

        vim.command(f"%s/{placeholder_text}/{result}/g")
        self.replace_placeholder(placeholder_text, result)

    def replace_placeholder(self, placeholder_text: str, result: str) -> None:
        vim.command(f"%s/{placeholder_text}/{result}/g")
