local M = {}

---@class plug_opts
---@field absolute_path boolean
---@field apikey string?
---@field local_path string
---@field save "local"|"online"

---@class config
---@field opts plug_opts
---@field ft table<string, string>

---@type config
M.config = {
  opts = {
    absolute_path = false,
    apikey = '',
    local_path = '/assets/imgs/',
    save = 'local',
  },
  ft = {
    html = '<img src="$IMG$" alt="">',
    markdown = '![]($IMG$)',
    tex = [[\includegraphics[width=\linewidth]{$IMG$}]],
  },
}

local imagePathRule

M.getConfig = function()
  imagePathRule = M.config.opts.local_path
  M.config.opts.local_path = nil
  return M.config
end

M.createImagePathName = function()
  if type(imagePathRule) == 'function' then
    return imagePathRule()
  end
  return imagePathRule
end

local function create_command()
  if not vim.fn.exists 'python3' then
    print 'Make sure python3 is installed for pastify.nvim to work.'
    return
  end

  vim.cmd [[
    python3 import pastify.main
    python3 image = pastify.main.Pastify()

    command! Pastify python3 image.paste_text()
  ]]
end

---@param params config
M.setup = function(params)
  M.config = vim.tbl_deep_extend('force', {}, M.config, params)
  create_command()
end

return M
