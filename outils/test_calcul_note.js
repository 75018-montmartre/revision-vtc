// Vérifie le calcul de la note de l'examen VTC (docs/js/calcul-note.js) sur des cas faits à la main,
// d'après l'arrêté du 6 avril 2017 (article 2 III et article 5). Usage : node outils/test_calcul_note.js
const assert = require('assert');
const D = require('../contenu/calcul_note.json');
require('../docs/js/calcul-note.js');
const { calculer, lireNote } = globalThis.NoteVTC;
const tout = (a, b, c, d, e, f, g) => ({ A: a, B: b, C: c, D: d, E: e, F: f, G: g });
let r;

// 0. Le barème lui-même : 7 épreuves, coefficients 3-2-3-2-1-3-3 (total 17), seuils 6 sauf anglais 4
assert.deepStrictEqual(D.epreuves.map(e => e.code).join(''), 'ABCDEFG');
assert.deepStrictEqual(D.epreuves.map(e => e.coef), [3, 2, 3, 2, 1, 3, 3]);
assert.deepStrictEqual(D.epreuves.map(e => e.elim), [6, 6, 6, 6, 4, 6, 6]);
assert.deepStrictEqual(D.epreuves.map(e => e.duree), [45, 45, 30, 30, 30, 30, 20]);
assert.strictEqual(D.epreuves.reduce((s, e) => s + e.coef, 0), 17);

// 1. Exemple « admissible » de la page : 36+18+42+22+5+24+30 = 177 points, 177/17 = 10,41
r = calculer(D.exemples.admissible, 'complet', D);
assert.strictEqual(r.points, 177); assert.strictEqual(r.moyenne, 10.41); assert.strictEqual(r.admissible, true);

// 2. Exemple « piège » : 212 points (12,47 de moyenne) mais 3/20 en anglais (sous 4) : non admissible
r = calculer(D.exemples.piege, 'complet', D);
assert.strictEqual(r.points, 212); assert.strictEqual(r.moyenne, 12.47);
assert.strictEqual(r.moyenneOk, true); assert.deepStrictEqual(r.elimines, ['E']); assert.strictEqual(r.admissible, false);

// 3. Pile 10 de moyenne (170 points) : admissible (« au moins dix »)
r = calculer(tout(10, 10, 10, 10, 10, 10, 10), 'complet', D);
assert.strictEqual(r.points, 170); assert.strictEqual(r.moyenne, 10); assert.strictEqual(r.admissible, true);

// 4. Un centième de moins : 169,99 points... impossible avec un coefficient 1 sauf en E : E = 9,99 -> 169,99 points
r = calculer(tout(10, 10, 10, 10, 9.99, 10, 10), 'complet', D);
assert.strictEqual(r.points, 169.99); assert.strictEqual(r.moyenneOk, false); assert.strictEqual(r.admissible, false);
assert.strictEqual(r.moyenne, 9.99);   // tronquée, jamais affichée 10,00

// 5. Seuils : 6 pile n'élimine pas, 5,99 élimine ; anglais : 4 pile passe, 3,99 élimine
r = calculer(tout(6, 14, 12, 12, 4, 12, 10), 'complet', D);   // 18+28+36+24+4+36+30 = 176
assert.strictEqual(r.points, 176); assert.deepStrictEqual(r.elimines, []); assert.strictEqual(r.admissible, true);
r = calculer(tout(5.99, 14, 12, 12, 3.99, 12, 10), 'complet', D);
assert.deepStrictEqual(r.elimines, ['A', 'E']); assert.strictEqual(r.admissible, false);

// 6. Moyenne trop basse sans note éliminatoire : tout à 9 -> 153 points, il manque 17 points
r = calculer(tout(9, 9, 9, 9, 9, 9, 9), 'complet', D);
assert.strictEqual(r.points, 153); assert.strictEqual(r.admissible, false); assert.strictEqual(r.pointsRequis - r.points, 17);

// 7. Notes partielles : A à E connues (36+18+42+22+5 = 123), il manque 47 points sur F et G (coef. 6) -> 7,84 de moyenne (47/6 = 7,833 arrondi au-dessus)
r = calculer({ A: 12, B: 9, C: 14, D: 11, E: 5, F: null, G: null }, 'complet', D);
assert.strictEqual(r.statut, 'besoin'); assert.strictEqual(r.manque, 47); assert.strictEqual(r.besoinMoyenne, 7.84);
assert.deepStrictEqual(r.restantes, ['F', 'G']);
// ... si les notes minimales suffisent : 6+6 en F et G = 36 points >= ce qui manque
r = calculer({ A: 16, B: 16, C: 16, D: 16, E: 16, F: null, G: null }, 'complet', D);   // 176 points, il en manque 0
assert.strictEqual(r.statut, 'minimum'); assert.strictEqual(r.manque, 0);
r = calculer({ A: 12, B: 12, C: 12, D: 12, E: 12, F: null, G: null }, 'complet', D);   // 132 points, il manque 38 > 36
assert.strictEqual(r.statut, 'besoin'); assert.strictEqual(r.manque, 38);
r = calculer({ A: 13, B: 12, C: 12, D: 12, E: 12, F: null, G: null }, 'complet', D);   // 135 points, il manque 35 <= 36
assert.strictEqual(r.statut, 'minimum');
// ... note éliminatoire déjà connue
r = calculer({ A: 5, B: null, C: null, D: null, E: null, F: null, G: null }, 'complet', D);
assert.strictEqual(r.statut, 'elimine');
// ... moyenne hors d'atteinte : A à E à 0 (non éliminatoire impossible, mais on teste le calcul) -> on ne peut pas, donc E à 4 et le reste au plus bas non éliminatoire, G seul restant
r = calculer({ A: 6, B: 6, C: 6, D: 6, E: 4, F: 6, G: null }, 'complet', D);   // 18+12+18+12+4+18 = 82, il manque 88 > 60
assert.strictEqual(r.statut, 'impossible'); assert.strictEqual(r.manque, 88);

// 8. Candidat admissible au taxi depuis moins de 3 ans (article 5) : seulement F et G, coefficient 3 chacune, moyenne sur 6
r = calculer({ F: 6, G: 14 }, 'passerelle', D);        // 18+42 = 60 = 10 x 6
assert.strictEqual(r.coefTotal, 6); assert.strictEqual(r.points, 60); assert.strictEqual(r.admissible, true);
r = calculer({ F: 5.5, G: 16 }, 'passerelle', D);      // moyenne 10,75 mais F sous 6
assert.strictEqual(r.moyenneOk, true); assert.strictEqual(r.admissible, false);
r = calculer({ A: 0, F: 9, G: 10.5 }, 'passerelle', D); // A ignorée ; 27+31,5 = 58,5 < 60
assert.strictEqual(r.lignes.length, 2); assert.strictEqual(r.admissible, false);

// 9. Lecture des saisies
assert.strictEqual(lireNote('12,5'), 12.5); assert.strictEqual(lireNote(' 12.25 '), 12.25); assert.strictEqual(lireNote('14/20'), 14);
assert.strictEqual(lireNote(''), null); assert.strictEqual(lireNote('20'), 20); assert.strictEqual(lireNote('0'), 0);
assert.ok(Number.isNaN(lireNote('21'))); assert.ok(Number.isNaN(lireNote('-1'))); assert.ok(Number.isNaN(lireNote('12,555')));
assert.ok(Number.isNaN(lireNote('abc'))); assert.ok(Number.isNaN(lireNote('1e1')));

// 10. Toutes les combinaisons de notes entières : le verdict suit exactement la règle du texte (17^7 ≈ 410 millions : on échantillonne 200 000 cas)
let graine = 12345; const alea = () => (graine = (graine * 1103515245 + 12345) % 2147483648) / 2147483648;
for (let i = 0; i < 200000; i++) {
  const n = {}; let somme = 0, elim = false;
  for (const e of D.epreuves) { const x = Math.round(alea() * 80) / 4; n[e.code] = x; somme += x * e.coef; if (x < e.elim) elim = true; }
  const attendu = somme / 17 >= 10 - 1e-9 && !elim;
  assert.strictEqual(calculer(n, 'complet', D).admissible, attendu, JSON.stringify(n));
}

console.log('Calcul de la note de l\'examen VTC : tous les tests passent.');

// 11. Conseils
// exemple admissible : E à 5 (seuil 4) et F à 8 ? non : F 8 >= 6+2 -> pas fragile ; E 5 < 6 -> fragile ; marge 7/17 = 0,41
r = calculer(D.exemples.admissible, 'complet', D);
assert.deepStrictEqual(r.fragiles, ['E']); assert.strictEqual(r.marge, 0.41); assert.strictEqual(r.levier, null);
// piège : E à 3, il manque 1 point pour atteindre 4
r = calculer(D.exemples.piege, 'complet', D);
assert.deepStrictEqual(r.rattrapage, [{ code: 'E', manque: 1, seuil: 4 }]); assert.strictEqual(r.levier, null);
// tout à 9 : il manque 17 points ; meilleur levier = coefficient 3, note la plus basse (A, première à égalité) : 17/3 = 5,67 points -> de 9 à 14,67
r = calculer(tout(9, 9, 9, 9, 9, 9, 9), 'complet', D);
assert.deepStrictEqual(r.levier, { code: 'A', coef: 3, ajout: 5.67, de: 9, a: 14.67 });
// le levier vise la note la plus basse parmi les coefficients 3 : F à 7
r = calculer(tout(9, 9, 9, 9, 9, 7, 9), 'complet', D);   // 147 points, il manque 23 -> 7,67 en F
assert.strictEqual(r.levier.code, 'F'); assert.strictEqual(r.levier.ajout, 7.67); assert.strictEqual(r.levier.a, 14.67);
// si aucune épreuve seule ne suffit (déjà proche de 20), pas de levier
r = calculer(tout(20, 0, 20, 0, 0, 20, 20), 'complet', D);   // 240 points : moyenne ok ; on teste un cas déficitaire saturé
assert.strictEqual(r.moyenneOk, true);
r = calculer(tout(18, 0, 18, 0, 0, 18, 18), 'complet', D);   // 216 points >= 170 : ok
r = calculer(tout(19, 6, 19, 6, 4, 19, 6), 'complet', D);     // 57+12+57+12+4+57+18 = 217 : ok, mais B, D, E, G fragiles
assert.deepStrictEqual(r.fragiles, ['B', 'D', 'E', 'G']);
r = calculer(tout(6, 6, 6, 6, 4, 19, 19), 'complet', D);      // 18+12+18+12+4+57+57 = 178 : admissible
assert.strictEqual(r.admissible, true);
r = calculer(tout(6, 6, 6, 6, 4, 6, 19), 'complet', D);       // 18+12+18+12+4+18+57 = 139 : il manque 31 ; A à 6 -> +10,34 -> 16,34
assert.deepStrictEqual(r.levier, { code: 'A', coef: 3, ajout: 10.34, de: 6, a: 16.34 });
r = calculer(tout(19, 0, 19, 0, 0, 19, 19), 'complet', D);    // 228 ok
r = calculer(tout(19.5, 0, 19.5, 0, 0, 19.5, 0), 'complet', D); // 175,5 ok
r = calculer(tout(19.5, 0, 19.5, 0, 0, 0, 0), 'complet', D);    // 117 : il manque 53 ; F ou G à 0 -> +17,67 possible
assert.strictEqual(r.levier.code, 'F'); assert.strictEqual(r.levier.ajout, 17.67);
r = calculer(tout(19, 19, 19, 19, 19, 19, 0), 'complet', D);  // 57+38+57+38+19+57 = 266 ok
r = calculer(tout(17, 0, 17, 0, 0, 17, 17), 'complet', D);    // 204 ok
r = calculer(tout(14, 0, 14, 0, 0, 14, 14), 'complet', D);    // 168 : il manque 2 -> 0,67 en A
assert.strictEqual(r.levier.ajout, 0.67);
r = calculer(tout(19, 0, 19, 0, 0, 19, 19.9), 'complet', D);  // 228 ok
r = calculer(tout(19.9, 0, 19.9, 0, 0, 19.9, 19.9), 'complet', D); // 238,8 ok
r = calculer(tout(20, 0, 20, 0, 0, 20, 0), 'complet', D);      // 180 ok
r = calculer(tout(20, 0, 20, 0, 0, 13, 0), 'complet', D);      // 159 : il manque 11 ; coef 3 : G (0) -> 3,67
assert.strictEqual(r.levier.code, 'G');
// le levier comble toujours exactement l'écart
for (let i = 0; i < 20000; i++) {
  const n = {}; for (const e of D.epreuves) n[e.code] = Math.round(alea() * 48) / 4;
  const x = calculer(n, 'complet', D);
  if (x.levier) { const m = { ...n, [x.levier.code]: x.levier.a }; assert.strictEqual(calculer(m, 'complet', D).moyenneOk, true, JSON.stringify(n)); }
  else if (!x.moyenneOk) assert.ok(D.epreuves.every(e => (20 - n[e.code]) * e.coef < x.pointsRequis - x.points + 1e-9), 'levier manquant ' + JSON.stringify(n));
}
console.log('Conseils : tous les tests passent.');
