# -*- coding: utf-8 -*-
"""Signale à IndexNow (Bing, Yandex, Seznam, Naver…) les pages ajoutées ou modifiées par une publication.

Lancé par GitHub Actions (.github/workflows/indexnow.yml) après chaque mise à jour de main :
  AVANT, APRES : identifiants des commits avant et après la publication
  python3 outils/indexnow.py            -> pages HTML de docs/ modifiées entre AVANT et APRES
  python3 outils/indexnow.py --tout     -> toutes les adresses du sitemap (premier envoi)
  python3 outils/indexnow.py --essai    -> affiche la liste sans rien envoyer
Les pages non indexables (noindex, redirections, 404) ne sont jamais envoyées.
"""
import json, os, re, subprocess, sys, urllib.request

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(RACINE, "docs")
HOTE = "revision-vtc.fr"
SITE = f"https://{HOTE}/"
EXCLUS = {"404.html", "examen.html", "textes.html"}

with open(os.path.join(RACINE, "contenu", "indexnow.json"), encoding="utf-8") as h:
    CLE = json.load(h)["cle"]


def indexable(chemin):
    if chemin in EXCLUS or not os.path.exists(os.path.join(DOCS, chemin)):
        return False
    with open(os.path.join(DOCS, chemin), encoding="utf-8") as h:
        t = h.read(6000)
    return 'content="noindex"' not in t and 'http-equiv="refresh"' not in t


def adresse(chemin):
    return SITE + (chemin[:-10] if chemin.endswith("index.html") else chemin)


def modifiees(avant, apres):
    if not avant or set(avant) == {"0"}:
        return None
    sortie = subprocess.run(["git", "diff", "--name-only", "--diff-filter=AM", avant, apres, "--", "docs/"],
                            cwd=RACINE, capture_output=True, text=True, check=True).stdout
    return [l[5:] for l in sortie.splitlines() if l.endswith(".html")]


def toutes():
    with open(os.path.join(DOCS, "sitemap.xml"), encoding="utf-8") as h:
        return re.findall(r"<loc>(.*?)</loc>", h.read())


def attendre_publication(chemin, minutes=15):
    """Attend que GitHub Pages serve la nouvelle version de la page, pour que Bing la lise à jour."""
    import time
    with open(os.path.join(DOCS, chemin), "rb") as h:
        attendu = h.read()
    for _ in range(minutes * 4):
        try:
            with urllib.request.urlopen(adresse(chemin) + f"?v={int(time.time())}", timeout=20) as r:
                if r.read() == attendu:
                    print("Nouvelle version en ligne :", adresse(chemin))
                    return True
        except Exception:
            pass
        time.sleep(15)
    print("La nouvelle version n'est pas encore en ligne : envoi quand même.")
    return False


def main():
    chemins = None
    if "--tout" in sys.argv:
        urls = toutes()
    else:
        chemins = modifiees(os.environ.get("AVANT", ""), os.environ.get("APRES", "HEAD"))
        urls = toutes() if chemins is None else [adresse(c) for c in chemins if indexable(c)]
    if "--attendre" in sys.argv and chemins and "--essai" not in sys.argv:
        attendre_publication(next((c for c in chemins if indexable(c)), chemins[0]))
    # l'en-tête et le menu étant communs, une petite modification touche toutes les pages :
    # on garde l'ordre (pages de contenu d'abord) et la limite du protocole (10 000 adresses).
    urls = sorted(set(urls), key=lambda u: (u.endswith("/"), u))[:10000]
    print(f"{len(urls)} adresse(s) à signaler")
    for u in urls[:30]:
        print(" ", u)
    if not urls or "--essai" in sys.argv:
        return
    corps = json.dumps({"host": HOTE, "key": CLE, "keyLocation": f"{SITE}{CLE}.txt", "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=corps, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("IndexNow :", r.status, "(200 ou 202 : reçu)")
    except urllib.error.HTTPError as e:
        # 403 : clé introuvable sur le site ; 422 : adresse hors du site ; 429 : trop d'envois
        print("IndexNow a refusé l'envoi :", e.code, e.read()[:300])
        sys.exit(1)


if __name__ == "__main__":
    main()
