from typing import Tuple, Iterable
from urllib.parse import urljoin
from pybase64 import b64encode

from consts import Constant

def is_key_line(line: bytes) -> bool:  
  return line.startswith(Constant.EXT_KEY)

def extract_key(line: bytes) -> Tuple[int, int]:
  apos = b'"'
  start = line.find(apos, len(Constant.EXT_KEY)) + 1
  end = line.find(apos, start)
  return (start, end)

def proxied_key_line(base: bytes, line: bytes) -> bytes:
  start, end = extract_key(line)
  key = line[start:end]
  if not key.startswith(b'http'):
    key = base + key
  b64_key = b64encode(key)
  proxied_key = b'%b%b.key' % (Constant.BASE_URL, b64_key)
  return line[:start] + proxied_key + line[end:]

def proxied_m3u8(url: bytes, text: bytes) -> Iterable[bytes]:
  base = url[:url.rfind(b'/') + 1]
  
  for line in text.splitlines():
    if is_key_line(line):
      yield proxied_key_line(base, line)
    elif line.startswith(b'#'):
      yield line
    else:
      if not line.startswith(b'http'):
        line = base + line 
      ext = line[line.rfind(b'.'):]
      b64 = b64encode(line)
      yield b'%b%b%b' % (Constant.BASE_URL, b64, ext)