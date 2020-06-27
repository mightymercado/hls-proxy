from gevent import monkey, pywsgi
monkey.patch_all()

import falcon
import re
import logging
logging.basicConfig(level=logging.DEBUG)

from pybase64 import b64decode
from requests import Session
from urllib.parse import urlparse, urljoin

from handlers import handlers
from consts import Constant
from pools import pools


def on_request(req, res):
  path = req.path[1:]

  for ext in Constant.EXTS:
    if path.endswith(ext):
      payload = path[:-len(ext)] + '==='
      url = b64decode(payload)
      
      parsed_url = urlparse(url)

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