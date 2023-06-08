local M = {}

---@class plug_opts
---@field computer boolean
---@field default_name string
---@field local_path string
---@field markdown_image boolean
---@field markdown_standard boolean
---@field online boolean
---@field apikey string?

---@class config
---@field options plug_opts
---@type config
M.config = {
  options = {
    computer = true,
    default_name = 'image',
    local_path = '/assets/imgs/',
    markdown_image = false,
    markdown_standard = true,
    online = false,
    apikey = '',
  },
}

M.getConfig = function()
  return M.config
end

function PasteTextAsync()
  vim.schedule(function()
    vim.api.nvim_command "lua require'paste_image.main'.PasteImage():paste_text()"
  end)
end

vim.api.nvim_command 'command! PasteAsLink lua PasteAsLink()'

local function create_command()
  if not vim.fn.exists 'python3' then
    print 'cannot find python3, returning [paste-image.nvim]'
    return
  end

  -- Set the runtime path to ./rplugin
  vim.cmd [[
    python3 import paste_image.main
    python3 image = paste_image.main.PasteImage()

    command! PasteAsLink python3 image.paste_text()
  ]]
end

---@param params config
M.setup = function(params)
  M.config = vim.tbl_deep_extend('force', {}, M.config, params or {})
  create_command()
end

return M
