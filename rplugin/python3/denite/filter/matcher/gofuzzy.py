from ..base import Base
import os
import logging
import hashlib
import subprocess
import time
import grpc
import sys

logger = logging.getLogger()
level = os.environ.get("NVIM_PYTHON_LOG_LEVEL", "WARNING")
logger.setLevel(logging.getLevelName(level))
logger.info("Loading fuzzy-denite")
logger.debug("GOFUZZY sys.path is %s" % sys.path)
pkgPath = os.path.dirname(__file__).split(os.path.sep)[:-3]
pkgPath = os.path.sep.join(pkgPath)
if pkgPath not in sys.path:
    logger.debug("added %s to sys.path" % pkgPath)
    sys.path.insert(0, pkgPath)
binDir = os.path.dirname(__file__).split(os.path.sep)[:-5]
binDir = binDir + ["bin", "fuzzy-denite"]
exe = os.path.sep.join(binDir)
import api_pb2_grpc
import api_pb2


class Filter(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'matcher/gofuzzy'
        self.description = 'go fuzzy matcher'

        self._initialized = False
        self._disabled = False
        self.proc = None
        self.debug("[%s] Loaded matcher/gofuzzy" % time.time())
        self.booted = False
        if sys.platform == 'linux':
            self.proto = "unix"
            self.port = "/tmp/fuzzy-denite-%s.sock" % os.getpid()
            self.endpoint = self.proto + ":" + self.port
        else:
            self.proto = "tcp"
            self.port = "51000"
            self.endpoint = "localhost:" + self.port

    def _startProcess(self):
        if not self._initialized:
            # reap any existing process
            self._reapProcess()
            # start the server here
            self.debug("[%s] starting fuzzy-denite GRPC server %s " %
                       (time.time(), exe))
            cmd = [exe, '--log', 'info', 'server', '-u', self.proto,
                   '-p', self.port, '--grpc']
            self.proc = subprocess.Popen(cmd)
            self.debug("Launching server: " + " ".join(cmd))
            self.debug("[%s] pid: %s" % (time.time(), self.proc.pid))
            self.conn = grpc.insecure_channel(self.endpoint)
            self.service = api_pb2_grpc.FuzzyStub(self.conn)
            self._initialized = True

            # force check on whether svc is callable
            self.booted = False
            time.sleep(0.05)

    def _reapProcess(self):
        if self.proc:
            exitcode = self.proc.poll()
            self.debug("Process exited with code %s" % exitcode)

    def _verifyService(self):
        maxTries, current = 3, 0
        lastEx = None
        while not self.booted and current < maxTries:
            current = current + 1
            self._startProcess()
            try:
                reply = self.service.Version(api_pb2.Empty())
                self.debug("startup attempt #%s server version is %s@%s" %
                           (current, reply.branch, reply.sha))
                self.booted = True
            except grpc.RpcError as ex:
                self.debug("Error calling version api; attempt #%s" %
                           current)
                self._initialized = False
                lastEx = ex
        if not self.booted:
            raise lastEx

    def filter(self, context):

        def getCandidate(s):
            for i in context['candidates']:
                if i['word'] == s:
                    return i

        if not context['candidates'] or not context[
                'input'] or self._disabled:
            return context['candidates']

        self._verifyService()

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
            self._initialized = False
            self.debug("Exception in gofuzzy - \n %s" % ex)
            return 200, "Ok", items
