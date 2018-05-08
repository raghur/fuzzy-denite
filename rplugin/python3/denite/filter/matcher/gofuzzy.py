from ..base import Base
import os
import logging
import http.client
import uuid
import pickle
import hashlib
import subprocess
logger = logging.getLogger()
logger.setLevel(logging.getLevelName("DEBUG"))


class Filter(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'matcher/gofuzzy'
        self.description = 'go fuzzy matcher'

        self._initialized = False
        self._disabled = False
        self.proc = None
        self.conn = http.client.HTTPConnection("localhost:9009")

    def filter(self, context):
        if not context['candidates'] or not context[
                'input'] or self._disabled:
            return context['candidates']

        if not self._initialized:
            # start the server here
            self.proc = subprocess.Popen(['fuzzy-denite', '--log', 'info',
                                          'server'])
            self.debug("started fuzzy-denite server. pid: %s"
                               % self.proc.pid)
            self.conn = http.client.HTTPConnection("localhost:9009")
            self._initialized = True

        ispath = (os.path.exists(context['candidates'][0]['word']))
        status, reason, result = self._get_fuzzy_results(
            ispath, context['candidates'], context['input'])
        if result is not None:
            # logging.debug("2GREPME....")
            # logging.debug(len(result))
            # logging.debug(result)
            return [x for x in context['candidates'] if x['word'] in result]
        else:
            self.error_message(context, "gofuzzy error: %s - %s" % (status, reason))
            return [x for x in context['candidates']]

    def _get_fuzzy_results(self, ispath, candidates, pattern):
        items = [d['word'] for d in candidates]
        items.sort()
        md5sum = hashlib.md5("".join(items).encode("utf8")).hexdigest()

        try:
            status, reason, content = self.post_multipart("/search",
                                                          {"cid": md5sum,
                                                           "pattern": pattern,
                                                           "max": "100"},
                                                          {})
            if status == 400:
                status, reason, content = self.post_multipart("/search",
                                                              {"cid": md5sum,
                                                               "pattern": pattern,
                                                               "max": "100"},
                                                              {"data": items})
            if status != 200:
                return status, reason, None
            else:
                m = pickle.loads(content)
                return status, reason, m
        except ConnectionResetError:
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
