local M = {}

---@class plug_opts
---@field absolute_path boolean
---@field apikey string?
---@field local_path string|function?
---@field save "local_file"|"local"|"online"
---@field filename string|function?
---@field default_ft string

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
    filename = '',
    default_ft = 'markdown',
  },
  ft = {
    html = '<img src="$IMG$" alt="$NAME$">',
    markdown = '![$NAME$]($IMG$)',
    tex = [[\includegraphics[width=\linewidth]{$IMG$}]],
    css = 'background-image: url("$IMG$");',
    js = 'const img = new Image(); img.src = "$IMG$";',
    xml = '<image src="$IMG$" />',
    php = '<?php echo "<img src="$IMG$" alt="$NAME$">"; ?>',
    python = '# $IMG$',
    java = '// $IMG$',
    c = '// $IMG$',
    cpp = '// $IMG$',
    swift = '// $IMG$',
    kotlin = '// $IMG$',
    go = '// $IMG$',
    typescript = '// $IMG$',
    ruby = '# $IMG$',
    vhdl = '-- $IMG$',
    verilog = '// $IMG$',
    systemverilog = '// $IMG$',
    lua = '-- $IMG$',
  },
}

local imagePathRule
local fileNameRule

M.getConfig = function()
  imagePathRule = M.config.opts.local_path
  fileNameRule = M.config.opts.filename
  M.config.opts.local_path = nil
  M.config.opts.filename = nil
  return M.config
end

M.getFileName = function()
  if type(fileNameRule) == 'function' then
    return fileNameRule()
  end
  return fileNameRule
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

    command! -range Pastify python3 image.paste_text(0)
    command! -range PastifyAfter python3 image.paste_text(1)
  ]]
end

---@param params config
M.setup = function(params)
  M.config = vim.tbl_deep_extend('force', {}, M.config, params)
  create_command()
end

return M
