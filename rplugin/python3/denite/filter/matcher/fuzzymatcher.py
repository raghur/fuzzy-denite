
from ..base import Base
from denite.util import convert2fuzzy_pattern
import os
import sys
import logging

logger = logging.getLogger()
pkgPath = os.path.dirname(__file__).split(os.path.sep)[:-3]
pkgPath = os.path.sep.join(pkgPath)
if pkgPath not in sys.path:
    logger.debug("added %s to sys.path" % pkgPath)
    sys.path.insert(0, pkgPath)

from pyfuzzy import scoreMatches


class Filter(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'matcher/pyfuzzy'
        self.description = 'py fuzzy matcher'

    def filter(self, context):
        if not context['candidates'] or not context['input']:
            return context['candidates']
        candidates = context['candidates']
        qry = context['input']
        # self.debug("candidates %s %s" % (qry, len(candidates)))
        results = scoreMatches(qry, candidates, 10, key=lambda x: x['word'])
        rset = [w[0] for w in results]
        # self.debug("rset %s" % rset)
        return rset

    def convert_pattern(self, input_str):
        # return convert2fuzzy_pattern(input_str)
        p = convert2fuzzy_pattern(input_str)
        # self.debug("pattern: %s : %s" % (input_str, p))
        return p
