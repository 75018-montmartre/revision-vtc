# -*- coding: utf-8 -*-
"""Génère le site revision-vtc.fr dans docs/ à partir des contenus de contenu/.

Usage (depuis la racine du dépôt) :  python3 outils/generer.py
- contenu/actualite/AAAA-MM-JJ.json : un numéro de l'Actualité VTC (voir README.md)
- contenu/mises-a-jour.json         : les corrections du livre après impression
Les pages fixes (accueil, examens, mentions légales, accessibilité) sont décrites ici.
"""
import json, os, re, glob, html, datetime, sys
from email.utils import format_datetime

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
from gabarit import page, achat

RACINE = os.path.dirname(ICI)
DOCS = os.path.join(RACINE, "docs")
CONTENU = os.path.join(RACINE, "contenu")
SITE = "https://revision-vtc.fr/"
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def ty(t):
    """Échappe le HTML puis applique la typographie française (apostrophe, espaces fines)."""
    t = html.escape(str(t), quote=False)
    t = t.replace("'", "\u2019")
    t = re.sub(r" ([:;?!%»€])", "\u202F\\1", t)
    t = re.sub(r"« ", "«\u202F", t)
    t = re.sub(r"(\d) (\d{3})\b", "\\1\u202F\\2", t)
    t = re.sub(r"\bn° ", "n°\u00A0", t)
    return t


def iso_fr(texte):
    """« 25 octobre 2026 » ou « 1er janvier 2027 » -> « 2026-10-25 »."""
    j, m, a = texte.replace("1er", "1").split()
    return f"{int(a):04d}-{MOIS.index(m) + 1:02d}-{int(j):02d}"


def date_fr(iso):
    d = datetime.date.fromisoformat(iso)
    j = "1er" if d.day == 1 else str(d.day)
    return f"{j} {MOIS[d.month - 1]} {d.year}"


AUTEUR = {"@type": "Person", "name": "Benjamin Blondin", "url": SITE + "a-propos.html"}
LIVRE_LD = {"@type": "Book", "@id": SITE + "#livre", "name": "Machine à Réussite · Examen VTC 2027", "author": AUTEUR,
            "isbn": "9798165280795", "bookFormat": "https://schema.org/Paperback", "numberOfPages": 540, "inLanguage": "fr",
            "datePublished": "2026-10", "image": SITE + "couverture.jpg",
            "url": "https://www.amazon.fr/dp/B0HPCMRKDR", "sameAs": ["https://www.amazon.fr/dp/B0HPCMRKDR"],
            "offers": {"@type": "Offer", "price": "24.90", "priceCurrency": "EUR", "availability": "https://schema.org/InStock", "url": "https://www.amazon.fr/dp/B0HPCMRKDR"},
            "about": "Préparation à l'examen d'accès à la profession de conducteur de voiture de transport avec chauffeur (VTC)"}
SITE_LD = {"@type": "WebSite", "@id": SITE + "#site", "name": "Révision VTC", "url": SITE, "inLanguage": "fr-FR",
           "description": "Réglementation VTC expliquée article par article, actualité du métier chaque semaine et examens blancs, par l'auteur du livre Machine à Réussite · Examen VTC 2027.",
           "publisher": AUTEUR}


def fil(*etapes):
    """Données structurées du fil d'Ariane : (nom, chemin relatif au site)."""
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": SITE + c} for i, (n, c) in enumerate(etapes, 1)]}


def _seo(chemin, contenu):
    """Ajoute l'adresse canonique et les balises de partage (Open Graph) à une page indexable."""
    if "</head>" not in contenu or 'content="noindex"' in contenu or 'http-equiv="refresh"' in contenu:
        return contenu
    titre = html.unescape(re.search(r"<title>(.*?)</title>", contenu, re.S).group(1))
    m = re.search(r'<meta name="description" content="(.*?)">', contenu)
    assert m and len(html.unescape(m.group(1))) >= 50, f"{chemin} : description absente ou trop courte"
    desc = html.unescape(m.group(1))
    url = SITE + (chemin[:-10] if chemin.endswith("index.html") else chemin)
    a = lambda t: html.escape(t, quote=True)
    type_og = "article" if chemin.startswith(("wiki/", "actualite/2", "questions/2")) or (chemin.startswith("dossiers/") and not chemin.endswith("index.html")) else "website"
    tete = (f'<link rel="canonical" href="{url}">\n'
            f'<meta property="og:site_name" content="Révision VTC">\n<meta property="og:locale" content="fr_FR">\n'
            f'<meta property="og:type" content="{type_og}">\n<meta property="og:title" content="{a(titre)}">\n'
            f'<meta property="og:description" content="{a(desc)}">\n<meta property="og:url" content="{url}">\n'
            + ("" if 'property="og:image"' in contenu else
               f'<meta property="og:image" content="{SITE}partage.jpg">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
               f'<meta property="og:image:alt" content="Révision VTC, le site du livre Machine à Réussite · Examen VTC 2027">\n') +
            f'<meta name="twitter:card" content="summary_large_image">\n')
    return contenu.replace("</head>", tete + "</head>", 1)


def ecrire(chemin, contenu):
    if chemin.endswith(".html"):
        contenu = _seo(chemin, contenu)
    chemin = os.path.join(DOCS, chemin)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)


def lire_numeros():
    nums = []
    for f in sorted(glob.glob(os.path.join(CONTENU, "actualite", "*.json")), reverse=True):
        with open(f, encoding="utf-8") as h:
            n = json.load(h)
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", n["date"]), f
        assert os.path.basename(f) == n["date"] + ".json", f
        for r in n["rubriques"]:
            for b in r["breves"]:
                assert b.get("sources"), f"{f} : brève sans source : {b['titre']}"
        nums.append(n)
    return nums


# ------------------------------------------------------------------ accueil
def tete_bloc(ident, surtitre, titre, lien=None, texte_lien=None, intro=None):
    """En-tête commun des blocs de l'accueil : surtitre, titre, lien « tout voir » aligné à droite."""
    l = f'<a class="lien-fleche" href="{lien}">{ty(texte_lien)}</a>' if lien else ""
    i = f'<p class="tete-intro">{ty(intro)}</p>' if intro else ""
    return f'''<div class="tete-bloc">
          <div><p class="surtitre">{ty(surtitre)}</p><h2 id="{ident}" class="sans-filet">{ty(titre)}</h2>{i}</div>
          {l}
        </div>'''


def accueil(nums, qs=()):
    dernier = ""
    if nums:
        n = nums[0]
        pts = "".join(f"<li>{ty(x)}</li>" for x in n["a_retenir"])
        dernier = f'''
    <section class="bloc bloc-doux" aria-labelledby="titre-dernier">
      <div class="page large">
        {tete_bloc("titre-dernier-rubrique", "Chaque lundi", "Le dernier numéro de l'Actualité VTC", "actualite/index.html", "Tous les numéros")}
        <article class="une-actu">
          <p class="meta">N° {n["numero"]} · {date_fr(n["date"])}</p>
          <h3 id="titre-dernier"><a href="actualite/{n["date"]}.html">{ty(n["titre"])}</a></h3>
          <ul class="points">{pts}</ul>
        </article>
      </div>
    </section>'''
    corps = f'''    <section class="une" aria-labelledby="titre-une">
      <div class="page large une-grille">
        <div class="une-texte">
          <p class="surtitre">Le site du livre <i>Machine à Réussite</i></p>
          <h1 id="titre-une">Réussir l’examen VTC avec des règles à jour</h1>
          <p class="chapeau">{ty("Le livre a été vérifié en octobre 2026. Ici, il continue : l'actualité du métier chaque semaine, les règles qui changent, et deux examens blancs en ligne.")}</p>
          <div class="actions">{achat("bouton clair")}<a class="bouton contour" href="actualite/index.html">Lire l’Actualité VTC</a></div>
        </div>
        <img class="une-couv" src="couverture.jpg" width="408" height="528" alt="Couverture du livre Machine à Réussite · Examen VTC 2027, de Benjamin Blondin">
      </div>
    </section>
    <section class="bloc" aria-labelledby="titre-rubriques">
      <div class="page large">
        {tete_bloc("titre-rubriques", "Le site", "Quatre rubriques, une seule exigence : des sources vérifiées")}
        <ul class="trois">
          <li><p class="surtitre">Chaque semaine</p><h3><a href="actualite/index.html">Actualité VTC</a></h3><p>{ty("Textes officiels, examen, plateformes, cotisations : ce qui change pour vous, toujours avec ses sources.")}</p></li>
          <li><p class="surtitre">L'essentiel du droit</p><h3><a href="wiki/index.html">Textes du métier</a></h3><p>{ty("Le droit du VTC article par article : le texte officiel, expliqué en clair avec un exemple.")}</p></li>
          <li><p class="surtitre">Après l'impression</p><h3><a href="mises-a-jour.html">Mises à jour du livre</a></h3><p>{ty("Chaque règle qui change, avec sa date, la fiche concernée et le texte qui la fonde.")}</p></li>
          <li><p class="surtitre">Réservé aux lecteurs</p><h3><a href="examens.html">Examens blancs n° 4 et 5</a></h3><p>{ty("À l'écran, chronométrés et corrigés, ou à imprimer.")}</p></li>
        </ul>
      </div>
    </section>{dernier}
    <section class="bloc bloc-blanc" aria-labelledby="titre-essentiel">
      <div class="page large">
        {tete_bloc("titre-essentiel", "Textes du métier", "Réglementation VTC : l'essentiel", "wiki/index.html", "Tous les textes expliqués",
                   "Les règles les plus utiles au quotidien, avec le texte officiel et une explication en clair.")}
        <ul class="essentiel-liens">{liens_essentiels()}</ul>
      </div>
    </section>{bloc_questions(qs)}'''
    ecrire("index.html", page("Examen VTC 2027 et réglementation VTC expliquée · Révision VTC", corps, "accueil", "",
                              "Réussir l'examen VTC 2027 : la réglementation VTC expliquée article par article, l'actualité du métier chaque semaine et deux examens blancs corrigés. Sources officielles citées.",
                              brut=True, jsonld=[{"@context": "https://schema.org", "@graph": [SITE_LD, LIVRE_LD]}]))


ESSENTIELS = [("l3120-2", "Réservation préalable et maraude : ce qui est interdit"), ("d3120-3", "Attente devant les gares et aéroports : une heure maximum"),
              ("l3122-9", "Le retour à la base après une course"), ("r3120-6", "La carte professionnelle VTC : conditions et délai"),
              ("arrete-6-avril-2017-examen", "L'examen VTC : épreuves, coefficients, notes éliminatoires"), ("l3122-3", "Le registre des VTC"),
              ("arrete-26-mars-2015-vehicules", "Le véhicule VTC : âge, dimensions, puissance"), ("arrete-6-aout-2025-reservation", "Le justificatif de réservation : les sept mentions"),
              ("l3124-12", "Maraude, démarchage, conduite sans carte : les sanctions")]


def bloc_questions(qs):
    if not qs:
        return ""
    li = "".join(f'<li><a href="questions/{q["date"]}-{q["slug"]}.html">{ty(q["question"])}</a><p>{ty(q["reponse_courte"])}</p></li>' for q in list(qs)[:4])
    return f'''
    <section class="bloc" aria-labelledby="titre-questions">
      <div class="page large">
        {tete_bloc("titre-questions", "Chaque jeudi", "Questions VTC : une question, une réponse sourcée", "questions/index.html", "Toutes les questions")}
        <ul class="questions questions-grille">{li}</ul>
      </div>
    </section>'''


def liens_essentiels():
    return "".join(f'<li><a href="wiki/{s}.html">{ty(t)}</a></li>' for s, t in ESSENTIELS)


# ------------------------------------------------------------------ actualité
def sources_html(b):
    items = []
    for s in b["sources"]:
        items.append(f'<a href="{html.escape(s["url"])}">{ty(s["nom"])}</a>' + (f", {ty(s['date'])}" if s.get("date") else ""))
    return '<p class="sources">Sources : ' + " ; ".join(items) + "</p>"


def numero(n, precedent, suivant):
    retenir = "".join(f"<li>{ty(x)}</li>" for x in n["a_retenir"])
    rub = ""
    for r in n["rubriques"]:
        rub += f'\n    <h2>{ty(r["titre"])}</h2>'
        for b in r["breves"]:
            paras = "".join(f"<p>{ty(p)}</p>" for p in b["texte"])
            rub += f'\n    <article class="breve"><h3>{ty(b["titre"])}</h3>{paras}{sources_html(b)}</article>'
    impact = "".join(f"<p>{ty(p)}</p>" for p in n["impact_livre"])
    nav = []
    if suivant:
        nav.append(f'<a href="{suivant["date"]}.html">Numéro suivant : n° {suivant["numero"]}</a>')
    if precedent:
        nav.append(f'<a href="{precedent["date"]}.html">Numéro précédent : n° {precedent["numero"]}</a>')
    navh = ('<p class="meta">' + " · ".join(nav) + "</p>") if nav else ""
    corps = f'''    <nav class="fil" aria-label="Fil d'Ariane"><ol><li><a href="index.html">Actualité VTC</a></li></ol></nav>
    <p class="surtitre">Actualité VTC · n° {n["numero"]}</p>
    <h1>{ty(n["titre"])}</h1>
    <p class="meta">Publié le {date_fr(n["date"])} · période couverte : {ty(n["periode"])}</p>
    <section class="retenir" aria-labelledby="titre-retenir"><h2 id="titre-retenir">À retenir</h2>
    <ul>{retenir}</ul></section>{rub}
    <h2>Ce que ça change pour le livre</h2>
    <div class="impact">{impact}</div>
    <p class="meta">{ty("Informations vérifiées le " + n["verifie"] + ". Chaque brève repose sur un texte officiel ou sur deux sources concordantes.")}</p>
    {navh}
    <p><a href="index.html">Tous les numéros</a></p>'''
    titre = f'{n["titre"]} · Actualité VTC n° {n["numero"]}'
    resume = " ".join(n["a_retenir"])
    ld = {"@context": "https://schema.org", "@type": "NewsArticle", "headline": n["titre"][:110], "description": resume[:300],
          "datePublished": n["date"], "dateModified": n["date"], "inLanguage": "fr", "author": AUTEUR, "publisher": AUTEUR,
          "image": SITE + "partage.jpg", "mainEntityOfPage": SITE + f'actualite/{n["date"]}.html',
          "citation": [s["url"] for r in n["rubriques"] for b in r["breves"] for s in b["sources"]][:20]}
    ecrire(f'actualite/{n["date"]}.html', page(html.escape(titre, quote=False), corps, "actualite", "../",
                                               html.escape(resume[:300].rsplit(" ", 1)[0] + "…"),
                                               jsonld=[ld, fil(("Accueil", ""), ("Actualité VTC", "actualite/"), (f'N° {n["numero"]}', f'actualite/{n["date"]}.html'))]))


def actualite(nums):
    liste = ""
    for n in nums:
        pts = "".join(f"<li>{ty(x)}</li>" for x in n["a_retenir"])
        liste += f'''
      <li><span class="numero" aria-hidden="true">{n["numero"]}</span><div><span class="meta">N° {n["numero"]} · {date_fr(n["date"])}</span><a href="{n["date"]}.html">{ty(n["titre"])}</a><ul>{pts}</ul></div></li>'''
    corps = f'''    <h1>Actualité VTC</h1>
    <p class="chapeau">{ty("Chaque semaine, ce qui bouge pour les chauffeurs VTC et les candidats à l'examen : textes officiels, examen, plateformes, cotisations.")}</p>
    <p>{ty("Chaque information repose sur un texte officiel ou sur deux sources concordantes, toujours citées. Quand une règle du livre change, elle est aussi inscrite dans les")} <a href="../mises-a-jour.html">mises à jour du livre</a>.</p>
    <p class="meta">Pour être prévenu de chaque numéro sans donner votre adresse e-mail : <a href="flux.xml">flux RSS</a>.</p>
    <h2>Les numéros</h2>
    <ol class="numeros" reversed>{liste}
    </ol>'''
    ecrire("actualite/index.html", page("Actualité VTC : l'info des chauffeurs VTC chaque semaine · Révision VTC", corps, "actualite", "../",
                                        "L'actualité VTC chaque semaine : textes officiels, examen, plateformes, cotisations. Sources citées."))


def flux(nums):
    items = ""
    for n in nums[:30]:
        d = datetime.datetime.fromisoformat(n["date"] + "T08:00:00+02:00")
        desc = " ".join(n["a_retenir"])
        items += f'''
  <item>
    <title>{html.escape("N° " + str(n["numero"]) + " · " + n["titre"])}</title>
    <link>{SITE}actualite/{n["date"]}.html</link>
    <guid isPermaLink="true">{SITE}actualite/{n["date"]}.html</guid>
    <pubDate>{format_datetime(d)}</pubDate>
    <description>{html.escape(desc)}</description>
  </item>'''
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>Actualité VTC · revision-vtc.fr</title>
  <link>{SITE}actualite/index.html</link>
  <description>L'actualité VTC chaque semaine, par l'auteur du livre Machine à Réussite · Examen VTC 2027.</description>
  <language>fr-FR</language>{items}
</channel>
</rss>
'''
    ecrire("actualite/flux.xml", xml)


# ------------------------------------------------------------------ mises à jour
def mises_a_jour():
    with open(os.path.join(CONTENU, "mises-a-jour.json"), encoding="utf-8") as h:
        m = json.load(h)
    if m["corrections"]:
        lignes = "".join(
            f'<tr><td>{ty(c["date"])}</td><td>{ty(c["fiche"])}</td><td>{ty(c["avant"])}</td><td>{ty(c["apres"])}</td><td>{ty(c["texte"])}</td></tr>'
            for c in m["corrections"])
        tableau = f'''<div class="defile"><table>
      <caption>Corrections du livre, de la plus récente à la plus ancienne</caption>
      <thead><tr><th scope="col">Date</th><th scope="col">Fiche</th><th scope="col">Ce que dit le livre</th><th scope="col">Ce qu’il faut retenir</th><th scope="col">Texte</th></tr></thead>
      <tbody>{lignes}</tbody></table></div>'''
    else:
        tableau = "<p>Aucune correction à ce jour : toutes les règles du livre sont à jour.</p>"
    surv = "".join(f"<li>{ty(x)}</li>" for x in m["a_surveiller"])
    corps = f'''    <h1>Mises à jour du livre</h1>
    <p class="chapeau">{ty("Les règles du livre ont été vérifiées en octobre 2026. Quand l'une d'elles change, elle est inscrite ici : la date, la fiche concernée, l'ancienne règle, la nouvelle, et le texte qui la fonde.")}</p>
    <h2>Les corrections</h2>
    {tableau}
    <p class="meta">Dernière vérification : {ty(m["derniere_verification"])}.</p>
    <h2>À surveiller en 2027</h2>
    <p>{ty("Le livre enseigne ces points en principe. Ils seront précisés ici dès que les textes seront publiés.")}</p>
    <ul>{surv}</ul>'''
    ecrire("mises-a-jour.html", page("Mises à jour du livre · Révision VTC", corps, "maj", "",
                                     "Les règles du livre Machine à Réussite · Examen VTC 2027 qui ont changé depuis l'impression."))


# ------------------------------------------------------------------ wiki des textes du métier
def lire_wiki():
    with open(os.path.join(CONTENU, "wiki.json"), encoding="utf-8") as h:
        w = json.load(h)
    for a in w["articles"]:
        assert a["en_clair"] and a["url"].startswith("https://www.legifrance.gouv.fr/"), a["num"]
    return w


def _sans_accents(t):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")


def _liens_articles(t, par_num, ici):
    """Transforme « article L. 3120-2 » du texte officiel en lien vers la page du wiki, si elle existe."""
    def rep(m):
        num = m.group(1) + m.group(2)
        a = par_num.get(num)
        if not a or a["slug"] == ici:
            return m.group(0)
        return f'<a href="{a["slug"]}.html">{m.group(0)}</a>'
    return re.sub(r"\b([LRD])\. ?\s?(\d{4}(?:-\d+)*)\b(?! du code (?:de la|du|de l))", rep, t)


def wiki():
    w = lire_wiki()
    arts = w["articles"]
    par_num = {a["num"].replace("R*", "R"): a for a in arts if not a.get("arrete")}
    themes = {t["cle"]: t for t in w["themes"]}
    source_date = w["verifie"]

    for a in arts:
        if a.get("arrete"):
            blocs = "".join(
                f'''<section class="officiel-art">
          <h3>{ty(p["num"])}</h3>
          {"".join(f"<p>{_liens_articles(ty(x), par_num, a['slug'])}</p>" for x in p["texte"])}
          {f'<p class="meta">{ty(p["vigueur"])}</p>' if p.get("vigueur") else ""}
        </section>''' for p in a["articles"])
            entete = f'<p class="surtitre">{ty("Arrêté")}</p>\n    <h1>{ty(a["titre"])}</h1>\n    <p class="texte-ref">{ty(a["source"])}</p>'
            renvois = set(re.findall(r"\b[LRD]\.\s?\d{4}(?:-\d+)*", " ".join(x for p in a["articles"] for x in p["texte"])))
        else:
            blocs = "".join(f"<p>{_liens_articles(ty(x), par_num, a['slug'])}</p>" for x in a["texte"])
            blocs += f'\n        <p class="meta">{ty(a["vigueur"])}' + (f' · {ty(a["modif"][0])}' if a.get("modif") else "") + "</p>"
            entete = f'<p class="surtitre">{ty(a["source"])}</p>\n    <h1><span class="num-art">Article {ty(a["num"])}</span> {ty(a["titre"])}</h1>'
            renvois = set(re.findall(r"\b[LRD]\.\s?\d{4}(?:-\d+)*", " ".join(a["texte"])))
        lies = []
        for r in sorted(renvois):
            x = par_num.get(re.sub(r"[.\s ]", "", r))
            if x and x["slug"] != a["slug"] and x not in lies:
                lies.append(x)
        for x in arts:
            if len(lies) >= 5:
                break
            if x["theme"] == a["theme"] and x["slug"] != a["slug"] and x not in lies:
                lies.append(x)
        voir = "".join(f'<li><a href="{x["slug"]}.html">{ty(x["num"] if not x.get("arrete") else "Arrêté")} · {ty(x["titre"])}</a></li>' for x in lies)
        livre = ""
        if a["fiches"]:
            livre = f'''<section class="cote-bloc wiki-livre" aria-labelledby="livre">
        <h2 id="livre">Dans le livre</h2>
        <ul>{"".join(f"<li><b>Fiche {ty(c)}</b> · {ty(t)}</li>" for c, t in a["fiches"])}</ul>
        <p class="pied-achat">{achat("bouton second petit", "Le livre sur Amazon")}</p>
      </section>'''
        th = themes[a["theme"]]
        corps = f'''    <nav class="fil" aria-label="Fil d'Ariane"><ol><li><a href="index.html">Textes du métier</a></li><li><a href="index.html#{a["theme"]}">{ty(th["titre"])}</a></li></ol></nav>
    {entete}
    <div class="deux-col"><div class="col-texte">
    <section class="en-clair" aria-labelledby="clair">
      <h2 id="clair">En clair</h2>
      <p>{ty(a["en_clair"])}</p>
      <p class="concretement"><b>Concrètement :</b> {ty(a["concretement"])}</p>
    </section>
    <section aria-labelledby="officiel">
      <h2 id="officiel">Le texte officiel</h2>
      <div class="officiel">
        {blocs}
      </div>
      <p class="source">{ty("Source : Légifrance, version en vigueur au " + source_date + ".")} <a href="{html.escape(a["url"])}">{ty("Voir sur Légifrance")}</a>. {ty("Texte reproduit sous Licence Ouverte 2.0. En cas de doute, seule la version publiée sur Légifrance fait foi.")}</p>
    </section>
    </div>
    <aside class="col-cote" aria-label="Pour aller plus loin">
    {livre}
    <section class="cote-bloc" aria-labelledby="voir">
      <h2 id="voir">Voir aussi</h2>
      <ul class="voir-aussi">{voir}</ul>
    </section>
    </aside></div>'''
        if a.get("arrete"):
            titre_page = f'{a["num"]} : {a["titre"][0].lower() + a["titre"][1:]} (VTC)'
            loi = {"@type": "Legislation", "name": a["source"], "legislationJurisdiction": "FR", "legislationType": "Arrêté",
                   "legislationLegalForce": "https://schema.org/InForce", "url": a["url"], "inLanguage": "fr"}
        else:
            titre_page = f'Article {a["num"]} du Code des transports : {a["titre"][0].lower() + a["titre"][1:]}'
            loi = {"@type": "Legislation", "name": f'Article {a["num"]} du Code des transports', "legislationIdentifier": a["num"],
                   "legislationJurisdiction": "FR", "legislationType": "Code", "legislationLegalForce": "https://schema.org/InForce",
                   "isPartOf": {"@type": "Legislation", "name": "Code des transports", "legislationIdentifier": "LEGITEXT000023086525"},
                   "url": a["url"], "inLanguage": "fr"}
        desc = a["en_clair"] if len(a["en_clair"]) <= 158 else a["en_clair"][:155].rsplit(" ", 1)[0] + "…"
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": titre_page[:110], "description": a["en_clair"],
              "inLanguage": "fr", "dateModified": iso_fr(source_date), "author": AUTEUR, "publisher": AUTEUR,
              "image": SITE + "partage.jpg", "mainEntityOfPage": SITE + f'wiki/{a["slug"]}.html', "about": loi,
              "isBasedOn": a["url"], "license": "https://www.etalab.gouv.fr/licence-ouverte-open-licence/"}
        ecrire(f'wiki/{a["slug"]}.html', page(html.escape(titre_page, quote=False), corps, "textes", "../", html.escape(desc),
                                             jsonld=[ld, fil(("Accueil", ""), ("Textes du métier", "wiki/"), (th["titre"], f'wiki/#{a["theme"]}'), (titre_page, f'wiki/{a["slug"]}.html'))]))

    # index
    sections, sommaire = [], []
    for t in w["themes"]:
        liste = [a for a in arts if a["theme"] == t["cle"]]
        sommaire.append(f'<li><a href="#{t["cle"]}">{ty(t["titre"])}</a></li>')
        items = "".join(
            f'''<li data-cherche="{html.escape(_sans_accents(a["num"] + " " + a["titre"] + " " + a["en_clair"] + " " + a["concretement"]))}"><a href="{a["slug"]}.html"><span class="num-art">{ty(a["num"] if not a.get("arrete") else "Arrêté")}</span> {ty(a["titre"])}</a></li>'''
            for a in liste)
        sections.append(f'''<section class="wiki-theme" aria-labelledby="{t["cle"]}">
      <div class="tete-bloc"><div><h2 id="{t["cle"]}">{ty(t["titre"])}</h2><p class="tete-intro">{ty(t["intro"])}</p></div><span class="meta">{len(liste)} {"textes" if len(liste) > 1 else "texte"}</span></div>
      <ul class="wiki-liste">{items}</ul>
    </section>''')
    autres = ""
    for g in w["autres"]:
        autres += f'<h3>{ty(g["titre"])}</h3><ul class="textes">' + "".join(
            f'<li class="texte"><p><a href="{html.escape(x["url"])}">{ty(x["nom"])}</a></p><p class="texte-ref">{ty(x["ref"])}</p><p>{ty(x["objet"])}</p></li>'
            for x in g["textes"]) + "</ul>"
    corps = f'''    <h1>Textes du métier</h1>
    <p class="chapeau">{ty("Les articles de loi, décrets et arrêtés qui encadrent le métier de conducteur VTC, chacun expliqué en clair avec un exemple, puis reproduit dans sa version officielle.")}</p>
    <div class="cherche">
      <label for="q">Chercher un article ou un mot</label>
      <input type="search" id="q" autocomplete="off" placeholder="{ty("Ex. : maraude, R3120-6, registre, vignette")}">
      <p id="q-res" class="meta" role="status" aria-live="polite"></p>
    </div>
    <nav class="sommaire" aria-label="Thèmes"><ul>{"".join(sommaire)}</ul></nav>
    {"".join(sections)}
    <section class="autres-textes" aria-labelledby="autres">
      <h2 id="autres">Les lois d'origine et les autres références</h2>
      <p>{ty("Ces textes ont façonné le métier ; leurs règles s'appliquent aujourd'hui à travers les articles ci-dessus. Les liens mènent au site officiel.")}</p>
      {autres}
    </section>
    <p class="meta">{ty("Textes vérifiés sur Légifrance le " + source_date + ". Ils sont comparés chaque semaine à la version en vigueur ; les changements sont annoncés dans l'Actualité VTC.")}</p>'''
    script = '''<script>
(function(){var q=document.getElementById("q"),r=document.getElementById("q-res");
function n(s){return s.toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g,"");}
q.addEventListener("input",function(){var v=n(q.value.trim()).replace(/\\s+/g," "),total=0;
document.querySelectorAll(".wiki-theme").forEach(function(s){var vis=0;
s.querySelectorAll("li[data-cherche]").forEach(function(li){var ok=!v||v.split(" ").every(function(m){return li.dataset.cherche.indexOf(m)>-1||li.dataset.cherche.replace(/-/g,"").indexOf(m.replace(/-/g,""))>-1;});li.hidden=!ok;if(ok)vis++;});
s.hidden=vis===0;total+=vis;});
r.textContent=v?(total?total+(total>1?" articles trouvés":" article trouvé"):"Aucun article ne correspond."):"";});})();
</script>
'''
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Réglementation VTC : les textes du métier expliqués",
          "url": SITE + "wiki/", "inLanguage": "fr", "dateModified": iso_fr(source_date), "author": AUTEUR, "isPartOf": {"@id": SITE + "#site"},
          "hasPart": [{"@type": "Article", "headline": a["titre"], "url": SITE + f'wiki/{a["slug"]}.html'} for a in arts]}
    ecrire("wiki/index.html", page("Réglementation VTC : les textes du métier expliqués en clair · Révision VTC", corps, "textes", "../",
                                   "La réglementation VTC article par article : réservation préalable, maraude, carte professionnelle, registre, véhicule, plateformes, sanctions. Texte officiel en vigueur et explication en clair.",
                                   scripts_fin=script, jsonld=[ld, fil(("Accueil", ""), ("Textes du métier", "wiki/"))]))
    # l'ancienne page renvoie vers le wiki
    ecrire("textes.html", f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>Textes du métier · Révision VTC</title>
<link rel="canonical" href="{SITE}wiki/index.html"><meta http-equiv="refresh" content="0; url=wiki/index.html"></head>
<body><p><a href="wiki/index.html">Les textes du métier ont déménagé : cliquez ici.</a></p></body></html>
''')
    return arts


# ------------------------------------------------------------------ examens
def examens():
    corps = f'''    <h1>Examens blancs n° 4 et 5</h1>
    <section id="porte" aria-labelledby="titre-porte">
      <h2 id="titre-porte" class="visuellement-cache">Accès réservé aux lecteurs</h2>
      <p class="chapeau">{ty("Ces deux examens complètent les trois examens imprimés dans le livre. Ils sont réservés à ses lecteurs.")}</p>
      <form class="acces" id="form-acces" novalidate>
        <label for="reponse">Quel est le dernier mot du titre de la fiche G2.6, page 160 du livre ?</label>
        <p class="aide" id="aide-reponse">Un seul mot, sans article. Majuscules et accents indifférents.</p>
        <input type="text" id="reponse" name="reponse" autocomplete="off" autocapitalize="none" spellcheck="false" aria-describedby="aide-reponse erreur">
        <p class="erreur" id="erreur" role="alert"></p>
        <button class="bouton" type="submit">Accéder aux examens</button>
      </form>
    </section>
    <section id="contenu-examens" hidden aria-labelledby="titre-examens">
      <h2 id="titre-examens" class="visuellement-cache">Les deux examens</h2>
      <p class="chapeau">{ty("Faites-les dans les conditions de l'examen : sans livre ni notes, en respectant la durée de chaque épreuve. Chaque corrigé renvoie à la fiche du livre à revoir.")}</p>
      <h2>Examen blanc n° 4</h2>
      <div class="actions"><a class="bouton" href="examen.html?n=4">Faire l’examen n° 4 à l’écran</a><a class="bouton second" href="pdf/Examen_blanc_4.pdf">Examen n° 4 à imprimer (PDF, 490 ko)</a></div>
      <h2>Examen blanc n° 5</h2>
      <div class="actions"><a class="bouton" href="examen.html?n=5">Faire l’examen n° 5 à l’écran</a><a class="bouton second" href="pdf/Examen_blanc_5.pdf">Examen n° 5 à imprimer (PDF, 490 ko)</a></div>
      <h2>Comment ça marche</h2>
      <ul>
        <li>{ty("Vous choisissez une épreuve. Le chronomètre démarre avec sa durée officielle ; vous pouvez le désactiver si vous préférez travailler sans limite de temps.")}</li>
        <li>{ty("Les QCM sont corrigés automatiquement. Pour les QRC, vous comparez votre réponse au corrigé type et vous notez vous-même vos points, avec le barème.")}</li>
        <li>{ty("À la fin, le tableau calcule votre moyenne avec les coefficients et indique si vous seriez admissible.")}</li>
        <li>{ty("Vos réponses restent dans votre navigateur : rien n'est envoyé.")}</li>
      </ul>
      <h2>De vrais sujets en plus</h2>
      <p>{ty("CMA France publie gratuitement les annales officielles de l'examen, de 2019 à 2022, toutes épreuves comprises :")} <a href="https://www.artisanat.fr/nous-connaitre/vous-accompagner/examens-taxi-vtc-vmdtr">{ty("annales sur artisanat.fr")}</a>. {ty("Les règles qu'elles citent datent de chaque session : en cas de différence, fiez-vous au livre et aux mises à jour de ce site.")}</p>
    </section>'''
    fin = '''<script src="js/acces.js"></script>
<script>
(function () {
  var porte = document.getElementById('porte'), contenu = document.getElementById('contenu-examens');
  function ouvrir(focus) { porte.hidden = true; contenu.hidden = false; if (focus) { var t = document.querySelector('main h1'); t.setAttribute('tabindex', '-1'); t.focus(); } }
  if (window.Acces.ouvert()) ouvrir(false);
  document.getElementById('form-acces').addEventListener('submit', async function (ev) {
    ev.preventDefault();
    var err = document.getElementById('erreur'), champ = document.getElementById('reponse');
    err.textContent = '';
    if (await window.Acces.verifier(champ.value)) { ouvrir(true); }
    else { err.textContent = 'Ce n’est pas le bon mot. Vérifiez le titre de la fiche G2.6, page 160.'; champ.setAttribute('aria-invalid', 'true'); champ.focus(); }
  });
})();
</script>
'''
    ecrire("examens.html", page("Examens blancs n° 4 et 5 · Révision VTC", corps, "examens", "",
                                "Les examens blancs n° 4 et 5 du livre Machine à Réussite · Examen VTC 2027, réservés aux lecteurs.", True, "", fin))
    barre = '''<div class="barre" id="barre" role="region" aria-label="Chronomètre de l’épreuve" hidden>
  <div class="page">
    <span class="titre" id="barre-titre"></span>
    <span class="chrono" id="chrono" role="timer" aria-live="off"></span>
  </div>
</div>
<p class="visuellement-cache" id="annonce" aria-live="polite"></p>
'''
    corps_ex = '    <p class="meta">Chargement de l’examen…</p>'
    fin_ex = '''<script src="js/acces.js"></script>
<script>
(function () {
  if (!window.Acces.ouvert()) { location.replace('examens.html'); return; }
  var n = new URLSearchParams(location.search).get('n');
  if (n !== '4' && n !== '5') { location.replace('examens.html'); return; }
  var s = document.createElement('script');
  s.src = 'data/examen-' + n + '.js';
  s.onload = function () { var a = document.createElement('script'); a.src = 'js/examen.js'; document.body.appendChild(a); };
  document.body.appendChild(s);
})();
</script>
'''
    ecrire("examen.html", page("Examen blanc · Révision VTC", corps_ex, "examens", "", "", True, "", fin_ex, barre))


# ------------------------------------------------------------------ pages légales
def legales():
    corps = f'''    <p class="surtitre">Informations</p>
    <h1>Mentions légales</h1>
    <h2>Éditeur du site</h2>
    <p>{ty("Ce site gratuit est édité à titre non professionnel par l'auteur du livre Machine à Réussite · Examen VTC 2027. Conformément à l'article 6, III, 2 de la loi n° 2004-575 du 21 juin 2004 pour la confiance dans l'économie numérique, l'éditeur a choisi de rester anonyme : ses coordonnées ont été communiquées à l'hébergeur.")}</p>
    <p>Contact : <a href="mailto:benjamin@revision-vtc.fr">benjamin@revision-vtc.fr</a></p>
    <h2>Hébergement</h2>
    <p>GitHub, Inc. (service GitHub Pages), 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis. Téléphone : +1 877 448 4820.</p>
    <h2>Données personnelles</h2>
    <p>{ty("Ce site ne dépose aucun cookie et n'affiche aucune publicité. Il mesure sa fréquentation avec GoatCounter, un outil sans cookie qui ne conserve que des chiffres d'ensemble (pages vues, site de provenance, type d'appareil, pays) et ne permet pas d'identifier les visiteurs. Vos réponses aux examens blancs sont enregistrées uniquement dans votre navigateur, pour que vous puissiez reprendre là où vous en étiez : elles ne sont jamais envoyées. Vous pouvez les effacer depuis l'examen (« Effacer mes réponses ») ou en vidant les données du site dans votre navigateur.")}</p>
    <p>{ty("Les polices de caractères sont hébergées sur ce site. Deux services tiers sont appelés : GoatCounter (gc.zgo.at), pour la mesure de fréquentation, et, seulement quand vous envoyez un message depuis la page Contact, Web3Forms (api.web3forms.com). L'hébergeur peut conserver des journaux techniques de connexion (adresse IP) pour la sécurité du service.")}</p>
    <h3>Formulaire de contact</h3>
    <p>{ty("Les informations saisies (prénom, nom, adresse e-mail, message) servent uniquement à répondre à votre message. Elles sont transmises par le service Web3Forms, qui les achemine par e-mail sans conserver les messages, puis conservées dans la boîte de réception de l'éditeur le temps de l'échange, et au plus un an. Elles ne sont ni cédées, ni utilisées pour de la prospection. Base légale : votre demande. Vous pouvez demander leur consultation, leur rectification ou leur effacement en écrivant à")} <a href="mailto:benjamin@revision-vtc.fr">benjamin@revision-vtc.fr</a>{ty(", et saisir la CNIL (cnil.fr) en cas de difficulté.")}</p>
    <h2>Propriété intellectuelle</h2>
    <p>{ty("Les textes, questions et corrigés de ce site sont la propriété de Benjamin Blondin. Toute reproduction sans autorisation est interdite (Code de la propriété intellectuelle, art. L122-4). Les brèves de l'Actualité VTC citent leurs sources, qui restent la propriété de leurs auteurs.")}</p>
    <p>{ty("Les textes officiels reproduits dans la rubrique Textes du métier proviennent de Légifrance (DILA). Ils sont réutilisés sous Licence Ouverte 2.0, avec mention de la source et de la date de version. Seule la version publiée sur Légifrance fait foi.")}</p>
    <h2>Avertissement</h2>
    <p>{ty("Ce site et le livre sont des ouvrages indépendants : ils ne sont édités ni par les chambres de métiers et de l'artisanat ni par l'État. Ils préparent à l'examen et ne remplacent pas un conseil juridique, comptable ou fiscal adapté à votre situation.")}</p>'''
    ecrire("mentions-legales.html", page("Mentions légales · Révision VTC", corps, None, "",
                                         "Mentions légales de revision-vtc.fr : éditeur, hébergeur, données personnelles, propriété intellectuelle et réutilisation des textes officiels."))
    corps = f'''    <p class="surtitre">Informations</p>
    <h1>Accessibilité</h1>
    <p class="chapeau">{ty("Ce site a été conçu pour être utilisable par tous, au clavier, avec un lecteur d'écran ou avec un zoom important.")}</p>
    <h2>Ce qui a été fait</h2>
    <ul>
      <li>{ty("Textes contrastés, taille de lecture confortable, mise en page qui s'adapte au téléphone et au zoom jusqu'à 400 %.")}</li>
      <li>{ty("Navigation au clavier, lien d'évitement vers le contenu, focus toujours visible.")}</li>
      <li>{ty("Titres hiérarchisés, tableaux avec en-têtes, champs de formulaire étiquetés, questions des examens regroupées avec leur énoncé.")}</li>
      <li>{ty("Le résultat d'une question n'est jamais indiqué par la couleur seule. Le chronomètre des examens peut être désactivé.")}</li>
      <li>{ty("Aucune animation, aucun contenu qui défile ou clignote ; thème sombre automatique si votre appareil le demande.")}</li>
    </ul>
    <h2>État de conformité</h2>
    <p>{ty("Le site n'a pas fait l'objet d'un audit de conformité au RGAA. Il a été vérifié avec des outils automatiques et une navigation au clavier.")}</p>
    <h2>Signaler un problème</h2>
    <p>{ty("Si un contenu vous est inaccessible, écrivez à")} <a href="mailto:benjamin@revision-vtc.fr">benjamin@revision-vtc.fr</a> {ty(": vous recevrez l'information sous une autre forme, et le problème sera corrigé.")}</p>'''
    ecrire("accessibilite.html", page("Accessibilité · Révision VTC", corps, None, "",
                                      "Ce qui a été fait pour que revision-vtc.fr soit utilisable par tous : clavier, lecteur d'écran, contrastes, zoom."))


# ------------------------------------------------------------------ questions VTC
def lire_questions(slugs_wiki):
    qs = []
    for f in sorted(glob.glob(os.path.join(CONTENU, "questions", "*.json")), reverse=True):
        with open(f, encoding="utf-8") as h:
            q = json.load(h)
        assert os.path.basename(f) == f'{q["date"]}-{q["slug"]}.json', f
        assert q["sources"] and all(x["url"].startswith("https://") for x in q["sources"]), f"{f} : source manquante"
        assert q["question"].endswith("?") and 50 <= len(q["reponse_courte"]) <= 400, f"{f} : question ou réponse courte"
        for w in q.get("wiki", []):
            assert w in slugs_wiki, f"{f} : page du wiki inconnue {w}"
        qs.append(q)
    slugs = [q["slug"] for q in qs]
    assert len(slugs) == len(set(slugs)), "deux questions ont la même adresse"
    return qs


def questions(qs, w):
    arts = {a["slug"]: a for a in w["articles"]}
    for q in qs:
        secs = "".join(f'<h2>{ty(x["titre"])}</h2>' + "".join(f"<p>{ty(p)}</p>" for p in x["texte"]) for x in q["sections"])
        wiki = "".join(f'<li><a href="../wiki/{s}.html">{ty(arts[s]["num"] if not arts[s].get("arrete") else "Arrêté")} · {ty(arts[s]["titre"])}</a></li>' for s in q.get("wiki", []))
        livre = "".join(f"<li><b>Fiche {ty(c)}</b> · {ty(t)}</li>" for c, t in q.get("fiches", []))
        src = "".join(f'<li><a href="{html.escape(x["url"])}">{ty(x["nom"])}</a>' + (f", {ty(x['date'])}" if x.get("date") else "") + "</li>" for x in q["sources"])
        autres = "".join(f'<li><a href="{x["date"]}-{x["slug"]}.html">{ty(x["question"])}</a></li>' for x in qs if x is not q)[:4000]
        corps = f'''    <nav class="fil" aria-label="Fil d'Ariane"><ol><li><a href="index.html">Questions VTC</a></li></ol></nav>
    <p class="surtitre">Question VTC</p>
    <h1>{ty(q["question"])}</h1>
    <p class="meta">Publié le {date_fr(q["date"])} · vérifié le {ty(q["verifie"])}</p>
    <div class="deux-col"><div class="col-texte">
    <section class="en-clair" aria-labelledby="courte">
      <h2 id="courte">La réponse courte</h2>
      <p>{ty(q["reponse_courte"])}</p>
    </section>
    {secs}
    <section class="retenir" aria-labelledby="retenir"><h2 id="retenir">À retenir</h2><ul>{"".join(f"<li>{ty(x)}</li>" for x in q["a_retenir"])}</ul></section>
    <h2>Sources</h2>
    <ul class="source">{src}</ul>
    <p class="source">{ty("Seule la version des textes publiée sur Légifrance fait foi. Cette réponse ne remplace pas un conseil juridique adapté à votre situation.")}</p>
    </div>
    <aside class="col-cote" aria-label="Pour aller plus loin">
    {f'<section class="cote-bloc"><h2>Les textes expliqués</h2><ul class="voir-aussi">{wiki}</ul></section>' if wiki else ""}
    {f'<section class="cote-bloc wiki-livre"><h2>Dans le livre</h2><ul>{livre}</ul><p class="pied-achat">{achat("bouton second petit", "Le livre sur Amazon")}</p></section>' if livre else ""}
    {f'<section class="cote-bloc"><h2>Autres questions</h2><ul class="voir-aussi">{autres}</ul></section>' if autres else ""}
    </aside></div>'''
        chemin = f'questions/{q["date"]}-{q["slug"]}.html'
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": q["question"][:110], "description": q["reponse_courte"],
              "datePublished": q["date"], "dateModified": iso_fr(q["verifie"]), "inLanguage": "fr", "author": AUTEUR, "publisher": AUTEUR,
              "image": SITE + "partage.jpg", "mainEntityOfPage": SITE + chemin, "citation": [x["url"] for x in q["sources"]],
              "mainEntity": {"@type": "Question", "name": q["question"], "acceptedAnswer": {"@type": "Answer", "text": q["reponse_courte"]}}}
        ecrire(chemin, page(html.escape(q["question"] + " · Révision VTC", quote=False), corps, "questions", "../",
                            html.escape(q["reponse_courte"] if len(q["reponse_courte"]) <= 158 else q["reponse_courte"][:155].rsplit(" ", 1)[0] + "…"),
                            jsonld=[ld, fil(("Accueil", ""), ("Questions VTC", "questions/"), (q["question"], chemin))]))
    liste = "".join(f'''<li><span class="meta">{date_fr(q["date"])}</span><a href="{q["date"]}-{q["slug"]}.html">{ty(q["question"])}</a><p>{ty(q["reponse_courte"])}</p></li>''' for q in qs)
    corps = f'''    <h1>Questions VTC</h1>
    <p class="chapeau">{ty("Les questions concrètes que se posent les chauffeurs VTC et les candidats à l'examen, avec une réponse courte, les textes qui la fondent et leurs sources.")}</p>
    <p>{ty("Une nouvelle question chaque semaine. Les règles citées sont expliquées article par article dans les")} <a href="../wiki/index.html">textes du métier</a>.</p>
    <ul class="questions">{liste}</ul>'''
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Questions VTC", "url": SITE + "questions/", "inLanguage": "fr",
          "hasPart": [{"@type": "Article", "headline": q["question"], "url": SITE + f'questions/{q["date"]}-{q["slug"]}.html'} for q in qs]}
    ecrire("questions/index.html", page("Questions VTC : réponses courtes et sourcées sur le métier et l'examen · Révision VTC", corps, "questions", "../",
                                        "Les questions concrètes des chauffeurs VTC et des candidats à l'examen : une réponse courte, les textes officiels qui la fondent et leurs sources. Une nouvelle question chaque semaine.",
                                        jsonld=[ld, fil(("Accueil", ""), ("Questions VTC", "questions/"))]))


# ------------------------------------------------------------------ contact
def contact():
    with open(os.path.join(CONTENU, "contact.json"), encoding="utf-8") as h:
        cle = json.load(h).get("web3forms_cle", "").strip()
    assert re.fullmatch(r"[0-9a-f-]{0,40}", cle), "clé Web3Forms invalide"
    MAX = 1000
    if cle:
        formulaire = f"""
    <form id="form-contact" class="contact" action="https://api.web3forms.com/submit" method="POST" novalidate>
      <input type="hidden" name="access_key" value="{cle}">
      <input type="hidden" name="subject" value="Message depuis revision-vtc.fr">
      <input type="hidden" name="from_name" value="revision-vtc.fr">
      <p class="piege" aria-hidden="true"><label>Ne pas remplir <input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off"></label></p>
      <p class="aide">Tous les champs sont obligatoires.</p>
      <div class="champs-2">
        <div class="champ"><label for="prenom">Prénom</label><input type="text" id="prenom" name="prenom" autocomplete="given-name" required maxlength="60" aria-describedby="err-prenom"><p class="erreur" id="err-prenom"></p></div>
        <div class="champ"><label for="nom">Nom</label><input type="text" id="nom" name="nom" autocomplete="family-name" required maxlength="60" aria-describedby="err-nom"><p class="erreur" id="err-nom"></p></div>
      </div>
      <div class="champ"><label for="email">Adresse e-mail</label><p class="aide" id="aide-email">Pour vous répondre. Exemple : prenom.nom@exemple.fr</p><input type="email" id="email" name="email" autocomplete="email" required maxlength="120" aria-describedby="aide-email err-email"><p class="erreur" id="err-email"></p></div>
      <div class="champ"><label for="message">Votre message</label><p class="aide" id="aide-message">1&#8239;000 caractères au maximum.</p><textarea id="message" name="message" required maxlength="{MAX}" rows="7" aria-describedby="aide-message compteur err-message"></textarea><p class="meta compteur" id="compteur" aria-live="polite">0 / {MAX}</p><p class="erreur" id="err-message"></p></div>
      <p class="aide">{ty("Vos données servent uniquement à vous répondre. Elles sont transmises par le service Web3Forms, qui ne conserve pas les messages, et ne sont jamais utilisées à d'autres fins. Détails dans les")} <a href="mentions-legales.html">mentions légales</a>.</p>
      <div class="actions"><button type="submit" class="bouton" id="envoyer">Envoyer le message</button></div>
      <div id="etat" role="status" aria-live="polite"></div>
    </form>"""
        script = """<script>
(function(){
  var f=document.getElementById('form-contact'); if(!f) return;
  var debut=Date.now(), b=document.getElementById('envoyer'), etat=document.getElementById('etat'), msg=document.getElementById('message'), cpt=document.getElementById('compteur');
  msg.addEventListener('input',function(){cpt.textContent=msg.value.length+' / '+msg.maxLength;});
  var regles={prenom:'Indiquez votre prénom.',nom:'Indiquez votre nom.',email:'Indiquez une adresse e-mail valide, par exemple prenom.nom@exemple.fr.',message:'Écrivez votre message.'};
  function verifier(){
    var premier=null;
    Object.keys(regles).forEach(function(id){
      var c=document.getElementById(id), e=document.getElementById('err-'+id), ok=c.value.trim()!=='' && c.checkValidity();
      e.textContent= ok ? '' : regles[id];
      if(ok) c.removeAttribute('aria-invalid'); else { c.setAttribute('aria-invalid','true'); if(!premier) premier=c; }
    });
    if(premier) premier.focus();
    return !premier;
  }
  f.addEventListener('submit',function(ev){
    ev.preventDefault();
    if(!verifier()) return;
    if(f.botcheck.checked || Date.now()-debut<3000){ etat.className='note'; etat.textContent='Merci, votre message a bien été envoyé.'; return; }
    b.disabled=true; b.textContent='Envoi en cours…'; etat.className=''; etat.textContent='';
    var donnees=Object.fromEntries(new FormData(f));
    donnees.name=donnees.prenom+' '+donnees.nom;
    fetch(f.action,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(donnees)})
      .then(function(r){return r.json();})
      .then(function(j){
        if(j.success){ f.reset(); cpt.textContent='0 / '+msg.maxLength; etat.className='note succes'; etat.textContent='Merci, votre message a bien été envoyé. Vous recevrez une réponse à l’adresse indiquée.'; }
        else throw new Error();
      })
      .catch(function(){ etat.className='note echec'; etat.innerHTML='Le message n’a pas pu partir. Réessayez dans un instant, ou écrivez directement à <a href="mailto:benjamin@revision-vtc.fr">benjamin@revision-vtc.fr</a>.'; })
      .finally(function(){ b.disabled=false; b.textContent='Envoyer le message'; etat.focus(); });
  });
  etat.setAttribute('tabindex','-1');
})();
</script>
"""
    else:
        formulaire = f"""
    <p class="note">{ty("Le formulaire de contact sera ouvert très prochainement. En attendant, écrivez à")} <a href="mailto:benjamin@revision-vtc.fr">benjamin@revision-vtc.fr</a>.</p>"""
        script = ""
    corps = f'''    <p class="surtitre">Le site</p>
    <h1>Contact</h1>
    <p class="chapeau">{ty("Une question sur le livre, une erreur à signaler, une règle qui a changé ? Écrivez ici : chaque message est lu et reçoit une réponse.")}</p>
    {formulaire}
    <h2>Avant d'écrire</h2>
    <ul>
      <li>{ty("Pour une question de réglementation, la réponse est peut-être déjà dans les")} <a href="wiki/index.html">textes du métier</a> {ty("ou les")} <a href="questions/index.html">Questions VTC</a>.</li>
      <li>{ty("Ce site ne donne pas de conseil juridique, comptable ou fiscal personnalisé.")}</li>
    </ul>'''
    ld = {"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact", "url": SITE + "contact.html", "inLanguage": "fr",
          "about": {"@id": SITE + "#site"}}
    ecrire("contact.html", page("Contact · Révision VTC", corps, None, "",
                                "Écrire à l'auteur du site Révision VTC et du livre Machine à Réussite · Examen VTC 2027 : question, erreur à signaler, règle qui a changé.",
                                scripts_fin=script, jsonld=[ld]))


# ------------------------------------------------------------------ dossiers
APERCU = "--apercu" in sys.argv   # génère aussi les brouillons, dans apercu/ (jamais publié)


def liens(t):
    """Texte déjà passé par ty() : transforme [texte](adresse) en lien (maillage interne et sources)."""
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', t)


def illustration(img, premiere=False):
    """Photo avec légende et crédit. Fichiers attendus dans docs/images/dossiers/ : <fichier>-640.webp et <fichier>-1200.webp
    (3:2, 1 200 × 800 px), plus <fichier>-1200.jpg pour l'image d'en-tête (partage sur les réseaux sociaux)."""
    base = f'images/dossiers/{img["fichier"]}'
    for taille in ("640", "1200"):
        assert os.path.exists(os.path.join(DOCS, f"{base}-{taille}.webp")), f"image manquante : {base}-{taille}.webp"
    assert 20 <= len(img["alt"]) <= 200, f"{base} : texte alternatif de 20 à 200 caractères"
    credit = f'<a href="{html.escape(img["lien"])}">{ty(img["credit"])}</a>' if img.get("lien") else ty(img["credit"])
    charge = 'fetchpriority="high"' if premiere else 'loading="lazy"'
    return (f'<figure class="illustration"><img src="../{base}-1200.webp" srcset="../{base}-640.webp 640w, ../{base}-1200.webp 1200w" '
            f'sizes="(min-width: 50rem) 46rem, calc(100vw - 3rem)" width="1200" height="800" alt="{html.escape(img["alt"])}" {charge} decoding="async">'
            f'<figcaption>{ty(img["legende"])} <span class="credit">Photo : {credit}, Pixabay.</span></figcaption></figure>')


def _bloc_dossier(b):
    """Un bloc d'une section : paragraphe (texte), liste, tableau chiffré, encart ou photo."""
    if isinstance(b, str):
        return f"<p>{liens(ty(b))}</p>"
    if "liste" in b:
        return "<ul>" + "".join(f"<li>{liens(ty(x))}</li>" for x in b["liste"]) + "</ul>"
    if "note" in b:
        return f'<p class="note">{liens(ty(b["note"]))}</p>'
    if "image" in b:
        return illustration(b["image"])
    t = b["tableau"]
    assert t.get("legende") and t["colonnes"] and t["lignes"], "tableau sans légende"
    nombres = set(t.get("nombres", []))
    cl = lambda i: ' class="nombre"' if i in nombres else ""
    tete = "".join(f'<th scope="col"{cl(i)}>{ty(c)}</th>' for i, c in enumerate(t["colonnes"]))
    def ligne(l, total=False):
        assert len(l) == len(t["colonnes"]), f"tableau « {t['legende']} » : ligne de {len(l)} cases"
        gras = (lambda x: f"<strong>{x}</strong>" if x else "") if total else (lambda x: x)
        return "<tr>" + f'<th scope="row">{liens(ty(l[0]))}</th>' + "".join(f"<td{cl(i)}>{gras(liens(ty(c)))}</td>" for i, c in enumerate(l[1:], 1)) + "</tr>"
    pied = f'<tfoot>{"".join(ligne(l, True) for l in t["total"])}</tfoot>' if t.get("total") else ""
    _bloc_dossier.n = getattr(_bloc_dossier, "n", 0) + 1
    ident = f"tableau-{_bloc_dossier.n}"
    # la zone défile sur téléphone : elle doit pouvoir recevoir le focus clavier (accessibilité)
    return (f'<div class="defile" tabindex="0" role="region" aria-labelledby="{ident}"><table><caption id="{ident}">{ty(t["legende"])}</caption><thead><tr>{tete}</tr></thead>'
            f'<tbody>{"".join(ligne(l) for l in t["lignes"])}</tbody>{pied}</table></div>')


def _texte_dossier(d):
    """Tout le texte d'un dossier, sans balises (comptage des mots, llms-full)."""
    morceaux = [d["chapeau"], *d["en_bref"]]
    for s in d["sections"]:
        morceaux.append(s["titre"])
        for b in s["blocs"]:
            if isinstance(b, str):
                morceaux.append(b)
            elif "liste" in b:
                morceaux += b["liste"]
            elif "note" in b:
                morceaux.append(b["note"])
            elif "image" in b:
                continue
            else:
                morceaux += [" ".join(l) for l in b["tableau"]["lignes"] + b["tableau"].get("total", [])]
    morceaux += d["a_retenir"]
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", "\n".join(morceaux))


def lire_dossiers(slugs_wiki):
    ds = []
    for f in sorted(glob.glob(os.path.join(CONTENU, "dossiers", "*.json"))):
        with open(f, encoding="utf-8") as h:
            d = json.load(h)
        assert os.path.basename(f) == d["slug"] + ".json", f"{f} : le nom du fichier doit être l'adresse de la page"
        assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", d["slug"]), f"{f} : adresse invalide"
        assert d["sources"] and all(x["url"].startswith("https://") for x in d["sources"]), f"{f} : source manquante"
        assert 50 <= len(d["description"]) <= 160, f"{f} : description de 50 à 160 caractères"
        for w in d.get("wiki", []):
            assert w in slugs_wiki, f"{f} : page du wiki inconnue {w}"
        for s in d["sections"]:
            assert re.fullmatch(r"[a-z0-9-]+", s["id"]), f"{f} : identifiant de section {s['id']}"
        d["mots"] = len(re.findall(r"\w+", _texte_dossier(d)))
        assert d.get("brouillon") or 1200 <= d["mots"] <= 3000, f"{f} : {d['mots']} mots (dossier : 1 500 à 2 500 mots)"
        if d.get("brouillon") and not APERCU:
            continue
        ds.append(d)
    ds.sort(key=lambda d: d["date"], reverse=True)
    assert len({d["numero"] for d in ds}) == len(ds), "deux dossiers ont le même numéro"
    return ds


def dossiers(ds, w, qs=()):
    arts = {a["slug"]: a for a in w["articles"]}
    for d in ds:
        secs = "".join(f'\n    <h2 id="{s["id"]}">{ty(s["titre"])}</h2>' + "".join(_bloc_dossier(b) for b in s["blocs"]) for s in d["sections"])
        sommaire = "".join(f'<li><a href="#{s["id"]}">{ty(s["titre"])}</a></li>' for s in d["sections"])
        wiki = "".join(f'<li><a href="../wiki/{s}.html">{ty(arts[s]["num"] if not arts[s].get("arrete") else "Arrêté")} · {ty(arts[s]["titre"])}</a></li>' for s in d.get("wiki", []))
        livre = "".join(f"<li><b>Fiche {ty(c)}</b> · {ty(t)}</li>" for c, t in d.get("fiches", []))
        autres = "".join(f'<li><a href="{x["slug"]}.html">{ty(x["titre"])}</a></li>' for x in ds if x is not d)
        src = "".join(f'<li><a href="{html.escape(x["url"])}">{ty(x["nom"])}</a>' + (f", {ty(x['date'])}" if x.get("date") else "") + "</li>" for x in d["sources"])
        maj = f' · mis à jour le {ty(d["mis_a_jour"])}' if d.get("mis_a_jour") else ""
        corps = f'''    <nav class="fil" aria-label="Fil d'Ariane"><ol><li><a href="index.html">Dossiers</a></li></ol></nav>
    <p class="surtitre">Dossier n° {d["numero"]}</p>
    <h1>{ty(d["titre"])}</h1>
    <p class="chapeau">{ty(d["chapeau"])}</p>
    <p class="meta">Publié le {date_fr(d["date"])}{maj} · chiffres vérifiés le {ty(d["verifie"])} · {d["mots"] // 230 + 1} min de lecture</p>
    <div class="deux-col"><div class="col-texte">
    {illustration(d["image"], premiere=True) if d.get("image") else ""}
    <section class="en-clair" aria-labelledby="en-bref">
      <h2 id="en-bref">La réponse en bref</h2>
      {"".join(f"<p>{liens(ty(p))}</p>" for p in d["en_bref"])}
    </section>{secs}
    <section class="retenir" aria-labelledby="retenir"><h2 id="retenir">À retenir</h2><ul>{"".join(f"<li>{liens(ty(x))}</li>" for x in d["a_retenir"])}</ul></section>
    <h2 id="sources">Sources</h2>
    <ul class="source">{src}</ul>
    <p class="source">{ty("Montants vérifiés le " + d["verifie"] + " sur les sites officiels cités ; les tarifs non réglementés (formation, assurance, véhicule) sont des fourchettes publiées, à comparer avec vos propres devis. Ce dossier ne remplace pas un conseil juridique, comptable ou financier adapté à votre situation.")}</p>
    </div>
    <aside class="col-cote" aria-label="Sommaire et pour aller plus loin">
    <nav class="cote-bloc" aria-labelledby="titre-sommaire"><h2 id="titre-sommaire">Sommaire</h2><ul class="voir-aussi">{sommaire}</ul></nav>
    {f'<section class="cote-bloc" aria-labelledby="titre-textes"><h2 id="titre-textes">Les textes expliqués</h2><ul class="voir-aussi">{wiki}</ul></section>' if wiki else ""}
    {f'<section class="cote-bloc wiki-livre" aria-labelledby="titre-livre"><h2 id="titre-livre">Dans le livre</h2><ul>{livre}</ul><p class="pied-achat">{achat("bouton second petit", "Le livre sur Amazon")}</p></section>' if livre else ""}
    {f'<section class="cote-bloc" aria-labelledby="titre-autres"><h2 id="titre-autres">Autres dossiers</h2><ul class="voir-aussi">{autres}</ul></section>' if autres else ""}
    </aside></div>'''
        chemin = f'dossiers/{d["slug"]}.html'
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": d["titre"][:110], "description": d["description"],
              "abstract": " ".join(d["en_bref"]), "datePublished": d["date"], "dateModified": iso_fr(d.get("mis_a_jour") or d["verifie"]) if iso_fr(d.get("mis_a_jour") or d["verifie"]) > d["date"] else d["date"],
              "inLanguage": "fr", "author": AUTEUR, "publisher": AUTEUR, "mainEntityOfPage": SITE + chemin,
              "image": [SITE + f'images/dossiers/{d["image"]["fichier"]}-1200.jpg'] if d.get("image") else SITE + "partage.jpg",
              "articleSection": "Dossiers", "wordCount": d["mots"], "keywords": d.get("mots_cles", []), "isPartOf": {"@id": SITE + "#site"},
              "citation": [x["url"] for x in d["sources"]]}
        partage = ""
        if d.get("image"):
            jpg = f'images/dossiers/{d["image"]["fichier"]}-1200.jpg'
            assert os.path.exists(os.path.join(DOCS, jpg)), f"image de partage manquante : {jpg}"
            partage = (f'<meta property="og:image" content="{SITE}{jpg}">\n<meta property="og:image:width" content="1200">\n'
                       f'<meta property="og:image:height" content="800">\n<meta property="og:image:alt" content="{html.escape(d["image"]["alt"])}">\n')
        ecrire(chemin, page(html.escape(d.get("titre_page", d["titre"]) + " · Révision VTC", quote=False), corps, "dossiers", "../", html.escape(d["description"]),
                            noindex=bool(d.get("brouillon")), scripts_tete=partage,
                            jsonld=[ld, fil(("Accueil", ""), ("Dossiers", "dossiers/"), (d["titre"], chemin))]))
    if ds:
        liste = "".join(f'''<li><span class="meta">Dossier n° {d["numero"]} · {date_fr(d["date"])}</span><a href="{d["slug"]}.html">{ty(d["titre"])}</a><p>{ty(d["description"])}</p></li>''' for d in ds)
        liste = f'<ul class="questions">{liste}</ul>'
    else:
        liste = f'<p class="note">{ty("Le premier dossier sera publié très prochainement.")}</p>'
    corps = f'''    <h1>Dossiers VTC</h1>
    <p class="chapeau">{ty("Les grandes questions du métier de chauffeur VTC, traitées à fond : coûts, revenus, statut, véhicule, cotisations. Chaque chiffre est daté et relié à sa source.")}</p>
    <p>{ty("Un nouveau dossier chaque semaine. Pour une réponse rapide à une question précise, voyez les")} <a href="../questions/index.html">Questions VTC</a> {ty("; pour le texte exact d'une règle, les")} <a href="../wiki/index.html">textes du métier</a>.</p>
    {liste}'''
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Dossiers VTC", "url": SITE + "dossiers/", "inLanguage": "fr",
          "isPartOf": {"@id": SITE + "#site"},
          "hasPart": [{"@type": "Article", "headline": d["titre"], "url": SITE + f'dossiers/{d["slug"]}.html'} for d in ds]}
    ecrire("dossiers/index.html", page("Dossiers VTC : coûts, revenus, statut, véhicule, expliqués et chiffrés · Révision VTC", corps, "dossiers", "../",
                                       "Les dossiers de Révision VTC : combien coûte le lancement en VTC, combien gagne un chauffeur, quel statut choisir. Chiffres datés et sources officielles.",
                                       jsonld=[ld, fil(("Accueil", ""), ("Dossiers", "dossiers/"))]))


def indexnow():
    """IndexNow (Bing, Yandex, Seznam…) : la clé publique doit être servie à la racine du site."""
    with open(os.path.join(CONTENU, "indexnow.json"), encoding="utf-8") as h:
        cle = json.load(h)["cle"]
    assert re.fullmatch(r"[0-9a-f]{32}", cle), "clé IndexNow invalide"
    ecrire(f"{cle}.txt", cle)


# ------------------------------------------------------------------ à propos, page 404
def a_propos():
    corps = f'''    <p class="surtitre">Le site</p>
    <h1>À propos et méthode</h1>
    <p class="chapeau">{ty("Révision VTC est un site gratuit et indépendant sur le métier de chauffeur VTC et l'examen d'accès à la profession. Il prolonge le livre Machine à Réussite · Examen VTC 2027.")}</p>
    <h2>Qui publie ce site</h2>
    <p>{ty("Le site est publié à titre non professionnel par Benjamin Blondin, auteur du livre Machine à Réussite · Examen VTC 2027 (540 pages, ISBN 979-8-1652-8079-5). Il ne contient aucune publicité et ne vend aucune formation. Il n'est édité ni par l'État, ni par les chambres de métiers et de l'artisanat, ni par une plateforme de VTC.")}</p>
    <h2>Ce que vous y trouvez</h2>
    <ul>
      <li><a href="wiki/index.html">{ty("Les textes du métier")}</a> {ty(": chaque article utile du Code des transports et chaque arrêté, avec le texte officiel en vigueur, une explication en clair et un exemple concret.")}</li>
      <li><a href="actualite/index.html">{ty("L'Actualité VTC")}</a> {ty(": chaque semaine, ce qui change pour les chauffeurs et les candidats, avec ses sources.")}</li>
      <li><a href="mises-a-jour.html">{ty("Les mises à jour du livre")}</a> {ty(": chaque règle qui a changé depuis l'impression, avec le texte qui la fonde.")}</li>
      <li><a href="examens.html">{ty("Deux examens blancs")}</a> {ty("corrigés, en plus des trois du livre.")}</li>
    </ul>
    <h2>Comment les informations sont vérifiées</h2>
    <ul>
      <li>{ty("Une information n'est publiée que si elle repose sur un texte officiel (Légifrance, Journal officiel, administration) ou sur deux sources indépendantes qui concordent.")}</li>
      <li>{ty("Chaque information cite sa source, avec un lien et une date. Ce qui n'a pas pu être vérifié n'est pas publié.")}</li>
      <li>{ty("Le site distingue toujours ce qui est en vigueur, ce qui est adopté mais pas encore applicable, et ce qui n'est qu'un projet.")}</li>
      <li>{ty("Les textes officiels du wiki sont recopiés tels quels depuis Légifrance, sans retouche, et comparés chaque semaine à la version en vigueur. La date de vérification figure sur chaque page.")}</li>
      <li>{ty("Quand une règle enseignée par le livre change, elle est inscrite dans les mises à jour du livre.")}</li>
    </ul>
    <h2>Les limites</h2>
    <p>{ty("Ce site prépare à l'examen et aide à comprendre la réglementation. Il ne remplace pas un conseil juridique, comptable ou fiscal adapté à votre situation. En cas de doute, seule la version des textes publiée sur Légifrance fait foi.")}</p>
    <h2>Signaler une erreur</h2>
    <p>{ty("Une erreur, un texte qui a changé, une question ? Écrivez à")} <a href="mailto:benjamin@revision-vtc.fr">benjamin@revision-vtc.fr</a>{ty(". Les corrections sont publiées avec leur date.")}</p>'''
    ld = {"@context": "https://schema.org", "@type": "AboutPage", "name": "À propos et méthode", "url": SITE + "a-propos.html",
          "inLanguage": "fr", "mainEntity": dict(AUTEUR, **{"@id": SITE + "a-propos.html#auteur", "description": "Auteur du livre Machine à Réussite · Examen VTC 2027",
                                                         "email": "benjamin@revision-vtc.fr"}), "about": {"@id": SITE + "#livre"}}
    ecrire("a-propos.html", page("À propos et méthode de vérification · Révision VTC", corps, None, "",
                                 "Qui publie Révision VTC et comment chaque information est vérifiée : textes officiels, deux sources concordantes, vérification hebdomadaire sur Légifrance.",
                                 jsonld=[ld]))


def page_404():
    corps = f'''    <p class="surtitre">Erreur 404</p>
    <h1>Page introuvable</h1>
    <p class="chapeau">{ty("Cette adresse n'existe pas, ou plus. Le contenu que vous cherchez est peut-être ici :")}</p>
    <ul>
      <li><a href="/wiki/index.html">{ty("La réglementation VTC, article par article")}</a></li>
      <li><a href="/actualite/index.html">{ty("L'Actualité VTC")}</a></li>
      <li><a href="/examens.html">{ty("Les examens blancs")}</a></li>
      <li><a href="/index.html">{ty("L'accueil du site")}</a></li>
    </ul>'''
    ecrire("404.html", page("Page introuvable · Révision VTC", corps, None, "/", noindex=True))


ROBOTS_IA = ["Googlebot", "Bingbot", "Google-Extended", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
             "Claude-User", "PerplexityBot", "Perplexity-User", "Applebot", "Applebot-Extended", "DuckAssistBot", "MistralAI-User", "CCBot"]


def plan(nums, arts, wiki_date, qs=(), ds=()):
    der = nums[0]["date"] if nums else wiki_date
    urls = [("", max(der, wiki_date)), ("actualite/", der), ("wiki/", wiki_date), ("a-propos.html", None), ("contact.html", None), ("mises-a-jour.html", None),
            ("examens.html", None), ("mentions-legales.html", None), ("accessibilite.html", None)]
    urls += [(f'actualite/{n["date"]}.html', n["date"]) for n in nums]
    urls += [(f'wiki/{a["slug"]}.html', wiki_date) for a in arts]
    if qs:
        urls.insert(3, ("questions/", qs[0]["date"]))
        urls += [(f'questions/{q["date"]}-{q["slug"]}.html', iso_fr(q["verifie"])) for q in qs]
    if ds:
        maj = lambda d: max(d["date"], iso_fr(d.get("mis_a_jour") or d["verifie"]))
        urls.insert(4, ("dossiers/", max(maj(d) for d in ds)))
        urls += [(f'dossiers/{d["slug"]}.html', maj(d)) for d in ds]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "".join(f"  <url><loc>{SITE}{u}</loc>" + (f"<lastmod>{d}</lastmod>" if d else "") + "</url>\n" for u, d in urls) + "</urlset>\n"
    ecrire("sitemap.xml", xml)
    # les moteurs de recherche et les assistants d'IA sont explicitement les bienvenus (référencement et citations)
    ecrire("robots.txt", "".join(f"User-agent: {r}\n" for r in ROBOTS_IA) + "Allow: /\nDisallow: /examen.html\n\n"
           f"User-agent: *\nAllow: /\nDisallow: /examen.html\n\nSitemap: {SITE}sitemap.xml\n")


def llms(nums, w, qs=(), ds=()):
    """llms.txt : le plan du site pour les assistants d'IA ; llms-full.txt : tout le wiki en texte brut, avec ses sources."""
    themes = {t["cle"]: t["titre"] for t in w["themes"]}
    l = ["# Révision VTC (revision-vtc.fr)", "",
         "> Site gratuit et indépendant sur le métier de chauffeur VTC en France et l'examen d'accès à la profession : "
         "la réglementation VTC expliquée article par article (texte officiel Légifrance en vigueur + explication en clair), "
         "l'actualité du métier chaque semaine avec ses sources, et des examens blancs. Tenu par Benjamin Blondin, auteur du livre "
         "« Machine à Réussite · Examen VTC 2027 » (ISBN 979-8-1652-8079-5).", "",
         f"Règles éditoriales : chaque information repose sur un texte officiel ou sur deux sources concordantes, toujours citées. "
         f"Les textes du wiki sont comparés chaque semaine à la version en vigueur sur Légifrance (dernière vérification : {w['verifie']}). "
         "Seule la version publiée sur Légifrance fait foi.", "",
         "## Pages principales", "",
         f"- [Réglementation VTC, les textes du métier]({SITE}wiki/): index de tous les articles par thème",
         f"- [Actualité VTC]({SITE}actualite/): un numéro par semaine, sources citées",
         f"- [Questions VTC]({SITE}questions/): une question concrète par semaine, réponse courte et sources officielles",
         f"- [Dossiers VTC]({SITE}dossiers/): articles longs et chiffrés (coût du lancement, revenus, statut, véhicule), sources datées",
         f"- [Mises à jour du livre]({SITE}mises-a-jour.html): règles qui ont changé depuis l'impression",
         f"- [Examens blancs]({SITE}examens.html): deux examens blancs corrigés, réservés aux lecteurs du livre",
         f"- [À propos et méthode]({SITE}a-propos.html): qui écrit, comment les informations sont vérifiées",
         f"- [Texte intégral du wiki]({SITE}llms-full.txt): toutes les explications et tous les textes officiels en texte brut", ""]
    for t in w["themes"]:
        l += [f"## {t['titre']}", ""]
        l += [f"- [{a['num'] if not a.get('arrete') else 'Arrêté'} · {a['titre']}]({SITE}wiki/{a['slug']}.html): {a['en_clair']}" for a in w["articles"] if a["theme"] == t["cle"]]
        l.append("")
    if ds:
        l += ["## Dossiers VTC", ""]
        l += [f"- [{d['titre']}]({SITE}dossiers/{d['slug']}.html): {' '.join(d['en_bref'])}" for d in ds]
        l.append("")
    if qs:
        l += ["## Questions VTC", ""]
        l += [f"- [{q['question']}]({SITE}questions/{q['date']}-{q['slug']}.html): {q['reponse_courte']}" for q in qs]
        l.append("")
    if nums:
        l += ["## Derniers numéros de l'Actualité VTC", ""]
        l += [f"- [{n['titre']}]({SITE}actualite/{n['date']}.html): {' '.join(n['a_retenir'])}" for n in nums[:8]]
        l.append("")
    ecrire("llms.txt", "\n".join(l))
    f = [f"# Réglementation VTC expliquée · revision-vtc.fr", "",
         f"Textes officiels recopiés de Légifrance, version en vigueur au {w['verifie']} (Licence Ouverte 2.0). "
         "Explications « En clair » et « Concrètement » publiées sous la responsabilité de Benjamin Blondin. Seule la version publiée sur Légifrance fait foi.", ""]
    for t in w["themes"]:
        f += [f"## {t['titre']}", ""]
        for a in [x for x in w["articles"] if x["theme"] == t["cle"]]:
            tete = a["num"] + " : " + a["titre"] if a.get("arrete") else f"Article {a['num']} du Code des transports : {a['titre']}"
            f += [f"### {tete}", "", f"Page : {SITE}wiki/{a['slug']}.html", f"Source officielle : {a['url']}", "",
                  f"En clair : {a['en_clair']}", "", f"Concrètement : {a['concretement']}", "", "Texte officiel :", ""]
            if a.get("arrete"):
                for p in a["articles"]:
                    f += [f"{p['num']}.", *p["texte"], ""]
            else:
                f += [*a["texte"], "", a["vigueur"] + "."]
            if a["fiches"]:
                f += ["", "Dans le livre Machine à Réussite · Examen VTC 2027 : " + " ; ".join(f"fiche {c} ({t2})" for c, t2 in a["fiches"]) + "."]
            f.append("")
    if ds:
        f += ["## Dossiers VTC", ""]
        for d in ds:
            f += [f"### {d['titre']}", "", f"Page : {SITE}dossiers/{d['slug']}.html",
                  f"Publié le {date_fr(d['date'])}, chiffres vérifiés le {d['verifie']}.", "", _texte_dossier(d), "",
                  "Sources : " + " ; ".join(f"{x['nom']} ({x['url']})" for x in d["sources"]) + ".", ""]
    ecrire("llms-full.txt", "\n".join(f))


if __name__ == "__main__":
    if APERCU:
        # aperçu des brouillons : une copie complète du site dans apercu/, jamais publiée (voir .gitignore)
        import shutil
        shutil.rmtree(os.path.join(RACINE, "apercu"), ignore_errors=True)
        shutil.copytree(DOCS, os.path.join(RACINE, "apercu"))
        DOCS = os.path.join(RACINE, "apercu")
    nums = lire_numeros()
    accueil(nums, lire_questions({a["slug"] for a in lire_wiki()["articles"]}))
    for i, n in enumerate(nums):
        numero(n, nums[i + 1] if i + 1 < len(nums) else None, nums[i - 1] if i > 0 else None)
    actualite(nums)
    flux(nums)
    arts = wiki()
    w = lire_wiki()
    qs = lire_questions({a["slug"] for a in w["articles"]})
    questions(qs, w)
    ds = lire_dossiers({a["slug"] for a in w["articles"]})
    dossiers(ds, w, qs)
    indexnow()
    mises_a_jour()
    examens()
    legales()
    a_propos()
    contact()
    page_404()
    llms(nums, w, qs, [d for d in ds if not d.get("brouillon")])
    plan(nums, arts, iso_fr(w["verifie"]), qs, [d for d in ds if not d.get("brouillon")])
    print(f"Site généré dans docs/ : {len(nums)} numéro(s) de l'Actualité VTC.")
