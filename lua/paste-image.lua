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

function PasteTextAsync()
  vim.schedule(function()
    vim.api.nvim_command "lua require'paste_image.main'.PasteImage():paste_text()"
  end)
end

vim.api.nvim_command 'command! PasteAsLink lua PasteAsLink()'

local function dump(o)
  if type(o) == 'table' then
    local s = '{ '
    for k, v in pairs(o) do
      if type(k) ~= 'number' then
        k = '"' .. k .. '"'
      end
      s = s .. '[' .. k .. '] = ' .. dump(v) .. ','
    end
    return s .. '} '
  else
    return tostring(o)
  end
end

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
  M.config = vim.tbl_deep_extend('force', {}, M.config, params)
  create_command()
end

return M
