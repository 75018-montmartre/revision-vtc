/* revision-vtc.fr · calcul de la note de l'examen VTC (admissibilité)
   Barème : arrêté du 6 avril 2017, articles 2 et 5 (contenu/calcul_note.json, injecté dans la page,
   balise <script id="note-donnees" type="application/json">). Rien n'est envoyé : tout est calculé ici.
   Les points sont comptés en centièmes entiers pour éviter les erreurs d'arrondi (9,999 n'est pas 10). */
(function (racine) {
  'use strict';

  /* ---------- le calcul (aussi utilisé par les tests) ---------- */
  // notes : { A: 12, B: null, ... } (null = pas encore connue) ; mode : 'complet' ou 'passerelle'
  function calculer(notes, mode, d) {
    var eps = d.epreuves.filter(function (e) { return mode !== 'passerelle' || !e.commune; });
    var coefTotal = 0, pts = 0, coefRestant = 0, minRestant = 0, maxRestant = 0;
    var lignes = [], elimines = [], restantes = [];
    eps.forEach(function (e) {
      coefTotal += e.coef;
      var n = notes[e.code];
      if (n === null || n === undefined) {
        coefRestant += e.coef; minRestant += e.elim * 100 * e.coef; maxRestant += 2000 * e.coef;
        restantes.push(e.code);
        lignes.push({ code: e.code, note: null, coef: e.coef, elim: e.elim, points: null, elimine: false });
        return;
      }
      var c = Math.round(n * 100);
      pts += c * e.coef;
      var elim = c < e.elim * 100;
      if (elim) elimines.push(e.code);
      lignes.push({ code: e.code, note: c / 100, coef: e.coef, elim: e.elim, points: c * e.coef / 100, elimine: elim });
    });
    var seuil = d.moyenne_requise * 100 * coefTotal;   // points pondérés nécessaires, en centièmes
    var r = { mode: mode, lignes: lignes, coefTotal: coefTotal, points: pts / 100, pointsRequis: seuil / 100,
              elimines: elimines, restantes: restantes, complet: restantes.length === 0 };
    if (r.complet) {
      r.moyenne = Math.floor(pts / coefTotal) / 100;   // tronquée au centième : jamais arrondie vers le haut
      r.moyenneOk = pts >= seuil;
      r.admissible = r.moyenneOk && elimines.length === 0;
      r.statut = r.admissible ? 'admissible' : 'non-admissible';
      // conseils : ce qui manque pour sortir des notes éliminatoires, l'épreuve où combler la moyenne, les points fragiles
      r.rattrapage = lignes.filter(function (l) { return l.elimine; })
        .map(function (l) { return { code: l.code, manque: (l.elim * 100 - Math.round(l.note * 100)) / 100, seuil: l.elim }; });
      r.marge = r.moyenneOk ? Math.floor((pts - seuil) / coefTotal) / 100 : 0;
      r.fragiles = lignes.filter(function (l) { return !l.elimine && l.note < l.elim + 2; }).map(function (l) { return l.code; });
      r.levier = null;
      if (!r.moyenneOk) {
        var deficit = seuil - pts;
        // l'épreuve qui comble l'écart avec le moins de points en plus : coefficient le plus fort, puis note la plus basse
        lignes.slice().sort(function (a, b) { return b.coef - a.coef || a.note - b.note; }).some(function (l) {
          var ajout = Math.ceil(deficit / l.coef);   // en centièmes de note
          if (Math.round(l.note * 100) + ajout > 2000) return false;
          r.levier = { code: l.code, coef: l.coef, ajout: ajout / 100, de: l.note, a: (Math.round(l.note * 100) + ajout) / 100 };
          return true;
        });
      }
    } else {
      var manque = Math.max(seuil - pts, 0);
      r.manque = manque / 100;
      r.besoinMoyenne = Math.ceil(manque / coefRestant) / 100;   // arrondie au centième supérieur : jamais trop optimiste
      if (elimines.length) r.statut = 'elimine';
      else if (manque > maxRestant) r.statut = 'impossible';
      else if (manque <= minRestant) r.statut = 'minimum';
      else r.statut = 'besoin';
    }
    return r;
  }

  // « 12,5 », « 12.5 », « 12,5/20 » -> 12.5 ; vide -> null ; invalide -> NaN
  function lireNote(texte) {
    var brut = String(texte).replace(/\s| | /g, '').replace(/\/20$/, '').replace(',', '.');
    if (brut === '') return null;
    if (!/^\d{1,2}(\.\d{1,2})?$/.test(brut)) return NaN;
    var n = Number(brut);
    return n >= 0 && n <= 20 ? n : NaN;
  }

  racine.NoteVTC = { calculer: calculer, lireNote: lireNote };
  if (typeof document === 'undefined') return;

  /* ---------- la page ---------- */
  var form = document.getElementById('note');
  var source = document.getElementById('note-donnees');
  if (!form || !source) return;
  var D = JSON.parse(source.textContent);
  var $ = function (id) { return document.getElementById(id); };
  function fr(x) {   // 10,4 ; 177 ; 12,25
    return (Math.round(x * 100) / 100).toFixed(2).replace(/\.?0+$/, '').replace('.', ',');
  }
  function fr2(x) { return x.toFixed(2).replace('.', ','); }
  function points(x, adj) { var p = x >= 2 ? 's' : ''; return fr(x) + ' point' + p + (adj ? ' ' + adj + p : ''); }
  var nomEpreuve = {};
  D.epreuves.forEach(function (e) { nomEpreuve[e.code] = e.code + ' (' + e.court.charAt(0).toLowerCase() + e.court.slice(1) + ')'; });
  function liste(codes) {
    var n = codes.map(function (c) { return nomEpreuve[c]; });
    return n.length < 2 ? n.join('') : n.slice(0, -1).join(', ') + ' et ' + n[n.length - 1];
  }
  function mode() { var m = form.querySelector('input[name="mode"]:checked'); return m ? m.value : 'complet'; }

  function afficher() {
    var m = mode(), notes = {}, valide = true;
    document.querySelectorAll('[data-commune]').forEach(function (b) { b.hidden = m === 'passerelle'; });
    D.epreuves.forEach(function (e) {
      var champ = $('note-' + e.code), err = $('err-note-' + e.code);
      if (m === 'passerelle' && e.commune) { err.textContent = ''; champ.removeAttribute('aria-invalid'); return; }
      var n = lireNote(champ.value);
      if (n !== n) {   // NaN
        valide = false;
        err.textContent = 'Indiquez une note entre 0 et 20, par exemple 12 ou 12,5.';
        champ.setAttribute('aria-invalid', 'true');
      } else {
        err.textContent = ''; champ.removeAttribute('aria-invalid');
        notes[e.code] = n;
      }
    });
    if (!valide) {
      $('res-verdict').textContent = 'Corrigez la note signalée.';
      $('res-verdict').className = 'resultat';
      $('res-moyenne').textContent = ''; $('res-explication').textContent = ''; $('res-detail').innerHTML = '';
      $('res-conseil').hidden = true;
      $('note-annonce').textContent = 'Une note est invalide.';
      return;
    }
    var r = calculer(notes, m, D);

    // verdict
    var v = $('res-verdict'), moy = $('res-moyenne'), ex = $('res-explication');
    var conseil = $('res-conseil'), conseils = [];
    var aucune = r.restantes.length === r.lignes.length;
    if (aucune) {
      v.className = 'resultat'; v.textContent = 'Saisissez vos notes';
      moy.textContent = 'Il faut ' + fr(r.pointsRequis) + ' points pondérés sur ' + fr(r.coefTotal * 20) + ', soit ' + D.moyenne_requise + ' / 20 de moyenne.';
      ex.textContent = '';
    } else if (r.complet) {
      v.className = 'resultat ' + (r.admissible ? 'ok' : 'ko');
      v.textContent = r.admissible ? 'Admissible' : 'Non admissible';
      moy.textContent = 'Moyenne : ' + fr2(r.moyenne) + ' / 20 (' + fr(r.points) + ' points pondérés sur ' + fr(r.coefTotal * 20) + ').';
      var raisons = [];
      if (!r.moyenneOk) raisons.push('la moyenne est inférieure à ' + D.moyenne_requise + ' / 20 : il manque ' + points(r.pointsRequis - r.points, 'pondéré'));
      if (r.elimines.length) raisons.push((r.elimines.length > 1 ? 'notes éliminatoires en ' : 'note éliminatoire en ') + liste(r.elimines));
      ex.textContent = r.admissible
        ? 'Moyenne d’au moins ' + D.moyenne_requise + ' / 20 et aucune note éliminatoire : vous pouvez passer l’épreuve pratique, où il faut ' + D.note_pratique + ' / 20.'
        : 'Pourquoi : ' + raisons.join(' ; ') + '.' + (r.moyenneOk && r.elimines.length ? ' Une bonne moyenne ne rattrape pas une note éliminatoire.' : '');
      // que travailler ?
      r.rattrapage.forEach(function (x) {
        conseils.push('Priorité : ' + nomEpreuve[x.code] + '. Il vous faut ' + points(x.manque) + ' de plus pour atteindre ' + x.seuil + ' / 20 et ne plus être éliminé.');
      });
      if (r.levier) conseils.push('Pour la moyenne : un point gagné dans une épreuve à coefficient ' + r.levier.coef + ' rapporte ' + points(r.levier.coef, 'pondéré') + '. Par exemple, passer de ' + fr(r.levier.de) + ' à ' + fr(r.levier.a) + ' / 20 en ' + nomEpreuve[r.levier.code] + ', soit ' + points(r.levier.ajout) + ' de plus, suffirait' + (r.rattrapage.length ? ' pour la moyenne.' : '.'));
      if (r.admissible) {
        if (r.fragiles.length) conseils.push((r.fragiles.length > 1 ? 'Points fragiles : ' : 'Point fragile : ') + liste(r.fragiles) + ', à moins de 2 points du seuil éliminatoire. Quelques erreurs de plus le jour J suffiraient à vous éliminer : c’est là qu’il faut consolider.');
        var coef3 = m === 'passerelle' ? 'F et G' : 'les épreuves à coefficient 3 (A, C, F et G)';
        if (r.marge < 1) conseils.push((r.marge === 0 ? 'Aucune marge : votre moyenne est pile à 10 / 20. ' : 'Marge faible : votre moyenne dépasse 10 / 20 de ' + fr2(r.marge) + ' point. ') + 'Visez au moins 1 point de marge, en travaillant d’abord ' + coef3 + '.');
        if (!r.fragiles.length && r.marge >= 1) conseils.push('Bonne marge : moyenne au-dessus de 10 / 20 de ' + fr2(r.marge) + ' point' + (r.marge >= 2 ? 's' : '') + ', et toutes vos notes dépassent les seuils d’au moins 2 points. Continuez les examens blancs pour confirmer ce niveau.');
      }
    } else {
      v.className = 'resultat' + (r.statut === 'elimine' || r.statut === 'impossible' ? ' ko' : '');
      var reste = liste(r.restantes);
      if (r.statut === 'elimine') {
        v.textContent = 'Non admissible';
        moy.textContent = (r.elimines.length > 1 ? 'Notes éliminatoires en ' : 'Note éliminatoire en ') + liste(r.elimines) + '.';
        ex.textContent = 'Quelles que soient les autres notes, une note éliminatoire empêche d’être admissible.';
      } else if (r.statut === 'impossible') {
        v.textContent = 'Moyenne hors d’atteinte';
        moy.textContent = 'Il manque ' + fr(r.manque) + ' points pondérés : même 20 / 20 en ' + reste + ' ne suffirait pas.';
        ex.textContent = '';
      } else if (r.statut === 'minimum') {
        v.textContent = 'En bonne voie';
        moy.textContent = r.manque === 0 ? 'Vous avez déjà assez de points pour la moyenne.'
          : 'Il manque ' + points(r.manque, 'pondéré') + ' : les notes minimales en ' + reste + ' suffiraient pour atteindre la moyenne.';
        ex.textContent = 'Il reste à ne pas avoir de note éliminatoire en ' + reste + ' : au moins 6 / 20' + (r.restantes.indexOf('E') >= 0 ? ' (4 / 20 en anglais)' : '') + '.';
      } else {
        v.textContent = 'Il vous manque ' + points(r.manque);
        moy.textContent = 'Soit au moins ' + fr2(r.besoinMoyenne) + ' / 20 de moyenne pondérée en ' + reste + '.';
        ex.textContent = 'Et aucune note éliminatoire : au moins 6 / 20 à chaque épreuve' + (r.restantes.indexOf('E') >= 0 ? ', 4 / 20 en anglais' : '') + '.';
      }
    }

    conseil.hidden = conseils.length === 0;
    conseil.innerHTML = '';
    conseils.forEach(function (t) { var p = document.createElement('p'); p.textContent = t; conseil.appendChild(p); });

    // détail par épreuve (l'état est écrit en toutes lettres, pas seulement en couleur)
    var corps = $('res-detail'); corps.innerHTML = '';
    r.lignes.forEach(function (l) {
      var tr = document.createElement('tr');
      var cel = function (t, nb) { var td = document.createElement(nb === 'th' ? 'th' : 'td'); if (nb === 'th') td.scope = 'row'; else if (nb) td.className = 'nombre'; td.textContent = t; tr.appendChild(td); };
      cel(l.code, 'th');
      cel(l.note === null ? '—' : fr(l.note), true);
      cel(String(l.coef), true);
      cel(l.points === null ? '—' : fr(l.points), true);
      cel(l.note === null ? 'à venir' : (l.elimine ? 'raté' : 'OK'), false);
      corps.appendChild(tr);
    });
    $('note-annonce').textContent = v.textContent + '. ' + moy.textContent;
  }

  form.addEventListener('input', afficher);
  form.addEventListener('change', afficher);
  form.addEventListener('submit', function (ev) { ev.preventDefault(); afficher(); $('resultat').focus(); });
  $('note-raz').addEventListener('click', function () {
    D.epreuves.forEach(function (e) { $('note-' + e.code).value = ''; });
    afficher(); $('note-' + (mode() === 'passerelle' ? 'F' : 'A')).focus();
  });
  form.hidden = false;
  $('resultat').hidden = false;
  $('note-sans-js').hidden = true;
  afficher();
})(typeof window !== 'undefined' ? window : globalThis);
