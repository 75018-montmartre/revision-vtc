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
from gabarit import page, achat, LIVRE

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


def mois_annee(iso):
    """« 2026-11-02 » -> « novembre 2026 » : les pages n'affichent plus le jour de publication (depuis le 7 novembre 2026)."""
    d = datetime.date.fromisoformat(iso)
    return f"{MOIS[d.month - 1]} {d.year}"


# Domaine d'une Question VTC ou d'un article : l'épreuve de l'examen qu'il prépare (A à G, intitulés de contenu/calcul_note.json),
# ou « X » pour l'examen lui-même (méthode, inscription). Par défaut, la lettre de la première fiche du livre citée ;
# le champ "domaine" du fichier JSON la remplace. Pictogrammes au trait, 24 × 24, couleur du texte (currentColor), décoratifs.
_PICTOS = {
    "A": '<path d="M12 3v17M8 20h8M5 7h14M5 7l-3 6a3 3 0 0 0 6 0zM19 7l-3 6a3 3 0 0 0 6 0z"/>',                       # balance : la loi
    "B": '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M8 6h8M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h4"/>',  # calculatrice
    "C": '<path d="M12 3 2 20h20z"/><path d="M12 9v5M12 17h.01"/>',                                                     # panneau de danger
    "D": '<path d="M21 15a2 2 0 0 1-2 2H8l-4 4V5a2 2 0 0 1 2-2h13a2 2 0 0 1 2 2z"/><path d="M8 8h9M8 12h6"/>',          # bulle de texte
    "E": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',             # globe
    "F": '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',                                                           # courbe qui monte
    "G": '<path d="M5 17H3v-5l2-5h14l2 5v5h-2M3 12h18M9 17h6"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/>',  # voiture
    "X": '<rect x="5" y="4" width="14" height="18" rx="2"/><path d="M9 4V2h6v2M9 13l2 2 4-4"/>',                        # liste cochée
}


def _domaines():
    with open(os.path.join(CONTENU, "calcul_note.json"), encoding="utf-8") as h:
        d = {e["code"]: (f'Épreuve {e["code"]}', e["court"]) for e in json.load(h)["epreuves"]}
    d["X"] = ("Examen", "Méthode et inscription")
    assert set(d) == set(_PICTOS), "un pictogramme par domaine"
    return d


DOMAINES = _domaines()


def domaine_de(x, nom):
    """Code du domaine d'une question ou d'un article (voir DOMAINES)."""
    code = x.get("domaine") or (x["fiches"][0][0][0] if x.get("fiches") else "")
    assert code in DOMAINES, f"{nom} : domaine inconnu ({code!r}) ; ajouter \"domaine\" ou une fiche du livre"
    return code


def picto(code):
    return (f'<svg class="picto" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_PICTOS[code]}</svg>')


def ligne_domaine(code):
    """Sous le titre d'une carte : pictogramme + épreuve concernée."""
    e, court = DOMAINES[code]
    return f'<p class="domaine">{picto(code)}<span>{ty(e)} : {ty(court.lower() if code == "X" else court)}</span></p>'


def legende_domaines():
    """Légende des pictogrammes (pages d'index des Questions VTC et des articles)."""
    return '<ul class="legende-domaines">' + "".join(
        f'<li>{picto(c)}<span><b>{ty(e)}</b> {ty(court)}</span></li>' for c, (e, court) in DOMAINES.items() if c != "X") + "</ul>"


def carte(numero, iso, lien, titre, code, texte, titre_num="Question"):
    """Carte des index Questions VTC et Articles : numéro, mois, titre (le lien), épreuve, résumé."""
    return (f'<li><p class="carte-tete"><span class="num-art"><span class="visuellement-cache">{titre_num} </span>n° {numero}</span>'
            f'<span class="meta">{mois_annee(iso).capitalize()}</span></p><a href="{lien}">{titre}</a>{ligne_domaine(code)}<p>{texte}</p>'
            f'<p class="carte-action" aria-hidden="true">{"Lire le guide" if titre_num == "Guide" else "Lire la réponse"}</p></li>')


AUTEUR = {"@type": "Person", "name": "Benjamin Blondin", "url": SITE + "a-propos.html"}
LIVRE_LD = {"@type": "Book", "@id": SITE + "#livre", "name": "Machine à Réussite · Examen VTC 2027", "author": AUTEUR,
            "isbn": "9798165280795", "bookFormat": "https://schema.org/Paperback", "numberOfPages": 540, "inLanguage": "fr",
            "datePublished": "2026-10", "image": SITE + "couverture.jpg",
            "url": "https://www.amazon.fr/dp/B0HPCMRKDR", "sameAs": ["https://www.amazon.fr/dp/B0HPCMRKDR"],
            "offers": {"@type": "Offer", "price": "24.90", "priceCurrency": "EUR", "availability": "https://schema.org/InStock", "url": "https://www.amazon.fr/dp/B0HPCMRKDR"},
            "about": "Préparation à l'examen d'accès à la profession de conducteur de voiture de transport avec chauffeur (VTC)"}
SITE_LD = {"@type": "WebSite", "@id": SITE + "#site", "name": "Révision VTC", "url": SITE, "inLanguage": "fr-FR",
           "description": "Réglementation VTC expliquée article par article, actualité du métier régulièrement et examens blancs, par l'auteur du livre Machine à Réussite · Examen VTC 2027.",
           "publisher": AUTEUR}


def fil(*etapes):
    """Données structurées du fil d'Ariane : (nom, chemin relatif au site)."""
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": SITE + c} for i, (n, c) in enumerate(etapes, 1)]}


def image_partage(chemin):
    """Image de partage propre à la page (faite par outils/images_partage.py), sinon l'image générique du site."""
    nom = chemin[:-5].replace("/", "-") + ".jpg"
    return SITE + "images/partage/" + nom if os.path.exists(os.path.join(DOCS, "images", "partage", nom)) else SITE + "partage.jpg"


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
               f'<meta property="og:image" content="{image_partage(chemin)}">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
               f'<meta property="og:image:alt" content="{a(titre if image_partage(chemin) != SITE + "partage.jpg" else "Révision VTC, le site du livre Machine à Réussite · Examen VTC 2027")}">\n') +
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
        # numéros précédents (trois au plus), à droite du dernier numéro ; rien s'il n'y en a pas
        prec = "".join(
            f'<li><span class="meta">N° {p["numero"]}, {date_fr(p["date"])}</span>'
            f'<a href="actualite/{p["date"]}.html">{ty(p["titre"])}</a></li>'
            for p in nums[1:4])
        precedents = ('\n          <aside class="actu-precedents" aria-labelledby="titre-precedents">'
                      '\n            <h3 id="titre-precedents">Numéros précédents</h3>'
                      f'\n            <ol>{prec}</ol>\n          </aside>') if prec else ""
        dernier = f'''
    <section class="bloc bloc-doux" aria-labelledby="titre-dernier">
      <div class="page large">
        {tete_bloc("titre-dernier-rubrique", "Chaque lundi", "Le dernier numéro de l'Actualité VTC", "actualite/index.html", "Tous les numéros")}
        <div class="actu-une">
          <article class="une-actu">
            <p class="meta">N° {n["numero"]}, {date_fr(n["date"])}</p>
            <h3 id="titre-dernier"><a href="actualite/{n["date"]}.html">{ty(n["titre"])}</a></h3>
            <ul class="points">{pts}</ul>
          </article>{precedents}
        </div>
      </div>
    </section>'''
    # exemple du simulateur (mêmes valeurs par défaut que la page du simulateur, base prudente)
    sim = lire_simulateur()
    ex = calcul_simulateur(sim)
    dsim = defauts_simulateur(sim)
    ex_sem = dsim["semaines"]
    # carte interactive : le calcul de js/simulateur.js (SimuVTC.calculer), avec les valeurs par défaut de la page du simulateur
    donnees_simu = json.dumps({"valeurs": sim["valeurs"]}, ensure_ascii=False).replace("</", "<\\/")
    defauts_simu = json.dumps(dsim, ensure_ascii=False).replace("</", "<\\/")
    fin_accueil = (f'<script id="simu-donnees" type="application/json">{donnees_simu}</script>\n'
                   f'<script id="simu-defauts" type="application/json">{defauts_simu}</script>\n'
                   '<script src="js/simulateur.js"></script>\n<script src="js/accueil-simu.js"></script>\n')
    n_wiki = len(lire_wiki()["articles"])
    # mois de la dernière vérification du wiki (« 25 octobre 2026 » -> « octobre 2026 ») : le surtitre reste vrai sans retouche
    verif = " ".join(lire_wiki()["verifie"].split()[-2:])
    simu = f'simulateurs/{sim["slug"]}.html'
    # « Par où commencer ? » : trois profils, trois liens chacun (liste de liens simples, un seul niveau de cadre ; audit visuel, lot 3)
    parcours = [
        ("Je prépare l'examen", "Les épreuves, le barème et de quoi réviser.",
         [("qcm/index.html", f"S'entraîner : {len(FICHES)} QCM corrigés"),
          ("simulateurs/calcul-note-examen-vtc.html", "Calculer ma note à l'examen"),
          ("le-livre.html", "Le livre pour préparer l'examen 2027")]),
        ("Je me lance", "Ce que coûte le démarrage et ce qu'il rapporte.",
         [("dossiers/cout-pour-devenir-chauffeur-vtc.html", "Combien coûte le lancement en VTC"),
          (simu, "Calculer mon revenu net"),
          ("dossiers/chauffeur-vtc-salarie-ou-independant.html", "Salarié ou indépendant : que choisir")]),
        ("Je roule déjà", "Ce qui change pour vous, au fil des textes.",
         [("actualite/index.html", "L'Actualité VTC du lundi"),
          ("questions/index.html", "La FAQ VTC : une question, une réponse sourcée"),
          ("dossiers/precompte-cotisations-vtc-plateformes-2027.html", "Le précompte des cotisations par les plateformes en 2027")]),
    ]
    cartes_parcours = "".join(
        f'\n          <li><h3>{ty(t)}</h3><p>{ty(d)}</p><ul class="liste-liens">'
        + "".join(f'<li><a href="{h}">{ty(l)}</a></li>' for h, l in liens) + "</ul></li>"
        for t, d, liens in parcours)
    corps = f'''    <section class="hero fond-nuit" aria-labelledby="titre-hero">
      <div class="page large hero-grille">
        <div class="hero-texte">
          <p class="surtitre">{ty(f"Examen VTC 2027, règles vérifiées en {verif}")}</p>
          <h1 id="titre-hero">{ty("Réussir l'examen VTC 2027, et savoir ce que vous gagnerez vraiment")}</h1>
          <p class="chapeau">{ty("Le droit du VTC expliqué à partir des textes officiels, un simulateur de revenu net gratuit, et le livre pour préparer l'examen. Tout est sourcé et tenu à jour régulièrement.")}</p>
          <div class="actions"><a class="bouton clair" href="le-livre.html">{ty("Préparer l'examen 2027")}</a><a class="bouton contour" href="{simu}">Calculer mon revenu net</a></div>
          <p class="hero-mention">Gratuit, sans inscription, sans publicité.</p>
        </div>
        <div class="hero-cartes">
          <div class="carte-hero carte-simu" id="carte-simu">
            <p class="carte-titre">Simulateur gratuit</p>
            <p class="carte-texte" id="cs-texte">{ty(f"Exemple mensuel : 1 000 € versés par semaine, {ex_sem} semaines par an")}</p>
            <div class="carte-curseurs" hidden>
              <div class="curseur"><label for="cs-verse">{ty("Versé par semaine")}</label><output id="cs-verse-val" for="cs-verse">{_euros(dsim["verse_semaine"])}</output><input type="range" id="cs-verse" min="200" max="2500" step="50" value="{dsim["verse_semaine"]}"></div>
              <div class="curseur"><label for="cs-loyer">{ty("Location par semaine")}</label><output id="cs-loyer-val" for="cs-loyer">{_euros(dsim["loyer_semaine"])}</output><input type="range" id="cs-loyer" min="0" max="600" step="10" value="{dsim["loyer_semaine"]}"></div>
            </div>
            <div class="carte-calcul">
              <p class="ligne"><span>{ty("Versé par les plateformes")}</span><span class="montant" id="cs-m-verse">{_euros(ex["verse"] / 12)}</span></p>
              <p class="ligne"><span>{ty("TVA, cotisations, voiture et frais")}</span><span class="montant" id="cs-m-retenues">− {_euros((ex["verse"] - ex["net"]) / 12)}</span></p>
              <p class="ligne total"><span>{ty("Il vous reste, avant impôt")}</span><span class="montant" id="cs-m-net">{_euros(ex["net"] / 12)}</span></p>
            </div>
            <p class="visuellement-cache" id="cs-annonce" aria-live="polite"></p>
            <a class="carte-lien" id="cs-lien" href="{simu}">Faire ma simulation avec mes chiffres</a>
          </div>
          <a class="carte-hero carte-livre" href="le-livre.html">
            <img src="couverture-petite.jpg" width="68" height="88" alt="">
            <span>
              <span class="carte-titre">{ty("Le livre Machine à Réussite")}</span>
              <span class="carte-texte">{ty("213 fiches de cours, 1 191 questions corrigées, 3 examens blancs + 2 sur le site.")}</span>
              <span class="carte-lien">Voir le livre</span>
            </span>
          </a>
        </div>
      </div>
    </section>
    <section class="preuves" aria-label="Pourquoi faire confiance au site">
      <ul class="page large">
        <li><b>{n_wiki} articles de loi</b> {ty("recopiés de Légifrance et expliqués en clair")}</li>
        <li><b>{ty("Chaque chiffre sourcé")}</b> {ty("et daté : texte officiel ou deux sources concordantes")}</li>
        <li><b>{ty("Mis à jour régulièrement")}</b> {ty(": actualité, questions et guides")}</li>
      </ul>
    </section>
    <section class="bloc bloc-blanc" aria-labelledby="titre-commencer">
      <div class="page large">
        {tete_bloc("titre-commencer", "Selon votre situation", "Par où commencer ?")}
        <ul class="parcours">{cartes_parcours}
        </ul>
      </div>
    </section>
    <section class="bloc bloc-doux" aria-labelledby="titre-essentiel">
      <div class="page large">
        {tete_bloc("titre-essentiel", "Textes officiels expliqués", "Réglementation VTC : l'essentiel", "wiki/index.html", "Tous les textes expliqués",
                   "Les règles les plus utiles au quotidien, avec le texte officiel et une explication en clair.")}
        <ul class="liste-liens liste-articles">{liste_essentiels()}</ul>
      </div>
    </section>{bloc_questions(qs)}{dernier}'''
    ecrire("index.html", page("Examen VTC 2027 et réglementation VTC expliquée · Révision VTC", corps, "accueil", "",
                              "Réussir l'examen VTC 2027 : la réglementation VTC expliquée article par article, l'actualité du métier mise à jour régulièrement et deux examens blancs corrigés. Sources officielles citées.",
                              brut=True, scripts_fin=fin_accueil, jsonld=[{"@context": "https://schema.org", "@graph": [SITE_LD, LIVRE_LD]}]))


ESSENTIELS = [("l3120-2", "Réservation préalable et maraude : ce qui est interdit"), ("d3120-3", "Attente devant les gares et aéroports : une heure maximum"),
              ("l3122-9", "Le retour à la base après une course"), ("r3120-6", "La carte professionnelle VTC : conditions et délai"),
              ("arrete-6-avril-2017-examen", "L'examen VTC : épreuves, coefficients, notes éliminatoires"), ("l3122-3", "Le registre des VTC"),
              ("arrete-26-mars-2015-vehicules", "Le véhicule VTC : âge, dimensions, puissance"), ("arrete-6-aout-2025-reservation", "Le justificatif de réservation : les sept mentions"),
              ("l3124-12", "Maraude, démarchage, conduite sans carte : les sanctions")]


def bloc_questions(qs):
    if not qs:
        return ""
    li = "".join(carte(q["numero"], q["date"], f'questions/{q["date"]}-{q["slug"]}.html', ty(q["question"]), q["code_domaine"], ty(q["reponse_courte"])) for q in list(qs)[:4])
    return f'''
    <section class="bloc bloc-blanc" aria-labelledby="titre-questions">
      <div class="page large">
        {tete_bloc("titre-questions", "Réponses sourcées", "FAQ VTC : une question, une réponse sourcée", "questions/index.html", "Toutes les questions")}
        <ul class="questions questions-grille">{li}</ul>
      </div>
    </section>'''


def liste_essentiels():
    """Accueil, « Réglementation VTC : l'essentiel » : une ligne par texte, numéro d'article en pastille jaune (comme en tête
    des pages du wiki), puis le titre en clair ; liste sur deux colonnes (une sur téléphone), sans tuile (audit visuel, lot 3)."""
    par_slug = {a["slug"]: a for a in lire_wiki()["articles"]}
    lignes = []
    for s, t in ESSENTIELS:
        a = par_slug[s]
        num = a["num"].replace("Arrêté du ", "Arrêté ") if a.get("arrete") else a["num"]
        lignes.append(f'<li><a href="wiki/{s}.html"><span class="num-art">{ty(num)}</span><span>{ty(t)}</span></a></li>')
    return "".join(lignes)


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
        nav.append(f'<a class="bouton second" href="{suivant["date"]}.html">Numéro suivant : n° {suivant["numero"]}</a>')
    if precedent:
        nav.append(f'<a class="bouton second" href="{precedent["date"]}.html">Numéro précédent : n° {precedent["numero"]}</a>')
    nav.append('<a class="bouton second" href="index.html">Tous les numéros</a>')
    navh = '<nav class="actions" aria-label="Autres numéros">' + "".join(nav) + "</nav>"
    corps = f'''    <nav class="fil" aria-label="Fil d'Ariane"><ol><li><a href="index.html">Actualité VTC</a></li></ol></nav>
    <p class="surtitre">Actualité VTC n° {n["numero"]}</p>
    <h1>{ty(n["titre"])}</h1>
    <p class="meta">Publié le {date_fr(n["date"])}, période couverte : {ty(n["periode"])}</p>
    <section class="retenir" aria-labelledby="titre-retenir"><h2 id="titre-retenir">À retenir</h2>
    <ul>{retenir}</ul></section>{rub}
    <h2>Ce que ça change pour le livre</h2>
    <div class="impact">{impact}</div>
    <p class="meta">{ty("Informations vérifiées le " + n["verifie"] + ". Chaque brève repose sur un texte officiel ou sur deux sources concordantes.")}</p>
    {navh}'''
    titre = f'{n["titre"]} · Actualité VTC n° {n["numero"]}'
    resume = " ".join(n["a_retenir"])
    ld = {"@context": "https://schema.org", "@type": "NewsArticle", "headline": n["titre"][:110], "description": resume[:300],
          "datePublished": n["date"], "dateModified": n["date"], "inLanguage": "fr", "author": AUTEUR, "publisher": AUTEUR,
          "image": image_partage(f'actualite/{n["date"]}.html'), "mainEntityOfPage": SITE + f'actualite/{n["date"]}.html',
          "citation": [s["url"] for r in n["rubriques"] for b in r["breves"] for s in b["sources"]][:20]}
    ecrire(f'actualite/{n["date"]}.html', page(html.escape(titre, quote=False), corps, "actualite", "../",
                                               html.escape(resume[:300].rsplit(" ", 1)[0] + "…"),
                                               jsonld=[ld, fil(("Accueil", ""), ("Actualité VTC", "actualite/"), (f'N° {n["numero"]}', f'actualite/{n["date"]}.html'))]))


def actualite(nums):
    liste = ""
    for n in nums:
        pts = "".join(f"<li>{ty(x)}</li>" for x in n["a_retenir"])
        liste += f'''
      <li><span class="numero" aria-hidden="true">{n["numero"]}</span><div><span class="meta">N° {n["numero"]}, {date_fr(n["date"])}</span><a href="{n["date"]}.html">{ty(n["titre"])}</a><ul>{pts}</ul></div></li>'''
    corps = f'''    <h1>Actualité VTC</h1>
    <p class="chapeau">{ty("Chaque semaine, ce qui bouge pour les chauffeurs VTC et les candidats à l'examen : textes officiels, examen, plateformes, cotisations.")}</p>
    <p>{ty("Chaque information repose sur un texte officiel ou sur deux sources concordantes, toujours citées. Quand une règle du livre change, elle est aussi inscrite dans les")} <a href="../mises-a-jour.html">mises à jour du livre</a>.</p>
    <p class="meta">Pour être prévenu de chaque numéro sans donner votre adresse e-mail : <a href="flux.xml">flux RSS</a>.</p>
    <h2>Les numéros</h2>
    <ol class="numeros" reversed>{liste}
    </ol>'''
    ecrire("actualite/index.html", page("Actualité VTC : l'info des chauffeurs VTC, textes officiels à l'appui · Révision VTC", corps, "actualite", "../",
                                        "L'actualité VTC, régulièrement : textes officiels, examen, plateformes, cotisations. Sources citées."))


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
  <description>L'actualité VTC, régulièrement, par l'auteur du livre Machine à Réussite · Examen VTC 2027.</description>
  <language>fr-FR</language>{items}
</channel>
</rss>
'''
    ecrire("actualite/flux.xml", xml)


# ------------------------------------------------------------------ mises à jour
def mises_a_jour():
    with open(os.path.join(CONTENU, "mises-a-jour.json"), encoding="utf-8") as h:
        m = json.load(h)
    with open(os.path.join(CONTENU, "livre_pages.json"), encoding="utf-8") as h:
        pages_livre = json.load(h)["fiches"]   # page de chaque fiche dans le livre imprimé, et de son corrigé
    with open(os.path.join(CONTENU, "fiches.json"), encoding="utf-8") as h:
        titres = json.load(h)
    cartes = []
    for i, c in enumerate(m["corrections"]):   # la plus récente en tête du fichier
        for champ in ("date", "fiche", "avant", "apres", "texte"):
            if not str(c.get(champ, "")).strip():
                sys.exit(f"mises-a-jour.json, correction {i + 1} : champ « {champ} » manquant")
        if c["fiche"] not in pages_livre:
            sys.exit(f"mises-a-jour.json, correction {i + 1} : fiche « {c['fiche']} » absente de contenu/livre_pages.json")
        pl = pages_livre[c["fiche"]]
        page_fiche = c.get("page", pl["page"])
        ou = f"page {page_fiche}" + (f", corrigé page {pl['corrige']}" if pl.get("corrige") and "page" not in c else "")
        titre = f"Fiche {c['fiche']}" + (f" · {titres[c['fiche']]}" if c["fiche"] in titres else "")
        texte = ty(c["texte"])
        if c.get("url"):
            texte = f'<a href="{html.escape(c["url"])}">{texte}</a>'
        versions = (f"Versions antérieures à la {c['corrigee_dans']} (corrigé dans la version {c['corrigee_dans']})"
                    if c.get("corrigee_dans") else "Toutes les versions imprimées")
        cartes.append(f'''<section class="note" aria-labelledby="corr-{i}">
      <h3 id="corr-{i}">{ty(titre)}</h3>
      <p class="meta">{ty("Publiée le " + c["date"] + " · dans le livre : " + ou)}</p>
      <dl>
        <dt>Ce que dit le livre</dt><dd>{ty(c["avant"])}</dd>
        <dt>Ce qu’il faut retenir</dt><dd>{ty(c["apres"])}</dd>
        <dt>Texte officiel</dt><dd>{texte}</dd>
        <dt>Exemplaires concernés</dt><dd>{ty(versions)}</dd>
      </dl>
    </section>''')
    if cartes:
        tableau = "\n    ".join(cartes)
    else:
        tableau = "<p>Aucune correction à ce jour : toutes les règles du livre sont à jour.</p>"
    surv = "".join(f"<li>{ty(x)}</li>" for x in m["a_surveiller"])
    corps = f'''    <h1>Mises à jour du livre</h1>
    <p class="chapeau">{ty("Les règles du livre ont été vérifiées en octobre 2026. Quand l'une d'elles change, elle est inscrite ici, dans un encadré : la date, la fiche et sa page dans le livre, ce que dit le livre, ce qu'il faut retenir, et le texte officiel qui fonde la nouvelle règle.")}</p>
    <h2>Les corrections</h2>
    {tableau}
    <p class="meta">Dernière vérification : {ty(m["derniere_verification"])}.</p>
    <p>{ty("Lecteur du livre ? Recevez chaque correction par e-mail, avec la page corrigée en PDF, et signalez une erreur depuis")} <a href="le-livre.html#lecteurs">{ty("l'espace lecteurs de la page du livre")}</a>.</p>
    <h2>Quelle version du livre avez-vous ?</h2>
    <p>{ty("Ouvrez le livre à la page 2. Si elle est blanche, vous avez la version 1.0 (octobre 2026). Si elle s'intitule « Ce livre est tenu à jour », la version est écrite en bas de cette page. Les numéros de page sont les mêmes dans toutes les versions : la page indiquée dans chaque encadré est la bonne.")}</p>
    <h2>À surveiller en 2027</h2>
    <p>{ty("Le livre enseigne ces points en principe. Ils seront précisés ici dès que les textes seront publiés.")}</p>
    <ul>{surv}</ul>'''
    ecrire("mises-a-jour.html", page("Mises à jour du livre · Révision VTC", corps, "maj", "",
                                     "Les règles du livre Machine à Réussite · Examen VTC 2027 qui ont changé depuis l'impression."))


# ------------------------------------------------------------------ fiches d'entraînement tirées du livre (contenu/entrainement/)
def _minutes(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def _heure(mn):
    """1060 -> « 17 h 40 » ; 1080 -> « 18 h »."""
    return f"{mn // 60} h" + (f" {mn % 60:02d}" if mn % 60 else "")


def schema_frise_attente(sc, ident):
    """Frise horaire en SVG (aux couleurs du site, lisible en clair et en sombre) : heure d'arrivée du chauffeur,
    heure de prise en charge et début du stationnement permis ; js/fiche.js la décale pour « Pour aller plus loin »."""
    d, f = _minutes(sc["debut"]), _minutes(sc["fin"])
    x0, x1 = 40, 600
    x = lambda mn: round(x0 + (mn - d) * (x1 - x0) / (f - d), 1)
    arr, prise = _minutes(sc["arrivee"]), _minutes(sc["prise"])
    lim = prise - sc["avance_max"]
    grad = ""
    for t in range(d, f + 1, 30):
        grad += f'<line class="graduation" x1="{x(t)}" x2="{x(t)}" y1="102" y2="{114 if t % 60 == 0 else 108}"/>'
        if t % 60 == 0:
            grad += f'<text class="petit" x="{x(t)}" y="130" text-anchor="middle">{_heure(t)}</text>'
    return f"""<figure class="schema" id="{ident}">
          <div class="schema-defile" tabindex="0" role="region" aria-label="{ty("Frise horaire, à faire défiler")}">
          <svg class="frise" viewBox="0 0 640 170" aria-hidden="true" data-debut="{d}" data-fin="{f}" data-x0="{x0}" data-x1="{x1}" data-avance="{sc["avance_max"]}" data-prise="{prise}" data-retard="{sc.get("retard_plus_loin", 0)}">
            <defs><pattern id="{ident}-hach" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect class="hach-fond" width="8" height="8"/><line class="hach-trait" x1="0" y1="0" x2="0" y2="8"/></pattern></defs>
            <rect class="zone-ko" fill="url(#{ident}-hach)" data-role="interdit" x="{x0}" y="58" width="{round(x(lim) - x0, 1)}" height="44"/>
            <rect class="zone-ok" data-role="permis" x="{x(lim)}" y="58" width="{round(x(prise) - x(lim), 1)}" height="44"/>
            <line class="axe" x1="{x0}" y1="102" x2="{x1}" y2="102"/>
            {grad}
            <g class="repere" data-role="limite" style="transform:translateX({x(lim)}px)"><line class="trait-ok" x1="0" y1="40" x2="0" y2="106"/><text x="0" y="32" text-anchor="middle">au plus tôt <tspan data-role="t-limite">{_heure(lim)}</tspan></text></g>
            <g class="repere" data-role="prise" style="transform:translateX({x(prise)}px)"><circle class="point" cx="0" cy="80" r="9"/><text x="0" y="152" text-anchor="middle">prise en charge <tspan data-role="t-prise">{_heure(prise)}</tspan></text></g>
            <g style="transform:translateX({x(arr)}px)"><circle class="point-ko" cx="0" cy="80" r="9"/><text x="0" y="152" text-anchor="middle">{ty(sc["libelle_arrivee"])}, {_heure(arr)}</text></g>
          </svg>
          </div>
          <figcaption>{ty(sc["legende"])}<span class="schema-legende"><span class="cle-ko">{ty("Hachures rouges : stationnement interdit aux abords.")}</span> <span class="cle-ok">{ty("Vert : permis avec la réservation, une heure au plus.")}</span></span></figcaption>
        </figure>"""


def lire_fiche(slug):
    with open(os.path.join(CONTENU, "entrainement", slug + ".json"), encoding="utf-8") as h:
        f = json.load(h)
    f["slug"] = slug
    f["qcms"] = f["qcm"] if isinstance(f["qcm"], list) else [f["qcm"]]
    for q in f["qcms"]:
        assert q["juste"] in [l for l, _ in q["options"]], f"{slug} : réponse juste absente des options"
    for _, u in f.get("sources", []) + f.get("liens", []):
        assert not u or os.path.exists(os.path.join(DOCS, u)) or u.startswith(("questions/", "dossiers/", "simulateurs/", "wiki/")), f"{slug} : lien inconnu {u}"
    return f


FICHES = []   # fiches d'entraînement, chargées au début de la génération (encadrés « Testez-vous »)


def lire_fiches():
    """Fiches d'entraînement (rubrique QCM VTC), dans l'ordre des épreuves puis des codes."""
    dossier = os.path.join(CONTENU, "entrainement")
    fs = [lire_fiche(n[:-5]) for n in os.listdir(dossier) if n.endswith(".json")]
    cle = lambda f: [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", f["code"])]
    return sorted(fs, key=cle)


def fiche_entrainement(slug, racine="", entete=True):
    """Une fiche du livre, jouable : situation, confiance, un ou plusieurs QCM corrigés au clic, réponse rédigée
    (si la fiche en a une) comparée au corrigé type, règle à retenir, piège, « pour aller plus loin », bilan et dates
    de révision (js/fiche.js). Sans JavaScript, toute la fiche et son corrigé restent lisibles (et indexés)."""
    f = lire_fiche(slug)
    fid = "fiche-" + slug
    qcms = f["qcms"]
    n = len(qcms)

    def heures(t):  # « 18 h 40 », « 17 h » : en étiquettes, ce sont elles qui décident souvent de la réponse
        return re.sub(r"\b(\d{1,2} h(?: \d{2})?)\b", r'<span class="heure">\1</span>', t)
    lang = f' lang="{f["langue_replique"]}"' if f.get("langue_replique") else ""
    situation = ""
    for p in f["situation"]:
        m = re.match(r"^(.*?)\s*:\s*(«[^«]*»)$", p)   # réplique finale entre guillemets : dans une bulle
        if re.fullmatch(r"«[^«]*»", p):                # paragraphe entier entre guillemets (texte lu, réponse écrite)
            situation += f'<p class="bulle"{lang}>{ty(p)}</p>'
        elif m:
            situation += f'<p>{heures(ty(m.group(1) + " :"))}</p><p class="bulle"{lang}>{ty(m.group(2))}</p>'
        else:
            situation += f"<p>{heures(ty(p))}</p>"
    pin = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>'
    schema = schema_frise_attente(f["schema"], fid + "-frise") if f.get("schema", {}).get("type") == "frise-attente" else ""

    blocs_qcm = ""
    for i, q in enumerate(qcms, 1):
        etiquette = "QCM" + (f" {i}" if n > 1 else "")
        options = "".join(f'<label><input type="radio" name="{fid}-qcm{i}" value="{l}"><span><b>{l}.</b> {ty(t)}<span class="verdict"></span></span></label>' for l, t in q["options"])
        corrige = "".join(f"<p>{ty(p)}</p>" for p in q["corrige"])
        blocs_qcm += f'''
      <fieldset class="fiche-bloc" data-qcm="{i}" data-juste="{q["juste"]}"><legend><span class="fiche-etiquette">{etiquette}</span> {ty(q["question"])}</legend>
        <div class="choix fiche-qcm">{options}</div>
      </fieldset>
      <div class="fiche-corrige" data-etape="qcm-{i}">
        <p class="fiche-verdict" data-role="verdict" aria-live="polite">{ty(("Réponse " if n == 1 else f"QCM {i} : réponse ") + q["juste"])}</p>
        {corrige}
        {schema if i == 1 else ""}
      </div>'''

    if f.get("qrc"):
        pts = [(p, 1) if isinstance(p, str) else (p[0], p[1]) for p in f["qrc"]["points"]]
        total = sum(v for _, v in pts)
        points = "".join(f'<label><input type="checkbox" name="{fid}-pt" data-valeur="{v}"><span>{ty(p)}{ty(f" ({v} points)") if v > 1 else ""}</span></label>' for p, v in pts)
        bareme = "Comptez vos points. " + f["qrc"].get("bareme", "Un point par élément.")
        suite = f'''
      <div class="fiche-bloc" data-etape="qrc-question">
        <h4><label for="{fid}-qrc">{ty("Je rédige ma réponse : " + f["qrc"]["question"])}</label></h4>
        <textarea id="{fid}-qrc" rows="4" data-js hidden placeholder="{ty("Écrivez votre réponse comme le jour de l'examen.")}"></textarea>
        <p class="fiche-action" data-js hidden><button type="button" class="bouton second" data-action="qrc">{ty("Comparer avec le corrigé type")}</button></p>
      </div>
      <div class="fiche-corrige" data-etape="qrc" data-total="{total}">
        <p class="fiche-verdict">{ty("Corrigé type")}</p>
        {"".join(f"<p>{ty(x)}</p>" for x in (f["qrc"]["corrige"] if isinstance(f["qrc"]["corrige"], list) else [f["qrc"]["corrige"]]))}
        <fieldset data-js hidden><legend>{ty(bareme)}</legend>
          <div class="choix">{points}</div>
          <p class="fiche-score" aria-live="polite">{ty("Votre score :")} <b><span data-role="score">0</span> / {total}</b></p>
        </fieldset>
        <p class="fiche-action" data-js hidden><button type="button" class="bouton second" data-action="bilan">{ty("Voir mon bilan")}</button></p>
      </div>'''
    else:
        suite = f'''
      <div data-etape="suite" data-js hidden><p class="fiche-action"><button type="button" class="bouton second" data-action="bilan">{ty("Voir mon bilan")}</button></p></div>'''

    src = "".join(f'<li><a href="{racine}{u}">{ty(t)}</a></li>' if u else f"<li>{ty(t)}</li>" for t, u in f["sources"])
    tete = (f'''<p class="fiche-tete"><span class="fiche-code">{f["code"]}</span> {ty("Épreuve " + f["epreuve"] + ", " + (f["epreuve_nom"] if f["epreuve"] in "DE" else f["epreuve_nom"][0].lower() + f["epreuve_nom"][1:]) + ", page " + str(f["page"]) + " du livre")}</p>
      <h3 id="{fid}-titre">{ty(f["titre"])}</h3>''' if entete else f'<h2 class="visuellement-cache">{ty("La fiche " + f["code"])}</h2><h3 class="visuellement-cache" id="{fid}-titre">{ty(f["titre"])}</h3>')
    etiq = f'aria-labelledby="{fid}-titre"'
    sortie = f"""<section class="fiche-essai" id="{fid}" {etiq} data-code="{f["code"]}" data-nb-qcm="{n}">
      {tete}

      <div class="bon-course">
        <div class="bon-tete"><h4>{pin}Situation</h4><span class="bon-ref">{ty("Fiche " + f["code"] + ", page " + str(f["page"]))}</span></div>
        <div class="bon-corps">{situation}</div>
      </div>

      <fieldset class="fiche-bloc" data-js hidden><legend>{ty("Avant de répondre : ma confiance")}</legend>
        <div class="choix en-ligne"><label><input type="radio" name="{fid}-conf" value="sur"><span>Sûr</span></label><label><input type="radio" name="{fid}-conf" value="hesitant"><span>Hésitant</span></label><label><input type="radio" name="{fid}-conf" value="hasard"><span>Au hasard</span></label></div>
      </fieldset>
{blocs_qcm}
{suite}

      <div class="fiche-corrige" data-etape="bilan">
        <div class="retenir"><h4>{ty("La règle à retenir")}</h4><p>{ty(f["retenir"])}</p></div>
        <div class="note"><h4>{ty("Le piège")}</h4><p>{ty(f["piege"])}</p></div>
        <div class="note"><h4>{ty("Pour aller plus loin")}</h4><p>{ty(f["plus_loin"]["question"])}</p>
          <p data-js hidden><button type="button" class="bouton second petit" data-action="plus-loin">{ty("Voir la réponse")}</button></p>
          <p data-role="plus-loin">{ty(f["plus_loin"]["reponse"])}</p></div>
        <div class="fiche-bilan" data-js hidden>
          <h4>Mon bilan</h4>
          <p data-role="resume" aria-live="polite"></p>
          <p data-role="conseil"></p>
          <p class="fiche-etiquette">{ty("Mes révisions, comptées à partir d'aujourd'hui")}</p>
          <ul class="fiche-revisions" data-role="revisions"></ul>
        </div>
        <p class="fiche-sources">{ty("Sources du corrigé, vérifiées en " + f["verifie"] + " : ")}</p>
        <ul class="fiche-sources">{src}</ul>
      </div>
    </section>"""
    return sortie


# ------------------------------------------------------------------ rubrique QCM VTC (fiches d'entraînement tirées du livre)
def renvoi_qcm(fs, lien, racine="../"):
    """Encadré latéral « Testez-vous » pour une question, un guide ou un article du wiki : les fiches qui portent sur la même règle."""
    lies = [f for f in fs if lien in [u for _, u in f.get("liens", [])]]
    if not lies:
        return ""
    li = "".join(f'<li><a href="{racine}qcm/{f["url"]}.html">{ty(f["code"] + " · " + f["titre"])}</a></li>' for f in lies)
    return f'<section class="cote-bloc"><h2>Testez-vous</h2><p>{ty("Un QCM corrigé, tiré du livre, sur cette règle :" if len(lies) == 1 else "Des QCM corrigés, tirés du livre, sur ces règles :")}</p><ul class="voir-aussi">{li}</ul></section>'


def titre_de(u):
    """Titre (h1) d'une page déjà générée du site, pour nommer un lien."""
    with open(os.path.join(DOCS, u), encoding="utf-8") as h:
        m = re.search(r"<h1[^>]*>(.*?)</h1>", h.read(), re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", m.group(1))).split("  ")[-1].strip() if m else u


def accroche(f):
    """Première phrase de la situation, pour la carte de la fiche (coupée proprement si elle est longue)."""
    t = " ".join(f["situation"])
    m = re.match(r"(.+?[.?!»])(\s|$)", t)
    p = m.group(1) if m else t
    return p if len(p) <= 170 else p[:165].rsplit(" ", 1)[0] + "…"


def qcm(fs):
    """Rubrique QCM VTC : page d'index (fiches regroupées par épreuve) et une page par fiche."""
    if not fs:
        return
    WIKI = {a["slug"]: a for a in lire_wiki()["articles"]}
    par_ep = {}
    for f in fs:
        par_ep.setdefault(f["epreuve"], []).append(f)
    for i, f in enumerate(fs):
        meme = par_ep[f["epreuve"]]
        k = meme.index(f)
        suivante = meme[k + 1] if k + 1 < len(meme) else (fs[(i + 1) % len(fs)] if len(fs) > 1 else None)
        vus = [u for _, u in f.get("liens", [])] + [u for _, u in f["sources"] if u.startswith("wiki/")]
        vus = list(dict.fromkeys(vus))
        def nom(u):
            a = WIKI.get(u[5:-5]) if u.startswith("wiki/") else None
            return ((a["num"] if not a.get("arrete") else "Arrêté") + " · " + a["titre"]) if a else re.sub(" +", " ", titre_de(u))
        lies = "".join(f'<li><a href="../{u}">{ty(nom(u))}</a></li>' for u in vus)
        nb = len(f["qcms"])
        chapeau = ("Deux QCM" if nb > 1 else "Un QCM") + (" et une réponse à rédiger" if f.get("qrc") else "") + \
                  ", corrigés et sourcés, tirés du livre Machine à Réussite · Examen VTC 2027. Répondez comme le jour de l'examen : le corrigé s'affiche après votre réponse."
        nav = f'<a class="bouton second" href="index.html">{ty("Toutes les fiches")}</a>'
        if suivante:
            nav = f'<a class="bouton" href="{suivante["url"]}.html">{ty("Fiche suivante : " + suivante["code"])}</a>' + nav
        corps = f'''    <nav class="fil" aria-label="Fil d'Ariane"><ol><li><a href="index.html">QCM VTC</a></li></ol></nav>
    <p class="surtitre">{ty(DOMAINES[f["epreuve"]][0] + " : " + DOMAINES[f["epreuve"]][1])}</p>
    <h1>{ty("QCM VTC : " + f["titre"])}</h1>
    <p class="chapeau">{ty(chapeau)}</p>
    <div class="page-fiche">
    {fiche_entrainement(f["slug"], "../", entete=False)}
    <div class="{"tuiles-2" if lies else "tuiles-1"}">
    {f'<section class="tuile" aria-labelledby="titre-regle"><h2 id="titre-regle">{ty("Pour réviser la règle")}</h2><ul class="voir-aussi">{lies}</ul></section>' if lies else ""}
    <section class="tuile" aria-labelledby="titre-livre"><h2 id="titre-livre">Dans le livre</h2><p>{ty(f"Cette fiche est l'une des 213 du livre (page {f['page']}, corrigé page {f['page_corrige']}), avec 1 191 questions corrigées et 3 examens blancs.")}</p><p>{achat("bouton achat", "Le livre sur Amazon")}</p></section>
    </div>
    <nav class="navigation-fiches" aria-label="{ty("Autres fiches")}">{nav}</nav>
    </div>'''
        chemin = f'qcm/{f["url"]}.html'
        ep, court = DOMAINES[f["epreuve"]]
        aligne = [{"@type": "AlignmentObject", "alignmentType": "educationalSubject", "targetName": f"Examen VTC, {ep} : {court}"},
                  {"@type": "AlignmentObject", "alignmentType": "educationalLevel", "targetName": "Examen d'accès à la profession de conducteur VTC"}]
        def question(q):
            ordre = [l for l, _ in q["options"]]
            rep = lambda l, t: {"@type": "Answer", "position": ordre.index(l), "encodingFormat": "text/html", "text": f"{l}. {t}"}
            return {"@type": "Question", "eduQuestionType": "Multiple choice", "learningResourceType": "Practice problem",
                    "name": q["question"], "text": " ".join(f["situation"]) + " " + q["question"], "encodingFormat": "text/html",
                    "typicalAgeRange": "18-", "assesses": f["retenir"], "educationalAlignment": aligne,
                    "comment": {"@type": "Comment", "text": " ".join(q["corrige"])},
                    "suggestedAnswer": [rep(l, t) for l, t in q["options"] if l != q["juste"]],
                    "acceptedAnswer": rep(q["juste"], dict(q["options"])[q["juste"]])}
        ld = {"@context": "https://schema.org", "@type": "Quiz", "name": f["titre_page"], "url": SITE + chemin, "inLanguage": "fr",
              "about": {"@type": "Thing", "name": f["titre"]}, "educationalAlignment": aligne, "learningResourceType": "Practice problem",
              "typicalAgeRange": "18-", "educationalLevel": "Examen VTC", "author": AUTEUR, "isPartOf": {"@id": SITE + "#site"},
              "hasPart": [question(q) for q in f["qcms"]]}
        ecrire(chemin, page(html.escape(f["titre_page"] + " · Révision VTC", quote=False), corps, "qcm", "../", html.escape(f["description"]),
                            scripts_fin='<script src="../js/fiche.js" defer></script>\n',
                            jsonld=[ld, fil(("Accueil", ""), ("QCM VTC", "qcm/"), (f["titre"], chemin))]))
    blocs = ""
    for code, (e, court) in DOMAINES.items():
        if code not in par_ep:
            continue
        cartes = "".join(f'''<li><p class="carte-tete"><span class="num-art">{f["code"]}</span><span class="meta">{ty(("Deux QCM" if len(f["qcms"]) > 1 else "QCM") + (" et réponse rédigée" if f.get("qrc") else ""))}</span></p><a href="{f["url"]}.html">{ty(f["titre"])}</a><p>{ty(" ".join(f["situation"]))}</p><p class="carte-action" aria-hidden="true">{ty("Faire la fiche")}</p></li>''' for f in par_ep[code])
        blocs += f'''
    <section class="bloc-index" aria-labelledby="ep-{code}">
    <h2 id="ep-{code}" class="titre-epreuve">{picto(code)}{ty(e + " : " + court)}</h2>
    <ul class="questions trois">{cartes}</ul>
    </section>'''
    corps = f'''    <h1>QCM VTC</h1>
    <p class="chapeau">{ty(f"{len(fs)} fiches d'entraînement à l'examen VTC, tirées du livre Machine à Réussite · Examen VTC 2027 : une situation de chauffeur, un ou deux QCM, souvent une réponse à rédiger, et le corrigé complet avec ses sources. Gratuites, sans inscription.")}</p>
    <p class="intro">{ty("Chaque fiche est reproduite telle qu'elle figure dans le livre. Les fiches sont classées par épreuve de l'examen ; de nouvelles fiches sont ajoutées régulièrement.")}</p>
    <section class="bloc-index" aria-label="Comment se fait une fiche">
    <h2>{ty("Comment se fait une fiche")}</h2>
    <ol class="etapes etapes-ligne">
      <li><b>{ty("Lisez la situation")}</b>{ty("Un cas de chauffeur, comme à l'examen. Avant de répondre, dites si vous êtes sûr, hésitant ou si vous répondez au hasard.")}</li>
      <li><b>{ty("Répondez au QCM, puis rédigez")}</b>{ty("Le corrigé s'affiche après votre choix. Rédigez ensuite la réponse courte et comparez-la au corrigé type, point par point.")}</li>
      <li><b>{ty("Lisez votre bilan")}</b>{ty("La règle à retenir, le piège à éviter, un conseil selon vos réponses, et vos dates de révision à J+1, J+3, J+7 et J+21.")}</li>
    </ol>
    </section>{blocs}
    <section class="bloc-index" aria-labelledby="livre-qcm">
    <h2 id="livre-qcm">{ty("Toutes les fiches sont dans le livre")}</h2>
    <p>{ty("Le livre en compte 213, avec 1 191 questions corrigées, un test diagnostic, des plannings de révision et 3 examens blancs, plus 2 sur ce site.")}</p>
    <div class="actions">{achat("bouton achat", "Acheter le livre sur Amazon")}<a class="bouton second" href="../le-livre.html">{ty("Découvrir le livre")}</a></div>
    </section>'''
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "QCM VTC", "url": SITE + "qcm/", "inLanguage": "fr", "isPartOf": {"@id": SITE + "#site"},
          "hasPart": [{"@type": "Quiz", "name": f["titre_page"], "url": SITE + f'qcm/{f["url"]}.html'} for f in fs]}
    ecrire("qcm/index.html", page("QCM VTC gratuits : fiches d'entraînement corrigées de l'examen VTC 2027 · Révision VTC", corps, "qcm", "../",
                                  html.escape(f"QCM VTC gratuits pour l'examen 2027 : {len(fs)} fiches corrigées et sourcées, classées par épreuve (A à G), tirées du livre Machine à Réussite. Sans inscription."),
                                  jsonld=[ld, fil(("Accueil", ""), ("QCM VTC", "qcm/"))]))


# ------------------------------------------------------------------ le livre tenu à jour (inscription des lecteurs, signalements)
def livre_vivant():
    """Page « Le livre » (présentation, depuis le 7 novembre 2026) : présentation et achat, une fiche du livre à essayer
    (fiche_entrainement), les vraies pages, la méthode, les engagements de vérification, les questions des acheteurs ;
    puis l'espace lecteurs : inscription aux mises à jour (n8n, double confirmation), signalement d'une erreur (Web3Forms),
    questions des lecteurs. Et les deux pages de retour des liens envoyés par e-mail."""
    with open(os.path.join(CONTENU, "livre.json"), encoding="utf-8") as h:
        conf = json.load(h)
    with open(os.path.join(CONTENU, "contact.json"), encoding="utf-8") as h:
        cle = json.load(h).get("web3forms_cle", "").strip()
    with open(os.path.join(CONTENU, "mises-a-jour.json"), encoding="utf-8") as h:
        m = json.load(h)
    url_inscription = conf["inscription_url"]
    assert re.fullmatch(r"https://[a-z0-9.-]+/webhook/livre-inscription", url_inscription), "adresse d'inscription invalide"
    assert re.fullmatch(r"[0-9a-f-]{36}", cle), "clé Web3Forms manquante"
    nb = len(m["corrections"])
    etat = ("Aucune correction à ce jour : toutes les règles du livre sont à jour." if nb == 0 else
            f"{nb} correction{'s' if nb > 1 else ''} publiée{'s' if nb > 1 else ''} depuis l'impression.")
    faq_achat = [
        ("Le livre couvre-t-il toutes les épreuves de l'examen VTC ?",
         "Oui. Ses 35 chapitres couvrent les sept épreuves écrites d'admissibilité (A à G) et l'épreuve pratique d'admission : 213 fiches de cours, dont 10 pour l'épreuve pratique."),
        ("Le livre est-il à jour pour l'examen 2027 ?",
         "Ses règles ont été vérifiées en octobre 2026 et il est à jour de la loi du 25 juin 2026. Les changements de 2026 et 2027 (précompte des cotisations par les plateformes au 1er janvier 2027, fin de l'accès par l'expérience, facturation électronique) sont signalés dans les fiches concernées. Si une règle change après l'impression, la correction est publiée sur la page Mises à jour du livre et envoyée aux lecteurs inscrits."),
        ("Puis-je essayer avant d'acheter ?",
         "Oui. La fiche A3.4 de cette page est reproduite telle qu'elle figure dans le livre, avec son corrigé. Les questions et les guides du site indiquent aussi les fiches du livre qui traitent chaque règle."),
        ("Comment faire les deux examens blancs en ligne ?",
         "Ils sont sur la page Examens blancs n° 4 et 5 de ce site, à faire à l'écran, chronométrés et corrigés, ou à imprimer. Ils sont réservés aux lecteurs : une question dont la réponse se trouve dans le livre en ouvre l'accès."),
    ]
    faq = [
        ("Faut-il avoir acheté le livre pour s'inscrire aux mises à jour ?",
         "Oui. Les pages corrigées sont réservées aux lecteurs : l'inscription demande un mot qui se trouve dans le livre. La liste des corrections reste publique sur la page Mises à jour du livre."),
        ("Combien d'e-mails vais-je recevoir ?",
         "Un e-mail seulement quand une règle du livre change ou qu'une erreur est corrigée. Pas de lettre d'information régulière, pas de publicité."),
        ("Que devient mon adresse e-mail ?",
         "Elle sert uniquement à vous envoyer les mises à jour du livre. Elle n'est ni vendue, ni prêtée, ni utilisée pour autre chose. Chaque e-mail contient un lien de désinscription, qui efface votre adresse."),
        ("J'ai trouvé une erreur : que se passe-t-il ensuite ?",
         "Elle est vérifiée sur le texte officiel. Si elle est confirmée, elle est corrigée, inscrite sur la page Mises à jour du livre et envoyée à tous les lecteurs inscrits. Si vous avez laissé votre adresse, vous recevez la réponse, même quand le livre était juste."),
    ]
    pages_livre = [
        ("fiche", "Une fiche, une règle : on part d'une situation réelle de chauffeur",
         "Page du livre : une fiche commence par une situation concrète, puis un QCM et une question à réponse courte, comme à l'examen, et une case pour suivre ses révisions."),
        ("corrige", "Chaque corrigé explique le raisonnement, la règle et le piège",
         "Page de corrigés du livre : pour chaque question, le raisonnement, la règle à retenir, le texte officiel qui la fonde et le piège dans lequel tombent les candidats."),
        ("a-jour", "Une carte des règles ouvre chaque chapitre",
         "Une carte des règles et la première page d'un examen blanc : chaque règle a été contrôlée sur le Code des transports, le Code de la route et les textes officiels de l'examen."),
    ]
    figures = "".join(f'''
      <figure>
        <picture><source srcset="images/livre/{n}.webp" type="image/webp"><img src="images/livre/{n}.jpg" width="970" height="600" loading="lazy" decoding="async" alt="{ty(alt)}"></picture>
        <figcaption>{ty(leg)}</figcaption>
      </figure>''' for n, leg, alt in pages_livre)
    corps = f'''    <p class="surtitre">Le livre</p>
    <h1>{ty("Machine à Réussite – Examen VTC 2027")}</h1>
    <p class="chapeau">{ty("Le cours et l'entraînement pour réussir l'examen VTC 2027 : les sept épreuves écrites et l'épreuve pratique, une règle par fiche, et chaque règle vérifiée sur son texte officiel.")}</p>

    <section class="presentation-livre" aria-labelledby="titre-presentation">
      <img src="couverture.jpg" width="408" height="528" alt="{ty("Couverture du livre Machine à Réussite – Examen VTC 2027, de Benjamin Blondin")}">
      <div>
        <h2 id="titre-presentation">{ty("Tout pour préparer l'examen, en 540 pages")}</h2>
        <ul class="liste-coches">
          <li><b>{ty("213 fiches de cours")}</b>{ty(", une règle par fiche, dans 35 chapitres")}</li>
          <li><b>{ty("1 191 questions corrigées")}</b>{ty(" : QCM et questions à réponse courte, chaque corrigé cite son texte officiel")}</li>
          <li><b>{ty("Un test diagnostic de 40 questions")}</b>{ty(" et trois plannings, sur 4, 8 ou 12 semaines")}</li>
          <li><b>{ty("3 examens blancs dans le livre")}</b>{ty(", plus 2 sur ce site, réservés aux lecteurs")}</li>
          <li><b>{ty("À jour de la loi du 25 juin 2026")}</b>{ty(", règles vérifiées en octobre 2026")}</li>
        </ul>
        <div class="actions">{achat("bouton achat", "Acheter le livre sur Amazon")}<a class="bouton second" href="#essayer">{ty("Essayer une fiche gratuitement")}</a></div>
        <p class="lecteurs-lien"><b>{ty("Déjà lecteur ?")}</b> <a href="#inscription">{ty("Recevoir les mises à jour")}</a> {ty("ou")} <a href="#signaler">{ty("signaler une erreur")}</a></p>
      </div>
    </section>

    <h2 id="essayer">{ty("Essayez une fiche du livre")}</h2>
    <p>{ty("Voici la fiche A3.4, telle qu'elle figure dans le livre. Répondez comme le jour de l'examen : le corrigé s'affiche après votre réponse.")}</p>
    {fiche_entrainement("a3-4")}
    <p>{ty(f"Envie d'en faire d'autres ? {len(FICHES)} fiches du livre, trois par épreuve écrite, sont en accès libre dans la rubrique")} <a href="qcm/index.html">{ty("QCM VTC")}</a>.</p>

    <h2 id="pages">{ty("À quoi ressemblent les pages")}</h2>
    <div class="pages-livre">{figures}
    </div>

    <h2 id="methode">{ty("La méthode : apprendre, se tester, réviser au bon moment")}</h2>
    <ol class="etapes">
      <li><b>{ty("Savoir d'où vous partez")}</b>{ty("Un test diagnostic de 40 questions mesure votre niveau. Selon votre score, vous suivez un planning sur 4, 8 ou 12 semaines, qui vous dit quoi faire chaque jour.")}</li>
      <li><b>{ty("Se tester avant de lire")}</b>{ty("Chaque chapitre commence par un pré-test de 5 questions, puis une carte des règles avec tableaux et schémas.")}</li>
      <li><b>{ty("Apprendre sur des cas concrets")}</b>{ty("Chaque fiche part d'une situation de chauffeur, puis vous fait répondre à un QCM et rédiger une réponse courte, comme à l'examen. La réponse n'est jamais sur la page de la question.")}</li>
      <li><b>{ty("Comprendre ses erreurs")}</b>{ty("Chaque corrigé donne le raisonnement complet, la règle à retenir, le texte officiel qui la fonde et le piège à éviter.")}</li>
      <li><b>{ty("Réviser au bon moment")}</b>{ty("Des cases J+1, J+3, J+7 et J+21 sur chaque corrigé : les révisions espacées font retenir durablement.")}</li>
      <li><b>{ty("S'entraîner en conditions réelles")}</b>{ty("Trois examens blancs complets dans le livre, deux de plus sur ce site, au format de l'examen, chronométrés et notés selon le barème.")}</li>
    </ol>
    <div class="actions">{achat("bouton achat", "Acheter le livre sur Amazon")}</div>

    <h2 id="engagements">{ty("Un livre vérifié, et tenu à jour après son impression")}</h2>
    <p>{ty("Les règles de l'examen VTC et du métier changent : décrets, arrêtés, cotisations, plateformes. Le livre ne s'arrête pas à sa date d'impression. Voici ce que l'auteur s'engage à faire.")}</p>
    <ol class="etapes">
      <li><b>{ty("Vérifier chaque règle sur sa source")}</b>{ty("Chaque corrigé du livre cite le texte officiel qui le fonde (Code des transports, Code de la route, arrêtés de l'examen, Urssaf, BOFiP) et le mois de sa vérification. Une règle qui ne repose pas sur un texte officiel, ou sur deux sources indépendantes qui concordent, n'est pas enseignée. En vigueur, adopté mais pas encore applicable, simple projet : les trois états sont toujours distingués.")}</li>
      <li><b>{ty("Revérifier le livre entier toutes les trois semaines")}</b>{ty("Les règles du livre sont recontrôlées sur les textes en vigueur, en plus de la veille du Journal officiel faite chaque semaine pour le site. Les articles de loi utiles au métier sont recopiés et expliqués dans la rubrique")} <a href="wiki/index.html">{ty("Réglementation VTC")}</a>.</li>
      <li><b>{ty("Publier chaque correction")}</b>{ty("Toute correction est inscrite sur la page")} <a href="mises-a-jour.html">{ty("Mises à jour du livre")}</a> {ty(": la date, la fiche et sa page dans le livre, ce que dit le livre, ce qu'il faut retenir et le texte qui fonde la nouvelle règle.")}</li>
      <li><b>{ty("Vous l'envoyer")}</b>{ty("Les lecteurs inscrits reçoivent la correction par e-mail, avec la page corrigée en PDF, à imprimer ou à garder sur leur téléphone.")}</li>
      <li><b>{ty("Répondre à chaque signalement")}</b>{ty("Une erreur, une règle qui a changé, un passage pas clair : chaque signalement est vérifié et reçoit une réponse. Une erreur confirmée est corrigée pour tous.")}</li>
    </ol>
    <p class="meta">{ty("Dernière vérification complète des règles : " + m["derniere_verification"] + ". " + etat)}</p>

    <h2 id="questions">Questions fréquentes</h2>
    {"".join(f"<h3>{ty(q)}</h3>\n    <p>{ty(r)}</p>\n    " for q, r in faq_achat)}
    <div class="actions">{achat("bouton achat", "Acheter le livre sur Amazon")}</div>

    <h2 id="lecteurs">{ty("Espace lecteurs")}</h2>
    <p>{ty("Vous avez le livre : recevez ses mises à jour, faites les")} <a href="examens.html">{ty("examens blancs n° 4 et 5")}</a>{ty(", ou signalez une erreur.")}</p>

    <h3 id="inscription">Recevoir les mises à jour du livre</h3>
    <p>{ty("Un e-mail seulement quand une règle change ou qu'une erreur est corrigée, avec la page corrigée en PDF. Vous confirmez votre inscription en cliquant sur le lien reçu par e-mail ; un lien dans chaque message permet de se désinscrire.")}</p>
    <form id="form-inscription" class="contact" action="{url_inscription}" method="POST" novalidate>
      <p class="piege" aria-hidden="true"><label>Ne pas remplir <input type="text" name="piege" tabindex="-1"></label></p>
      <div class="champ"><label for="ins-email">Adresse e-mail</label><p class="aide" id="aide-ins-email">Exemple : prenom.nom@exemple.fr</p><input type="email" id="ins-email" name="email" autocomplete="email" required maxlength="120" aria-describedby="aide-ins-email err-ins-email"><p class="erreur" id="err-ins-email"></p></div>
      <div class="champ"><label for="ins-reponse">{ty("Quel est le dernier mot du titre de la fiche G2.6, page 160 du livre ?")}</label><p class="aide" id="aide-ins-reponse">{ty("Un seul mot, sans article. Cette question réserve l'envoi des pages corrigées aux lecteurs du livre.")}</p><input type="text" id="ins-reponse" name="reponse" required maxlength="40" autocapitalize="none" spellcheck="false" aria-describedby="aide-ins-reponse err-ins-reponse"><p class="erreur" id="err-ins-reponse"></p></div>
      <p class="option-chrono"><input type="checkbox" id="ins-accord" name="consentement" value="oui" required aria-describedby="err-ins-accord"><label for="ins-accord">{ty("J'accepte de recevoir par e-mail les mises à jour et les pages corrigées du livre.")}</label></p>
      <p class="erreur" id="err-ins-accord"></p>
      <p class="aide">{ty("Votre adresse sert uniquement à ces envois. Elle n'est ni vendue, ni prêtée. Détails dans les")} <a href="mentions-legales.html#lecteurs">mentions légales</a>.</p>
      <div class="actions"><button type="submit" class="bouton" id="ins-envoyer">Je m’inscris</button></div>
      <div id="ins-etat" role="status" aria-live="polite"></div>
    </form>

    <h3 id="signaler">Signaler une erreur ou faire une critique</h3>
    <p>{ty("Vous avez repéré une règle qui a changé, une erreur, une réponse qui vous semble fausse, un passage pas clair ? Dites-le : chaque signalement est vérifié sur le texte officiel. Le livre doit être juste, pas seulement avoir raison.")}</p>
    <form id="form-signalement" class="contact" action="https://api.web3forms.com/submit" method="POST" novalidate>
      <input type="hidden" name="access_key" value="{cle}">
      <input type="hidden" name="subject" value="Signalement sur le livre, depuis revision-vtc.fr">
      <input type="hidden" name="from_name" value="revision-vtc.fr (le livre)">
      <p class="piege" aria-hidden="true"><label>Ne pas remplir <input type="checkbox" name="botcheck" tabindex="-1"></label></p>
      <div class="champs-2">
        <div class="champ"><label for="sig-type">Type de signalement</label><select id="sig-type" name="type">
          <option>Une erreur dans le livre</option><option>Une règle qui a changé</option><option>Un passage pas clair</option><option>Une autre critique ou une suggestion</option></select></div>
        <div class="champ"><label for="sig-fiche">Fiche ou page</label><p class="aide" id="aide-sig-fiche">{ty("Exemple : A3.4, page 66")}</p><input type="text" id="sig-fiche" name="fiche" maxlength="60" aria-describedby="aide-sig-fiche"></div>
      </div>
      <div class="champ"><label for="sig-message">Ce qui pose problème</label><p class="aide" id="aide-sig-message">1&#8239;000 caractères au maximum.</p><textarea id="sig-message" name="message" required maxlength="1000" rows="6" aria-describedby="aide-sig-message err-sig-message"></textarea><p class="erreur" id="err-sig-message"></p></div>
      <div class="champ"><label for="sig-source">Votre source, si vous en avez une (facultatif)</label><p class="aide" id="aide-sig-source">Exemple : un lien vers Légifrance, service-public.fr ou l'Urssaf</p><input type="text" id="sig-source" name="source" maxlength="300" aria-describedby="aide-sig-source"></div>
      <div class="champ"><label for="sig-email">Votre adresse e-mail, pour recevoir la réponse (facultatif)</label><input type="email" id="sig-email" name="email" autocomplete="email" maxlength="120" aria-describedby="err-sig-email"><p class="erreur" id="err-sig-email"></p></div>
      <p class="aide">{ty("Ces informations servent uniquement à vérifier le signalement et à vous répondre. Elles sont transmises par le service Web3Forms, qui ne conserve pas les messages. Détails dans les")} <a href="mentions-legales.html#signalements">mentions légales</a>.</p>
      <div class="actions"><button type="submit" class="bouton" id="sig-envoyer">Envoyer le signalement</button></div>
      <div id="sig-etat" role="status" aria-live="polite"></div>
    </form>

    <h3 id="questions-lecteurs">{ty("Questions des lecteurs")}</h3>
    <dl class="faq-lecteurs">{"".join(f"<dt>{ty(q)}</dt><dd>{ty(r)}</dd>" for q, r in faq)}</dl>'''
    fin = '''<script src="js/acces.js"></script>
<script>
(function(){
  function etatMsg(el, classe, html){ el.className = classe; el.innerHTML = html; el.setAttribute('tabindex','-1'); el.focus(); }
  function erreur(id, texte){ var c = document.getElementById(id), e = document.getElementById('err-' + id); e.textContent = texte || ''; if (texte) c.setAttribute('aria-invalid','true'); else c.removeAttribute('aria-invalid'); return !texte; }
  var emailOk = function(v){ return /^[^@\\s]+@[^@\\s]+\\.[a-z]{2,}$/i.test(v.trim()); };

  var fi = document.getElementById('form-inscription');
  if (fi) {
    var bi = document.getElementById('ins-envoyer'), ei = document.getElementById('ins-etat');
    fi.addEventListener('submit', async function(ev){
      ev.preventDefault();
      var email = document.getElementById('ins-email'), rep = document.getElementById('ins-reponse'), accord = document.getElementById('ins-accord');
      var ok1 = erreur('ins-email', emailOk(email.value) ? '' : 'Indiquez une adresse e-mail valide, par exemple prenom.nom@exemple.fr.');
      var ok2 = erreur('ins-reponse', rep.value.trim() === '' ? 'Indiquez le dernier mot du titre de la fiche G2.6, page 160.' : ((await window.Acces.verifier(rep.value)) ? '' : 'Ce n’est pas le bon mot. Vérifiez le titre de la fiche G2.6, page 160.'));
      var ok3 = erreur('ins-accord', accord.checked ? '' : 'Cochez la case pour accepter de recevoir les mises à jour.');
      if (!(ok1 && ok2 && ok3)) { (ok1 ? (ok2 ? accord : rep) : email).focus(); return; }
      if (fi.piege.value) { etatMsg(ei, 'note succes', 'Presque fini : ouvrez l’e-mail que vous venez de recevoir et cliquez sur le lien pour confirmer.'); return; }
      bi.disabled = true; bi.textContent = 'Inscription en cours…'; ei.className = ''; ei.textContent = '';
      fetch(fi.action, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: email.value.trim(), reponse: rep.value, consentement: 'oui', piege: '' }) })
        .then(function(r){ return r.json().then(function(j){ return { ok: r.ok, j: j }; }); })
        .then(function(x){
          if (!x.ok || !x.j.ok) throw new Error();
          fi.reset();
          etatMsg(ei, 'note succes', x.j.deja ? 'Cette adresse est déjà inscrite : vous recevrez les prochaines mises à jour.' : 'Presque fini : ouvrez l’e-mail que vous venez de recevoir et cliquez sur le lien pour confirmer. Pensez à regarder dans les courriers indésirables.');
        })
        .catch(function(){ etatMsg(ei, 'note echec', 'L’inscription n’a pas pu se faire. Réessayez dans un instant, ou écrivez à <a href="mailto:benjamin@revision-vtc.fr">benjamin@revision-vtc.fr</a>.'); })
        .finally(function(){ bi.disabled = false; bi.textContent = 'Je m’inscris'; });
    });
  }

  var fs = document.getElementById('form-signalement');
  if (fs) {
    var debut = Date.now(), bs = document.getElementById('sig-envoyer'), es = document.getElementById('sig-etat');
    fs.addEventListener('submit', function(ev){
      ev.preventDefault();
      var msg = document.getElementById('sig-message'), mail = document.getElementById('sig-email');
      var ok1 = erreur('sig-message', msg.value.trim() ? '' : 'Décrivez ce qui pose problème.');
      var ok2 = erreur('sig-email', !mail.value.trim() || emailOk(mail.value) ? '' : 'Cette adresse ne semble pas valide. Laissez le champ vide si vous ne voulez pas de réponse.');
      if (!(ok1 && ok2)) { (ok1 ? mail : msg).focus(); return; }
      if (fs.botcheck.checked || Date.now() - debut < 3000) { etatMsg(es, 'note succes', 'Merci, votre signalement a bien été envoyé.'); return; }
      bs.disabled = true; bs.textContent = 'Envoi en cours…'; es.className = ''; es.textContent = '';
      var d = Object.fromEntries(new FormData(fs));
      d.name = d.email ? d.email : 'Lecteur anonyme';
      fetch(fs.action, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(d) })
        .then(function(r){ return r.json(); })
        .then(function(j){ if (!j.success) throw new Error(); fs.reset(); etatMsg(es, 'note succes', 'Merci, votre signalement a bien été envoyé. Il sera vérifié sur le texte officiel' + (d.email ? ', et vous recevrez la réponse à l’adresse indiquée.' : '.')); })
        .catch(function(){ etatMsg(es, 'note echec', 'Le signalement n’a pas pu partir. Réessayez dans un instant, ou écrivez à <a href="mailto:benjamin@revision-vtc.fr">benjamin@revision-vtc.fr</a>.'); })
        .finally(function(){ bs.disabled = false; bs.textContent = 'Envoyer le signalement'; });
    });
  }
})();
</script>
'''
    titre = "Livre examen VTC 2027 : cours, 1 191 questions corrigées et examens blancs"
    desc = ("Le livre pour réussir l'examen VTC 2027 : 213 fiches, 1 191 questions corrigées, 3 examens blancs, "
            "règles à jour de la loi du 25 juin 2026. Essayez une fiche gratuitement.")
    ld_page = {"@context": "https://schema.org", "@type": "WebPage", "name": titre, "url": SITE + "le-livre.html", "description": desc,
               "inLanguage": "fr", "isPartOf": {"@id": SITE + "#site"}, "about": {"@id": SITE + "#livre"}, "author": AUTEUR}
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in faq_achat + faq]}
    ld_livre = dict(LIVRE_LD, **{"@context": "https://schema.org"})
    ecrire("le-livre.html", page(html.escape(titre + " · Révision VTC", quote=False), corps, "livre", "", html.escape(desc),
                                 scripts_fin='<script src="js/fiche.js" defer></script>\n' + fin, jsonld=[ld_page, ld_livre, ld_faq, fil(("Accueil", ""), ("Le livre", "le-livre.html"))]))

    corps_ok = f'''    <p class="surtitre">Le livre</p>
    <h1 id="titre-retour">Inscription confirmée</h1>
    <p class="chapeau" id="texte-retour">{ty("Merci. Vous recevrez par e-mail chaque mise à jour du livre, avec la page corrigée en PDF. Chaque message contient un lien pour vous désinscrire.")}</p>
    <p><a href="mises-a-jour.html">{ty("Voir les mises à jour déjà publiées")}</a></p>'''
    fin_ok = '''<script>
(function(){
  if (new URLSearchParams(location.search).get('lien') !== 'invalide') return;
  document.getElementById('titre-retour').textContent = 'Ce lien ne fonctionne plus';
  document.getElementById('texte-retour').innerHTML = 'Le lien de confirmation est incomplet ou a déjà servi. Si vous n’êtes pas encore inscrit, recommencez depuis <a href="le-livre.html#inscription">l’espace lecteurs de la page du livre</a>.';
  document.title = 'Ce lien ne fonctionne plus · Révision VTC';
})();
</script>
'''
    ecrire("le-livre-confirmation.html", page("Inscription confirmée · Révision VTC", corps_ok, "livre", "", noindex=True, scripts_fin=fin_ok))
    corps_fin = f'''    <p class="surtitre">Le livre</p>
    <h1>Vous êtes désinscrit</h1>
    <p class="chapeau">{ty("Votre adresse a été effacée : vous ne recevrez plus les mises à jour du livre. Elles restent consultables sur la page Mises à jour du livre.")}</p>
    <p><a href="mises-a-jour.html">Voir les mises à jour du livre</a></p>
    <p><a href="le-livre.html#inscription">{ty("Se réinscrire")}</a></p>'''
    ecrire("le-livre-desinscription.html", page("Désinscription · Révision VTC", corps_fin, "livre", "", noindex=True))


# ------------------------------------------------------------------ wiki des textes réglementaires
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
        <p class="pied-achat">{achat("bouton achat petit", "Le livre sur Amazon")}</p>
      </section>'''
        th = themes[a["theme"]]
        corps = f'''    <nav class="fil" aria-label="Fil d'Ariane"><ol><li><a href="index.html">Réglementation VTC</a></li><li><a href="index.html#{a["theme"]}">{ty(th["titre"])}</a></li></ol></nav>
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
    {renvoi_qcm(FICHES, f'wiki/{a["slug"]}.html')}
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
              "image": image_partage(f'wiki/{a["slug"]}.html'), "mainEntityOfPage": SITE + f'wiki/{a["slug"]}.html', "about": loi,
              "isBasedOn": a["url"], "license": "https://www.etalab.gouv.fr/licence-ouverte-open-licence/"}
        ecrire(f'wiki/{a["slug"]}.html', page(html.escape(titre_page, quote=False), corps, "textes", "../", html.escape(desc),
                                             jsonld=[ld, fil(("Accueil", ""), ("Réglementation VTC", "wiki/"), (th["titre"], f'wiki/#{a["theme"]}'), (titre_page, f'wiki/{a["slug"]}.html'))]))

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
        autres += f'<h3>{ty(g["titre"])}</h3><ul class="wiki-liste textes-ref">' + "".join(
            f'<li><a href="{html.escape(x["url"])}">{ty(x["nom"])}</a><span class="texte-ref">{ty(x["ref"])}</span><span class="objet">{ty(x["objet"])}</span></li>'
            for x in g["textes"]) + "</ul>"
    corps = f'''    <h1>Réglementation VTC</h1>
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
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Réglementation VTC : les textes officiels expliqués",
          "url": SITE + "wiki/", "inLanguage": "fr", "dateModified": iso_fr(source_date), "author": AUTEUR, "isPartOf": {"@id": SITE + "#site"},
          "hasPart": [{"@type": "Article", "headline": a["titre"], "url": SITE + f'wiki/{a["slug"]}.html'} for a in arts]}
    ecrire("wiki/index.html", page("Réglementation VTC : les textes officiels expliqués en clair · Révision VTC", corps, "textes", "../",
                                   "La réglementation VTC article par article : réservation préalable, maraude, carte professionnelle, registre, véhicule, plateformes, sanctions. Texte officiel en vigueur et explication en clair.",
                                   scripts_fin=script, jsonld=[ld, fil(("Accueil", ""), ("Réglementation VTC", "wiki/"))]))
    # l'ancienne page renvoie vers le wiki
    ecrire("textes.html", f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>Réglementation VTC · Révision VTC</title>
<link rel="canonical" href="{SITE}wiki/"><meta http-equiv="refresh" content="0; url=wiki/index.html"></head>
<body><p><a href="wiki/index.html">La réglementation VTC a déménagé : cliquez ici.</a></p></body></html>
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
    <h3 id="lecteurs">Inscription aux mises à jour du livre</h3>
    <p>{ty("L'adresse e-mail saisie dans l'espace lecteurs de la page Le livre sert uniquement à envoyer aux lecteurs les mises à jour et les pages corrigées du livre. Base légale : votre consentement, donné en cochant la case puis confirmé par le lien reçu par e-mail ; sans confirmation, l'adresse ne reçoit rien d'autre que ce lien. Sont conservés : l'adresse, les dates d'inscription et de confirmation, et le texte de la case cochée, pour prouver le consentement. Les données sont enregistrées dans l'outil d'automatisation n8n installé sur un serveur loué par l'éditeur à Hostinger, et les e-mails partent de la boîte benjamin@revision-vtc.fr, hébergée par Gandi. Elles ne sont ni vendues, ni prêtées, ni utilisées pour de la prospection. Le lien de désinscription présent dans chaque e-mail efface l'adresse ; une adresse jamais confirmée est effacée au bout de trois mois. Vous pouvez aussi demander leur consultation, leur rectification ou leur effacement en écrivant à")} <a href="mailto:benjamin@revision-vtc.fr">benjamin@revision-vtc.fr</a>{ty(", et saisir la CNIL (cnil.fr) en cas de difficulté.")}</p>
    <h3 id="signalements">Signalement d'une erreur dans le livre</h3>
    <p>{ty("Les informations saisies dans le formulaire de signalement (type, fiche, message, source et, si vous la donnez, votre adresse e-mail) servent uniquement à vérifier le signalement et à vous répondre. Elles sont transmises par le service Web3Forms, qui les achemine par e-mail sans conserver les messages, puis conservées dans la boîte de réception de l'éditeur le temps de l'échange, et au plus un an. Base légale : votre demande. Mêmes droits que pour le formulaire de contact.")}</p>
    <h2>Propriété intellectuelle</h2>
    <p>{ty("Les textes, questions et corrigés de ce site sont la propriété de Benjamin Blondin. Toute reproduction sans autorisation est interdite (Code de la propriété intellectuelle, art. L122-4). Les brèves de l'Actualité VTC citent leurs sources, qui restent la propriété de leurs auteurs.")}</p>
    <p>{ty("Les textes officiels reproduits dans la rubrique Réglementation VTC proviennent de Légifrance (DILA). Ils sont réutilisés sous Licence Ouverte 2.0, avec mention de la source et de la date de version. Seule la version publiée sur Légifrance fait foi.")}</p>
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
        q["code_domaine"] = domaine_de(q, f)
        qs.append(q)
    for i, q in enumerate(qs):
        q["numero"] = len(qs) - i   # numéro d'ordre de publication : la plus ancienne est la n° 1
    slugs = [q["slug"] for q in qs]
    assert len(slugs) == len(set(slugs)), "deux questions ont la même adresse"
    return qs


def questions(qs, w):
    arts = {a["slug"]: a for a in w["articles"]}
    for q in qs:
        secs = "".join(f'<h2>{ty(x["titre"])}</h2>' + "".join(f"<p>{liens(ty(p))}</p>" for p in x["texte"]) for x in q["sections"])   # [texte](adresse) : maillage vers un article ou une autre question
        wiki = "".join(f'<li><a href="../wiki/{s}.html">{ty(arts[s]["num"] if not arts[s].get("arrete") else "Arrêté")} · {ty(arts[s]["titre"])}</a></li>' for s in q.get("wiki", []))
        livre = "".join(f"<li><b>Fiche {ty(c)}</b> · {ty(t)}</li>" for c, t in q.get("fiches", []))
        src = "".join(f'<li><a href="{html.escape(x["url"])}">{ty(x["nom"])}</a>' + (f", {ty(x['date'])}" if x.get("date") else "") + "</li>" for x in q["sources"])
        autres = "".join(f'<li><a href="{x["date"]}-{x["slug"]}.html">{ty(x["question"])}</a></li>' for x in qs if x is not q)[:4000]
        corps = f'''    <nav class="fil" aria-label="Fil d'Ariane"><ol><li><a href="index.html">FAQ VTC</a></li></ol></nav>
    <p class="surtitre">Question VTC n° {q["numero"]}</p>
    <h1>{ty(q["question"])}</h1>
    <p class="meta">{DOMAINES[q["code_domaine"]][0]} : {ty(DOMAINES[q["code_domaine"]][1].lower() if q["code_domaine"] == "X" else DOMAINES[q["code_domaine"]][1])}. Publiée en {mois_annee(q["date"])}, vérifiée en {mois_annee(iso_fr(q["verifie"]))}.</p>
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
    {renvoi_qcm(FICHES, f'questions/{q["date"]}-{q["slug"]}.html')}
    {f'<section class="cote-bloc wiki-livre"><h2>Dans le livre</h2><ul>{livre}</ul><p class="pied-achat">{achat("bouton achat petit", "Le livre sur Amazon")}</p></section>' if livre else ""}
    {f'<section class="cote-bloc"><h2>Autres questions</h2><ul class="voir-aussi">{autres}</ul></section>' if autres else ""}
    </aside></div>'''
        chemin = f'questions/{q["date"]}-{q["slug"]}.html'
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": q["question"][:110], "description": q["reponse_courte"],
              "datePublished": q["date"], "dateModified": iso_fr(q["verifie"]), "inLanguage": "fr", "author": AUTEUR, "publisher": AUTEUR,
              "image": image_partage(chemin), "mainEntityOfPage": SITE + chemin, "citation": [x["url"] for x in q["sources"]],
              "mainEntity": {"@type": "Question", "name": q["question"], "acceptedAnswer": {"@type": "Answer", "text": q["reponse_courte"]}}}
        ecrire(chemin, page(html.escape(q["question"] + " · Révision VTC", quote=False), corps, "questions", "../",
                            html.escape(q["reponse_courte"] if len(q["reponse_courte"]) <= 158 else q["reponse_courte"][:155].rsplit(" ", 1)[0] + "…"),
                            jsonld=[ld, fil(("Accueil", ""), ("FAQ VTC", "questions/"), (q["question"], chemin))]))
    liste = "".join(carte(q["numero"], q["date"], f'{q["date"]}-{q["slug"]}.html', ty(q["question"]), q["code_domaine"], ty(q["reponse_courte"])) for q in qs)
    corps = f'''    <h1>FAQ VTC</h1>
    <p class="chapeau">{ty("Les questions concrètes que se posent les chauffeurs VTC et les candidats à l'examen, avec une réponse courte, les textes qui la fondent et leurs sources.")}</p>
    <p class="intro">{ty("Combien de temps peut-on attendre un client devant une gare ? Faut-il un siège auto pour transporter un enfant ? Quand repasser la visite médicale ? Chaque page part d'une question que l'on se pose vraiment, au volant ou en préparant l'examen, et y répond sans détour, texte officiel à l'appui.")}</p>
    <section class="bloc-index" aria-label="Comment lire une réponse">
    <h2>{ty("Comment se lit une réponse")}</h2>
    <ol class="etapes etapes-ligne">
      <li><b>{ty("La réponse courte, tout de suite")}</b>{ty("En deux ou trois phrases, l'essentiel à retenir, avec les chiffres et les délais exacts.")}</li>
      <li><b>{ty("L'explication pas à pas")}</b>{ty("La règle détaillée, un exemple concret quand il aide à comprendre, et l'erreur à éviter.")}</li>
      <li><b>{ty("Les textes et les sources")}</b>{ty("L'article du Code des transports ou l'arrêté qui fonde la réponse, expliqué dans nos")} <a href="../wiki/index.html">textes réglementaires</a>{ty(", puis la liste des sources consultées et la fiche du livre qui traite le sujet.")}</li>
    </ol>
    </section>
    <section class="bloc-index">
    <h2>{ty("Repérez l'épreuve concernée")}</h2>
    <p>{ty("Chaque question est rattachée à l'épreuve de l'examen VTC qu'elle aide à préparer, signalée par un pictogramme. Pratique pour réviser une matière d'un coup :")}</p>
    {legende_domaines()}
    <p>{ty("De nouvelles questions sont ajoutées régulièrement. Vous ne trouvez pas la vôtre ?")} <a href="../contact.html">{ty("Posez-la")}</a>.</p>
    </section>
    <h2>{ty("Toutes les questions")}</h2>
    <ul class="questions trois">{liste}</ul>'''
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "FAQ VTC", "url": SITE + "questions/", "inLanguage": "fr",
          "hasPart": [{"@type": "Article", "headline": q["question"], "url": SITE + f'questions/{q["date"]}-{q["slug"]}.html'} for q in qs]}
    ecrire("questions/index.html", page("FAQ VTC : les questions des chauffeurs et des candidats à l'examen, réponses sourcées · Révision VTC", corps, "questions", "../",
                                        "Les questions concrètes des chauffeurs VTC et des candidats à l'examen : une réponse courte, les textes officiels qui la fondent et leurs sources, classées par épreuve de l'examen.",
                                        jsonld=[ld, fil(("Accueil", ""), ("FAQ VTC", "questions/"))]))


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
      <p class="piege" aria-hidden="true"><label>Ne pas remplir <input type="checkbox" name="botcheck" tabindex="-1"></label></p>
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
      <li>{ty("Pour une question de réglementation, la réponse est peut-être déjà dans les")} <a href="wiki/index.html">textes réglementaires</a> {ty("ou la")} <a href="questions/index.html">FAQ VTC</a>.</li>
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
    """Texte déjà passé par ty() : transforme [texte](adresse) en lien (maillage interne et sources) et **texte** en gras."""
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)   # **mot** : mise en gras (début d'un élément de liste, par exemple)
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


def _chiffres_cles(c):
    """Bloc « chiffres clés » : 3 ou 4 grands chiffres, une ligne d'explication chacun, la source dessous (charte, « Visuels »)."""
    assert 2 <= len(c["items"]) <= 4 and c.get("source"), "chiffres clés : 2 à 4 chiffres et une source"
    items = "".join(f'<li><span class="cc-valeur">{ty(i["valeur"])}</span> <span class="cc-texte">{liens(ty(i["texte"]))}</span></li>'
                    for i in c["items"])
    return f'<div class="chiffres-cles"><ul>{items}</ul><p class="source">Source : {liens(ty(c["source"]))}</p></div>'


def _graphique(g):
    """Graphique dessiné en HTML et CSS à partir de chiffres déjà publiés sur la page (charte, « Visuels »).
    Trois formes : « colonnes » (évolution sur quelques années), « barres » (comparaison, une ou deux séries),
    « parts » (répartition en pourcentages, une barre par ligne). Les valeurs affichées sont du texte (lu par les
    lecteurs d'écran, les moteurs et les assistants) ; la barre n'est qu'une longueur, cachée aux lecteurs d'écran.
    Le tableau d'origine, s'il y en a un, reste dans la page, replié sous le graphique."""
    _graphique.n = getattr(_graphique, "n", 0) + 1
    ident = f"graphique-{_graphique.n}"
    if g.get("donnees") == "bareme-examen":   # valeurs lues dans contenu/calcul_note.json, comme le simulateur de note
        g = {**g, **donnees_bareme()}
    forme = g["type"]
    assert forme in ("colonnes", "barres", "parts") and g.get("titre") and g.get("lecture") and g.get("source"), \
        f"graphique « {g.get('titre')} » : type, titre, phrase de lecture et source obligatoires"
    barre = '<span class="g-barre" aria-hidden="true"></span>'
    sep = '<span class="visuellement-cache"> : </span>'
    legende = ""
    if forme == "colonnes":
        vmax = max(v["valeur"] for v in g["valeurs"])
        donnees = "".join(
            f'<li{" class=\"estime\"" if v.get("estime") else ""} style="--v:{100 * v["valeur"] / vmax:.1f}">'
            f'<span class="g-libelle">{ty(v["libelle"])}</span>{sep}<span class="g-valeur">{ty(v["affiche"])}</span>{barre}</li>'
            for v in g["valeurs"])
    elif forme == "barres":
        series = g["series"]
        vmax = g.get("max") or max(x for grp in g["groupes"] for x in grp["valeurs"])
        def un(grp):
            assert len(grp["valeurs"]) == len(series) == len(grp["affiche"]), f"graphique « {g['titre']} » : une valeur par série"
            detail = f' <span class="g-detail">{ty(grp["detail"])}</span>' if grp.get("detail") else ""
            return (f'<li{" class=\"g-attenue\"" if grp.get("attenue") else ""}><span class="g-libelle">{ty(grp["libelle"])}</span>{detail}<ul class="g-series">'
                    + "".join(f'<li class="s{i + 1}" style="--v:{100 * v / vmax:.1f}"><span class="visuellement-cache">{ty(series[i])} : </span>'
                              f'{barre}<span class="g-valeur">{ty(af)}</span></li>' for i, (v, af) in enumerate(zip(grp["valeurs"], grp["affiche"])))
                    + "</ul></li>")
        donnees = "".join(un(grp) for grp in g["groupes"])
        if len(series) > 1:
            legende = '<p class="g-legende" aria-hidden="true">' + "".join(f'<span class="s{i + 1}">{ty(x)}</span>' for i, x in enumerate(series)) + "</p>"
    else:
        series = g["series"]
        def ligne(r):
            assert len(r["parts"]) == len(series) and abs(sum(v for v, _ in r["parts"]) - 100) <= 1, f"graphique « {g['titre']} » : parts qui font 100 %"
            return (f'<li><span class="g-libelle">{ty(r["libelle"])}</span><span class="g-parts">'
                    + "".join(f'<span class="s{i + 1}" style="--v:{v}"><span class="visuellement-cache">{ty(series[i])} : </span>'
                              f'<span class="g-valeur">{ty(af)}</span></span>' for i, (v, af) in enumerate(r["parts"]))
                    + "</span></li>")
        donnees = "".join(ligne(r) for r in g["lignes"])
        legende = '<p class="g-legende" aria-hidden="true">' + "".join(f'<span class="s{i + 1}">{ty(x)}</span>' for i, x in enumerate(series)) + "</p>"
    tableau = ""
    if g.get("tableau"):
        tableau = f'<details class="g-tableau"><summary>Voir les chiffres en tableau</summary>{_bloc_dossier({"tableau": g["tableau"]})}</details>'
    return (f'<figure class="graphique graphique-{forme}" aria-labelledby="{ident}">'
            f'<figcaption><span class="g-titre" id="{ident}">{ty(g["titre"])}</span> <span class="g-lecture">{liens(ty(g["lecture"]))}</span></figcaption>'
            f'{legende}<ul class="g-donnees">{donnees}</ul>'
            f'<p class="source">Source : {liens(ty(g["source"]))}</p>{tableau}</figure>')


def _flux(f):
    """Schéma « qui verse quoi à qui » (charte, « Visuels ») : un ou plusieurs scénarios (par exemple avant / après une
    réforme), chacun fait de liens « acteur → acteur » avec une légende sur la flèche. L'acteur « vous » est mis en avant.
    Tout est du texte : un lecteur d'écran lit « Application, vers Vous : verse le prix des courses »."""
    _graphique.n = getattr(_graphique, "n", 0) + 1
    ident = f"graphique-{_graphique.n}"
    assert f.get("titre") and f.get("lecture") and f.get("source") and f.get("etats"), "schéma : titre, lecture, source et scénarios obligatoires"
    def acteur(nom, cache=False):   # l'acteur d'arrivée est déjà annoncé (« vers … ») : caché aux lecteurs d'écran
        return (f'<span class="f-acteur{" f-vous" if nom.lower() in ("vous", "le chauffeur") else ""}"'
                f'{" aria-hidden=\"true\"" if cache else ""}>{ty(nom)}</span>')
    etats = ""
    for e in f["etats"]:
        liens_ = "".join(f'<li>{acteur(de)}<span class="f-fleche"><span class="visuellement-cache">, vers {ty(vers)} : </span>'
                         f'<span class="f-libelle">{liens(ty(lib))}</span></span>{acteur(vers, True)}</li>' for de, vers, lib in e["liens"])
        etats += (f'<div class="f-etat{" f-nouveau" if e.get("nouveau") else ""}"><p class="f-quand">{ty(e["quand"])}</p>'
                  f'<ul class="f-liens">{liens_}</ul></div>')
    alerte = f'<p class="f-alerte"><span class="f-attention">Attention</span> {liens(ty(f["alerte"]))}</p>' if f.get("alerte") else ""
    return (f'<figure class="graphique schema-flux" aria-labelledby="{ident}">'
            f'<figcaption><span class="g-titre" id="{ident}">{ty(f["titre"])}</span> <span class="g-lecture">{liens(ty(f["lecture"]))}</span></figcaption>'
            f'<div class="f-etats">{etats}</div>{alerte}<p class="source">Source : {liens(ty(f["source"]))}</p></figure>')


_MONTANT = re.compile(r"\d[\d\s\u00a0\u202f]*(?:,\d+)?\s?(?:€|%)")


def donnees_bareme():
    """Graphique « poids de chaque épreuve dans la moyenne », lu dans le barème du simulateur de note (une seule source)."""
    eps = lire_calcul_note()["epreuves"]
    total = sum(e["coef"] for e in eps)
    num = lambda x: (f"{x:.1f}".rstrip("0").rstrip(".")).replace(".", ",")
    poids = [round(e["coef"] * 100 / total, 1) for e in eps]
    return {"type": "barres", "series": ["Poids dans la moyenne"], "max": max(poids),
            "groupes": [{"libelle": f'{e["code"]} · {e["court"]}', "detail": f'coefficient {e["coef"]}, éliminatoire sous {e["elim"]} / 20',
                         "valeurs": [p], "affiche": [num(p) + " %"]} for e, p in zip(eps, poids)]}


def _valeurs_affichees(b):
    """Les chiffres qu'un bloc visuel affiche (contrôle : chacun doit être écrit ailleurs dans la page)."""
    if "chiffres" in b:
        return [i["valeur"] for i in b["chiffres"]["items"]]
    if "flux" in b:   # tout montant en € ou en % écrit dans le schéma
        f = b["flux"]
        textes = [f["lecture"], f.get("alerte", "")] + [lib for e in f["etats"] for _, _, lib in e["liens"]]
        return [m.group(0).strip() for t in textes for m in _MONTANT.finditer(t)]
    g = b["graphique"]
    if g.get("donnees") == "bareme-examen":
        g = {**g, **donnees_bareme()}
    if g["type"] == "colonnes":
        return [v["affiche"] for v in g["valeurs"]]
    if g["type"] == "barres":
        return [a for grp in g["groupes"] for a in grp["affiche"]]
    return [af for r in g["lignes"] for _, af in r["parts"]]


def _bloc_dossier(b):
    """Un bloc d'une section : paragraphe (texte), liste, tableau chiffré, encart, photo, chiffres clés, graphique ou schéma."""
    if isinstance(b, str):
        return f"<p>{liens(ty(b))}</p>"
    if "chiffres" in b:
        return _chiffres_cles(b["chiffres"])
    if "graphique" in b:
        return _graphique(b["graphique"])
    if "flux" in b:
        return _flux(b["flux"])
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


def _texte_dossier(d, visuels=True):
    """Tout le texte d'un dossier, sans balises (comptage des mots, llms-full) ; sans les visuels pour le contrôle des chiffres."""
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
            elif "chiffres" in b:
                if visuels:
                    morceaux += [f'{i["valeur"]} {i["texte"]}' for i in b["chiffres"]["items"]]
            elif "flux" in b:
                f = b["flux"]
                if visuels:
                    morceaux += [f["titre"], f["lecture"], f.get("alerte", "")] + [f"{de} vers {vers} : {lib}" for e in f["etats"] for de, vers, lib in e["liens"]]
            elif "graphique" in b:
                g = b["graphique"]
                if visuels:
                    morceaux += [g["titre"], g["lecture"]]
                if g.get("tableau"):   # le tableau replié sous le graphique est une source de la page
                    morceaux += [" ".join(l) for l in g["tableau"]["lignes"] + g["tableau"].get("total", [])]
            else:
                morceaux += [" ".join(l) for l in b["tableau"]["lignes"] + b["tableau"].get("total", [])]
    morceaux += d["a_retenir"]
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", "\n".join(morceaux)).replace("**", "")


def _controle_visuels(d):
    """Règle « aucun chiffre inventé » : chaque valeur d'un graphique ou d'un chiffre clé doit être écrite, telle quelle,
    dans le texte ou un tableau de la même page. Sinon la génération s'arrête."""
    plat = lambda x: re.sub(r"[\s\u00a0\u202f]+", " ", x).strip()
    texte = plat(_texte_dossier(d, visuels=False))
    for s in d["sections"]:
        for b in s["blocs"]:
            if isinstance(b, dict) and ("chiffres" in b or "graphique" in b or "flux" in b):
                for v in _valeurs_affichees(b):
                    assert plat(v) in texte, f"{d['slug']} : « {v} » est affiché dans un visuel mais écrit nulle part ailleurs dans la page"


# Exemple chiffré du simulateur de revenu net, repris dans les guides (« Combien gagne-t-on vraiment de l'heure ? » et
# ceux qui y renvoient). Les montants qui dépendent du prix du carburant (mis à jour automatiquement) ne sont jamais
# écrits à la main : les guides portent des repères {{simu:…}}, remplacés ici à chaque génération (depuis le 13 novembre 2026).
EXEMPLE_HEURE_ATTENTE = 35.40   # Uber, attente comprise (guide « Combien gagne… », 2e tableau, notre calcul d'après l'ARPE 2025)


def exemple_simulateur():
    s = lire_simulateur()
    d = defauts_simulateur(s)
    assert d["verse_semaine"] == 1000 and d["semaines"] == 47, \
        "simulateur : les guides écrivent « 1 000 € par semaine, 47 semaines » ; mettre leur texte à jour avec les nouvelles valeurs par défaut"
    a, b = calcul_simulateur(s), calcul_simulateur(s, base="verse")
    heures = round(a["verse"] / EXEMPLE_HEURE_ATTENTE)
    assert heures == 1328, "guide « Combien gagne… » : il écrit 1 328 heures par an ; le recalculer"
    e10 = s["valeurs"]["prix_e10"]
    reperes = {"net_mois_clients": _euros(a["net"] / 12), "net_mois_verse": _euros(b["net"] / 12),
               "heure_clients": _euros(a["net"] / heures, True), "heure_verse": _euros(b["net"] / heures, True),
               "cout_km": _euros(a["km"], True), "date_carburant": e10["date"], "prix_e10": f'{e10["valeur"]:.3f}'.replace(".", ",") + " €"}
    m = lambda x: x / 12
    postes = [("Cotisations sociales", m(a["social"] + a["vl"])), ("TVA reversée, moins celle récupérée", m(a["tva"])),
              ("Location de la voiture", m(a["loyer"] + a["amortissement"])), ("Carburant", m(a["energie"])),
              ("Assurance", m(a["assurance"])), ("Entretien", m(a["entretien"])), ("Frais réglementaires et autres frais", m(a["regl"] + a["autres"]))]
    postes = [(n, v) for n, v in postes if round(v) > 0]
    assert abs(sum(v for _, v in postes) + m(a["net"]) - m(a["verse"])) < 1, "exemple du simulateur : la répartition doit refaire le montant versé"
    graphique = {"type": "barres", "series": ["Par mois"], "max": max(m(a["net"]), *(v for _, v in postes)),
                 "groupes": [{"libelle": n, "valeurs": [v], "affiche": [_euros(v)], "attenue": True} for n, v in postes]
                            + [{"libelle": "Ce qui vous reste, avant impôt", "valeurs": [m(a["net"])], "affiche": [_euros(m(a["net"]))]}],
                 "tableau": {"legende": f"Où vont les sommes versées par les plateformes : exemple du simulateur, moyenne par mois (prix du carburant du {e10['date']}, montants arrondis)",
                             "colonnes": ["Poste", "Par mois"], "nombres": [1],
                             "lignes": [[n, _euros(v)] for n, v in postes] + [["Ce qui vous reste, avant impôt", _euros(m(a["net"]))]],
                             "total": [["Montant versé par les plateformes", _euros(m(a["verse"]))]]}}
    return reperes, graphique


def _remplir_reperes(x, reperes):
    """Remplace les repères {{simu:…}} dans tout un dossier (textes, tableaux, résumés)."""
    if isinstance(x, str):
        for k, v in reperes.items():
            x = x.replace("{{simu:" + k + "}}", v)
        assert "{{" not in x, f"repère inconnu : {x[x.index('{{'):][:40]}"
        return x
    if isinstance(x, list):
        return [_remplir_reperes(y, reperes) for y in x]
    if isinstance(x, dict):
        return {k: _remplir_reperes(v, reperes) for k, v in x.items()}
    return x


def _donnees_graphiques(d, graphique_simu):
    """Graphiques dont les valeurs viennent d'une autre source du site (« donnees ») : complétés une fois pour toutes."""
    for s in d["sections"]:
        for i, b in enumerate(s["blocs"]):
            if isinstance(b, dict) and "graphique" in b and b["graphique"].get("donnees"):
                g = b["graphique"]
                plus = {"bareme-examen": donnees_bareme, "exemple-simulateur": lambda: graphique_simu}[g["donnees"]]()
                s["blocs"][i] = {"graphique": {**{k: v for k, v in g.items() if k != "donnees"}, **plus}}


def lire_dossiers(slugs_wiki):
    ds = []
    reperes, graphique_simu = exemple_simulateur()
    for f in sorted(glob.glob(os.path.join(CONTENU, "dossiers", "*.json"))):
        with open(f, encoding="utf-8") as h:
            d = _remplir_reperes(json.load(h), reperes)
        _donnees_graphiques(d, graphique_simu)
        assert os.path.basename(f) == d["slug"] + ".json", f"{f} : le nom du fichier doit être l'adresse de la page"
        assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", d["slug"]), f"{f} : adresse invalide"
        assert d["sources"] and all(x["url"].startswith("https://") for x in d["sources"]), f"{f} : source manquante"
        assert 50 <= len(d["description"]) <= 160, f"{f} : description de 50 à 160 caractères"
        for w in d.get("wiki", []):
            assert w in slugs_wiki, f"{f} : page du wiki inconnue {w}"
        for s in d["sections"]:
            assert re.fullmatch(r"[a-z0-9-]+", s["id"]), f"{f} : identifiant de section {s['id']}"
        d["code_domaine"] = domaine_de(d, f)
        _controle_visuels(d)
        d["mots"] = len(re.findall(r"\w+", _texte_dossier(d)))
        assert d.get("brouillon") or 1200 <= d["mots"] <= 3000, f"{f} : {d['mots']} mots (article : 1 500 à 2 500 mots)"
        if d.get("brouillon") and not APERCU:
            continue
        ds.append(d)
    ds.sort(key=lambda d: (d["date"], d["numero"]), reverse=True)   # le plus récent d'abord ; même jour : le numéro le plus grand
    assert len({d["numero"] for d in ds}) == len(ds), "deux articles ont le même numéro"
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
        maj = f', mis à jour en {mois_annee(iso_fr(d["mis_a_jour"]))}' if d.get("mis_a_jour") else ""
        corps = f'''    <nav class="fil" aria-label="Fil d'Ariane"><ol><li><a href="index.html">Guides VTC</a></li></ol></nav>
    <p class="surtitre">Guide n° {d["numero"]}</p>
    <h1>{ty(d["titre"])}</h1>
    <p class="chapeau">{ty(d["chapeau"])}</p>
    <p class="meta">{DOMAINES[d["code_domaine"]][0]} : {ty(DOMAINES[d["code_domaine"]][1].lower() if d["code_domaine"] == "X" else DOMAINES[d["code_domaine"]][1])}. Publié en {mois_annee(d["date"])}{maj}, chiffres vérifiés en {mois_annee(iso_fr(d["verifie"]))}. Lecture : {d["mots"] // 230 + 1} min.</p>
    <div class="deux-col"><div class="col-texte">
    {illustration(d["image"], premiere=True) if d.get("image") else ""}
    <section class="en-clair" aria-labelledby="en-bref">
      <h2 id="en-bref">Un exemple pour commencer</h2>
      {"".join(f"<p>{liens(ty(p))}</p>" for p in d["en_bref"])}
    </section>{secs}
    <section class="retenir" aria-labelledby="retenir"><h2 id="retenir">À retenir</h2><ul>{"".join(f"<li>{liens(ty(x))}</li>" for x in d["a_retenir"])}</ul></section>
    <h2 id="sources">Sources</h2>
    <ul class="source">{src}</ul>
    <p class="source">{ty("Montants vérifiés en " + mois_annee(iso_fr(d["verifie"])) + " sur les sites officiels cités ; les tarifs non réglementés (formation, assurance, véhicule) sont des fourchettes publiées, à comparer avec vos propres devis. Cet article ne remplace pas un conseil juridique, comptable ou financier adapté à votre situation.")}</p>
    </div>
    <aside class="col-cote" aria-label="Sommaire et pour aller plus loin">
    <nav class="cote-bloc" aria-labelledby="titre-sommaire"><h2 id="titre-sommaire">Sommaire</h2><ul class="voir-aussi">{sommaire}</ul></nav>
    {f'<section class="cote-bloc" aria-labelledby="titre-textes"><h2 id="titre-textes">Les textes expliqués</h2><ul class="voir-aussi">{wiki}</ul></section>' if wiki else ""}
    {renvoi_qcm(FICHES, f'dossiers/{d["slug"]}.html')}
    {f'<section class="cote-bloc wiki-livre" aria-labelledby="titre-livre"><h2 id="titre-livre">Dans le livre</h2><ul>{livre}</ul><p class="pied-achat">{achat("bouton achat petit", "Le livre sur Amazon")}</p></section>' if livre else ""}
    <section class="cote-bloc" aria-labelledby="titre-simu"><h2 id="titre-simu">Simulateur gratuit</h2><ul class="voir-aussi"><li><a href="../simulateurs/cout-revient-revenu-net-vtc.html">{ty("Coût de revient de la voiture et revenu net : faites le calcul avec vos chiffres")}</a></li></ul></section>
    {f'<section class="cote-bloc" aria-labelledby="titre-autres"><h2 id="titre-autres">Autres guides</h2><ul class="voir-aussi">{autres}</ul></section>' if autres else ""}
    </aside></div>'''
        chemin = f'dossiers/{d["slug"]}.html'
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": d["titre"][:110], "description": d["description"],
              "abstract": " ".join(d["en_bref"]), "datePublished": d["date"], "dateModified": iso_fr(d.get("mis_a_jour") or d["verifie"]) if iso_fr(d.get("mis_a_jour") or d["verifie"]) > d["date"] else d["date"],
              "inLanguage": "fr", "author": AUTEUR, "publisher": AUTEUR, "mainEntityOfPage": SITE + chemin,
              "image": [SITE + f'images/dossiers/{d["image"]["fichier"]}-1200.jpg'] if d.get("image") else SITE + "partage.jpg",
              "articleSection": "Guides VTC", "wordCount": d["mots"], "keywords": d.get("mots_cles", []), "isPartOf": {"@id": SITE + "#site"},
              "citation": [x["url"] for x in d["sources"]]}
        partage = ""
        if d.get("image"):
            jpg = f'images/dossiers/{d["image"]["fichier"]}-1200.jpg'
            assert os.path.exists(os.path.join(DOCS, jpg)), f"image de partage manquante : {jpg}"
            partage = (f'<meta property="og:image" content="{SITE}{jpg}">\n<meta property="og:image:width" content="1200">\n'
                       f'<meta property="og:image:height" content="800">\n<meta property="og:image:alt" content="{html.escape(d["image"]["alt"])}">\n')
        ecrire(chemin, page(html.escape(d.get("titre_page", d["titre"]) + " · Révision VTC", quote=False), corps, "dossiers", "../", html.escape(d["description"]),
                            noindex=bool(d.get("brouillon")), scripts_tete=partage,
                            jsonld=[ld, fil(("Accueil", ""), ("Guides VTC", "dossiers/"), (d["titre"], chemin))]))
    if ds:
        liste = "".join(carte(d["numero"], d["date"], f'{d["slug"]}.html', ty(d["titre"]), d["code_domaine"], ty(d["description"]), "Guide") for d in ds)
        liste = f'<ul class="questions trois">{liste}</ul>'
    else:
        liste = f'<p class="note">{ty("Le premier guide sera publié très prochainement.")}</p>'
    corps = f'''    <h1>Guides VTC</h1>
    <p class="chapeau">{ty("Les grandes questions du métier de chauffeur VTC, traitées à fond : ce que coûte le lancement, ce que l'on gagne vraiment, le statut à choisir, la voiture, les cotisations. Chaque chiffre est daté et relié à sa source.")}</p>
    <p class="intro">{ty("Avant de vous lancer, vous voulez savoir si le métier tient ses promesses, et à quel prix. Ici, pas de chiffres ronds repris d'une publicité : chaque guide part d'une situation réelle, fait le calcul sous vos yeux et montre d'où vient chaque montant. De quoi décider en connaissance de cause, et réviser au passage les épreuves de gestion de l'examen.")}</p>
    <section class="bloc-index" aria-label="Ce que contient un guide">
    <h2>{ty("Ce que vous trouvez dans chaque guide")}</h2>
    <ol class="etapes etapes-ligne">
      <li><b>{ty("Un exemple pour commencer")}</b>{ty("Un chauffeur, une situation, des montants concrets : on part du terrain avant d'entrer dans les règles.")}</li>
      <li><b>{ty("Le détail, poste par poste")}</b>{ty("Les règles officielles, les tarifs publiés et les calculs, avec leurs sources et la date de vérification.")}</li>
      <li><b>{ty("De quoi passer à l'action")}</b>{ty("Refaire le calcul avec vos propres chiffres dans")} <a href="../simulateurs/cout-revient-revenu-net-vtc.html">{ty("le simulateur de coût de revient et de revenu net")}</a>{ty(", lire les textes qui s'appliquent, retrouver les fiches du livre.")}</li>
    </ol>
    </section>
    <section class="bloc-index">
    <h2>{ty("Repérez l'épreuve concernée")}</h2>
    <p>{ty("Chaque guide est rattaché à l'épreuve de l'examen VTC qu'il aide à préparer, signalée par un pictogramme. Pratique pour réviser une matière d'un coup :")}</p>
    {legende_domaines()}
    <p>{ty("De nouveaux guides sont mis en ligne régulièrement, et ceux déjà publiés sont mis à jour quand un montant ou une règle change. Pour une réponse rapide à une question précise, voyez la")} <a href="../questions/index.html">FAQ VTC</a>{ty(" ; pour le texte exact d'une règle, les")} <a href="../wiki/index.html">textes réglementaires</a>.</p>
    </section>
    <h2>{ty("Tous les guides")}</h2>
    {liste}'''
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Guides VTC", "url": SITE + "dossiers/", "inLanguage": "fr",
          "isPartOf": {"@id": SITE + "#site"},
          "hasPart": [{"@type": "Article", "headline": d["titre"], "url": SITE + f'dossiers/{d["slug"]}.html'} for d in ds]}
    ecrire("dossiers/index.html", page("Guides VTC : coûts, revenus, statut, véhicule, expliqués et chiffrés · Révision VTC", corps, "dossiers", "../",
                                       "Les guides de Révision VTC : combien coûte le lancement en VTC, combien gagne un chauffeur, quel statut choisir. Chiffres datés et sources officielles.",
                                       jsonld=[ld, fil(("Accueil", ""), ("Guides VTC", "dossiers/"))]))


# ------------------------------------------------------------------ simulateur
def lire_simulateur():
    """Hypothèses du simulateur (contenu/simulateur.json) : chaque valeur non marquée « exemple » cite au moins une source."""
    with open(os.path.join(CONTENU, "simulateur.json"), encoding="utf-8") as h:
        s = json.load(h)
    ids = {x["id"] for x in s["sources"]}
    assert all(x["url"].startswith("https://") for x in s["sources"]), "simulateur : source sans adresse"
    for cle, v in s["valeurs"].items():
        assert v.get("exemple") or v.get("sources"), f"simulateur : {cle} sans source"
        for i in v.get("sources", []):
            assert i in ids, f"simulateur : source inconnue {i}"
    c = s["valeurs"]
    assert c["prix_e10"]["date"] == c["prix_gazole"]["date"], "simulateur : les deux prix des carburants doivent avoir la même date"
    pc = next(x for x in s["sources"] if x["id"] == "prix_carburants")
    assert c["prix_e10"]["date"] in pc["nom"], "simulateur : la source des prix des carburants doit citer leur date"
    assert 0.5 < c["prix_e10"]["valeur"] < 5 and 0.5 < c["prix_gazole"]["valeur"] < 5, "simulateur : prix des carburants invraisemblable"
    return s


def calcul_simulateur(s, **e):
    """Même calcul que docs/js/simulateur.js (comparé à lui par outils/test_coherence_simulateur.py) : sert aux exemples chiffrés.
    Entrées : les mêmes noms que dans la page (verse_semaine, commission, semaines, km_an, mode, loyer_semaine, energie, prix_energie…)."""
    v = {k: x["valeur"] for k, x in s["valeurs"].items()}
    V = s["valeurs"]
    e = {**defauts_simulateur(s), **e}
    verse = e["verse_semaine"] * e["semaines"]
    c = e["commission"] / 100
    prix = verse / (1 - c) if c < 1 else verse
    commission = prix - verse
    ca_brut = verse if e["base"] == "verse" else prix
    redevable = ca_brut > V["seuil_tva"]["majore"]
    tn, tt = v["taux_tva_normal"] / 100, v["taux_tva_transport"] / 100
    tva_collectee = ca_brut * tt / (1 + tt) if redevable else 0
    ca = ca_brut - tva_collectee
    cma = {"moselle": V["taux_cma"]["moselle"], "rhin": V["taux_cma"]["bas_haut_rhin"]}.get(e["cma"], v["taux_cma"])
    taux = (v["taux_acre"] if e["acre"] else v["taux_cotisations"]) + v["taux_formation"] + cma
    social = ca * taux / 100
    vl = ca * v["taux_vl"] / 100 if e["vl"] else 0
    loyer = amort = 0
    if e["mode"] == "location":
        loyer = e["loyer_semaine"] * 52
    elif e["mode"] == "lld":
        loyer = e["loyer_mois"] * 12
    else:
        amort = max(e["prix_achat"] - e["revente"], 0) / e["duree_ans"] if e["duree_ans"] > 0 else 0
    elec = e["energie"] == "electricite"
    energie = e["km_an"] * (e["conso_elec"] if elec else e["conso_thermique"]) / 100 * e["prix_energie"]
    entretien = e["entretien_mois"] * 12
    voiture = loyer + amort + energie + e["assurance"] + entretien
    regl = v["reglementaire_5ans"] / 5
    autres = e["autres_mois"] * 12 + e["cfe"]
    tva_recuperee = tva_commission = 0
    if redevable:
        tva_recuperee = (loyer + amort + entretien + (0 if elec else energie)) * tn / (1 + tn)
        if not e["etranger"]:
            tva_recuperee += commission * tn / (1 + tn)
    elif e["etranger"]:
        tva_commission = commission * tn
    tva = tva_collectee - tva_recuperee + tva_commission
    net = verse - social - vl - tva - voiture - regl - autres
    return {"verse": verse, "prix": prix, "commission": commission, "ca_brut": ca_brut, "ca": ca, "taux": taux, "social": social, "vl": vl,
            "tva_collectee": tva_collectee, "tva_recuperee": tva_recuperee, "tva_commission": tva_commission, "tva": tva,
            "regime": "redevable" if redevable else ("base" if ca_brut > V["seuil_tva"]["valeur"] else None),
            "loyer": loyer, "amortissement": amort, "energie": energie, "assurance": e["assurance"], "entretien": entretien,
            "voiture": voiture, "regl": regl, "autres": autres, "net": net, "km": voiture / e["km_an"] if e["km_an"] else 0}


def defauts_simulateur(s):
    """Valeurs par défaut de la page (location à la semaine, hybride essence, cotisations sur le prix payé par les clients,
    commission facturée depuis l'étranger), reprises par la page du simulateur, l'accueil et les tests."""
    V = s["valeurs"]
    d = {k: V[k]["valeur"] for k in ("verse_semaine", "commission", "semaines", "heures", "km_an", "loyer_semaine", "loyer_mois", "prix_achat",
                                     "duree_ans", "revente", "entretien_mois", "autres_mois", "conso_thermique", "conso_elec", "cfe")}
    return {**d, "prix_energie": V["prix_e10"]["valeur"], "assurance": V["assurance_rc"]["valeur"], "base": "clients", "mode": "location",
            "energie": "essence", "cma": "france", "vl": False, "etranger": True, "acre": False}


def _euros(x, cts=False):
    t = f"{x:,.2f}" if cts else f"{round(x):,}"
    return t.replace(",", " ").replace(".", ",") + " €"


def simulateur(ds, note=None):
    s = lire_simulateur()
    V = {k: x for k, x in s["valeurs"].items()}
    src = {x["id"]: x for x in s["sources"]}
    num = lambda x: str(x).replace(".", ",")
    refs = lambda cle: " ; ".join(f'<a href="#source-{i}">{ty(src[i]["nom"].split(" (")[0].split(", «")[0].split(" «")[0])}</a>' for i in V[cle].get("sources", []))

    def champ(ident, libelle, cle, unite, aide="", mn=0, mx=1e9, valeur=None, mode=None, energie=None):
        val = num(V[cle]["valeur"] if valeur is None else valeur)
        attr = (f' data-mode="{mode}"' if mode else "") + (f' data-energie="{energie}"' if energie else "")
        ident_aide = f"aide-{ident}"
        u = f'<span class="unite" id="unite-{ident}">{ty(unite)}</span>' if ident == "prix_energie" else f'<span class="unite">{ty(unite)}</span>'
        return (f'<div class="champ"{attr}><label for="{ident}">{ty(libelle)} {u}</label>'
                + (f'<p class="aide" id="{ident_aide}">{aide}</p>' if aide else "")
                + f'<input type="text" inputmode="decimal" autocomplete="off" id="{ident}" name="{ident}" value="{val}" data-min="{mn}" data-max="{mx}" '
                f'aria-describedby="{ident_aide + " " if aide else ""}err-{ident}"><p class="erreur" id="err-{ident}"></p></div>')

    def radios(nom, legende, options, aide=""):
        o = "".join(f'<label><input type="radio" name="{nom}" value="{val}"{" checked" if i == 0 else ""}><span>{ty(t)}</span></label>' for i, (val, t) in enumerate(options))
        return f'<fieldset class="groupe"><legend>{ty(legende)}</legend>' + (f'<p class="aide">{aide}</p>' if aide else "") + f'<div class="choix">{o}</div></fieldset>'

    sdes = src["sdes"]
    formulaire = f'''
    <form id="simu" class="simu" novalidate hidden aria-describedby="simu-intro">
      <p class="aide" id="simu-intro">{ty("Les valeurs proposées sont des hypothèses sourcées ou des exemples : remplacez-les par vos chiffres. Le résultat se met à jour à chaque saisie ; rien n'est envoyé.")} <a class="lien-resultat" href="#resultat">{ty("Aller au résultat")}</a></p>
      <fieldset class="bloc-simu"><legend>1. Votre activité</legend>
        {champ("verse_semaine", "Montant versé par les plateformes", "verse_semaine", "(€ par semaine)",
               ty("Ce que vous recevez chaque semaine, commission déjà retirée, sans les pourboires. Repère : en septembre et octobre 2024, les plateformes ont versé en moyenne 38 € par heure de course, approche comprise, attente non comprise (") + f'<a href="#source-sdes">SDES</a>).', 0, 20000)}
        <div class="champs-2">
          {champ("commission", "Commission moyenne", "commission", "(%)", ty("Uber : de 3 à 45 % selon la course ; Bolt : 24 % dans les grandes villes ; environ 25 % en moyenne."), 0, 60)}
          {champ("semaines", "Semaines travaillées", "semaines", "(par an)", ty("Exemple : 52 semaines moins 5 de repos."), 1, 52)}
        </div>
        <div class="champs-2">
          {champ("km_an", "Kilomètres parcourus", "km_an", "(par an)", ty("Courses, approches et retours compris. Repère publié : de 40 000 à 80 000 km."), 0, 300000)}
          {champ("heures", "Heures de travail", "heures", "(par semaine, facultatif)", ty("Attente comprise, pour calculer votre revenu net par heure."), 0, 100)}
        </div>
        {radios("base", "Sur quel montant calculer les cotisations ?", [("clients", "Le prix payé par les clients, commission comprise (prudent)"), ("verse", "Le montant versé par les plateformes")],
                ty("Aucun texte officiel ne tranche ce point : voir plus bas « Ce que le simulateur ne tranche pas »."))}
        <p class="option-chrono"><input type="checkbox" id="etranger" name="etranger" checked aria-describedby="aide-etranger"><label for="etranger">{ty("Ma plateforme facture sa commission depuis l'étranger (Uber, Bolt)")}</label></p>
        <p class="aide" id="aide-etranger">{ty("Uber et Bolt facturent leur commission depuis les Pays-Bas et l'Estonie, sans TVA : c'est au chauffeur de déclarer et payer la TVA française de 20 % sur cette commission, même en franchise de TVA, et dans ce cas sans pouvoir la récupérer. Décochez si votre plateforme est française et vous facture sa TVA.")}</p>
      </fieldset>
      <fieldset class="bloc-simu"><legend>2. Votre voiture</legend>
        {radios("mode", "Comment disposez-vous de la voiture ?", [("location", "Location à la semaine (assurance du véhicule et entretien compris)"), ("lld", "Location longue durée ou avec option d'achat"), ("achat", "Achat")])}
        {champ("loyer_semaine", "Loyer", "loyer_semaine", "(€ par semaine)", ty("Hybride chez un loueur spécialisé : de 210 à 350 € par semaine. Compté 52 semaines par an : la voiture reste louée pendant vos repos."), 0, 2000, mode="location")}
        {champ("loyer_mois", "Loyer", "loyer_mois", "(€ par mois)", ty("Offres publiées : de 400 à 1 200 € par mois, assurance non comprise."), 0, 5000, mode="lld")}
        <div class="champs-2" data-mode="achat">
          {champ("prix_achat", "Prix d'achat", "prix_achat", "(€)", ty("Exemple : berline hybride Toyota Corolla 2026, à partir de 34 200 €."), 0, 200000)}
          {champ("duree_ans", "Durée de détention", "duree_ans", "(années)", ty("Une voiture thermique doit avoir moins de 7 ans ; pas de limite pour une hybride."), 1, 15)}
        </div>
        {champ("revente", "Valeur de revente estimée", "revente", "(€)", ty("Laissez 0 si vous ne savez pas : le calcul reste prudent."), 0, 200000, mode="achat")}
        <div class="champ"><label for="assurance">Assurance <span class="unite">(€ par an)</span></label>
          <p class="aide" id="aide-assurance-location">{ty("Responsabilité civile professionnelle seule (le loueur assure la voiture) : de 350 à 600 € par an pour un débutant.")}</p>
          <p class="aide" id="aide-assurance-complete" hidden>{ty("Voiture et responsabilité civile professionnelle, débutant : de 2 000 à 4 100 € par an en formule de base, jusqu'à 7 580 € en tous risques ; plus cher en Île-de-France.")}</p>
          <input type="text" inputmode="decimal" autocomplete="off" id="assurance" name="assurance" value="{num(V["assurance_rc"]["valeur"])}" data-min="0" data-max="30000" aria-describedby="aide-assurance-location aide-assurance-complete err-assurance"><p class="erreur" id="err-assurance"></p></div>
        {champ("entretien_mois", "Entretien et pneus", "entretien_mois", "(€ par mois)", ty("À indiquer si la voiture n'est pas louée à la semaine : aucun montant de référence fiable n'est publié."), 0, 5000, mode="lld achat")}
        {radios("energie", "Énergie", [("essence", "Essence (hybride)"), ("gazole", "Gazole"), ("electricite", "Électricité")])}
        <div class="champs-2">
          {champ("conso_thermique", "Consommation", "conso_thermique", "(L / 100 km)", ty("Corolla hybride : 4,3 à 4,9 L/100 km au cycle d'homologation ; souvent plus en ville."), 0, 30, energie="thermique")}
          {champ("conso_elec", "Consommation", "conso_elec", "(kWh / 100 km)", ty("Tesla Model 3 : 12,5 à 13,6 kWh/100 km au cycle d'homologation."), 0, 60, energie="electricite")}
          {champ("prix_energie", "Prix", "prix_e10", "(€ par litre)", ty(f"Moyennes nationales du {V['prix_e10']['date']} : SP95-E10 {num(V['prix_e10']['valeur'])} €, gazole {num(V['prix_gazole']['valeur'])} € le litre. Électricité à domicile : 0,20 € le kWh (tarif réglementé, option Base). La recharge rapide coûte plus cher."), 0, 5)}
        </div>
      </fieldset>
      <fieldset class="bloc-simu"><legend>3. Autres frais et impôt</legend>
        {champ("autres_mois", "Autres frais", "autres_mois", "(€ par mois)", ty("Téléphone, eau et lavage, péages, stationnement, comptable, banque… La carte, le registre et la visite médicale sont déjà comptés."), 0, 10000)}
        {champ("cfe", "Cotisation foncière des entreprises (CFE)", "cfe", "(€ par an)", ty("Rien l'année de création ; ensuite, le montant de votre avis de CFE, qui dépend de la commune. Laissez 0 si vous ne le connaissez pas encore."), 0, 10000)}
        {radios("cma", "Où est immatriculée votre entreprise ?", [("france", "Hors Alsace-Moselle"), ("rhin", "Bas-Rhin ou Haut-Rhin"), ("moselle", "Moselle")])}
        <p class="option-chrono"><input type="checkbox" id="acre" name="acre" aria-describedby="aide-acre"><label for="acre">{ty("Première année avec l'Acre (cotisations à 15,9 % au lieu de 21,2 %)")}</label></p>
        <p class="aide" id="aide-acre">{ty("Pour une micro-entreprise créée depuis le 1er juillet 2026, sur demande à l'Urssaf et sous conditions (demandeur d'emploi indemnisé, moins de 26 ans, bénéficiaire du RSA…), jusqu'à la fin du 3e trimestre civil qui suit le début d'activité.")}</p>
        <p class="option-chrono"><input type="checkbox" id="vl" name="vl"><label for="vl">{ty("J'ai opté pour le versement libératoire de l'impôt (1,7 % du chiffre d'affaires)")}</label></p>
      </fieldset>
      <div class="actions"><button type="submit" class="bouton">Voir le résultat</button><button type="button" class="bouton second" id="simu-raz">Revenir aux valeurs par défaut</button></div>
      <p class="erreur" id="simu-etat" role="status"></p>
    </form>
    <p class="note" id="simu-sans-js">{ty("Le simulateur a besoin de JavaScript. Sans lui, l'exemple chiffré plus bas donne le calcul complet avec les valeurs par défaut.")}</p>'''

    resultat = f'''
    <section class="cote-bloc resultat-simu" id="resultat" tabindex="-1" aria-labelledby="titre-resultat" hidden>
      <h2 id="titre-resultat">Votre résultat</h2>
      <p class="meta">Revenu net estimé, par mois</p>
      <p class="resultat" id="res-net"></p>
      <p class="meta" id="res-net-an"></p>
      <div class="repartition" aria-hidden="true"><span id="barre-social" class="part-social"></span><span id="barre-voiture" class="part-voiture"></span><span id="barre-autres" class="part-autres"></span><span id="barre-net" class="part-net"></span></div>
      <p class="meta" id="barre-texte"></p>
      <dl class="chiffres">
        <div><dt>Coût de revient de la voiture</dt><dd><span id="res-km"></span> par km · <span id="res-voiture-mois"></span> par mois</dd></div>
        <div><dt>Seuil de rentabilité</dt><dd><span id="res-seuil"></span> versés par semaine</dd></div>
        <div id="res-heure-bloc" hidden><dt>Revenu net par heure de travail</dt><dd id="res-heure"></dd></div>
      </dl>
      <p class="meta"><a href="#detail-resultat">Le détail du calcul</a></p>
      <p class="visuellement-cache" id="simu-annonce" aria-live="polite"></p>
    </section>
    <aside class="barre-resultat cachee" id="barre-resultat" aria-label="Résultat en bref" hidden>
      <p><span class="barre-legende">Revenu net estimé</span> <b id="barre-res-net"></b> <span class="barre-legende">par mois</span></p>
      <a class="bouton clair petit" href="#resultat">Voir le détail</a>
    </aside>'''

    # détail du résultat : sous le formulaire, dans la colonne principale (le panneau collant ne garde que l'essentiel)
    detail = f'''
    <section class="col-detail" id="detail-resultat" aria-labelledby="titre-detail" hidden>
      <h2 id="titre-detail">{ty("Le détail de votre résultat")}</h2>
      <div id="res-alertes"></div>
      <table><caption>Le détail, en euros par mois (montants arrondis)</caption><tbody id="res-detail"></tbody></table>
      <p class="meta" id="res-impot"></p>
      <div class="actions"><button type="button" class="bouton second petit" id="simu-lien">Copier le lien de cette simulation</button></div>
      <p class="meta" id="lien-etat" aria-live="polite"></p>
    </section>'''

    # exemple chiffré avec les valeurs par défaut (location à la semaine, hybride essence)
    defaut = defauts_simulateur(s)
    a = calcul_simulateur(s)
    b = calcul_simulateur(s, base="verse")
    m = lambda x: _euros(x / 12)
    exemple = {"tableau": {"legende": "Exemple : 1 000 € versés par semaine, 47 semaines, voiture hybride louée à la semaine, en euros par mois (montants arrondis)",
                           "colonnes": ["Poste", "Cotisations sur le prix payé par les clients", "Cotisations sur le montant versé"], "nombres": [1, 2],
                           "lignes": [["Prix payé par les clients", m(a["prix"]), m(b["prix"])],
                                      ["Commission (25 %)", "− " + m(a["commission"]), "− " + m(b["commission"])],
                                      ["Versé par les plateformes", m(a["verse"]), m(b["verse"])],
                                      ["TVA à reverser (10 % des courses, moins la TVA récupérée sur la location et le carburant)", "− " + m(a["tva"]), "− " + m(b["tva"])],
                                      [f'Cotisations et contributions ({num(round(a["taux"], 2))} % du chiffre d\'affaires hors taxe)', "− " + m(a["social"]), "− " + m(b["social"])],
                                      ["Location (280 € × 52 semaines)", "− " + m(a["loyer"]), "− " + m(b["loyer"])],
                                      [f"Carburant (60 000 km, 4,9 L/100 km, {num(V['prix_e10']['valeur'])} €/L)", "− " + m(a["energie"]), "− " + m(b["energie"])],
                                      ["Assurance (responsabilité civile professionnelle)", "− " + m(a["assurance"]), "− " + m(b["assurance"])],
                                      ["Carte, registre, visite médicale (sur 5 ans)", "− " + m(a["regl"]), "− " + m(b["regl"])]],
                           "total": [["Revenu net avant impôt", m(a["net"]), m(b["net"])]]}}
    ecart = b["net"] - a["net"]

    lignes_hyp = [
        ("Commission des plateformes", "25 %", "commission"), ("Kilomètres par an", "60 000 km", "km_an"),
        ("Location d'une hybride à la semaine", "280 € (fourchette 210 à 350 €)", "loyer_semaine"),
        ("Location longue durée ou LOA", "800 € par mois (fourchette 400 à 1 200 €)", "loyer_mois"),
        ("Prix d'achat d'une berline hybride", "34 200 €", "prix_achat"),
        ("Assurance, responsabilité civile professionnelle seule", "600 € par an (haut de la fourchette 350 à 600 €)", "assurance_rc"),
        ("Assurance voiture et RC pro, débutant", "4 100 € par an (haut des formules de base)", "assurance_complete"),
        ("Prix du SP95-E10 / du gazole", f"{num(V['prix_e10']['valeur'])} € / {num(V['prix_gazole']['valeur'])} € le litre ({V['prix_e10']['date']})", "prix_e10"),
        ("Consommation d'une hybride", "4,9 L/100 km (cycle WLTP)", "conso_thermique"),
        ("Électricité à domicile", "0,20 € le kWh (option Base, 6 kVA)", "prix_kwh"),
        ("Consommation d'une électrique", "13,6 kWh/100 km (cycle WLTP)", "conso_elec"),
        ("Cotisations sociales", "21,2 % du chiffre d'affaires", "taux_cotisations"),
        ("Cotisations avec l'Acre (création depuis le 1er juillet 2026)", "15,9 %", "taux_acre"),
        ("Formation professionnelle", "0,3 %", "taux_formation"),
        ("Taxe de chambre de métiers", "0,48 % (0,65 % Bas-Rhin et Haut-Rhin, 0,83 % Moselle)", "taux_cma"),
        ("Versement libératoire / abattement fiscal", "1,7 % / 50 %", "taux_vl"),
        ("Carte, registre, visite médicale", "263,60 € tous les 5 ans (hors envoi et vignettes)", "reglementaire_5ans"),
        ("Franchise de TVA", "37 500 € (seuil majoré 41 250 €)", "seuil_tva"),
        ("TVA sur les courses de VTC", "10 % (taux des transports de voyageurs)", "taux_tva_transport"),
        ("TVA sur la commission facturée depuis l'étranger", "20 %, à payer par le chauffeur, même en franchise", "tva_commission"),
        ("TVA récupérable si la TVA est due", "loyer, achat, entretien et carburant d'une voiture affectée au VTC", "tva_deductible_voiture"),
        ("Plafond de la micro-entreprise", "83 600 €", "seuil_micro")]
    hyp = {"tableau": {"legende": f"Les hypothèses par défaut, vérifiées le {s['verifie']}", "colonnes": ["Hypothèse", "Valeur", "Source"],
                       "lignes": [[l, v, "__REF__" + c] for l, v, c in lignes_hyp]}}
    tab_hyp = _bloc_dossier(hyp)
    for _, _, c in lignes_hyp:
        tab_hyp = tab_hyp.replace(ty("__REF__" + c), refs(c), 1)
    sources = "".join(f'<li id="source-{x["id"]}"><a href="{html.escape(x["url"])}">{ty(x["nom"])}</a>, {ty(x["date"])}</li>' for x in s["sources"])
    dossier1 = '<a href="../dossiers/cout-pour-devenir-chauffeur-vtc.html">' + ty("Combien coûte vraiment le lancement en VTC ?") + "</a>"

    corps = f'''    <nav class="fil" aria-label="Fil d'Ariane"><ol><li><a href="index.html">Simulateurs</a></li></ol></nav>
    <p class="surtitre">Simulateur gratuit</p>
    <h1>{ty("Simulateur VTC : coût de revient de la voiture et revenu net")}</h1>
    <p class="chapeau">{ty("Ce que vous versent les plateformes, moins la voiture, le carburant, l'assurance et les cotisations : le simulateur calcule ce qui vous reste vraiment, en euros par mois.")}</p>
    <p class="meta">{ty("Pour les chauffeurs VTC en micro-entreprise, TVA comprise. Hypothèses vérifiées le " + s["verifie"] + ". Calcul fait dans votre navigateur : rien n'est envoyé.")}</p>
    <div class="deux-col"><div class="col-texte">
    {formulaire}
    </div>
    <aside class="col-cote" aria-label="Résultat de la simulation">{resultat}
    </aside>{detail}</div>
    <!-- mode d'emploi et exemple : après le formulaire et le résultat (audit visuel, lot 2) -->
    <section aria-labelledby="mode-emploi">
      <h2 id="mode-emploi">{ty("Comment ça marche")}</h2>
      <ol class="etapes">
        <li><b>{ty("Vous décrivez votre activité")}</b>{ty("Ce que les plateformes vous versent par semaine, le nombre de semaines où vous travaillez dans l'année et les kilomètres que vous parcourez.")}</li>
        <li><b>{ty("Vous décrivez votre voiture et vos frais")}</b>{ty("Louée à la semaine, en location longue durée ou achetée ; essence, gazole ou électrique ; votre assurance et vos autres dépenses (téléphone, lavage, péages…).")}</li>
        <li><b>{ty("Le simulateur fait le calcul et vous répond")}</b>{ty("Il retire les cotisations, la TVA, le coût de la voiture et les frais obligatoires du métier (carte professionnelle, registre, visite médicale), puis affiche :")}
          <ul>
            <li>{ty("votre revenu net, par mois et par an ;")}</li>
            <li>{ty("ce que vous coûte la voiture à chaque kilomètre ;")}</li>
            <li>{ty("le montant à faire chaque semaine pour ne pas travailler à perte.")}</li>
          </ul></li>
      </ol>
      <p>{ty("Les cases sont déjà remplies avec un exemple réaliste, dont chaque valeur est sourcée : changez seulement ce que vous connaissez, le résultat se met à jour tout seul.")}</p>
      <div class="note">
        <dl>
          <dt>{ty("Montant versé")}</dt><dd>{ty("Ce que la plateforme vous vire, sa commission déjà retirée. C'est le chiffre de vos relevés Uber, Bolt ou Heetch.")}</dd>
          <dt>{ty("Coût de revient de la voiture")}</dt><dd>{ty("Tout ce que coûte la voiture sur l'année (loyer ou achat, énergie, assurance, entretien), divisé par les kilomètres parcourus.")}</dd>
          <dt>{ty("Seuil de rentabilité")}</dt><dd>{ty("Le montant versé par semaine en dessous duquel vos frais dépassent ce que vous gagnez.")}</dd>
          <dt>{ty("Revenu net")}</dt><dd>{ty("Ce qui vous reste pour vivre, avant l'impôt sur le revenu.")}</dd>
        </dl>
      </div>
    </section>
    <section class="en-clair" aria-labelledby="en-bref">
      <h2 id="en-bref">Un exemple chiffré</h2>
      <p>{ty(f"Exemple : un chauffeur à qui les plateformes versent 1 000 € par semaine pendant 47 semaines, avec une hybride louée 280 € par semaine et 60 000 km par an, garde environ {_euros(a['net'] / 12)} par mois avant impôt si ses cotisations portent sur le prix payé par les clients, et {_euros(b['net'] / 12)} si elles portent sur le montant versé. Sa voiture lui coûte {_euros(a['km'], True)} par kilomètre, carburant et assurance compris.")}</p>
      <p>{ty("La location, le carburant et les cotisations pèsent le plus. Les sommes versées par les plateformes ne sont pas un revenu : elles doivent d'abord couvrir tous ces frais.")}</p>
    </section>
    <h2 id="calcul">Comment le simulateur calcule</h2>
    <ol>
      <li>{ty("Montant versé sur l'année = montant versé par semaine × semaines travaillées. Prix payé par les clients = montant versé ÷ (1 − commission).")}</li>
      <li>{ty("Cotisations et contributions = chiffre d'affaires (hors taxe si la TVA est due) × 21,98 % (21,2 % de cotisations sociales, 0,3 % de formation professionnelle, 0,48 % de taxe de chambre de métiers hors Alsace-Moselle), plus 1,7 % si vous avez choisi le versement libératoire.")}</li>
      <li>{ty("Voiture = loyer (ou prix d'achat moins revente, divisé par la durée de détention) + énergie (kilomètres × consommation × prix) + assurance + entretien. Divisé par les kilomètres, c'est le coût de revient au kilomètre.")}</li>
      <li>{ty("TVA, au-delà de 41 250 € de chiffre d'affaires par an : le prix des courses comprend 10 % de TVA, soit 1/11 du montant, à reverser. On en retire la TVA de 20 % comprise dans le loyer, l'achat, l'entretien et le carburant (1/6 du montant payé), récupérable parce que la voiture sert au transport de personnes. Les cotisations portent alors sur le chiffre d'affaires hors taxe. Le calcul vaut pour une année complète.")}</li>
      <li>{ty("TVA, en franchise : rien à facturer, mais si la commission est facturée depuis l'étranger, la TVA de 20 % sur cette commission est due et ne se récupère pas.")}</li>
      <li>{ty("Revenu net = montant versé − cotisations − TVA − voiture − carte, registre et visite médicale − autres frais. La commission est déjà retirée du montant versé.")}</li>
      <li>{ty("Seuil de rentabilité = montant versé par semaine à partir duquel le revenu net devient positif.")}</li>
    </ol>
    {_bloc_dossier(exemple)}
    <p>{ty(f"Dans cet exemple, le chiffre d'affaires ({_euros(a['ca_brut'])} par an) dépasse le seuil majoré de la franchise de TVA : le chauffeur doit reverser {_euros(a['tva_collectee'] / 12)} de TVA par mois, et en récupère {_euros(a['tva_recuperee'] / 12)} sur la location et le carburant. Le choix de la base des cotisations change le revenu net de {_euros(ecart / 12)} par mois.")}</p>
    <h2 id="non-tranche">Ce que le simulateur ne tranche pas</h2>
    <h3>{ty("Les cotisations : sur le prix payé par les clients ou sur le montant versé ?")}</h3>
    <p>{ty("En micro-entreprise, les cotisations sont un pourcentage du chiffre d'affaires, sans déduction des frais. Pour un chauffeur de plateforme, le chiffre d'affaires est-il le prix payé par le client, ou ce que la plateforme reverse après sa commission ? Aucun texte officiel ne le dit. Des experts-comptables recommandent de déclarer le prix avant commission, par prudence ; la même source rapporte qu'Uber invite à déclarer le montant après commission. Le simulateur calcule les deux : choisissez, et en cas de doute, faites le point avec un expert-comptable ou l'Urssaf.")}</p>
    <h3>{ty("La TVA : l'année du dépassement et l'option")}</h3>
    <p>{ty("Un chauffeur en micro-entreprise ne facture pas la TVA tant que son chiffre d'affaires ne dépasse pas 37 500 € sur l'année précédente et 41 250 € sur l'année en cours (seuils 2026). Le simulateur calcule une année complète au même rythme : au-delà de 41 250 €, toute l'année avec la TVA ; entre 37 500 € et 41 250 €, l'année en franchise, la TVA n'étant due que l'année suivante. L'année où le seuil de 41 250 € est franchi, la TVA n'est due qu'à partir du jour du dépassement : le résultat réel se situe entre les deux.")}</p>
    <p>{ty("Avec une commission facturée depuis l'étranger, la franchise n'est pas toujours la solution la moins chère : la TVA sur la commission y est due sans être récupérable, alors qu'un chauffeur qui paie la TVA la récupère, comme celle de la voiture. Il est possible de renoncer à la franchise sur option : faites le calcul avec un expert-comptable avant de choisir.")}</p>
    <h3>{ty("Les aides et les changements de 2027")}</h3>
    <p>{ty("L'Acre réduit les cotisations sociales au début de l'activité : 15,9 % au lieu de 21,2 % pour une micro-entreprise créée depuis le 1er juillet 2026, sur demande et sous conditions, jusqu'à la fin du 3e trimestre civil qui suit le début d'activité. Cochez la case pour la compter : le résultat montre alors une année entière au taux réduit, c'est un maximum. Le précompte des cotisations par les plateformes, prévu au 1er janvier 2027, change la façon de payer, pas les taux. Le détail des taux est dans la question")} <a href="../questions/2026-10-28-cotisations-vtc-micro-entreprise.html">{ty("« Quelles cotisations paie un chauffeur VTC en micro-entreprise ? »")}</a>.</p>
    <h2 id="non-compte">Ce que le simulateur ne compte pas</h2>
    <ul>
      <li>{ty("l'impôt sur le revenu sans versement libératoire : il dépend de votre foyer ; le simulateur donne seulement le revenu imposable après l'abattement de 50 % ;")}</li>
      <li>{ty("la cotisation foncière des entreprises (CFE), si vous n'indiquez pas son montant : il dépend de la commune ;")}</li>
      <li>{ty("la TVA récupérable sur l'électricité et sur les autres frais : elle ne l'est que sur facture au nom de l'entreprise, ce qui est rare pour la recharge à domicile ; le calcul reste donc prudent ;")}</li>
      <li>{ty("le stage de formation continue et le contrôle technique annuel, à prix libres ; les intérêts d'un crédit ;")}</li>
      <li>{ty("les dépenses de lancement (examen, formation, caution du loueur) : elles sont détaillées dans l'article")} {dossier1}.</li>
    </ul>
    <h2 id="hypotheses">Les hypothèses par défaut et leurs sources</h2>
    <p>{ty("Chaque valeur proposée vient d'un texte officiel, d'une donnée publique ou de deux sources concordantes. Les prix libres (location, assurance) sont des fourchettes publiées, pas des tarifs : comparez avec vos devis. Le montant versé par semaine, les semaines travaillées et la durée de détention sont des exemples à remplacer.")}</p>
    {tab_hyp}
    <h2 id="sources">Sources</h2>
    <ul class="source">{sources}</ul>
    <p class="source">{ty("Simulation indicative pour un chauffeur VTC en micro-entreprise ; elle ne remplace pas un conseil comptable ou fiscal adapté à votre situation. Les prix moyens des carburants sont mis à jour chaque matin à partir des prix déclarés la veille par les stations-service ; les autres valeurs ont été vérifiées à la date indiquée en haut de la page.")}</p>'''

    donnees = json.dumps({"valeurs": s["valeurs"]}, ensure_ascii=False).replace("</", "<\\/")
    fin = f'<script id="simu-donnees" type="application/json">{donnees}</script>\n<script src="../js/simulateur.js"></script>\n'
    chemin = f'simulateurs/{s["slug"]}.html'
    titre = "Simulateur VTC : coût de revient de la voiture et revenu net"
    desc = "Simulateur VTC gratuit : coût de revient de votre voiture au km et revenu net après commission, cotisations, location, carburant et assurance. Hypothèses sourcées."
    ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": titre, "url": SITE + chemin, "description": desc,
          "applicationCategory": "FinanceApplication", "operatingSystem": "Navigateur web", "inLanguage": "fr", "isAccessibleForFree": True,
          "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "author": AUTEUR, "publisher": AUTEUR,
          "datePublished": s["date"], "dateModified": iso_fr(s["verifie"]), "isPartOf": {"@id": SITE + "#site"},
          "isBasedOn": [x["url"] for x in s["sources"]]}
    ecrire(chemin, page(html.escape(titre + " · Révision VTC", quote=False), corps, "simulateurs", "../", html.escape(desc),
                        scripts_fin=fin, jsonld=[ld, fil(("Accueil", ""), ("Simulateurs", "simulateurs/"), (titre, chemin))]))

    note_li = (f'<li><span class="meta">{ty("Mis à jour le " + note["verifie"])}</span><a href="{note["slug"]}.html">{ty(note["titre"])}</a><p>{ty("Après un examen blanc : admissible ou non, pourquoi, et quelle épreuve travailler en priorité, selon le barème officiel (coefficients et notes éliminatoires).")}</p></li>') if note else ""
    liste = f'''<ul class="questions"><li><span class="meta">{ty("Mis à jour le " + s["verifie"])}</span><a href="{s["slug"]}.html">{ty(titre)}</a><p>{ty("Le coût de revient de votre voiture au kilomètre et ce qu'il vous reste chaque mois, après commission, cotisations, location, carburant et assurance.")}</p></li>{note_li}</ul>'''
    corps = f'''    <h1>Simulateurs VTC</h1>
    <p class="chapeau">{ty("Calculez votre note à l'examen VTC, ou ce que votre activité de chauffeur vous rapporte vraiment. Vous saisissez vos propres chiffres ; chaque règle et chaque valeur proposée par défaut est sourcée et datée, et le calcul se fait dans votre navigateur.")}</p>
    <p>{ty("Pour comprendre les montants avant de les saisir, lisez les")} <a href="../dossiers/index.html">guides</a> {ty("; pour les règles du métier, les")} <a href="../wiki/index.html">textes réglementaires</a>.</p>
    {liste}'''
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Simulateurs VTC", "url": SITE + "simulateurs/", "inLanguage": "fr",
          "isPartOf": {"@id": SITE + "#site"}, "hasPart": [{"@type": "WebApplication", "name": titre, "url": SITE + chemin}]
          + ([{"@type": "WebApplication", "name": note["titre"], "url": SITE + f'simulateurs/{note["slug"]}.html'}] if note else [])}
    ecrire("simulateurs/index.html", page("Simulateurs VTC gratuits : note de l'examen, coût de revient, revenu net · Révision VTC", corps, "simulateurs", "../",
                                          "Outils gratuits VTC : calcul de la note de l'examen avec le barème officiel, coût de revient de la voiture au kilomètre et revenu net mensuel, sources datées.",
                                          jsonld=[ld, fil(("Accueil", ""), ("Simulateurs", "simulateurs/"))]))
    return s


# ------------------------------------------------------------------ calcul de la note de l'examen
def lire_calcul_note():
    """Barème de l'examen (contenu/calcul_note.json), recopié de l'arrêté du 6 avril 2017, article 2 : contrôles de cohérence."""
    with open(os.path.join(CONTENU, "calcul_note.json"), encoding="utf-8") as h:
        n = json.load(h)
    eps = n["epreuves"]
    assert [e["code"] for e in eps] == list("ABCDEFG"), "calcul de la note : épreuves A à G attendues"
    assert sum(e["coef"] for e in eps) == 17, "calcul de la note : la somme des coefficients doit être 17"
    assert all(e["elim"] == (4 if e["code"] == "E" else 6) for e in eps), "calcul de la note : seuils éliminatoires 6 (4 en anglais)"
    assert [e["code"] for e in eps if not e["commune"]] == ["F", "G"], "calcul de la note : F et G sont les épreuves spécifiques VTC"
    assert n["sources"] and all(x["url"].startswith("https://") for x in n["sources"]), "calcul de la note : source sans adresse"
    # recoupement avec le texte officiel de l'arrêté, recopié de Légifrance dans le wiki et comparé chaque semaine à la version en vigueur :
    # si l'arrêté change, le générateur s'arrête ici tant que le barème n'est pas mis à jour
    arr = [a for a in lire_wiki()["articles"] if a["slug"] == "arrete-6-avril-2017-examen"][0]
    art2 = " ".join([p for p in arr["articles"] if p["num"] == "Article 2"][0]["texte"]).replace("\u2019", "'")
    chiffres = {1: "un", 2: "deux", 3: "trois", 20: "vingt", 30: "trente", 45: "quarante-cinq"}
    marques = {"A": "A. - Une épreuve portant sur la réglementation du transport public particulier", "B": "B. - Une épreuve portant sur la gestion",
               "C": "C. - Une épreuve portant sur la sécurité routière", "D": "D. - Une épreuve destinée à évaluer la capacité d'expression et de compréhension en langue française",
               "E": "E. - Une épreuve destinée à évaluer la capacité d'expression et de compréhension en langue anglaise", "F": 'A. - Une épreuve " F (V) "', "G": 'B. - Une épreuve " G (V) "'}
    for e in eps:
        i = art2.index(marques[e["code"]])
        bout = art2[i:i + 400]
        assert f'{chiffres[e["duree"]]} minutes' in bout and f'coefficient {chiffres[e["coef"]]}.' in bout, \
            f"calcul de la note : durée ou coefficient de l'épreuve {e['code']} différent du texte de l'arrêté (wiki)"
    for phrase in ("une note moyenne d'au moins dix sur vingt", "une note d'au moins six sur vingt à chacune des épreuves A, B, C, D, F et G",
                   "une note d'au moins quatre sur vingt à l'épreuve E", "trois fois à l'épreuve d'admission dans un délai d'un an"):
        assert phrase in art2, f"calcul de la note : « {phrase} » absent du texte de l'arrêté (wiki)"
    art3 = " ".join([p for p in arr["articles"] if p["num"] == "Article 3"][0]["texte"]).replace("\u2019", "'")
    assert "au moins douze sur vingt à l'épreuve pratique" in art3 and n["note_pratique"] == 12, "calcul de la note : note de l'épreuve pratique"
    return n


def calcul_note_ex(n, notes):
    """Même calcul que docs/js/calcul-note.js (vérifié par outils/test_calcul_note.js), en centièmes entiers."""
    pts = sum(round(notes[e["code"]] * 100) * e["coef"] for e in n["epreuves"])
    elim = [e["code"] for e in n["epreuves"] if round(notes[e["code"]] * 100) < e["elim"] * 100]
    return {"points": pts / 100, "moyenne": (pts // 17) / 100, "elimines": elim,
            "admissible": pts >= n["moyenne_requise"] * 1700 and not elim}


def calcul_note():
    n = lire_calcul_note()
    eps = n["epreuves"]
    compteur = getattr(_bloc_dossier, "n", 0)   # identifiants de tableaux propres à cette page : ne décale pas ceux des autres pages
    num = lambda x: (f"{x:.2f}".rstrip("0").rstrip(".")).replace(".", ",")
    src = " · ".join(f'<a href="#source-{x["id"]}">{ty(x["nom"].split(",")[0])}</a>' for x in n["sources"])

    def champ(e):
        attr = ' data-commune=""' if e["commune"] else ""
        aide = f'Coefficient {e["coef"]} · éliminatoire sous {e["elim"]} / 20 · {e["duree"]} min'
        return (f'<div class="champ"{attr}><label for="note-{e["code"]}">{e["code"]} · {ty(e["court"])} <span class="unite">(sur 20)</span></label>'
                f'<p class="aide" id="aide-note-{e["code"]}">{ty(aide)}</p>'
                f'<input type="text" inputmode="decimal" autocomplete="off" id="note-{e["code"]}" name="note-{e["code"]}" value="" '
                f'aria-describedby="aide-note-{e["code"]} err-note-{e["code"]}"><p class="erreur" id="err-note-{e["code"]}"></p></div>')

    formulaire = f'''
    <form id="note" class="simu" novalidate hidden aria-describedby="note-intro">
      <p class="aide" id="note-intro">{ty("Saisissez les notes que vous avez, ou celles que vous visez, par exemple 12 ou 12,5. Laissez vide une épreuve pas encore passée : le calculateur vous dit ce qu'il vous faut. Rien n'est envoyé.")} <a class="lien-resultat" href="#resultat">{ty("Aller au résultat")}</a></p>
      <fieldset class="bloc-simu"><legend>1. Votre situation</legend>
        <fieldset class="groupe"><legend>{ty("Quelles épreuves passez-vous ?")}</legend>
          <div class="choix">
            <label><input type="radio" name="mode" value="complet" checked><span>{ty("Les sept épreuves écrites, de A à G (cas général)")}</span></label>
            <label><input type="radio" name="mode" value="passerelle"><span>{ty("Seulement F et G : j'ai été déclaré admissible à l'examen de taxi il y a moins de 3 ans")}</span></label>
          </div></fieldset>
      </fieldset>
      <fieldset class="bloc-simu"><legend>2. Vos notes</legend>
        {"".join(champ(e) for e in eps)}
      </fieldset>
      <div class="actions"><button type="submit" class="bouton">Voir le résultat</button><button type="button" class="bouton second" id="note-raz">Effacer les notes</button></div>
    </form>
    <p class="note" id="note-sans-js">{ty("Le calculateur a besoin de JavaScript. Sans lui, faites le calcul à la main avec le barème ci-dessous : multipliez chaque note par son coefficient, additionnez, il faut 170 points sur 340 et aucune note éliminatoire.")}</p>'''

    resultat = f'''
    <section class="cote-bloc resultat-simu" id="resultat" tabindex="-1" aria-labelledby="titre-resultat" hidden>
      <h2 id="titre-resultat">Votre résultat</h2>
      <p class="resultat" id="res-verdict"></p>
      <p class="meta" id="res-moyenne"></p>
      <p id="res-explication"></p>
      <p class="meta"><a href="#detail-resultat">{ty("Le détail par épreuve")}</a></p>
      <p class="visuellement-cache" id="note-annonce" aria-live="polite"></p>
    </section>
    <aside class="barre-resultat cachee" id="barre-resultat" aria-label="Résultat en bref" hidden>
      <p><span class="barre-legende">Votre résultat</span> <b id="barre-res-verdict"></b></p>
      <a class="bouton clair petit" href="#resultat">Voir le détail</a>
    </aside>'''

    # détail : sous le formulaire, dans la colonne principale (le panneau collant ne garde que l'essentiel)
    detail = f'''
    <section class="col-detail" id="detail-resultat" aria-labelledby="titre-detail" hidden>
      <h2 id="titre-detail">{ty("Le détail de votre résultat")}</h2>
      <div class="note" id="res-conseil" hidden></div>
      <div class="defile" tabindex="0" role="region" aria-labelledby="cap-detail"><table><caption id="cap-detail">Le détail par épreuve (seuil éliminatoire : OK ou raté)</caption>
        <thead><tr><th scope="col">Épreuve</th><th scope="col" class="nombre">Note</th><th scope="col" class="nombre">Coef.</th><th scope="col" class="nombre">Points</th><th scope="col">Seuil</th></tr></thead>
        <tbody id="res-detail"></tbody></table></div>
    </section>'''

    bareme = {"tableau": {"legende": "Les sept épreuves d'admissibilité de l'examen VTC (arrêté du 6 avril 2017, article 2)",
                          "colonnes": ["Épreuve", "Durée", "Coef.", "Poids dans la moyenne", "Composition (sur 20 points)", "Éliminatoire sous"], "nombres": [1, 2, 3, 5],
                          "lignes": [[f'{e["code"]} · {e["titre"]}', f'{e["duree"]} min', str(e["coef"]), num(round(e["coef"] * 100 / 17, 1)) + " %", e["composition"], f'{e["elim"]} / 20'] for e in eps],
                          "total": [["Total", "3 h 50", "17", "100 % (arrondis)", "Moyenne pondérée : points ÷ 17", ""]]}}
    assert sum(e["duree"] for e in eps) == 230, "calcul de la note : durée totale 3 h 50"

    ex = n["exemples"]["admissible"]; a = calcul_note_ex(n, ex)
    assert a["admissible"], "l'exemple « admissible » doit l'être"
    tab_ex = {"tableau": {"legende": "Exemple : un candidat admissible avec une note faible en anglais", "colonnes": ["Épreuve", "Note", "Coef.", "Points"], "nombres": [1, 2, 3],
                          "lignes": [[f'{e["code"]} · {e["court"]}', num(ex[e["code"]]), str(e["coef"]), num(ex[e["code"]] * e["coef"])] for e in eps],
                          "total": [["Total", "", "17", num(a["points"])]]}}
    pg = n["exemples"]["piege"]; b = calcul_note_ex(n, pg)
    assert not b["admissible"] and b["elimines"] == ["E"], "l'exemple « piège » doit être éliminé en anglais seulement"
    sources = "".join(f'<li id="source-{x["id"]}"><a href="{html.escape(x["url"])}">{ty(x["nom"])}</a>, {ty(x["date"])}</li>' for x in n["sources"])
    faq = [("Quelle note faut-il pour réussir l'examen VTC ?",
            "Pour être admissible, il faut au moins 10 / 20 de moyenne pondérée sur les sept épreuves écrites, au moins 6 / 20 à chacune des épreuves A, B, C, D, F et G, et au moins 4 / 20 en anglais. Il faut ensuite au moins 12 / 20 à l'épreuve pratique pour être reçu."),
           ("Quelle est la note éliminatoire à l'examen VTC ?",
            "Une note sous 6 / 20 à l'une des épreuves A, B, C, D, F ou G, ou sous 4 / 20 à l'épreuve E (anglais), rend le candidat non admissible, quelle que soit sa moyenne."),
           ("Comment calculer sa moyenne à l'examen VTC ?",
            "Multipliez chaque note par son coefficient (A, C, F et G : 3 ; B et D : 2 ; E : 1), additionnez et divisez par 17. Il faut au moins 170 points sur 340, soit 10 / 20."),
           ("Combien de fois peut-on passer l'épreuve pratique ?",
            "Un candidat admissible peut se présenter trois fois à l'épreuve pratique, dans un délai d'un an à compter de la publication des résultats des épreuves écrites.")]
    faq_html = "".join(f"<h3>{ty(q)}</h3><p>{ty(r)}</p>" for q, r in faq)
    wiki_lien = '<a href="../wiki/arrete-6-avril-2017-examen.html">' + ty("le texte de l'arrêté, recopié de Légifrance et expliqué") + "</a>"

    corps = f'''    <nav class="fil" aria-label="Fil d'Ariane"><ol><li><a href="index.html">Simulateurs</a></li></ol></nav>
    <p class="surtitre">Outil gratuit</p>
    <h1>{ty("Calcul de la note de l'examen VTC : suis-je admissible ?")}</h1>
    <p class="chapeau">{ty("Entrez vos notes d'examen blanc : vous saurez si vous seriez admissible au barème officiel (coefficients et notes éliminatoires), pourquoi, et quelle épreuve travailler en priorité.")}</p>
    <p class="meta">{ty("Barème de l'arrêté du 6 avril 2017, vérifié le " + n["verifie"] + " sur Légifrance. Calcul fait dans votre navigateur : rien n'est envoyé.")}</p>
    <div class="deux-col"><div class="col-texte">
    {formulaire}
    </div>
    <aside class="col-cote" aria-label="Résultat du calcul">{resultat}
    </aside>{detail}</div>
    <!-- mode d'emploi et exemple : après le formulaire et le résultat (audit visuel, lot 2) -->
    <section aria-labelledby="mode-emploi">
      <h2 id="mode-emploi">{ty("Comment s'en servir")}</h2>
      <ol class="etapes">
        <li><b>{ty("Faites un examen blanc")}</b>{ty("Un des trois examens blancs du livre ou un des deux examens blancs de ce site. Notez votre note sur 20 à chaque épreuve.")}</li>
        <li><b>{ty("Entrez vos notes")}</b>{ty("Toutes, ou seulement celles que vous avez : une épreuve laissée vide est une épreuve à venir. Le calculateur vous dit alors ce qu'il vous faudra à celles qui restent.")}</li>
        <li><b>{ty("Lisez le verdict et le conseil")}</b>{ty("Admissible ou non, avec la raison ; la note éliminatoire à rattraper en priorité ; l'épreuve où chaque point compte le plus ; les notes trop proches du seuil, qui peuvent vous faire tomber le jour de l'examen.")}</li>
      </ol>
      <p>{ty("Refaites le calcul après chaque examen blanc : vous voyez votre progression épreuve par épreuve, et vous savez où mettre vos heures de révision.")}</p>
    </section>
    <section class="en-clair" aria-labelledby="en-bref">
      <h2 id="en-bref">La règle en bref</h2>
      <p>{ty("Vous êtes admissible si vous remplissez les trois conditions en même temps :")}</p>
      <ul>
        <li>{ty("au moins 10 / 20 de moyenne sur les sept épreuves, chaque note étant multipliée par son coefficient, soit au moins 170 points sur 340 ;")}</li>
        <li>{ty("au moins 6 / 20 aux épreuves A, B, C, D, F et G ;")}</li>
        <li>{ty("au moins 4 / 20 à l'épreuve E, l'anglais.")}</li>
      </ul>
      <p>{ty("Une seule note sous le seuil suffit à être recalé, même avec 15 de moyenne. Les épreuves A, C, F et G comptent triple : à elles quatre, elles pèsent 12 coefficients sur 17.")}</p>
    </section>
    <h2 id="bareme">{ty("Le barème officiel des sept épreuves")}</h2>
    <p>{ty("Les épreuves A à E sont communes aux examens de taxi et de VTC ; F et G sont propres au VTC. Toutes sont notées sur 20, avec des questions à choix multiples (QCM) et des questions à réponse courte (QRC).")}</p>
    {_graphique({"donnees": "bareme-examen", "titre": "Le poids de chaque épreuve dans la moyenne",
                  "lecture": "Un point gagné dans une épreuve de coefficient 3 vaut trois points gagnés en anglais ; une seule note sous le seuil éliminatoire suffit pourtant à échouer.",
                  "source": "Arrêté du 6 avril 2017, article 2 (Légifrance) ; poids dans la moyenne : notre calcul", "tableau": bareme["tableau"]})}
    <p>{ty("Lecture : un point gagné en réglementation, en sécurité routière, en développement commercial ou en réglementation VTC (coefficient 3) vaut trois points gagnés en anglais (coefficient 1). À elles quatre, ces épreuves font 70,6 % de la moyenne.")}</p>
    <h2 id="exemples">{ty("Deux exemples pour comprendre")}</h2>
    <p>{ty(f"Premier exemple : ce candidat n'a que {num(ex['E'])} / 20 en anglais et {num(ex['F'])} / 20 en développement commercial, mais il totalise {num(a['points'])} points, soit {num(a['moyenne'])} de moyenne, sans aucune note sous le seuil. Il est admissible.")}</p>
    {_bloc_dossier(tab_ex)}
    <p>{ty(f"Second exemple : un candidat a de très bonnes notes partout ({num(pg['A'])} en A, {num(pg['C'])} en C, {num(pg['G'])} en G), soit {num(b['moyenne'])} de moyenne, mais seulement {num(pg['E'])} / 20 en anglais. Cette note est sous le seuil de 4 : il n'est pas admissible. Ne négligez aucune épreuve, surtout celles qui vous semblent faciles.")}</p>
    <h2 id="pratique">{ty("Après l'admissibilité : l'épreuve pratique")}</h2>
    <p>{ty("Une fois admissible, vous passez l'épreuve pratique : une mission de transport en VTC réalisée en situation réelle, avec au moins 20 minutes de conduite en circulation. Il faut au moins 12 / 20 pour être reçu. Elle est notée en quatre parties : préparation et réalisation du parcours (3 points) ; sécurité et souplesse de la conduite et respect du code de la route (10 points) ; prise en charge, relation client et informations touristiques (5 points) ; facturation (2 points). Si l'examinateur doit intervenir sur la double commande ou le volant, l'épreuve s'arrête et le candidat est ajourné.")}</p>
    <p>{ty("Vous pouvez vous présenter trois fois à l'épreuve pratique, dans un délai d'un an à compter de la publication des résultats des épreuves écrites.")}</p>
    <h2 id="limites">{ty("Ce que le calculateur ne fait pas")}</h2>
    <ul>
      <li>{ty("Il ne corrige pas vos copies : il calcule à partir des notes que vous saisissez. Pour vous entraîner, les examens blancs corrigés donnent une note par épreuve.")}</li>
      <li>{ty("En français (épreuve D), un point est retiré au-delà de cinq fautes d'orthographe dans les réponses rédigées : saisissez la note après ce retrait.")}</li>
      <li>{ty("Il ne traite que la dispense prévue pour les candidats déjà admissibles à l'examen de taxi depuis moins de 3 ans. Pour toute autre dispense, renseignez-vous auprès de votre chambre de métiers et de l'artisanat (CMA).")}</li>
      <li>{ty("Seuls les résultats publiés par la CMA font foi.")}</li>
    </ul>
    <p>{ty("Pour lire la règle à la source :")} {wiki_lien}. {ty("Dans le livre")} <i>Machine à Réussite</i>, {ty("la fiche A2.4 explique l'examen, et les trois examens blancs du livre, comme les")} <a href="../examens.html">{ty("deux examens blancs de ce site")}</a>, {ty("sont notés selon ce barème.")}</p>
    <h2 id="questions">{ty("Questions fréquentes sur la note de l'examen VTC")}</h2>
    {faq_html}
    <h2 id="sources">Sources</h2>
    <ul class="source">{sources}</ul>
    <p class="source">{ty("Outil indicatif, gratuit et indépendant, sans lien avec les chambres de métiers et de l'artisanat qui organisent l'examen. Le barème est recoupé à chaque mise à jour du site avec le texte de l'arrêté, que le site compare chaque semaine à la version en vigueur sur Légifrance.")}</p>'''

    donnees = json.dumps({k: n[k] for k in ("moyenne_requise", "note_pratique", "epreuves")}, ensure_ascii=False).replace("</", "<\\/")
    fin = f'<script id="note-donnees" type="application/json">{donnees}</script>\n<script src="../js/calcul-note.js"></script>\n'
    chemin = f'simulateurs/{n["slug"]}.html'
    titre = "Calcul de la note de l'examen VTC : suis-je admissible ?"
    desc = "Calcul de la note de l'examen VTC : moyenne pondérée sur 17, notes éliminatoires (6/20, 4/20 en anglais), ce qu'il vous manque. Barème officiel en vigueur."
    ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": titre, "url": SITE + chemin, "description": desc,
          "applicationCategory": "EducationalApplication", "operatingSystem": "Navigateur web", "inLanguage": "fr", "isAccessibleForFree": True,
          "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "author": AUTEUR, "publisher": AUTEUR,
          "datePublished": n["date"], "dateModified": iso_fr(n["verifie"]), "isPartOf": {"@id": SITE + "#site"},
          "isBasedOn": [x["url"] for x in n["sources"]]}
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in faq]}
    ecrire(chemin, page(html.escape(titre + " · Révision VTC", quote=False), corps, "simulateurs", "../", html.escape(desc),
                        scripts_fin=fin, jsonld=[ld, ld_faq, fil(("Accueil", ""), ("Simulateurs", "simulateurs/"), (titre, chemin))]))
    n["titre"] = titre
    _bloc_dossier.n = compteur
    return n


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
      <li><a href="wiki/index.html">{ty("Les textes réglementaires")}</a> {ty(": chaque article utile du Code des transports et chaque arrêté, avec le texte officiel en vigueur, une explication en clair et un exemple concret.")}</li>
      <li><a href="actualite/index.html">{ty("L'Actualité VTC")}</a> {ty(": régulièrement, ce qui change pour les chauffeurs et les candidats, avec ses sources.")}</li>
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
    <ul class="essentiel-liens">
      <li><a href="/wiki/index.html">{ty("La réglementation VTC, article par article")}</a></li>
      <li><a href="/actualite/index.html">{ty("L'Actualité VTC")}</a></li>
      <li><a href="/examens.html">{ty("Les examens blancs")}</a></li>
      <li><a href="/index.html">{ty("L'accueil du site")}</a></li>
    </ul>'''
    ecrire("404.html", page("Page introuvable · Révision VTC", corps, None, "/", noindex=True))


ROBOTS_IA = ["Googlebot", "Bingbot", "Google-Extended", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
             "Claude-User", "PerplexityBot", "Perplexity-User", "Applebot", "Applebot-Extended", "DuckAssistBot", "MistralAI-User", "CCBot"]


def plan(nums, arts, wiki_date, qs=(), ds=(), simu=None, note=None, fs=()):
    der = nums[0]["date"] if nums else wiki_date
    urls = [("", max(der, wiki_date)), ("actualite/", der), ("wiki/", wiki_date), ("a-propos.html", None), ("contact.html", None), ("le-livre.html", None), ("mises-a-jour.html", None),
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
    if simu:
        urls.insert(5, ("simulateurs/", iso_fr(simu["verifie"])))
        urls.append((f'simulateurs/{simu["slug"]}.html', iso_fr(simu["verifie"])))
    if note:
        urls.append((f'simulateurs/{note["slug"]}.html', iso_fr(note["verifie"])))
    if fs:
        urls.insert(6, ("qcm/", None))
        urls += [(f'qcm/{f["url"]}.html', None) for f in fs]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "".join(f"  <url><loc>{SITE}{u}</loc>" + (f"<lastmod>{d}</lastmod>" if d else "") + "</url>\n" for u, d in urls) + "</urlset>\n"
    ecrire("sitemap.xml", xml)
    # les moteurs de recherche et les assistants d'IA sont explicitement les bienvenus (référencement et citations)
    ecrire("robots.txt", "".join(f"User-agent: {r}\n" for r in ROBOTS_IA) + "Allow: /\nDisallow: /examen.html\n\n"
           f"User-agent: *\nAllow: /\nDisallow: /examen.html\n\nSitemap: {SITE}sitemap.xml\n")


def llms(nums, w, qs=(), ds=(), simu=None):
    """llms.txt : le plan du site pour les assistants d'IA ; llms-full.txt : tout le wiki en texte brut, avec ses sources."""
    themes = {t["cle"]: t["titre"] for t in w["themes"]}
    l = ["# Révision VTC (revision-vtc.fr)", "",
         "> Site gratuit et indépendant sur le métier de chauffeur VTC en France et l'examen d'accès à la profession : "
         "la réglementation VTC expliquée article par article (texte officiel Légifrance en vigueur + explication en clair), "
         "l'actualité du métier, régulièrement, avec ses sources, et des examens blancs. Tenu par Benjamin Blondin, auteur du livre "
         "« Machine à Réussite · Examen VTC 2027 » (ISBN 979-8-1652-8079-5).", "",
         f"Règles éditoriales : chaque information repose sur un texte officiel ou sur deux sources concordantes, toujours citées. "
         f"Les textes du wiki sont comparés chaque semaine à la version en vigueur sur Légifrance (dernière vérification : {w['verifie']}). "
         "Seule la version publiée sur Légifrance fait foi.", "",
         "## Pages principales", "",
         f"- [Réglementation VTC, les textes officiels expliqués]({SITE}wiki/): index de tous les articles par thème",
         f"- [Actualité VTC]({SITE}actualite/): un numéro par semaine, sources citées",
         f"- [FAQ VTC]({SITE}questions/): les questions concrètes des chauffeurs et des candidats, réponse courte et sources officielles",
         f"- [Guides VTC]({SITE}dossiers/): guides de fond chiffrés (coût du lancement, revenus, statut, véhicule), sources datées",
         f"- [Simulateur VTC : coût de revient de la voiture et revenu net]({SITE}simulateurs/cout-revient-revenu-net-vtc.html): calcul gratuit pour un chauffeur VTC en micro-entreprise (commission, cotisations, location ou achat, carburant, assurance), hypothèses sourcées et datées",
         f"- [Calcul de la note de l'examen VTC]({SITE}simulateurs/calcul-note-examen-vtc.html): admissibilité selon l'arrêté du 6 avril 2017 (moyenne pondérée sur 17 coefficients, au moins 10/20, notes éliminatoires sous 6/20 et sous 4/20 en anglais), et ce qu'il manque aux épreuves restantes",
         f"- [QCM VTC]({SITE}qcm/): fiches d'entraînement gratuites tirées du livre, classées par épreuve (A à G) : situation, QCM, réponse à rédiger, corrigé sourcé",
         f"- [Mises à jour du livre]({SITE}mises-a-jour.html): règles qui ont changé depuis l'impression",
         f"- [Examens blancs]({SITE}examens.html): deux examens blancs corrigés, réservés aux lecteurs du livre",
         f"- [À propos et méthode]({SITE}a-propos.html): qui écrit, comment les informations sont vérifiées",
         f"- [Texte intégral du wiki]({SITE}llms-full.txt): toutes les explications et tous les textes officiels en texte brut", ""]
    for t in w["themes"]:
        l += [f"## {t['titre']}", ""]
        l += [f"- [{a['num'] if not a.get('arrete') else 'Arrêté'} · {a['titre']}]({SITE}wiki/{a['slug']}.html): {a['en_clair']}" for a in w["articles"] if a["theme"] == t["cle"]]
        l.append("")
    if ds:
        l += ["## Guides VTC", ""]
        l += [f"- [{d['titre']}]({SITE}dossiers/{d['slug']}.html): {' '.join(d['en_bref'])}" for d in ds]
        l.append("")
    if FICHES:
        l += ["## QCM VTC (fiches d'entraînement)", ""]
        l += [f"- [{f['titre_page']}]({SITE}qcm/{f['url']}.html): {f['retenir']}" for f in FICHES]
        l.append("")
    if qs:
        l += ["## FAQ VTC", ""]
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
        f += ["## Guides VTC", ""]
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
    FICHES[:] = lire_fiches()
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
    note = calcul_note()
    simu = simulateur(ds, note)
    indexnow()
    mises_a_jour()
    fs = FICHES
    qcm(fs)
    livre_vivant()
    examens()
    legales()
    a_propos()
    contact()
    page_404()
    llms(nums, w, qs, [d for d in ds if not d.get("brouillon")], simu)
    plan(nums, arts, iso_fr(w["verifie"]), qs, [d for d in ds if not d.get("brouillon")], simu, note, fs)
    print(f"Site généré dans docs/ : {len(nums)} numéro(s) de l'Actualité VTC.")
