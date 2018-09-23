import test


c = {'abbr':
 '~/code/go/src/github.com/raghur/fuzzy-denite/rplugin/python3/denite/filter/matcher/fuzzymatcher.py',
 'source_name': 'file_mru',
 'word':
 '~/code/go/src/github.com/raghur/fuzzy-denite/rplugin/python3/denite/filter/matcher/fuzzymatcher.py',
 'source_index': 0,
 'action__path': '/home/raghu/code/go/src/github.com/raghur/fuzzy-denite/rplugin/python3/denite/filter/matcher/fuzzymatcher.py'}

print(test.scoreMatches([c]))
