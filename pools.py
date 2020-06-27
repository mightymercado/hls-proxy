from utils import keydefaultdict

from urllib3.poolmanager import PoolManager, ProxyManager
from urllib3.util import make_headers

headers = {
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9'
}
pools = PoolManager(num_pools=10, headers=headers)
