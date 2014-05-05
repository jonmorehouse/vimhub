if !exists("g:github_access_token")
  let g:github_access_token = ""
endif

if !exists("g:github_upstream_issues")
  let g:github_upstream_issues = 0
endif

if !exists("g:github_api_url")
  let g:github_api_url = "https://api.github.com/"
endif

if !exists("g:github_max_api_pages")
  let g:github_max_api_pages = 1
endif

" force issues and what not to stay in the same window
if !exists("g:github_same_window")
  let g:github_same_window = 0
endif

