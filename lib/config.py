import os

try:
    import vim
except ImportError:
    vim = False

api_url = "https://api.github.com"
access_token = os.environ["GITHUB_TOKEN"]
max_api_pages = 1000
upstream_issues = True

# now initialize elements
if vim:
    api_url = vim.eval("g:github_api_url")
    max_api_pages = int(vim.eval("g:github_max_api_pages"))
    same_window = vim.eval("g:github_same_window")

else: # test environment
    upstream_issues = True
    # test repository for all local testing
    repo_path = os.path.expandvars("$HOME/Desktop/issue-test")
    repo_uri = "jonmorehouse/issues"
    debug = True
    same_window = False

