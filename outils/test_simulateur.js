// Vérifie le calcul du simulateur (docs/js/simulateur.js) sur des cas faits à la main.
// Usage, depuis la racine du dépôt : node outils/test_simulateur.js
const assert = require('assert');
const D = require('../contenu/simulateur.json');
require('../docs/js/simulateur.js');
const { calculer } = globalThis.SimuVTC;

const base = { verse_semaine: 1000, commission: 25, semaines: 47, heures: 0, km_an: 60000, loyer_semaine: 280, loyer_mois: 800,
  prix_achat: 34200, duree_ans: 5, revente: 0, assurance: 600, entretien_mois: 0, conso_thermique: 4.9, conso_elec: 13.6,
  prix_energie: 2.116, autres_mois: 0, base: 'clients', mode: 'location', energie: 'essence', cma: 'france', vl: false };
const proche = (a, b, m) => assert.ok(Math.abs(a - b) < 0.01, `${m} : ${a} au lieu de ${b}`);

// 1. Valeurs par défaut, cotisations sur le prix payé par les clients
let r = calculer(base, D);
proche(r.verse, 47000, 'versé');
proche(r.prixClients, 62666.6667, 'prix clients');
proche(r.social, 62666.6667 * 0.2198, 'cotisations');
proche(r.loyer, 14560, 'loyer');
proche(r.energie, 60000 * 4.9 / 100 * 2.116, 'carburant');            // 6 221,04 €
proche(r.reglementaire, 52.72, 'carte, registre, visite');
proche(r.net, 47000 - 62666.6667 * 0.2198 - (14560 + 6221.04 + 600) - 52.72, 'net');
assert.strictEqual(r.tva, 'majore');
// seuil : au montant versé seuil, le revenu net est nul
const s = calculer({ ...base, verse_semaine: r.seuilSemaine }, D);
proche(s.net, 0, 'seuil de rentabilité');

// 2. Cotisations sur le montant versé, versement libératoire, Moselle
r = calculer({ ...base, base: 'verse', vl: true, cma: 'moselle' }, D);
proche(r.social, 47000 * (21.2 + 0.3 + 0.83) / 100, 'cotisations Moselle');
proche(r.vl, 47000 * 0.017, 'versement libératoire');
assert.strictEqual(r.imposable, null);

// 3. Achat, électrique, entretien, heures
r = calculer({ ...base, mode: 'achat', revente: 4200, energie: 'electricite', prix_energie: 0.2, assurance: 4100, entretien_mois: 150, heures: 45 }, D);
proche(r.amortissement, 6000, 'amortissement');
proche(r.energie, 60000 * 13.6 / 100 * 0.2, 'électricité');           // 1 632 €
proche(r.voiture, 6000 + 1632 + 4100 + 1800, 'voiture');
proche(r.voitureKm, (6000 + 1632 + 4100 + 1800) / 60000, 'coût au km');
proche(r.netHeure, r.net / (45 * 47), 'net par heure');

// 4. Petite activité : abattement minimal de 305 € et pas de TVA
r = calculer({ ...base, verse_semaine: 10, semaines: 40, base: 'verse' }, D);
proche(r.imposable, 400 - 305, 'abattement minimal');
assert.strictEqual(r.tva, null);

console.log('Simulateur : tous les calculs sont justes.');
