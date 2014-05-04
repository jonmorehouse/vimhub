import imp

try: 
    imp.find_module("vim")
    test = False
    import vim
except ImportError:
    import os
    test = True


# now initialize elements
if not test:
    api_url = vim.eval("g:github_api_url")
    access_token = vim.eval("g:github_access_token")
    upstream_isses = vim.eval("g:github_upstream_issues")
    max_api_pages = vim.eval("g:github_max_api_pages")
    debug = vim.eval("g:github_debug")

else: # test environment
    access_token = os.environ["GITHUB_TOKEN"]
    api_url = "https://api.github.com"
    upstream_issues = True
    # test repository for all local testing
    test_repo_path = os.path.expandvars("$HOME/Desktop/issues")
    max_api_pages = 1000
    debug = True


