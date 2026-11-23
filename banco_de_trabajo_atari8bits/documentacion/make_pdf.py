#!/usr/bin/env python3
"""HTML -> PDF con el Chromium de Playwright. uso: make_pdf.py entrada.html salida.pdf"""
import sys, pathlib
from playwright.sync_api import sync_playwright
src, out = pathlib.Path(sys.argv[1]).resolve(), sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(src.as_uri()); pg.wait_for_load_state('networkidle')
    pg.pdf(path=out, print_background=True, prefer_css_page_size=True)
    b.close()
print('pdf', out)
