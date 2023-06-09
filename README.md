# pastify.nvim

<div align="center">
  <p><strong>Paste screenshots directly into files asynchronously</strong></p>
</div>

Local Saving               |  Online Hosting
:-------------------------:|:-------------------------:
![](./static/gifs/local.gif)  |  ![](./static/gifs/online.gif)

## Requirements

- Neovim 0.8+
- Python3
- Pip3
- For saving images online
  - [Imgbb](https://api.imgbb.com/) api key (free)

## Installation

Make sure Neovim has python3 by running `:checkhealth`, if you have python but it is not linked, run `pip3 install neovim`.
Then, run `pip3 install pillow`.

```lua
return {
  'TobinPalmer/pastify.nvim',
  cmd = { 'Pastify' },
  config = function()
    require('pastify').setup {
      opts = {
        apikey = "YOUR API KEY (https://api.imgbb.com/)", -- Needed if you want to save online.
      },
    }
  end
}
```


## Configuration

These are the default options, you don't need to copy them into `setup()`

```lua
require('pastify').setup {
  opts = {
    local_path = '/assets/imgs/', -- The path to put local files in, ex ~/Projects/<name>/assets/images/<imgname>.png
    save = 'local', -- Either 'local' or 'online'
    apikey = '', -- Api key, required for online saving
  },
  ft = { -- Custom snippets for different filetypes, will replace $IMG$ with the image url
    html = '<img src="$IMG$" alt="">',
    markdown = '![]($IMG$)',
    tex = [[\includegraphics[width=\linewidth]{$IMG$}]],
  },
}
```

## Comparison and similar plugins

| Feature                      | pastify.nvim | img-paste.vim | clipboard-image.nvim |
|------------------------------|--------------|---------------|----------------------|
| Vimscript                    |              | ✅            |                      |
| Async                        | ✅           |               |                      |
| Local                        | ✅           | ✅            | ✅                   |
| Online                       | ✅           |               |                      |
| Highly Customizable          | ✅           |               | ✅                   |
| Custom Snippets For Filetype | ✅           | ✅            | ✅                   |

