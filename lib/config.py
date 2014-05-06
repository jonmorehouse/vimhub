import os

try:
    import vim
except ImportError:
    vim = False

update_interval = 2 # minutes between updates

# now initialize elements
if vim:
    api_url = vim.eval("g:github_api_url")
    access_token = vim.eval("g:github_access_token")
    upstream_issues = vim.eval("g:github_upstream_issues")
    max_api_pages = int(vim.eval("g:github_max_api_pages"))
    same_window = vim.eval("g:github_same_window")

else: # test environment
    access_token = os.environ["GITHUB_TOKEN"]
    api_url = "https://api.github.com"
    upstream_issues = True
    # test repository for all local testing
    repo_path = os.path.expandvars("$HOME/Desktop/issue-test")
    repo_uri = "jonmorehouse/issues"
    max_api_pages = 1000
    debug = True
    same_window = False

