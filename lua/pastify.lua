local M = {}

---@class plug_opts
---@field local_path string
---@field save "local"|"online"
---@field apikey string?

---@class config
---@field opts plug_opts
---@field ft table<string, string>

---@type config
M.config = {
  opts = {
    local_path = '/assets/imgs/',
    save = 'local',
    apikey = '',
  },
  ft = {
    html = '<img src="$IMG$" alt="">',
    markdown = '![]($IMG$)',
    tex = [[\includegraphics[width=\linewidth]{$IMG$}]],
  },
}

M.getConfig = function()
  return M.config
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
