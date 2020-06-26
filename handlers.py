from requests import Session
from urllib.parse import ParseResult
from modifier import proxied_m3u8

import falcon

session = Session()

def handle_ts(url: str, res) -> None:
  up_res = session.get(url, stream=True)
  res.content_type = up_res.headers.get('Content-Type', falcon.MEDIA_HTML)
  res.status = falcon.code_to_http_status(up_res.status_code)
  res.stream = up_res.iter_content()

def handle_m3u8(url: str, res) -> None:
  up_res = session.get(url)
  res.content_type = up_res.headers.get('Content-Type', falcon.MEDIA_HTML)
  res.status = falcon.code_to_http_status(up_res.status_code)
  res.body = '\n'.join(proxied_m3u8(url, up_res.text))

def handle_key(url: str, res) -> None:
  client_res = session.get(url)
  res.content_type = up_res.headers.get('Content-Type', falcon.MEDIA_HTML)
  res.status = falcon.code_to_http_status(up_res.status_code)
  res.body = up_res.text

handlers = {
  '.ts': handle_ts,
  '.m3u8': handle_m3u8,
  '.key': handle_key
}