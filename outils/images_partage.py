# -*- coding: utf-8 -*-
"""Images de partage (Open Graph) : une image 1200 × 630 par page, aux couleurs du site.

C'est l'image qui s'affiche quand un lien du site est partagé (WhatsApp, Facebook, LinkedIn, X…).
Le script lit les pages déjà générées dans docs/ (rubrique, surtitre, titre, numéro d'article ou épreuve)
et dessine l'image avec Pillow : aucune image générée par IA, seulement du texte, les pictogrammes
d'épreuve du site et la couverture du livre.

    python3 outils/generer.py            # le site
    python3 outils/images_partage.py     # les images qui manquent ou dont le titre a changé
    python3 outils/generer.py            # relie chaque page à son image (og:image)

Le générateur du site n'a pas besoin de Pillow : il utilise l'image d'une page si elle existe, l'image
générique docs/partage.jpg sinon. Les guides gardent leur photo.
Option : --exemples DOSSIER  écrit seulement 5 images d'essai dans DOSSIER, sans toucher au site.
"""
import glob, hashlib, html, json, os, re, sys
from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ICI, "..", "docs")
SORTIE = os.path.join(DOCS, "images", "partage")
VERSION = "1"   # à changer si le dessin change : toutes les images sont alors refaites

# couleurs de la charte (site.css, :root)
NUIT, NUIT2, JAUNE, BLANC, DOUX_NUIT, ROUGE = "#18212F", "#243042", "#EDB321", "#FFFFFF", "#C9D1DC", "#C9361B"
L, H, MARGE = 1200, 630, 72


def police(nom, taille):
    return ImageFont.truetype(os.path.join(ICI, "partage", nom + ".ttf"), taille)


COND7 = lambda t: police("barlow-condensed-latin-700-normal", t)
COND6 = lambda t: police("barlow-condensed-latin-600-normal", t)
SANS6 = lambda t: police("barlow-latin-600-normal", t)


def texte_brut(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).replace(" ", " ").replace(" ", " ").strip()


def lire_page(chemin):
    """Rubrique, surtitre, titre, numéro d'article, épreuve : lus dans la page générée."""
    with open(os.path.join(DOCS, chemin), encoding="utf-8") as h:
        p = h.read()
    if 'property="og:image" content="https://revision-vtc.fr/images/dossiers/' in p:
        return None   # guide : il garde sa photo
    m = re.search(r"<h1[^>]*>(.*?)</h1>", p, re.S)
    if not m:
        return None
    h1 = m.group(1)
    art = re.search(r'<span class="num-art">(.*?)</span>', h1)
    titre = texte_brut(re.sub(r'<span class="num-art">.*?</span>', "", h1))
    fil = re.findall(r"<li><a [^>]*>(.*?)</a></li>", (re.search(r'<nav class="fil".*?</nav>', p, re.S) or re.search("", "")).group(0))
    rubrique = texte_brut(fil[1]) if len(fil) > 1 else ""
    sur = re.search(r'<p class="surtitre">(.*?)</p>', p, re.S)
    ep = re.search(r"Épreuve ([A-G])\s*:\s*([^.<]+)", p[m.end():m.end() + 1500])
    return {"rubrique": rubrique, "surtitre": texte_brut(sur.group(1)) if sur else "", "titre": titre,
            "article": texte_brut(art.group(1)) if art else "", "epreuve": (ep.group(1), texte_brut(ep.group(2))) if ep else None}


def lignes(draw, texte, fonte, largeur):
    mots, out, cour = texte.split(), [], ""
    for m in mots:
        essai = (cour + " " + m).strip()
        if draw.textlength(essai, font=fonte) <= largeur or not cour:
            cour = essai
        else:
            out.append(cour); cour = m
    return out + ([cour] if cour else [])


def titre_ajuste(draw, texte, largeur, hauteur_max):
    """Plus grande taille (76 à 44 px) qui tient en 4 lignes au plus dans la place disponible."""
    for t in range(76, 43, -2):
        f = COND7(t)
        ls = lignes(draw, texte, f, largeur)
        if len(ls) <= 4 and len(ls) * t * 1.08 <= hauteur_max:
            return f, ls, t
    f = COND7(44)
    ls = lignes(draw, texte, f, largeur)[:4]
    ls[-1] = ls[-1].rstrip(" ,;:") + "…"
    return f, ls, 44


def dessiner(info):
    im = Image.new("RGB", (L, H), NUIT)
    d = ImageDraw.Draw(im, "RGBA")
    # quadrillage « plan de ville », discret, comme les en-têtes de page
    for x in range(0, L, 56):
        d.line([(x, 0), (x, H)], fill=(255, 255, 255, 10))
    for y in range(0, H, 56):
        d.line([(0, y), (L, y)], fill=(255, 255, 255, 10))
    # marque du site
    d.rounded_rectangle([MARGE, 56, MARGE + 52, 108], 8, fill=ROUGE)
    d.text((MARGE + 26, 83), "R", font=COND7(40), fill=BLANC, anchor="mm")
    d.text((MARGE + 68, 82), "Révision VTC", font=SANS6(30), fill=BLANC, anchor="lm")
    # couverture du livre, à droite, avec un relief jaune foncé comme sur le site
    couv = Image.open(os.path.join(DOCS, "couverture.jpg")).convert("RGB")
    cw = 252; ch = round(couv.height * cw / couv.width)
    couv = couv.resize((cw, ch), Image.LANCZOS)
    cx, cy = L - MARGE - cw, (H - ch) // 2 - 6
    d.rectangle([cx + 8, cy + 8, cx + cw + 8, cy + ch + 8], fill="#B3850F")
    im.paste(couv, (cx, cy))
    d.text((cx + cw // 2, cy + ch + 34), "Le livre Examen VTC 2027", font=SANS6(22), fill=DOUX_NUIT, anchor="mm")
    largeur = cx - MARGE - 56
    # rubrique et repère (numéro d'article ou épreuve)
    y = 168
    # rubrique · surtitre, sans redite : « Actualité VTC n° 6 » seul, mais « Réglementation VTC · Code des transports »
    r, st = info["rubrique"], info["surtitre"]
    debut = lambda x: x.lower()[:4]
    rub = (st if (not r or (st and debut(st) == debut(r))) else (r + ("  ·  " + st if st else ""))).upper()
    d.text((MARGE, y), rub, font=COND6(28), fill=JAUNE, anchor="lt")
    y += 52
    if info["article"]:
        f = COND7(34)
        w = d.textlength(info["article"], font=f)
        d.rounded_rectangle([MARGE, y, MARGE + w + 28, y + 50], 6, fill=JAUNE)
        d.text((MARGE + 14, y + 25), info["article"], font=f, fill=NUIT, anchor="lm")
        y += 72
    elif info["epreuve"]:
        code, nom = info["epreuve"]
        d.rounded_rectangle([MARGE, y, MARGE + 50, y + 50], 6, fill=JAUNE)
        pic = Image.open(os.path.join(ICI, "partage", "pictos", code + ".png")).convert("RGBA").resize((34, 34), Image.LANCZOS)
        im.paste(pic, (MARGE + 8, y + 8), pic)
        d.text((MARGE + 66, y + 25), f"Épreuve {code} · {nom}", font=SANS6(26), fill=BLANC, anchor="lm")
        y += 72
    # titre
    bas = H - 120
    f, ls, t = titre_ajuste(d, info["titre"], largeur, bas - y)
    for i, l in enumerate(ls):
        d.text((MARGE, y + i * round(t * 1.08)), l, font=f, fill=BLANC, anchor="lt")
    # pied : adresse du site et trait jaune (la route)
    d.text((MARGE, H - 62), "revision-vtc.fr", font=SANS6(28), fill=JAUNE, anchor="ls")
    d.rectangle([0, H - 12, L, H], fill=JAUNE)
    return im


# image générique docs/partage.jpg : repli pour les pages qui n'ont pas encore la leur
GENERIQUE = {"rubrique": "", "surtitre": "Le site du livre Examen VTC 2027", "article": "", "epreuve": None,
             "titre": "Examen, réglementation et métier de chauffeur VTC, expliqués à partir des textes officiels"}


def cle(info):
    return hashlib.sha1((VERSION + json.dumps(info, ensure_ascii=False, sort_keys=True)).encode()).hexdigest()[:10]


def nom_image(chemin):
    return chemin[:-5].replace("/", "-") + ".jpg"


def pages():
    for f in sorted(glob.glob(os.path.join(DOCS, "**", "*.html"), recursive=True)):
        c = os.path.relpath(f, DOCS).replace(os.sep, "/")
        if c.startswith(("examens/", "google")) or c in ("404.html",):
            continue
        yield c


def main():
    if "--exemples" in sys.argv:
        dest = sys.argv[sys.argv.index("--exemples") + 1]
        os.makedirs(dest, exist_ok=True)
        for c in ["index.html", "wiki/l3120-2.html", "questions/2026-10-25-vtc-attente-gare-aeroport.html",
                  "simulateurs/cout-revient-revenu-net-vtc.html", "actualite/2026-11-09.html"]:
            dessiner(lire_page(c)).save(os.path.join(dest, nom_image(c)), quality=82, optimize=True, progressive=True, subsampling=2)
            print(os.path.join(dest, nom_image(c)))
        return
    os.makedirs(SORTIE, exist_ok=True)
    index_f = os.path.join(SORTIE, "index.json")
    index = json.load(open(index_f, encoding="utf-8")) if os.path.exists(index_f) else {}
    faites, gardees = 0, {}
    for c in pages():
        info = lire_page(c)
        if not info:
            continue
        k, n = cle(info), nom_image(c)
        if index.get(c) != k or not os.path.exists(os.path.join(SORTIE, n)):
            dessiner(info).save(os.path.join(SORTIE, n), quality=82, optimize=True, progressive=True, subsampling=2)
            faites += 1
        gardees[c] = k
    for n in os.listdir(SORTIE):   # images de pages qui n'en ont plus besoin
        if n.endswith(".jpg") and n not in {nom_image(c) for c in gardees if not c.startswith("_")}:
            os.remove(os.path.join(SORTIE, n))
    k = cle(GENERIQUE)
    if index.get("_generique") != k:
        dessiner(GENERIQUE).save(os.path.join(DOCS, "partage.jpg"), quality=82, optimize=True, progressive=True, subsampling=2)
        faites += 1
    gardees["_generique"] = k
    with open(index_f, "w", encoding="utf-8") as h:
        json.dump(gardees, h, ensure_ascii=False, indent=0, sort_keys=True)
    print(f"Images de partage : {faites} faite(s), {len(gardees)} au total.")


if __name__ == "__main__":
    main()
