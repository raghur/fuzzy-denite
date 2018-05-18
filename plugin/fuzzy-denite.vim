if exists("g:loaded_fuzzy_denite")
    finish
endif

let g:loaded_fuzzy_denite = 1

function! s:installFuzzyDenite()
    " just running ./install doesn't work on windows.
    " form full path and call.
    let out = system(getcwd() . "/install")
endfunction
command! -nargs=0 FuzzyDeniteInstall call s:installFuzzyDenite()
