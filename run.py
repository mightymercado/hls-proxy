from gevent import monkey, pywsgi
monkey.patch_all()

import falcon
import re

from pybase64 import b64decode
from requests import Session
from collections import defaultdict
from urllib.parse import urlparse, urljoin

from handlers import handlers
from consts import Constant

def on_request(req, res):
  path = req.path[1:]

  for ext in Constant.EXTS:
    if path.endswith(ext):
      payload = path[:-len(ext)].encode() + b'==='
      url = b64decode(payload).decode()
      
      parsed_url = urlparse(url)
      host = parsed_url.hostname

      handlers[ext](url, res)
      break
  else:
    res.status = '400'
    res.body = 'NG'

app = falcon.App()
app.add_sink(on_request, '/')

if __name__ == '__main__':
  port = 8000
  server = pywsgi.WSGIServer(("localhost", port), app)
  server.serve_forever()