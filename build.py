"""Package the site, optionally under a GitHub Pages project base path."""
from pathlib import Path
import argparse
import re
import shutil

root = Path(__file__).parent
parser = argparse.ArgumentParser()
parser.add_argument('--base-path', default='')
parser.add_argument('--output', default='dist', choices=['dist','docs'])
args = parser.parse_args()
base = '/' + args.base_path.strip('/') if args.base_path.strip('/') else ''
if base and not re.fullmatch(r'/[A-Za-z0-9_-]+',base):
    parser.error('Base path must be one URL-safe path segment')
out = root / args.output
if out.exists():
    shutil.rmtree(out)
out.mkdir()
for path in root.iterdir():
    if path.is_file() and path.suffix in {'.html','.css','.js'}:
        shutil.copy2(path,out/path.name)
    elif path.is_dir() and path.name not in {'docs','dist'} and (path.name=='assets' or (path/'index.html').is_file()):
        shutil.copytree(path,out/path.name)
if base:
    for path in out.rglob('*'):
        if path.suffix in {'.html','.css','.js'}:
            text=path.read_text()
            text=re.sub(r'''(["'])/(?!/)''',lambda match:match[1]+base+'/',text)
            text=text.replace('url=/','url='+base+'/')
            path.write_text(text)
(out/'.nojekyll').touch()
print('Static build ready in '+args.output+'/, base path: '+(base or '/'))
