rem
rem 設定個人 VIM 環境
rem

set src=D:\stxt\config\vim
set dst=C:\vim

copy _vimrc %dst%

if not exist %dst%\vimfiles mkdir %dst%\vimfiles

copy %src%\format.vim %dst%\vimfiles

if not exist %dst%\vimfiles\ftdetect mkdir %dst%\vimfiles\ftdetect

copy %dst%\vimfiles\ftdetect\
