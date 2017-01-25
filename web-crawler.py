import sys
import requests
from lxml import etree
from collections import OrderedDict
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
queued_urls = OrderedDict({ url: '' })

while len(queued_urls) > 0:
    (u, i) = queued_urls.popitem(last=False)
#   print(u)
    try:
        req = requests.get(u, timeout=5)
        res = req.status_code
#       if res != requests.codes.ok: continue
        root = etree.HTML(req.text, base_url=u)
    except requests.ConnectionError as e:
        res = e
        continue
    except requests.Timeout as e:
        res = e
        continue
    except requests.TooManyRedirects as e:
        res = e
        continue
    except ValueError as e:
        res = e
        continue
    finally:
        visited_urls.add(u)
        pfx = "{}[{}]".format(i, len(visited_urls))
        print(pfx, u, res)

    # ignore non-HTML documents
    # e.g.: http://famfamfam.com/feed.xml
    if root is None: continue

#   print([a.get('href') for a in root.xpath('//a')])
    for a in root.xpath('//a'):
        if (len(visited_urls) + len(queued_urls) >= count):
            break
        href = a.get('href')
#       print(href)
        # why href is None?
        if href is None: continue
        # ignore named anchor
        (uj, sep, ui) = urljoin(a.base, href).partition('#')
        if uj not in visited_urls and uj not in queued_urls:
            # could we handle other url types?
            if uj.startswith('http'): queued_urls[uj] = pfx
#       print(a.base, href, uj)
    if (len(visited_urls) >= count):
        break
#   print(queued_urls)
