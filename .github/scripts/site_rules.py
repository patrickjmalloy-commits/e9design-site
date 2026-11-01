#!/usr/bin/env python3
"""Site rules: static checks every page must pass before it can go live.

Run from the repo root:  python3 .github/scripts/site_rules.py
Exits 1 and lists every violation if any rule fails. The promote-production
workflow runs this on each staging push, so a failing page blocks the
approval request. Same idea as the Revelance site rules, trimmed for E9.
"""
import json
import os
import re
import subprocess
import sys
from html.parser import HTMLParser

# Pages that deliberately stay out of search.
NOINDEX = {'404.html', 'thank-you/index.html'}
PALETTE = {'--pine': '#12343A', '--turf': '#2F6B3A', '--oak': '#C08A4E',
           '--cream': '#F6F3EC', '--ink': '#172426'}
MENU = [('/simulators/', 'Simulators'), ('/how-it-works/', 'How It Works'),
        ('/showroom/', 'Showroom'), ('/contact/', 'Contact')]
PHONE = 'tel:+15138866654'


class _Structure(HTMLParser):
    TAGS = ('span', 'a', 'div', 'section', 'article', 'main', 'ul', 'ol', 'button', 'p',
            'h1', 'h2', 'h3', 'h4', 'header', 'footer', 'nav', 'form', 'label', 'table',
            'figure', 'picture', 'details', 'summary', 'select', 'textarea')

    def __init__(self):
        super().__init__()
        self.stack, self.errors = [], []

    def handle_starttag(self, tag, attrs):
        if tag in self.TAGS:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag not in self.TAGS:
            return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
            return
        self.errors.append((tag, self.getpos()[0]))
        for k in range(len(self.stack) - 1, -1, -1):
            if self.stack[k][0] == tag:
                del self.stack[k:]
                break


def pages():
    out = subprocess.check_output(
        ['git', 'ls-files', '-co', '--exclude-standard', '*.html']).decode().split()
    return [p for p in out if not p.startswith(('node_modules/', '.github/'))]


def check(path, s, errors):
    def err(msg):
        errors.append(f'{path}: {msg}')

    blank = lambda m: '\n' * m.group(0).count('\n')
    no_code = re.sub(r'(?is)<(script|style)\b.*?</\1>', blank, s)

    # 1. No breadcrumbs (same rule as Revelance).
    if re.search(r'(?i)breadcrumb', no_code) or '"BreadcrumbList"' in s:
        err('breadcrumbs found (the site does not use breadcrumbs)')

    # 2. No JavaScript printed as page text (missing opening <script>).
    m = re.search(r'</script>\s*(/\*|//|\(function|var |let |const |document\.|window\.)', s)
    if m:
        err(f'line {s.count(chr(10), 0, m.start()) + 1}: JavaScript outside a <script> tag')

    # 3. Every opened container closes in order.
    p = _Structure()
    p.feed(re.sub(r'(?s)<!--.*?-->', blank, no_code))
    p.close()
    for tag, line in p.errors[:3]:
        err(f'line {line}: </{tag}> does not match an open <{tag}> (missing or extra tag)')
    if p.stack and not p.errors:
        tag, line = p.stack[-1]
        err(f'line {line}: <{tag}> is never closed')

    # 4. Structured data is valid JSON.
    for m in re.finditer(r'(?s)<script type="application/ld\+json">(.*?)</script>', s):
        try:
            json.loads(m.group(1))
        except ValueError:
            err(f'line {s.count(chr(10), 0, m.start()) + 1}: structured data (JSON-LD) is not valid JSON')

    # 5. Basics every page needs.
    for needle, what in (('<title>', 'a <title>'), ('name="description"', 'a meta description'),
                         ('rel="canonical"', 'a canonical link'), ('/css/site.css', 'the site stylesheet'),
                         ('name="viewport"', 'a viewport tag')):
        if needle not in s:
            err(f'missing {what}')
    if s.count('<h1') != 1:
        err(f'has {s.count("<h1")} <h1> headings; each page needs exactly one')
    for img in re.findall(r'<img\b[^>]*>', s):
        if 'alt=' not in img:
            err(f'image without alt text: {img[:80]}')
        if 'width=' not in img or 'height=' not in img:
            err(f'image without width/height (causes layout shift): {img[:80]}')

    # 6. Indexing: only the thank-you and 404 pages are noindex.
    noindex = 'noindex' in s
    if path in NOINDEX and not noindex:
        err('should be noindex')
    if path not in NOINDEX and noindex:
        err('is noindex but should be in search')

    # 7. Analytics: GA4 loaded means GA4 configured; phone/email links are tracked.
    if 'googletagmanager.com/gtag/js' in s and "gtag('config'" not in s:
        err("GA4 script loads but gtag('config', ...) is missing; no visits are recorded")
    if re.search(r'href="(tel:|mailto:)', s) and 'id="e9-contact-clicks"' not in s:
        err('phone/email links without the e9-contact-clicks tracker')

    # 8. Same menu and phone number everywhere.
    for href, label in MENU:
        if not re.search(r'<a href="' + re.escape(href) + r'"( aria-current="page")?>' + re.escape(label) + '</a>', s):
            err(f'menu is missing the "{label}" link')
    for tel in set(re.findall(r'href="(tel:[^"]+)"', s)):
        if tel != PHONE:
            err(f'phone link {tel}; the business number is {PHONE}')

    # 9. Local links point at pages that exist.
    for href in set(re.findall(r'(?:href|src)="(/[^"#?]*)', s)):
        f = href.lstrip('/')
        if href.endswith('/'):
            f += 'index.html'
        if f and not os.path.exists(f):
            err(f'link to {href}, which does not exist')


def check_css(errors):
    css = open('css/site.css', encoding='utf-8').read()
    for var, want in PALETTE.items():
        for v in re.findall(re.escape(var) + r':\s*(#[0-9A-Fa-f]{6})', css):
            if v.upper() != want:
                errors.append(f'css/site.css: {var} is {v}; brand standard is {want}')


def check_repo_files(errors):
    # Repo notes (CLAUDE.md, SETUP.md, README.md) sit in the publish folder, and
    # Netlify serves any spelling of their names. The build command deletes them.
    toml = open('netlify.toml', encoding='utf-8').read()
    m = re.search(r'(?m)^\s*command\s*=\s*"([^"]*)"', toml)
    cmd = m.group(1) if m else ''
    for f in sorted(os.listdir('.')):
        if f.lower().endswith('.md') and f not in cmd.split():
            errors.append(f'{f}: would be published; add it to the build command in netlify.toml')


def main():
    errors = []
    files = pages()
    for p in files:
        with open(p, encoding='utf-8') as fh:
            check(p, fh.read(), errors)
    check_css(errors)
    check_repo_files(errors)
    if errors:
        print(f'Site rules: {len(errors)} problem(s)')
        for e in errors:
            print('  ' + e)
        sys.exit(1)
    print(f'Site rules: all {len(files)} pages pass')


if __name__ == '__main__':
    main()
