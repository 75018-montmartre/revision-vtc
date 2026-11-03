# -*- coding: utf-8 -*-
"""Met à jour chaque jour les prix moyens du SP95-E10 et du gazole du simulateur (contenu/simulateur.json).

Source : flux quotidien officiel des prix déclarés par les stations-service (site prix-carburants.gouv.fr,
ministère de l'Économie, Licence Ouverte 2.0) : https://donnees.roulez-eco.fr/opendata/jour/AAAAMMJJ
(archive zip contenant PrixCarburants_quotidien_AAAAMMJJ.xml, encodé en ISO-8859-1).

Méthode (citée dans la source du simulateur) :
  - pour chaque station, le dernier prix du carburant relevé le jour J (prix mis à jour ce jour-là) ;
  - on écarte les prix à plus de 20 % de la médiane (erreurs de saisie, par exemple du gazole à 1,25 €) ;
  - moyenne arithmétique des prix restants, arrondie au millième d'euro.

Lancé chaque matin par GitHub Actions (.github/workflows/carburants.yml) pour le jour précédent :
  python3 outils/carburants.py                      -> télécharge le fichier de la veille (heure de Paris)
  python3 outils/carburants.py --jour 2026-11-02    -> télécharge le fichier de ce jour
  python3 outils/carburants.py --fichier X.xml|zip  -> utilise un fichier déjà téléchargé (jour lu dans le nom)
  --essai : affiche le résultat sans rien écrire
Si le fichier est absent, incomplet ou invraisemblable, le script s'arrête en erreur sans rien modifier :
le simulateur garde les prix précédents (et leur date).
"""
import datetime, io, json, os, re, statistics, sys, time, urllib.request, zipfile
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FICHIER = os.path.join(RACINE, "contenu", "simulateur.json")
URL = "https://donnees.roulez-eco.fr/opendata/jour/{}"
CARBURANTS = {"prix_e10": "E10", "prix_gazole": "Gazole"}
MINIMUM = 1500          # nombre minimal de stations par carburant pour publier une moyenne
ECART = 0.20            # écart maximal à la médiane
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


def en_lettres(d, jour_semaine=False):
    j = "1er" if d.day == 1 else str(d.day)
    t = f"{j} {MOIS[d.month - 1]} {d.year}"
    return f"{JOURS[d.weekday()]} {t}" if jour_semaine else t


def num(x, n=3):
    return f"{x:.{n}f}".replace(".", ",")


def mille(n):
    return f"{n:,}".replace(",", " ")


def telecharger(jour):
    url = URL.format(jour.strftime("%Y%m%d"))
    for essai in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "revision-vtc.fr (simulateur)"})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except Exception as e:
            print(f"Téléchargement impossible ({url}) : {e}", file=sys.stderr)
            time.sleep(30)
    sys.exit(1)


def lire_xml(donnees):
    if donnees[:2] == b"PK":
        with zipfile.ZipFile(io.BytesIO(donnees)) as z:
            noms = [n for n in z.namelist() if n.lower().endswith(".xml")]
            assert len(noms) == 1, f"archive inattendue : {z.namelist()}"
            donnees = z.read(noms[0])
    return ET.fromstring(donnees)


def moyennes(racine, jour):
    iso = jour.isoformat()
    derniers = {}
    for pdv in racine.iter("pdv"):
        for p in pdv.findall("prix"):
            maj, nom = p.get("maj", ""), p.get("nom")
            if not maj.startswith(iso) or nom not in CARBURANTS.values():
                continue
            cle = (pdv.get("id"), nom)
            if cle not in derniers or maj > derniers[cle][0]:
                derniers[cle] = (maj, float(p.get("valeur")))
    res = {}
    for cle, nom in CARBURANTS.items():
        v = [x for (_, n), (_, x) in derniers.items() if n == nom]
        if len(v) < MINIMUM:
            sys.exit(f"{nom} : {len(v)} prix relevés le {iso}, moins que {MINIMUM} : fichier incomplet, rien n'est modifié.")
        med = statistics.median(v)
        garde = [x for x in v if abs(x - med) <= ECART * med]
        m = round(statistics.mean(garde), 3)
        if not 0.5 < m < 5:
            sys.exit(f"{nom} : moyenne invraisemblable ({m} €), rien n'est modifié.")
        res[cle] = {"valeur": m, "stations": len(garde), "ecartes": len(v) - len(garde)}
    return res


def ecrire(res, jour):
    with open(FICHIER, encoding="utf-8") as h:
        texte = h.read()
    date = en_lettres(jour)
    ancien = json.loads(texte)["valeurs"]["prix_e10"]["date"]
    for cle, r in res.items():
        texte, n = re.subn(rf'("{cle}": \{{"valeur": )[0-9.]+(, "date": ")[^"]*(")', rf'\g<1>{r["valeur"]}\g<2>{date}\g<3>', texte)
        assert n == 1, f"{cle} introuvable dans simulateur.json"
    nom = ("Ministère de l'Économie, site officiel prix-carburants.gouv.fr, flux quotidien des prix déclarés par les stations-service "
           f"(données ouvertes, Licence Ouverte 2.0) : moyennes nationales TTC du {en_lettres(jour, True)} calculées par Révision VTC "
           f"sur les prix relevés ce jour-là (SP95-E10 : {mille(res['prix_e10']['stations'])} stations, gazole : {mille(res['prix_gazole']['stations'])} stations ; "
           "prix à plus de 20 % de la médiane écartés)")
    consulte = "téléchargé le " + en_lettres(jour + datetime.timedelta(days=1))
    ligne = json.dumps({"id": "prix_carburants", "nom": nom, "url": "https://www.prix-carburants.gouv.fr/rubrique/opendata/", "date": consulte}, ensure_ascii=False)
    texte, n = re.subn(r'\{"id": "prix_carburants", [^\n]*?\}(?=,?\n)', lambda _: ligne, texte)
    assert n == 1, "source prix_carburants introuvable dans simulateur.json"
    json.loads(texte)  # le fichier reste du JSON valide
    with open(FICHIER, "w", encoding="utf-8") as h:
        h.write(texte)
    print(f"Prix du {date} (avant : {ancien}) : SP95-E10 {num(res['prix_e10']['valeur'])} €, gazole {num(res['prix_gazole']['valeur'])} €.")


def main():
    a = sys.argv[1:]
    essai = "--essai" in a
    if "--fichier" in a:
        chemin = a[a.index("--fichier") + 1]
        m = re.search(r"(\d{8})", os.path.basename(chemin))
        jour = datetime.datetime.strptime(m.group(1), "%Y%m%d").date()
        with open(chemin, "rb") as h:
            donnees = h.read()
    else:
        if "--jour" in a:
            jour = datetime.date.fromisoformat(a[a.index("--jour") + 1])
        else:
            jour = datetime.datetime.now(ZoneInfo("Europe/Paris")).date() - datetime.timedelta(days=1)
        donnees = telecharger(jour)
    res = moyennes(lire_xml(donnees), jour)
    for cle, r in res.items():
        print(f"{CARBURANTS[cle]} : {num(r['valeur'])} € ({r['stations']} stations, {r['ecartes']} prix écartés)")
    if not essai:
        ecrire(res, jour)


if __name__ == "__main__":
    main()
