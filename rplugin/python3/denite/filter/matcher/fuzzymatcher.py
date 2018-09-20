
from ..base import Base
import os
import sys
import logging

logger = logging.getLogger()
pkgPath = os.path.dirname(__file__).split(os.path.sep)[:-3]
pkgPath = os.path.sep.join(pkgPath)
if pkgPath not in sys.path:
    logger.debug("added %s to sys.path" % pkgPath)
    sys.path.insert(0, pkgPath)

from pyfuzzy import fuzzyMatches, scoreMatches


class Filter(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'matcher/pyfuzzy'
        self.description = 'py fuzzy matcher'

    def filter(self, context):
        if not context['candidates'] or not context['input']:
            return context['candidates']
        candidates = context['candidates']
        items = (d['word'] for d in candidates)
        qry = context['input']
        results = scoreMatches(fuzzyMatches(qry, items, 10), 10)
        # self.debug("results %s" % results)
        resultItems = set([w[0] for w in results])
        rset =  [c for c in candidates if c['word'] in resultItems]
        # self.debug("rset %s" % rset)
        return rset
