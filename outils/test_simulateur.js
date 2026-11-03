// Vérifie le calcul du simulateur (docs/js/simulateur.js) sur des cas faits à la main.
// Usage, depuis la racine du dépôt : node outils/test_simulateur.js
const assert = require('assert');
const D = require('../contenu/simulateur.json');
require('../docs/js/simulateur.js');
const { calculer } = globalThis.SimuVTC;

const base = { verse_semaine: 1000, commission: 25, semaines: 47, heures: 0, km_an: 60000, loyer_semaine: 280, loyer_mois: 800,
  prix_achat: 34200, duree_ans: 5, revente: 0, assurance: 600, entretien_mois: 0, conso_thermique: 4.9, conso_elec: 13.6,
  prix_energie: 2.116, autres_mois: 0, base: 'clients', mode: 'location', energie: 'essence', cma: 'france', vl: false, etranger: true };
const proche = (a, b, m) => assert.ok(Math.abs(a - b) < 0.01, `${m} : ${a} au lieu de ${b}`);

// 1. Valeurs par défaut : 62 667 € de chiffre d'affaires, au-delà de 41 250 € : TVA due, année complète
let r = calculer(base, D);
proche(r.verse, 47000, 'versé');
proche(r.prixClients, 62666.6667, 'prix clients');
proche(r.tvaCollectee, 62666.6667 / 11, 'TVA collectée (10 % compris dans le prix)');       // 5 696,97 €
proche(r.ca, 62666.6667 * 10 / 11, 'chiffre d\'affaires hors taxe');
proche(r.social, 62666.6667 * 10 / 11 * 0.2198, 'cotisations sur le hors taxe');
proche(r.loyer, 14560, 'loyer');
proche(r.energie, 60000 * 4.9 / 100 * 2.116, 'carburant');            // 6 221,04 €
proche(r.tvaRecuperee, (14560 + 6221.04) / 6, 'TVA récupérée sur le loyer et le carburant');
proche(r.tvaCommission, 0, 'TVA sur la commission : autoliquidée et déduite');
proche(r.reglementaire, 52.72, 'carte, registre, visite');
proche(r.net, 47000 - 62666.6667 * 10 / 11 * 0.2198 - (62666.6667 / 11 - (14560 + 6221.04) / 6) - (14560 + 6221.04 + 600) - 52.72, 'net');
assert.strictEqual(r.tva, 'redevable');
// seuil : en dessous, le revenu net est négatif ; à partir du seuil, il est positif ou nul
// (ici, le seuil tombe sur le passage à la TVA : en franchise, la TVA sur la commission n'est pas récupérable)
assert.ok(calculer({ ...base, verse_semaine: r.seuilSemaine - 0.01 }, D).net < 0, 'sous le seuil, revenu négatif');
assert.ok(calculer({ ...base, verse_semaine: r.seuilSemaine }, D).net >= -0.01, 'au seuil, revenu positif');
// sans commission étrangère ni passage de seuil, le revenu net est nul au seuil
const s = calculer({ ...base, commission: 0, km_an: 20000, verse_semaine: 1 }, D);
proche(calculer({ ...base, commission: 0, km_an: 20000, verse_semaine: s.seuilSemaine }, D).net, 0, 'seuil de rentabilité');

// 1 bis. Franchise (500 € versés par semaine, 31 333 € de chiffre d'affaires) : TVA de 20 % sur la commission facturée de l'étranger
r = calculer({ ...base, verse_semaine: 500 }, D);
assert.strictEqual(r.tva, null);
proche(r.tvaCollectee, 0, 'pas de TVA collectée en franchise');
proche(r.tvaCommission, (31333.3333 - 23500) * 0.2, 'TVA autoliquidée sur la commission');
proche(r.social, 31333.3333 * 0.2198, 'cotisations sur le chiffre d\'affaires');
r = calculer({ ...base, verse_semaine: 500, etranger: false }, D);
proche(r.tvaCommission, 0, 'plateforme française : TVA déjà comprise dans la commission');

// 1 ter. Entre les deux seuils : franchise cette année, alerte pour l'année suivante
r = calculer({ ...base, verse_semaine: 600 }, D);                    // 37 600 €
assert.strictEqual(r.tva, 'base');
proche(r.tvaCollectee, 0, 'franchise entre 37 500 et 41 250 €');

// 2. Cotisations sur le montant versé, versement libératoire, Moselle
r = calculer({ ...base, base: 'verse', vl: true, cma: 'moselle' }, D);
proche(r.social, 47000 / 1.1 * (21.2 + 0.3 + 0.83) / 100, 'cotisations Moselle sur le hors taxe');
proche(r.vl, 47000 / 1.1 * 0.017, 'versement libératoire');
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
