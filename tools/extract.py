"""Extrait de l'export Open Food Facts les produits vendus en France
(avec ingrédients), classés par popularité, en JSON lignes compact.

usage : python -I extract.py export.csv.gz dossier_sortie
"""
import csv
import gzip
import html
import json
import os
import re
import sys

csv.field_size_limit(10**9)
src, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)

KEEP_PREFIX = re.compile(r'^[3458]')  # FR, DE/BE/UK, IT/ES... (pas 6xx : Afrique, Moyen-Orient)
rows = []
total = 0
with gzip.open(src, 'rt', encoding='utf-8', errors='replace', newline='') as f:
    r = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
    header = next(r)
    ix = {h: i for i, h in enumerate(header)}
    need = ['code', 'product_name', 'brands', 'categories_tags',
            'countries_tags', 'ingredients_text', 'unique_scans_n', 'lang']
    idx = {k: ix.get(k) for k in need}
    print({k: v for k, v in idx.items()})
    n = len(header)
    for row in r:
        total += 1
        if len(row) < n // 2:
            continue

        def g(k):
            i = idx[k]
            return row[i] if i is not None and i < len(row) else ''

        code = g('code')
        if not code.isdigit() or len(code) < 8 or not KEEP_PREFIX.match(code):
            continue
        if 'en:france' not in g('countries_tags'):
            continue
        name = html.unescape(g('product_name')).strip()
        ingr = html.unescape(g('ingredients_text')).strip()
        if not name or name == code or len(ingr) < 8 or '�' in name:
            continue
        try:
            scans = int(g('unique_scans_n') or 0)
        except ValueError:
            scans = 0
        brand = html.unescape(g('brands').split(',')[0]).strip()
        tags = [t[3:] for t in g('categories_tags').split(',') if t.startswith('en:')][-8:]
        rows.append((scans, code, name[:120], brand[:60], tags, ingr[:600], g('lang')))

print('lignes lues', total, '| candidats', len(rows))
rows.sort(key=lambda x: (-x[0], x[1]))
fr = sum(1 for x in rows if x[1][0] == '3')
print('dont codes français (3x)', fr)
print('scans >=1', sum(1 for x in rows if x[0] >= 1), '>=5', sum(1 for x in rows if x[0] >= 5),
      '>=20', sum(1 for x in rows if x[0] >= 20))


def write(name, limit):
    path = os.path.join(outdir, name)
    with gzip.open(path, 'wt', encoding='utf-8', compresslevel=9) as out:
        for scans, code, pname, brand, tags, ingr, lang in rows[:limit]:
            out.write(json.dumps({'c': code, 'n': pname, 'b': brand, 't': tags, 'i': ingr},
                                 ensure_ascii=False, separators=(',', ':')) + '\n')
    print(name, min(limit, len(rows)), 'produits', round(os.path.getsize(path) / 1e6, 1), 'Mo')


for label, limit in (('20k', 20000), ('50k', 50000), ('100k', 100000), ('all', len(rows))):
    write(f'products_{label}.jsonl.gz', limit)
