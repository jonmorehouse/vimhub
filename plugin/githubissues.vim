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
import os
import sys
sys.path.append(os.path.expandvars("$HOME/Documents/programs/vim-github"))
from lib.issue_list import IssueList 
from lib.issue import Issue
EOF

" create issue list
command! -nargs=* Gissues :python IssueList.show_issues(<f-args>)

" create a new issue
command! -nargs=* Gissue :python Issue.show_issue(<f-args>)


