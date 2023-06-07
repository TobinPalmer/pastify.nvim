import vim
import asyncio
import io
import codecs
import json
import secrets
from PIL import ImageGrab


class PasteImage(object):
    def __init__(self):
        self.nonce = secrets.token_urlsafe()

    def paste_text(self) -> None:
        img = ImageGrab.grabclipboard()
        if img is None:
            print("No image in clipboard")
            return

        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        base64_data = codecs.encode(img_bytes.getvalue(), 'base64')
        base64_text = codecs.decode(base64_data, 'ascii')

        placeholder_text = f"Upload In Progress... {self.nonce}"
        vim.command(f"normal! i![]({placeholder_text})")

        asyncio.create_task(self.get_image(base64_text, placeholder_text))

    async def get_image(self, base64_text: str, placeholder_text: str):
        import re
        curl_command = f'curl --location --request POST "https://api.imgbb.com/1/upload?expiration=600&key=97d55249779898d0d31f3b4d9915f129" --form "image={base64_text}"'

        process = await asyncio.create_subprocess_shell(
            curl_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        output, _ = await process.communicate()
        result = re.escape(json.loads(output.decode('utf-8'))
                           ['data']['url']).replace('/', r'\/')
        # vim.command(f"norm! i{result}")

        vim.command(f"%s/{placeholder_text}/{result}/g")
        self.replace_placeholder(placeholder_text, result)

    def replace_placeholder(self, placeholder_text: str, result: str):
        # Replace the placeholder text with the result
        vim.command(f"%s/{placeholder_text}/{result}/g")
