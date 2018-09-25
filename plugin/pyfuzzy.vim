
if exists("g:loaded_pyfuzzy")
    finish
endif

let g:loaded_pyfuzzy = 1
if !exists("g:pyfuzzy#usenative")
    let g:pyfuzzy#usenative = 0
endif

