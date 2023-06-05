local M = {}

---@class plug_opts

---@class config

---@type config
M.config = {
  options = {},
}

local function create_command()
  if not vim.fn.exists 'python3' then
    return
  end

  vim.cmd [[
    python3 import paste_image.main
    python3 finder = paste_image.main.Finder()

    command! FindTest python3 finder.find()
  ]]
end

---@param params config
M.setup = function(params)
  M.config = vim.tbl_deep_extend('force', {}, M.config, params or {})
  create_command()
end

return M
