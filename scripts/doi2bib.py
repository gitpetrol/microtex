


import sys
import urllib.request
from urllib.error import HTTPError

BASE_URL = 'http://dx.doi.org/'

try:
    doi = sys.argv[1]
except IndexError:
    print('Usage:\n{} <doi>'.format(sys.argv[0]))
    sys.exit(1)

url = BASE_URL + doi
req = urllib.request.Request(url)
req.add_header('Accept', 'application/x-bibtex')
try:
    with urllib.request.urlopen(req) as f:
        bibtex = f.read().decode()
    print(bibtex)
except HTTPError as e:
    if e.code == 404:
        print('DOI not found.')
    else:
        print('Service unavailable.')
    sys.exit(1)