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
  echo "github-issues.vim requires Python support."
  finish
endif

python <<EOF
from os import path as p
import sys
import vim
import imp

# generate path that needs to 
base_path = p.abspath(p.join(vim.eval("expand('<sfile>:p:h')"), "../lib"))
sys.path.insert(0, base_path)

import issue
import issue_list

def reload_vimhub():
  imp.reload(issue)
  imp.reload(issue_list)
EOF

" create issue list
command! -nargs=* Gissues :python issue_list.IssueList.show_issues(<f-args>)

" create a new issue
command! -nargs=* Gissue :python issue.Issue.open(<f-args>)

" reload module
command! VimHubReload :python reload_vimhub()

