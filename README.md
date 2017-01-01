## Introduction
This is a my first vim plugin to implement a simple function: using online **Bing** dictionary to translate **English** to **Chinese** and vice verse! 

The main intention why I wrote this plugin is for practicing and learning how to use Python in Vimscript. I'm sorry that **You Cannot** get other languages translation from it since there is no free dictionary API available. 

## Installation

Copy **plugin** direction into your **~/.vim/plugin** or use plugin management, such as: **[Vundle](https://github.com/VundleVim/Vundle.vim)**

## Usage

You need to map your favor keys for the below three functions:

* Look up the word under the cursor, the map key looks like:

  ```vim
  nnoremap <leader>lw :call dict#LookupCWord()<cr>
  ```
  
* Look up you inputted English text, the map key looks like:

  ```vim
  nnoremap <leader>lei :call dict#LookupEnglish()<cr>
  ```
  
* Look up you inputted Chinese text, the map key looks like:

  ```vim
  nnoremap <leader>lci :call dict#LookupChinese()<cr>
  ```
