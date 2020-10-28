function! s:TestSnippets()
  if s:first_run == 1
    s:first_run = 0
    return { 'foo': { 'description': 'first' } }
  else
    return { 'foo2': { 'description': 'second' } }
  endif
endfunction


function! UltiSnips#SnippetsInCurrentScope( num )
  let ulti_func = get( s:, 'ultisnips_func' )
  if ulti_func
    return ulti_func
  else
    return {}
  endif
endfunction


function! UltiSnips#Enable()
  let s:first_run = 1
  let s:ultisnisp_func = funcref( 's:TestSnippets' )
endfunction


function! UltiSnips#Disable()
  unlet s:first_run
  unlet s:ultisnips_func
endfunction
