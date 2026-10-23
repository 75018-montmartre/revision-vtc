# -*- coding: utf-8 -*-
"""Gabarit commun des pages de revision-vtc.fr (en-tête, navigation, pied)."""

NAV = [("index.html", "Accueil", "accueil"), ("actualite/index.html", "Actualité VTC", "actualite"),
       ("mises-a-jour.html", "Mises à jour du livre", "maj"), ("examens.html", "Examens blancs", "examens")]


def page(titre, corps, actif=None, racine="", description="", noindex=False, scripts_tete="", scripts_fin="", avant_main="", brut=False):
    nav = "".join(
        f'<li><a href="{racine}{href}"' + (' aria-current="page"' if cle == actif else "") + f">{nom}</a></li>"
        for href, nom, cle in NAV)
    meta = f'<meta name="description" content="{description}">\n' if description else ""
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titre}</title>
{meta}{robots}<link rel="stylesheet" href="{racine}css/site.css">
<link rel="alternate" type="application/rss+xml" title="Actualité VTC · revision-vtc.fr" href="{racine}actualite/flux.xml">
{scripts_tete}</head>
<body>
<a class="evitement" href="#contenu">Aller au contenu</a>
<header class="entete">
  <div class="page">
    <a class="nom-site" href="{racine}index.html"><span class="marque" aria-hidden="true">R</span><span class="nom">Révision VTC<span class="sous">Le site du livre Machine à Réussite</span></span></a>
    <nav class="nav" aria-label="Menu principal"><ul>{nav}</ul></nav>
  </div>
</header>
{avant_main}<main id="contenu" tabindex="-1">
{corps if brut else '  <div class="page">' + chr(10) + corps + chr(10) + '  </div>'}
</main>
<footer class="pied">
  <div class="page">
    <div class="pied-livre">
      <img src="{racine}couverture-petite.jpg" width="68" height="88" alt="">
      <p><b>Machine à Réussite · Examen VTC 2027</b><br>Le cours, 1 191 questions corrigées et 5 examens blancs, à jour de la loi du 25 juin 2026.</p>
    </div>
    <ul>
      <li><a href="{racine}mentions-legales.html">Mentions légales</a></li>
      <li><a href="{racine}accessibilite.html">Accessibilité</a></li>
      <li><a href="{racine}actualite/flux.xml">Flux RSS</a></li>
    </ul>
    <p class="copyright">© Benjamin Blondin, 2026</p>
  </div>
</footer>
{scripts_fin}</body>
</html>
'''
