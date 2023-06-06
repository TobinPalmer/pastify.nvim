import pynvim


def createCallbackCommand(f, args):
    """
    This is a helper function to use python callbacks nicely -- the way I
    figured out it works, don't know whether that really makes sense or whether
    there's a better way (some pynvim solution I haven't foudn yet?)
    """
    args_str = ", ".join(list(map(str, args)))
    # cut of 'function:' from _nvim_rpc_method_name
    rpc_name = f._nvim_rpc_method_name[9:]
    # wrap it into a vim command that will be called
    return f':call {rpc_name}({args_str})'


@pynvim.plugin
class PynvimExample(object):

    def __init__(self, nvim):
        self.nvim = nvim

        self.configureFromLua()
        # self.configureFromVimL()

    def configureFromLua(self):
        # default config
        self.config = {
                'height': 10,
                }

        # fetch lua config from lua/pynvimExample.lua
        # with this wrapper it's possible to configure this module
        # like a "native" lua module: require('module').setup(config_table)
        cfg = self.nvim.exec_lua('return require("pynvimExample").getConfig()')

        self.config.update(cfg)

    def configureFromVimL(self):

        def getConfigValue(key, default=None):
            return self.nvim.vars.get('PynvimExample_' + key, default)

        # read values from g:PynvimExample_<key>
        self.config = {
                'height': getConfigValue('height', default=10),
                }

    def getOutputWinOptions(self):
        return {'relative': 'win',
                'width': self.nvim.current.window.width,
                'height': self.config['height'],
                'col': 0,
                'row': self.nvim.current.window.height - self.config['height'],
                }

    @pynvim.function('PynvimExampleClose')
    def close(self, args):
        """
        This is a callback handler registered at the bottom of this file

        The same effect could be achieve with just calling ':q' as command
        for the autocmd, but for testing and demonstration purpose...
        """
        assert len(args) == 1
        self.nvim.api.clear_autocmds({'group': 'PynvimExampleAutoCmds'})
        self.nvim.api.win_close(int(args[0]), True)

    @pynvim.command('PynvimExampleRun', nargs='0')
    def run(self, _):
        # === start plugin work: execute current buffer and capture stdout ===
        from io import StringIO
        import sys

        orig_stdout, sys.stdout = sys.stdout, StringIO()
        exec('\n'.join(self.nvim.current.buffer[:]), {})
        sys.stdout, stdoutBuffer = orig_stdout, sys.stdout
        # === end plugin work ===

        # create new buffer and set some options and lines
        buf = self.nvim.api.create_buf(False, True)
        buf.api.set_option('bufhidden', 'wipe')
        buf[:] = stdoutBuffer.getvalue().split('\n')
        buf.api.set_option('modifiable', False)

        # create a window and show the buffer
        win = self.nvim.api.open_win(buf, True, self.getOutputWinOptions())

        # create a callback that will be called on 'WinLeave' for the buffer
        self.nvim.api.create_augroup("PynvimExampleAutoCmds", {'clear': True})

        callback_cmd = createCallbackCommand(self.close, [win.handle])
        self.nvim.api.create_autocmd(['WinLeave'],
                                     {'group': 'PynvimExampleAutoCmds',
                                      'buffer': buf.handle,
                                      'command': callback_cmd})

# import pynvim
# import os
# import tkinter as tk
# import io
# import codecs
# import subprocess
# import json
# from PIL import ImageGrab
#
#
# @pynvim.plugin
# class PasteImage(object):
#     def __init__(self, nvim):
#         self.nvim = nvim
#
#     @pynvim.command('PasteImage', sync=True)
#     def paste_text(self) -> None:
#         img = ImageGrab.grabclipboard()
#         if img is None:
#             print("No image in clipboard")
#             return
#
#         img_bytes = io.BytesIO()
#         img.save(img_bytes, format='PNG')
#         base64_data = codecs.encode(img_bytes.getvalue(), 'base64')
#         base64_text = codecs.decode(base64_data, 'ascii')
#
#         curl_command = f'curl --location --request POST "https://api.imgbb.com/1/upload?expiration=600&key=97d55249779898d0d31f3b4d9915f129" --form "image={base64_text}"'
#
#         output = subprocess.check_output(curl_command, shell=True)
#         json_output = json.loads(output.decode('utf-8'))
#         vim.command(f"normal! i![]({json_output['data']['display_url']})")
