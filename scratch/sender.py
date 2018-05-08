import http.client
import mimetypes
import sys
import codecs
import uuid
import binascii
import io
import os
import pickle


def post_multipart(host, selector, fields, files):
    headers, body = multipart_encoder(fields, files)
    h = http.client.HTTPConnection(host)
    h.request('POST', selector, body, headers)
    res = h.getresponse()
    return res.status, res.reason, res.read()


def multipart_encoder(params, files):
    boundry = uuid.uuid4().hex
    lines = list()
    for key, val in params.items():
        if val is None:
            continue
        lines.append('--' + boundry)
        lines.append('Content-Disposition: form-data; name="%s"' % key)
        lines.extend(['', val])

    for key, uri in files.items():
        name = os.path.basename(uri)
        mime = mimetypes.guess_type(uri)[0] or 'application/octet-stream'

        lines.append('--' + boundry)
        lines.append('Content-Disposition: form-data; name="{0}"; filename="{1}"'.format(key, name))
        lines.append('Content-Type: ' + mime)
        lines.append('')
        lines.append(open(uri, 'rb').read())

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


def create(args):
    l = open(args[0]).read().splitlines()[:1000]
    f = open(args[1], "wb")
    pickle.dump(file=f, protocol=2, obj=l)
    f.close()

def send(args):
    """TODO: Docstring for main.

    :arg1: TODO
    :returns: TODO

    """
    try:
        print(args)
        while True:
            qry = sys.stdin.readline().rstrip("\n")
            status, reason, content = post_multipart('localhost', "/search",
                                                     {"pattern": qry,
                                                      "algo": args[0],
                                                      "cid": "12345",
                                                      "max": "10"},
                                                     {})
            if status == 400:
                print("resending with data")
                status, reason, content = post_multipart('localhost', "/search",
                                                         {"pattern": qry,
                                                          "cid": "12345",
                                                          "algo": args[0],
                                                          "max": "10"},
                                                         {"data": args[1]})
            print(status, reason)
            m = pickle.loads(content)
            print(len(m))
            [print(i) for i in m]
    except KeyboardInterrupt:
        print("Exiting")


if __name__ == "__main__":
    # print(sys.argv)
    if len(sys.argv) == 1:
        print("script.py [send|create]")
        print("send args: filename")
        print("create args: infile, outfile")
    elif sys.argv[1] == 'create':
        create(sys.argv[2:])
    elif sys.argv[1] == 'send':
        send(sys.argv[2:])
    else:
        print("unknown arg")


