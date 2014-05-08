# VimHub

> Github Issues for Vim 

## Installation

This plugin was built on mac and has only been tested with mac for now. However, assuming your vim was included with python 2.7, you shouldn't have any problems. No external python modules are required.

~~~ vim
" vimrc
set rtp+=~/.vim/bundle/vundle/
call vundle#rc()

Plugin 'jonmorehouse/vimhub'
~~~

~~~ sh
# homebrew vim comes with python 
$ brew install vim 

# install all vundle plugins
vim +PluginInstall +qall

# add $GITHUB_TOKEN to your environment
$ export GITHUB_TOKEN="YOUR ACCESS TOKEN"
~~~

Since I haven't solidified all of the features / functionality, I haven't included a custom syntax. I recommend using a markdown syntax plugin to keep things looking nice. 

~~~ vim
" vimrc
Plugin 'tpope/vim-markdown'
~~~

## Issue List

Browse issues for any github repository you have access to

If working on a fork, vimhub will use upstream issues if available.

<img src='http://cl.ly/image/2a0R2M1s080v/temp.png' />

~~~ vim
" browse issues for <your_username>/vim
:Gissues vim 

"# browse jonmorehouse/vim
:Gissues jonmorehouse/vim 

" browse all issues (default state is open)
:Gissues state=all
:Gissues jonmorehouse/vim state=all

~~~


### Available issue list commands

Open, create and browse issues

<img src='http://cl.ly/image/2a0R2M1s080v/temp.png' />

~~~ vim
" press i to create a new issue
<Normal> i

" press enter to open an issue
<Normal> <ENTER>

" press b to browse an issue in your default browser 
<Normal> b
~~~

## Open an Issue

Create or open an issue for editing, viewing and commenting

<img src='http://cl.ly/image/383A0w0U1W2e/temp.png' />

~~~ vim
" open an issue in current repository (if you are working from within a git repository)
:Gissue

" open a specific issue in current repository
:Gissue 3

" open any issue
:Gissue jonmorehouse/vim 5

" open new issue in any project you have access too
:Gissue vim
:Gissue jonmorehouse/vim
~~~



### Available issue commands

~~~ vim
" save current issue
<Normal> s

" open current issue in browser
<Normal> <ENTER>

" toggle open/close issue
<Normal> c
~~~



## Some Upcoming Features

> Feel free to open an issue for anything that seems relevant for this plugin

1. More detailed github issues (information on pull requests, open/close states etc) 
2. Pull Requests - create/merge pull requests
3. Milestones - create,edit,open,close milestones 
4. Omnicomplete (for milestones, and issues)
5. Ability to auto-guess repos that are in your organization.

