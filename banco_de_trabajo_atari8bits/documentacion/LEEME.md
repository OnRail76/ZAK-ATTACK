# Generadores de documentación

```
python3 render_assets.py ../../codigo_fuente/gfx capturas img   # sprites, tiles, jefes y recortes de capturas
python3 build_atlas.py ../../codigo_fuente/gfx                   # atlas.html (A4 apaisado)
python3 build_manual.py                                          # manual.html (A5)
python3 make_pdf.py atlas.html atlas.pdf
python3 make_pdf.py manual.html manual.pdf
```

`capturas/` son PNG de `shot.py` (cuadros elegidos con `run8`). Los nombres de las capturas
que usa cada página están en `common.py` (sector, jefe) y en los propios scripts.
Fuentes: Inter, Inter Display y DejaVu Sans Mono instaladas en el sistema.
