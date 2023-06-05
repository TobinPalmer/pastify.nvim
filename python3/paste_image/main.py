import vim
import os
import tkinter as tk
import io
import codecs
import subprocess
import json

from PIL import ImageGrab

class Finder:
    def test(self) -> None:
        print("hello world")
        img = ImageGrab.grabclipboard()
        if img is None:
            print("no image in clipboard")
            return

        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        base64_data = codecs.encode(img_bytes.getvalue(), 'base64')
        base64_text = codecs.decode(base64_data, 'ascii')

        curl_command = f'curl --location --request POST "https://api.imgbb.com/1/upload?expiration=600&key=97d55249779898d0d31f3b4d9915f129" --form "image={base64_text}"'

        output = subprocess.check_output(curl_command, shell=True)
        json_output = json.loads(output.decode('utf-8'))
        vim.command(f"normal! i![]({json_output['data']['display_url']})")

