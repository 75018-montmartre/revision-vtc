# -*- coding: utf-8 -*-
"""Gabarit commun des pages de revision-vtc.fr (en-tête, navigation, pied)."""
import json, os

with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "contenu", "livre.json"), encoding="utf-8") as _h:
    LIVRE = json.load(_h)


def achat(classe="bouton", texte="Acheter le livre sur Amazon"):
    """Lien d'achat du livre ; tant que l'adresse Amazon n'est pas renseignée, une mention « bientôt disponible »."""
    if LIVRE.get("amazon"):
        return f'<a class="{classe}" href="{LIVRE["amazon"]}">{texte}</a>'
    return f'<span class="{classe} bientot">Bientôt disponible sur Amazon</span>'

# menu principal : les cinq rubriques du site ; le livre a son propre menu, à droite (MENU_LIVRE).
# L'accueil n'est plus dans le menu : le logo y mène (et le fil d'Ariane de chaque page).
NAV = [("actualite/index.html", "Actualité VTC", "actualite"), ("questions/index.html", "Questions VTC", "questions"), ("dossiers/index.html", "Articles", "dossiers"),
       ("wiki/index.html", "Textes du métier", "textes"), ("simulateurs/index.html", "Simulateur", "simulateurs")]
MENU_LIVRE = [("mises-a-jour.html", "Mises à jour du livre", "maj"), ("examens.html", "Examens blancs n° 4 et 5", "examens")]


SURTITRES = {"actualite": "Chaque lundi", "questions": "Chaque jeudi", "dossiers": "Articles VTC", "simulateurs": "Simulateur gratuit", "textes": "Réglementation VTC",
             "maj": "Le livre", "examens": "Réservé aux lecteurs"}


def _tete_page(corps, actif, racine):
    """Sort l'en-tête de la page (fil d'Ariane, surtitre, titre, chapeau) du corps et le place dans
    la bande commune « tete-page ». Toutes les pages intérieures ont ainsi le même en-tête."""
    import re as _re
    m = _re.search(r"<h1[^>]*>.*?</h1>", corps, _re.S)
    if not m:
        return "", corps, "mp-colonne"
    avant, h1, apres = corps[:m.start()], m.group(0), corps[m.end():]
    suite = ""
    while True:
        n = _re.match(r'\s*<p class="(?:chapeau|meta|texte-ref)">.*?</p>', apres, _re.S)
        if not n:
            break
        suite += n.group(0)
        apres = apres[n.end():]
    if 'class="surtitre"' not in avant:
        avant += f'\n    <p class="surtitre">{SURTITRES.get(actif, "Révision VTC")}</p>'
    accueil = f'<li><a href="{racine or "./"}index.html">Accueil</a></li>'
    if 'class="fil"' in avant:
        avant = avant.replace("<ol>", "<ol>" + accueil, 1)
    if 'class="deux-col"' in apres:
        mp = "mp-cote"
    elif any(c in apres for c in ('class="wiki-theme"', 'class="questions', 'class="numeros"', 'class="dossiers')):
        mp = "mp-grille"
    else:
        mp = "mp-colonne"
    tete = f'''<header class="tete-page {mp}">
  <div class="page">
{avant.strip()}
    {h1}{suite}
  </div>
</header>'''
    return tete, apres, mp


def page(titre, corps, actif=None, racine="", description="", noindex=False, scripts_tete="", scripts_fin="", avant_main="", brut=False, jsonld=None):
    import json as _json
    if jsonld:
        scripts_tete += "".join('<script type="application/ld+json">' + _json.dumps(j, ensure_ascii=False).replace("</", "<\\/") + "</script>\n" for j in jsonld)
    tete, reste, mp = ('', corps, '') if brut else _tete_page(corps, actif, racine)
    courant = lambda cle: ' aria-current="page"' if cle == actif else ""
    nav = "".join(f'<li><a href="{racine}{href}"{courant(cle)}>{nom}</a></li>' for href, nom, cle in NAV)
    livre = "".join(f'<li><a href="{racine}{href}"{courant(cle)}>{nom}</a></li>' for href, nom, cle in MENU_LIVRE)
    if LIVRE.get("amazon"):
        livre += f'<li><a href="{LIVRE["amazon"]}">Acheter le livre sur Amazon</a></li>'
    livre_actif = " actif" if actif in {c for _, _, c in MENU_LIVRE} else ""
    meta = f'<meta name="description" content="{description}">\n' if description else ""
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titre}</title>
{meta}{robots}<link rel="stylesheet" href="{racine}css/site.css">
<link rel="icon" href="{racine}favicon.ico" sizes="48x48">
<link rel="icon" href="{racine}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{racine}apple-touch-icon.png">
<link rel="preload" href="{racine}fonts/eb-garamond-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{racine}fonts/inter-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="alternate" type="application/rss+xml" title="Actualité VTC · revision-vtc.fr" href="{racine}actualite/flux.xml">
{scripts_tete}</head>
<body>
<a class="evitement" href="#contenu">Aller au contenu</a>
<header class="entete">
  <div class="page">
    <a class="nom-site" href="{racine}index.html"{courant("accueil")}><span class="marque" aria-hidden="true">R</span><span class="nom">Révision VTC<span class="sous">Examen, réglementation et métier de chauffeur VTC</span></span></a>
    <nav class="nav" aria-label="Menu principal"><ul>{nav}</ul></nav>
    <details class="menu-livre{livre_actif}"><summary>Le livre</summary><ul>{livre}</ul></details>
  </div>
</header>
{avant_main}<main id="contenu" tabindex="-1">
{corps if brut else tete + chr(10) + f'  <div class="page corps-page {mp}">' + chr(10) + reste + chr(10) + '  </div>'}
</main>
<footer class="pied">
  <div class="page">
    <div class="pied-livre">
      <img src="{racine}couverture-petite.jpg" width="68" height="88" alt="">
      <div>
        <p><b>Machine à Réussite · Examen VTC 2027</b><br>Le cours, 1 191 questions corrigées et 3 examens blancs, plus 2 ici. À jour de la loi du 25 juin 2026.</p>
        <p class="pied-achat">{achat("bouton clair petit")}</p>
      </div>
    </div>
    <ul>
      <li><a href="{racine}contact.html">Contact</a></li>
      <li><a href="{racine}a-propos.html">À propos et méthode</a></li>
      <li><a href="{racine}wiki/index.html">Réglementation VTC</a></li>
      <li><a href="{racine}mentions-legales.html">Mentions légales</a></li>
      <li><a href="{racine}accessibilite.html">Accessibilité</a></li>
      <li><a href="{racine}actualite/flux.xml">Flux RSS</a></li>
    </ul>
    <p class="copyright">© Benjamin Blondin, 2026</p>
  </div>
</footer>
<script src="{racine}js/site.js" defer></script>
{scripts_fin}<script data-goatcounter="https://revision-vtc.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</body>
</html>
'''
