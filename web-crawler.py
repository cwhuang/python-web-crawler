import sys
import requests
from lxml import etree
from collections import deque
try: from urlparse import urljoin # Python2
except ImportError: from urllib.parse import urljoin # Python3

if len(sys.argv) < 2:
    print("Usage: {} URL".format(sys.argv[0]))
    sys.exit(-1)
else:
    url = sys.argv[1]
    if len(sys.argv) > 2:
        count = int(sys.argv[2])
    else:
        count = 100


visited_urls = set()
queued_urls = [ url ]

while len(visited_urls) < count and len(queued_urls) > 0:
    urls = list()
    for u in queued_urls:
#       print(u)
        try:
            req = requests.get(u, timeout=5)
            res = req.status_code
        except Exception as e:
            res = e
            continue
        finally:
            visited_urls.add(u)
            print("[{}]".format(len(visited_urls)), u, res)
#       if r.status_code != requests.codes.ok: continue
        root = etree.HTML(req.text, base_url=u)
#       print([a.get('href') for a in root.xpath('//a')])
        for a in root.xpath('//a'):
            h = a.get('href')
#           print(h)
            # why h is None?
            if h is None: continue
            (uj, sep, ui) = urljoin(a.base, h).partition('#')
            if uj not in visited_urls and uj not in queued_urls and uj not in urls:
                if uj.startswith('http'): urls.append(uj)
#           print(a.base, h, uj)
        if (len(visited_urls) >= count):
            break
    queued_urls = urls
#   print(queued_urls)
