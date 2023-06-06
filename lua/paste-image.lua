local M = {}

---@class plug_opts

---@class config

---@type config
M.config = {
  options = {},
}

local function create_command()
  if not vim.fn.exists 'python3' then
    print 'cannot find python3, returning (paste-image.nvim)'
    return
  end

  -- Set the runtime path to ./rplugin
  vim.cmd [[
    " python3 import paste_image.main
    " python3 image = paste_image.main.PasteImage()
    "
    " command! PasteAsLink python3 image.paste_text()
  ]]

  vim.keymap.set('n', '<C-V>', '<CMD>PasteAsLink<CR>')
end

---@param params config
M.setup = function(params)
  M.config = vim.tbl_deep_extend('force', {}, M.config, params or {})
  create_command()
end

return M
