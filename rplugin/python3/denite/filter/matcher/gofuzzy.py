from ..base import Base
import os
import logging
import http.client
import uuid
import pickle
import hashlib
import subprocess
import time
import grpc
import sys
sys.path.insert(1, os.path.dirname(__file__))
import api_pb2
import api_pb2_grpc

logger = logging.getLogger()
level = os.environ.get("NVIM_PYTHON_LOG_LEVEL", "WARNING")
logger.setLevel(logging.getLevelName(level))


class Filter(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'matcher/gofuzzy'
        self.description = 'go fuzzy matcher'

        self._initialized = False
        self._disabled = False
        self.proc = None
        self.conn = http.client.HTTPConnection("localhost:9009")
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

    def filter(self, context):
        if not context['candidates'] or not context[
                'input'] or self._disabled:
            return context['candidates']

        self._startProcess()

        ispath = (os.path.exists(context['candidates'][0]['word']))
        status, reason, result = self._get_fuzzy_results(
            ispath, context['candidates'], context['input'])
        if result is not None:
            # logging.debug("2GREPME....")
            # logging.debug(len(result))
            # logging.debug(result)
            return [x for x in context['candidates'] if x['word'] in result]
        else:
            # just return the current list as is.. if this is due to 
            # the server not running, then when the user types the next
            # chars, the server will be started
            self.error_message(context, "gofuzzy error: %s - %s" % (status, reason))
            return [x for x in context['candidates']]

    def _get_fuzzy_results(self, ispath, candidates, pattern):
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
        except ConnectionResetError as cex:
            self.debug(cex)
            self.debug("ConnnectionResetError: will try restarting server")
            self._initialized = False
            return "ConnectionResetError", "ConnectionResetError", None
        except ConnectionRefusedError:
            self.debug("ConnectionRefusedError: will try restarting server")
            self._initialized = False
            return "ConnectionRefusedError", "ConnectionRefusedError", None
        except Exception:
            raise

    def post_multipart(self, selector, fields, files):
        fields["Connection"] = "keep-alive"
        headers, body = self.multipart_encoder(fields, files)
        self.conn.request('POST', selector, body, headers)
        res = self.conn.getresponse()
        return res.status, res.reason, res.read()

    def multipart_encoder(self, params, files):
        boundry = uuid.uuid4().hex
        lines = list()
        for key, val in params.items():
            if val is None:
                continue
            lines.append('--' + boundry)
            lines.append('Content-Disposition: form-data; name="%s"' % key)
            lines.extend(['', val])

        for key, uri in files.items():
            mime = 'application/octet-stream'

            lines.append('--' + boundry)
            lines.append('Content-Disposition: form-data; name="{0}"; filename="data"'.format(key))
            lines.append('Content-Type: ' + mime)
            lines.append('')
            lines.append(pickle.dumps(uri, protocol=2))

        lines.append('--%s--' % boundry)

        body = bytes()
        for l in lines:
            if isinstance(l, bytes):
                body += l + b'\r\n'
            else:
                body += bytes(l, encoding='utf8') + b'\r\n'

        headers = {
            'Content-Type': 'multipart/form-data; boundary=' + boundry,
        }

        return headers, body
