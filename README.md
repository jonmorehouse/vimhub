# Vim Github

> Github Issues from Vim

## Installation

> Only tested for Mac as of now

```
# homebrew vim comes with python 
$ brew install vim 

# installation with vundle
# vimrc:

set rtp+=~/.vim/bundle/vundle/
call vundle#rc()

Plugin 'jonmorehouse/vimhub'

# install all vundle plugins
vim +PluginInstall +qall
```

## Issue List

> Browse issues for any github repository you have access to

```
# browse issues for <your_username>/vim
:Gissues vim 


# browse jonmorehouse/vim
:Gissues jonmorehouse/vim 

```

<img src='http://cl.ly/image/2a0R2M1s080v/temp.png' />

### Navigating an issue list

> Open, create and browse issues

```
# press i to create a new issue
<Normal> i

# press enter to open an issue
<Normal> <ENTER>

# press b to browse an issue in your default browser 
<Normal> b

```



## Open an Issue


## Feature Pipeline

* ability to pass in github-uri for issue creation / issue list
* browse project locally
* pull-request


