"""Compare le calcul du simulateur en Python (outils/generer.py, exemples chiffrés des pages)
au calcul en JavaScript de la page (docs/js/simulateur.js), sur les valeurs par défaut et 400 cas tirés au hasard.
Usage, depuis la racine du dépôt : python3 outils/test_coherence_simulateur.py   (nécessite node)"""
import json, os, random, subprocess, sys

sys.path.insert(0, os.path.dirname(__file__))
import generer as g

s = g.lire_simulateur()
base = g.defauts_simulateur(s)
random.seed(2026)
cas = [dict(base)]
for _ in range(400):
    e = dict(base)
    e.update(verse_semaine=random.choice([0, 50, 300, 700, 850, 878, 879, 1000, 1500, 3000]) + random.random() * 50,
             commission=random.choice([0, 10, 25, 45]), semaines=random.randint(1, 52), km_an=random.choice([0, 20000, 60000, 90000]),
             mode=random.choice(["location", "lld", "achat"]), energie=random.choice(["essence", "gazole", "electricite"]),
             base=random.choice(["clients", "verse"]), cma=random.choice(["france", "rhin", "moselle"]), vl=random.random() < .5,
             etranger=random.random() < .7, entretien_mois=random.choice([0, 150]), autres_mois=random.choice([0, 80]),
             revente=random.choice([0, 6000]), duree_ans=random.randint(1, 8), loyer_mois=random.choice([400, 800]),
             prix_energie=random.choice([0.2, 1.9, 2.3]), assurance=random.choice([600, 4100]))
    cas.append(e)

js = r"""
const D = JSON.parse(require('fs').readFileSync('contenu/simulateur.json', 'utf8'));
require('./docs/js/simulateur.js');
const cas = JSON.parse(require('fs').readFileSync(0, 'utf8'));
process.stdout.write(JSON.stringify(cas.map(e => globalThis.SimuVTC.calculer(e, D, true))));
"""
sortie = subprocess.run(["node", "-e", js], input=json.dumps(cas), capture_output=True, text=True, check=True).stdout
resultats = json.loads(sortie)
paires = [("verse", "verse"), ("prix", "prixClients"), ("ca", "ca"), ("social", "social"), ("vl", "vl"), ("tva", "tvaNette"),
          ("voiture", "voiture"), ("net", "net")]
erreurs = 0
for e, r in zip(cas, resultats):
    p = g.calcul_simulateur(s, **e)
    for kp, kj in paires:
        if abs(p[kp] - r[kj]) > 0.005:
            erreurs += 1
            print(f"écart sur {kp} : Python {p[kp]:.2f}, JavaScript {r[kj]:.2f} pour {e}")
    if (p["regime"] or None) != (r["tva"] or None):
        erreurs += 1
        print(f"régime de TVA différent : Python {p['regime']}, JavaScript {r['tva']} pour {e}")
if erreurs:
    sys.exit(f"{erreurs} écart(s) entre le calcul Python et le calcul JavaScript")
print(f"Simulateur : calculs Python et JavaScript identiques sur {len(cas)} cas.")
