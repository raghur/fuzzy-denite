from ..base import Base
import os
import logging
import hashlib
import subprocess
import time
import grpc
import sys
import api_pb2_grpc
import api_pb2

logger = logging.getLogger()
level = os.environ.get("NVIM_PYTHON_LOG_LEVEL", "WARNING")
logger.setLevel(logging.getLevelName(level))
logger.info("Loading fuzzy-denite")
logger.debug("GOFUZZY sys.path is %s" % sys.path)


class Filter(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'matcher/gofuzzy'
        self.description = 'go fuzzy matcher'

        self._initialized = False
        self._disabled = False
        self.proc = None
        self.debug("[%s] Loaded matcher/gofuzzy" % time.time())

    def _startProcess(self):
        if not self._initialized:
            # start the server here
            self.debug("[%s] starting fuzzy-denite GRPC server" % (time.time()))
            self.proc = subprocess.Popen(['fuzzy-denite', '--log', 'info',
                                          'server', '-p', '51000', '--grpc'])
            self.debug("[%s] pid: %s" % (time.time(), self.proc.pid))
            self.conn = grpc.insecure_channel('localhost:51000')
            self.service = api_pb2_grpc.FuzzyStub(self.conn)
            self._initialized = True

    def _reapProcess(self):
        if self.proc:
            exitcode = self.proc.poll()
            self.debug("Process exited with code %s" % exitcode)


    def filter(self, context):

        if not context['candidates'] or not context[
                'input'] or self._disabled:
            return context['candidates']

        self._startProcess()

        def getCandidate(s):
            for i in context['candidates']:
                if i['word'] == s:
                    return i

        # ispath = (os.path.exists(context['candidates'][0]['word']))
        status, reason, result = self._get_fuzzy_results(
            context['candidates'], context['input'])
        if result is not None:
            # logging.debug("2GREPME....")
            # logging.debug(len(result))
            # logging.debug(result)
            return [x for x in map(getCandidate, result)]
        else:
            # just return the current list as is.. if this is due to 
            # the server not running, then when the user types the next
            # chars, the server will be started
            self.error_message(context, "gofuzzy error: %s - %s" % (status, reason))
            return [x for x in context['candidates']]

    def _get_fuzzy_results(self, candidates, pattern):
        items = [d['word'] for d in candidates]
        items.sort()
        md5sum = hashlib.md5("".join(items).encode("utf8")).hexdigest()

        try:
            # just send cid & let server tell us if data is not available.
            reply = self.service.Match(
                                    api_pb2.FuzzyRequest(
                                        cid=md5sum,
                                        qry=pattern,
                                        max=20,
                                        algo="fuzzy",
                                        data=[]))
            if reply.code == 400:
                reply = self.service.Match(
                                    api_pb2.FuzzyRequest(
                                        cid=md5sum,
                                        qry=pattern,
                                        max=20,
                                        algo="fuzzy",
                                        data=items))

            if reply.code != 200:
                return reply.code, reply.msg, None
            else:
                return reply.code, reply.msg, reply.match
        except grpc.RpcError as ex:
            self._reapProcess()
            self._initialized = False
            self.debug("Exception in gofuzzy - \n %s" % ex)
            return 200, "Ok", items
