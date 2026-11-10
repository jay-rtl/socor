"""Validate the public multi-page structure without external dependencies."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

root = Path(__file__).parent
class Check(HTMLParser):
    def __init__(self):
        super().__init__()
        self.headings = []
        self.links = []
        self.assets = []
        self.ids = set()
        self.title = ''
        self.in_title = False
        self.description = ''
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ['h1','h2','h3','h4','h5','h6']:
            self.headings.append(int(tag[1]))
        if tag == 'title':
            self.in_title = True
        if tag == 'meta' and attrs.get('name') == 'description':
            self.description = attrs.get('content','')
        if tag == 'a':
            self.links.append(attrs.get('href',''))
        if tag in ['img','script'] and attrs.get('src'):
            self.assets.append(attrs['src'])
        if tag == 'link' and attrs.get('rel') in ['stylesheet','preload']:
            self.assets.append(attrs['href'])
        if attrs.get('id'):
            assert attrs['id'] not in self.ids, ('Duplicate ID', attrs['id'])
            self.ids.add(attrs['id'])
        if tag == 'img':
            assert attrs.get('alt'), 'Missing image alternative'
            if attrs.get('src'):
                assert attrs.get('width') and attrs.get('height'), 'Image dimensions missing'
    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
    def handle_data(self, data):
        if self.in_title: self.title += data

pages = {}
for path in root.rglob('index.html'):
    if any(part in {'dist','docs'} for part in path.parts) or any(part.startswith('new-') for part in path.parts):
        continue
    check = Check()
    check.feed(path.read_text())
    assert check.headings.count(1) == 1, path
    assert check.title and check.description, path
    assert 40 <= len(check.description) <= 165, (path, len(check.description))
    assert all(b <= a+1 for a,b in zip(check.headings, check.headings[1:])), ('Heading skip',path)
    pages[path] = check
assert len(pages) == 11, len(pages)
assert len({page.title for page in pages.values()}) == 11, 'Duplicate page title'
assert len({page.description for page in pages.values()}) == 11, 'Duplicate page description'
for path, check in pages.items():
    for asset in check.assets:
        if asset.startswith('/'):
            assert (root / asset.lstrip('/')).is_file(), (path,asset)
    for link in check.links:
        parsed = urlsplit(link)
        if parsed.scheme or parsed.netloc:
            continue
        target = root / parsed.path.strip('/') / 'index.html' if parsed.path.startswith('/') else path
        assert target.is_file(), (path,link)
        if parsed.fragment:
            assert unquote(parsed.fragment) in pages[target].ids, (path,link)
print('PASS: 11 pages; unique titles/descriptions; headings; IDs; link targets/fragments; image alternatives/dimensions; local assets')
