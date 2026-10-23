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


def date_fr(iso):
    d = datetime.date.fromisoformat(iso)
    j = "1er" if d.day == 1 else str(d.day)
    return f"{j} {MOIS[d.month - 1]} {d.year}"


def ecrire(chemin, contenu):
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
def accueil(nums):
    dernier = ""
    if nums:
        n = nums[0]
        pts = "".join(f"<li>{ty(x)}</li>" for x in n["a_retenir"])
        dernier = f'''
    <section class="bloc doux" aria-labelledby="titre-dernier">
      <div class="page">
        <p class="surtitre">Actualité VTC · n° {n["numero"]} · {date_fr(n["date"])}</p>
        <h2 id="titre-dernier" class="sans-filet"><a href="actualite/{n["date"]}.html">{ty(n["titre"])}</a></h2>
        <ul class="points">{pts}</ul>
        <p><a class="lien-fleche" href="actualite/index.html">Tous les numéros</a></p>
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
        <h2 id="titre-rubriques" class="visuellement-cache">Les rubriques du site</h2>
        <ul class="trois">
          <li><p class="surtitre">Chaque semaine</p><h3><a href="actualite/index.html">Actualité VTC</a></h3><p>{ty("Textes officiels, examen, plateformes, cotisations : ce qui change pour vous, toujours avec ses sources.")}</p></li>
          <li><p class="surtitre">L'essentiel du droit</p><h3><a href="textes.html">Textes du métier</a></h3><p>{ty("Les lois, décrets et arrêtés qui encadrent le VTC, avec le lien vers leur version en vigueur.")}</p></li>
          <li><p class="surtitre">Après l'impression</p><h3><a href="mises-a-jour.html">Mises à jour du livre</a></h3><p>{ty("Chaque règle qui change, avec sa date, la fiche concernée et le texte qui la fonde.")}</p></li>
          <li><p class="surtitre">Réservé aux lecteurs</p><h3><a href="examens.html">Examens blancs n° 4 et 5</a></h3><p>{ty("À l'écran, chronométrés et corrigés, ou à imprimer.")}</p></li>
        </ul>
      </div>
    </section>{dernier}'''
    ecrire("index.html", page("Révision VTC · Le site du livre Machine à Réussite", corps, "accueil", "",
                              "Le site du livre Machine à Réussite · Examen VTC 2027 : actualité VTC chaque semaine, mises à jour du livre et examens blancs en ligne.", brut=True))


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
    corps = f'''    <p class="surtitre">Actualité VTC · n° {n["numero"]}</p>
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
    ecrire(f'actualite/{n["date"]}.html', page(html.escape(titre), corps, "actualite", "../",
                                               html.escape(" ".join(n["a_retenir"])[:300])))


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
    ecrire("actualite/index.html", page("Actualité VTC · Révision VTC", corps, "actualite", "../",
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


# ------------------------------------------------------------------ textes du métier
def textes():
    with open(os.path.join(CONTENU, "textes.json"), encoding="utf-8") as h:
        d = json.load(h)
    sommaire, groupes = [], []
    for i, g in enumerate(d["groupes"], 1):
        ident = f"groupe-{i}"
        sommaire.append(f'<li><a href="#{ident}">{ty(g["titre"])}</a></li>')
        items = "".join(
            f'''<li class="texte">
          <h3><a href="{html.escape(x["url"])}">{ty(x["nom"])}</a></h3>
          <p class="texte-ref">{ty(x["ref"])}</p>
          <p>{ty(x["objet"])}</p>
          <p class="texte-fiches">Dans le livre : {ty(x["fiches"])}</p>
        </li>''' for x in g["textes"])
        intro = f'<p>{ty(g["intro"])}</p>' if g.get("intro") else ""
        groupes.append(f'''<section aria-labelledby="{ident}">
      <h2 id="{ident}">{ty(g["titre"])}</h2>
      {intro}
      <ul class="textes">{items}</ul>
    </section>''')
    corps = f'''    <h1>Textes du métier</h1>
    <p class="chapeau">{ty("L'essentiel des textes qui encadrent le métier de conducteur VTC. Chaque lien mène à la version officielle, sur Légifrance ou EUR-Lex : c'est elle qui fait foi.")}</p>
    <nav class="sommaire" aria-label="Sur cette page"><ul>{"".join(sommaire)}</ul></nav>
    {"".join(groupes)}
    <p class="meta">{ty("Liste vérifiée le " + d["verifie"] + ". Les changements sont annoncés dans l'Actualité VTC et, quand ils touchent une règle du livre, dans les mises à jour du livre.")}</p>'''
    ecrire("textes.html", page("Textes du métier · Révision VTC", corps, "textes", "",
                               "Les lois, décrets et arrêtés qui encadrent le métier de conducteur VTC, avec le lien vers leur version officielle."))


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
    corps = f'''    <h1>Mentions légales</h1>
    <h2>Éditeur du site</h2>
    <p>{ty("Ce site gratuit est édité à titre non professionnel par l'auteur du livre Machine à Réussite · Examen VTC 2027. Conformément à l'article 6, III, 2 de la loi n° 2004-575 du 21 juin 2004 pour la confiance dans l'économie numérique, l'éditeur a choisi de rester anonyme : ses coordonnées ont été communiquées à l'hébergeur.")}</p>
    <p>Contact : <a href="mailto:benjamin@revision-vtc.fr">benjamin@revision-vtc.fr</a></p>
    <h2>Hébergement</h2>
    <p>GitHub, Inc. (service GitHub Pages), 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis. Téléphone : +1 877 448 4820.</p>
    <h2>Données personnelles</h2>
    <p>{ty("Ce site ne dépose aucun cookie de mesure d'audience ni de publicité et ne collecte aucune donnée personnelle. Vos réponses aux examens blancs sont enregistrées uniquement dans votre navigateur, pour que vous puissiez reprendre là où vous en étiez : elles ne sont jamais envoyées. Vous pouvez les effacer depuis l'examen (« Effacer mes réponses ») ou en vidant les données du site dans votre navigateur.")}</p>
    <p>{ty("Les polices de caractères sont hébergées sur ce site : aucune requête n'est faite à un service tiers. L'hébergeur peut conserver des journaux techniques de connexion (adresse IP) pour la sécurité du service.")}</p>
    <h2>Propriété intellectuelle</h2>
    <p>{ty("Les textes, questions et corrigés de ce site sont la propriété de Benjamin Blondin. Toute reproduction sans autorisation est interdite (Code de la propriété intellectuelle, art. L122-4). Les brèves de l'Actualité VTC citent leurs sources, qui restent la propriété de leurs auteurs.")}</p>
    <h2>Avertissement</h2>
    <p>{ty("Ce site et le livre sont des ouvrages indépendants : ils ne sont édités ni par les chambres de métiers et de l'artisanat ni par l'État. Ils préparent à l'examen et ne remplacent pas un conseil juridique, comptable ou fiscal adapté à votre situation.")}</p>'''
    ecrire("mentions-legales.html", page("Mentions légales · Révision VTC", corps, None, ""))
    corps = f'''    <h1>Accessibilité</h1>
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
    ecrire("accessibilite.html", page("Accessibilité · Révision VTC", corps, None, ""))


def plan(nums):
    urls = ["", "actualite/index.html", "textes.html", "mises-a-jour.html", "examens.html", "mentions-legales.html", "accessibilite.html"]
    urls += [f'actualite/{n["date"]}.html' for n in nums]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    ecrire("sitemap.xml", xml)
    ecrire("robots.txt", f"User-agent: *\nDisallow: /examen.html\nSitemap: {SITE}sitemap.xml\n")


if __name__ == "__main__":
    nums = lire_numeros()
    accueil(nums)
    for i, n in enumerate(nums):
        numero(n, nums[i + 1] if i + 1 < len(nums) else None, nums[i - 1] if i > 0 else None)
    actualite(nums)
    flux(nums)
    textes()
    mises_a_jour()
    examens()
    legales()
    plan(nums)
    print(f"Site généré dans docs/ : {len(nums)} numéro(s) de l'Actualité VTC.")
