#!/usr/bin/env python3
"""Renderiza atlas.html y folleto.html a PDF y saca miniaturas de cada página para revisarlas."""
import sys, subprocess
from playwright.sync_api import sync_playwright
R = '/home/claude/final/'
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, w, h in (('atlas', '210mm', '297mm'), ('folleto', '148mm', '210mm')):
        pg = b.new_page()
        pg.goto('file://' + R + name + '.html'); pg.wait_for_timeout(500)
        pg.pdf(path=R + name + '.pdf', width=w, height=h, print_background=True, prefer_css_page_size=True)
        print(name, 'pdf ok')
    b.close()
for name in ('atlas', 'folleto'):
    subprocess.run(['pdftoppm', '-r', '40', '-png', R + name + '.pdf', R + 'prev/' + name])
