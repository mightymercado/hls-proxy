from typing import Tuple, Iterable
from urllib.parse import urljoin
from pybase64 import b64encode

from consts import Constant

def is_key_line(line: str) -> bool:  
  return line.startswith(Constant.EXT_KEY)

def extract_key(line: str) -> Tuple[int, int]:
  apos = '"'
  start = line.find(apos, len(Constant.EXT_KEY))
  end = line.find(apos, start)
  return (start + 1, end)

def proxied_key_line(base: str, line: str) -> str:
  start, end = extract_key(line)
  full_key = base + line[start:end]
  b64_key = b64encode(full_key.encode()).decode()
  proxied_key = f'{Constant.BASE_URL}{b64_key}.key'
  return line[:start] + proxied_key + line[end + 1:]

def proxied_m3u8(url: str, text: str) -> Iterable[str]:
  base = url[:url.rfind('/') + 1]
  
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