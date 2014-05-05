" File:        github-issues.vim
" Version:     3.0.0b
" Description: Pulls github issues into Vim
" Maintainer:  Jonathan Warner <jaxbot@gmail.com> <http://github.com/jaxbot>
" Homepage:    http://jaxbot.me/
" Repository:  https://github.com/jaxbot/github-issues.vim
" License:     Copyright (C) 2014 Jonathan Warner
"              Released under the MIT license
"        ======================================================================

" do not load twice
if exists("g:github_issues_loaded") || &cp
  finish
endif

let g:github_issues_loaded = 1

" do not continue if Vim is not compiled with Python2.7 support
if !has("python")
  echo "github-issues.vim requires Python support, sorry :c"
  finish
endif

python <<EOF
import os
import sys
sys.path.append(os.path.expandvars("$HOME/Documents/programs/github-issues.vim/lib"))
import lib as l
EOF

" build out mappings / shortcuts as needed
" show issue
command

" create issue
command Gissues :python l.issue_list.IssueList()






if !exists("g:github_access_token")
  let g:github_access_token = ""
endif

if !exists("g:github_upstream_issues")
  let g:github_upstream_issues = 0
endif

if !exists("g:github_issues_urls")
  let g:github_issues_urls = ["github.com:", "https://github.com/"]
endif

if !exists("g:github_api_url")
  let g:github_api_url = "https://api.github.com/"
endif

if !exists("g:github_issues_max_pages")
  let g:github_issues_max_pages = 1
endif

" force issues and what not to stay in the same window
if !exists("g:github_same_window")
  let g:github_same_window = 0
endif

