#!/usr/bin/env python3
"""Rulează acest script să generezi CV-ul PDF cu poza ta."""
from weasyprint import HTML

HTML(filename='cv_template.html').write_pdf('cv_europass.pdf')
print("✅ cv_europass.pdf generat")
