" =============================================================================
" File:         dict.vim
" Description:  Use online Bing dictionary to translate english to chinese and
"               vice verse
" Maintainer:   esc.chao@gmail.com
" License:      Apache 2.0
" =============================================================================
function! dict#LookupWord()
let g:plugin_path = expand('<sfile>:p:h')
let s:True = 1
let s:False = 0

" Call python to lookup text through online Bing dictionary
function! dict#Lookup(text, isE2C)
python << endpython

import os
import sys
import vim

pluginPath = vim.eval("g:plugin_path")
sys.path.append(pluginPath)

from translator import Translator

text = vim.eval("a:text")
isE2C = int(vim.eval("a:isE2C"))

t = Translator()
if (isE2C > 0):
    t.translateE2C(text)
else:
    t.translateC2E(text)

print("{}".format(text))
isTranslated = False

# print phonetic, only English words
if (isE2C > 0 and t.result['phonetic'] != None):
    isTranslated = True
    print("{}".format(t.result['phonetic']))

# print meanings of text
if (t.result['meaning'] != None):
    isTranslated = True
    print ("{}".format('\n'.join(t.result['meaning'])))

# print web meaning of text.
if (t.result['web'] != None):
    isTranslated = True
    print("{}".format(t.result['web']))

if (not isTranslated):
    print("Can't translate text!")

endpython
endfunction

" lookup the word under current cursor
function! dict#LookupCWord()
    let s:cword = expand("<cword>")
    echo "\r"
    call dict#Lookup(s:cword, s:True)
endfunction

" lookup user inputted English text
function! dict#LookupEnglish()
    let words = input('>')
    echo "\r"
    call dict#Lookup(words, s:True)
endfunction

" lookup user inputted Chinese text
function! dict#LookupChinese()
    let words = input('>')
    echo "\r"
    call dict#Lookup(words, 0)
endfunction
