from requests import Session
from urllib.parse import ParseResult
from modifier import proxied_m3u8
from pools import pools
import gzip

import falcon

def chunked_read(up_res, chunk=64 * 1024, decode_content=None):
  while True:
    data = up_res.read(chunk, decode_content=decode_content)
    if not data:
      break
    yield data

def full_read(up_res, decode_content=None):
  data = up_res.read(decode_content=decode_content)
  return data

def handle_ts(url: bytes, res) -> None:
  up_res = pools.urlopen(url=url.decode(), method='GET', preload_content=False)
  res.content_type = up_res.headers.get('Content-Type', falcon.MEDIA_HTML)
  res.status = falcon.code_to_http_status(up_res.status)
  res.set_header('content-encoding', up_res.headers.get('content-encoding', ''))
  res.set_header('Access-Control-Allow-Origin', '*')
  res.stream = chunked_read(up_res, decode_content=False)

def handle_m3u8(url: bytes, res) -> None:
  up_res = pools.urlopen(url=url.decode(), method='GET', preload_content=False)
  res.content_type = up_res.headers.get('Content-Type', falcon.MEDIA_HTML)
  res.status = falcon.code_to_http_status(up_res.status)
  res.set_header('content-encoding', 'gzip')
  res.set_header('Access-Control-Allow-Origin', '*')
  res.body = gzip.compress(b'\n'.join(proxied_m3u8(url, full_read(up_res))))

def handle_key(url: bytes, res) -> None:
  up_res = pools.urlopen(url=url.decode(), method='GET', preload_content=False)
  res.content_type = up_res.headers.get('Content-Type', falcon.MEDIA_HTML)
  res.status = falcon.code_to_http_status(up_res.status)
  res.set_header('Access-Control-Allow-Origin', '*')
  res.body = full_read(up_res, decode_content=False)

handlers = {
  '.ts': handle_ts,
  '.m3u8': handle_m3u8,
  '.key': handle_key
}