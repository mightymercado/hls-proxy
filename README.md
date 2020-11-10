# Fast HLS Proxy

This is a fast and lightweight HTTP/S server that redirects and rewrites encrypted HLS streams to avoid CORS and Geoblocking.

# Benchmark

| source | fast-hls-proxy | [hls-proxy](https://github.com/warren-bank/HLS-Proxy/tree/master/hls-proxy) |
| - | - | - |
| cloudfront | 200-300ms | 1.7s-2.0s |

# Features
1. Uses fast asynchronous IO with green threads (i.e. `gevent`)
2. Uses fast byte string processing without regex and splits
3. Uses lightweight / fast HTTP server with `Falcon` and `Gunicorn`
4. Compatible with Pypy3
5. Uses persistent connections with urllib `PoolManager`
6. Uses chunked response stream
7. Proxies raw GZIP upstream data without decoding

## Todo
1. Write todo
