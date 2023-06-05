local M = {}

---@class plug_opts

---@class config

---@type config
M.config = {
  options = {},
}

local function buffer_to_file()
  -- Assuming you have a Neovim instance and a buffer object called 'buf'

  -- Redirect the register content to a temporary file
  vim.cmd [[redir! > /Users/tobin/clip.png']]

  -- Paste the register content
  vim.api.nvim_command 'silent! normal! "+p'

  -- Stop the redirection
  vim.cmd [[redir END]]

  -- Read the temporary file
  local file = io.open('/Users/tobin/clip.png', 'rb')
  local clipboardContent = file:read '*a'
  if file == nil then
    return
  end
  file:close()

  -- Print the clipboard content
  print(clipboardContent)
end

local function create_command() end

---@param params config
M.setup = function(params)
  M.config = vim.tbl_deep_extend('force', {}, M.config, params or {})
end

return M
