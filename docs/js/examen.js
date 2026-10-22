// Examen blanc interactif : sommaire, épreuves (chronométrées ou non), correction, notes et moyenne.
// Accessibilité : questions en fieldset/legend, focus placé sur le titre à chaque écran,
// annonces vocales discrètes (5 minutes restantes, fin du temps), résultat jamais indiqué par la seule couleur.
(function () {
  var X = window.EXAMEN, ORDRE = X.ordre.split(''), CLE = 'mar-vtc-2027-examen-' + X.numero, CLE_CHRONO = 'mar-vtc-2027-chrono';
  var app = document.querySelector('main .page'), barre = document.getElementById('barre');
  var chronoEl = document.getElementById('chrono'), barreTitre = document.getElementById('barre-titre'), annonce = document.getElementById('annonce');
  var minuteur = null;

  function ty(t) {
    return String(t).replace(/'/g, '’').replace(/ ([:;?!»%€])/g, ' $1').replace(/« /g, '« ');
  }
  function el(tag, attrs, enfants) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) {
      if (k === 'texte') e.textContent = ty(attrs[k]);
      else if (k === 'classe') e.className = attrs[k];
      else e.setAttribute(k, attrs[k]);
    }
    (enfants || []).forEach(function (c) { if (c) e.appendChild(typeof c === 'string' ? document.createTextNode(ty(c)) : c); });
    return e;
  }
  function dire(t) { annonce.textContent = ''; setTimeout(function () { annonce.textContent = ty(t); }, 50); }
  function focusTitre() { var h = app.querySelector('h1'); if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); } window.scrollTo(0, 0); }

  // ---------------------------------------------------------------- préférences et état
  function chronoActif() { try { return localStorage.getItem(CLE_CHRONO) !== 'non'; } catch (e) { return true; } }
  function setChrono(v) { try { localStorage.setItem(CLE_CHRONO, v ? 'oui' : 'non'); } catch (e) {} }
  function neuf() {
    var st = { ep: {} };
    ORDRE.forEach(function (L) {
      var E = X.epreuves[L];
      st.ep[L] = { fin: null, termine: false, qcm: E.qcm.map(function () { return null; }),
                   qrc: E.qrc.map(function () { return ''; }), auto: E.qrc.map(function () { return null; }) };
    });
    return st;
  }
  var st;
  try { st = JSON.parse(localStorage.getItem(CLE)) || neuf(); } catch (e) { st = neuf(); }
  if (!st.ep || !st.ep.A) st = neuf();
  function sauver() { try { localStorage.setItem(CLE, JSON.stringify(st)); } catch (e) {} }

  function note(L) {
    var E = X.epreuves[L], S = st.ep[L], pts = 0, aNoter = 0;
    E.qcm.forEach(function (q, i) { if (S.qcm[i] === q.r) pts += E.pq; });
    E.qrc.forEach(function (r, i) { if (S.auto[i] == null) aNoter++; else pts += S.auto[i]; });
    return { pts: pts, aNoter: aNoter };
  }
  function fmt(x) { return String(Math.round(x * 100) / 100).replace('.', ','); }

  // ---------------------------------------------------------------- chronomètre
  function arreterChrono() { if (minuteur) clearInterval(minuteur); minuteur = null; barre.hidden = true; }
  function lancerChrono(L) {
    var S = st.ep[L], prevenu = false;
    barre.hidden = false;
    barreTitre.textContent = ty('Épreuve ' + L + ' · ' + X.epreuves[L].nom);
    if (!S.fin) { chronoEl.textContent = 'sans chronomètre'; return; }
    function tic() {
      var reste = Math.max(0, Math.round((S.fin - Date.now()) / 1000));
      var m = Math.floor(reste / 60), s = reste % 60;
      chronoEl.textContent = m + ' min ' + String(s).padStart(2, '0') + ' s';
      chronoEl.setAttribute('aria-label', 'Temps restant : ' + m + ' minutes');
      if (reste <= 300 && reste > 0 && !prevenu) { prevenu = true; dire('Plus que 5 minutes pour cette épreuve.'); }
      if (reste === 0) { dire('Temps écoulé : l\'épreuve est terminée.'); terminer(L, true); }
    }
    tic(); minuteur = setInterval(tic, 1000);
  }

  // ---------------------------------------------------------------- sommaire
  function sommaire() {
    arreterChrono();
    app.innerHTML = '';
    app.appendChild(el('p', { classe: 'surtitre', texte: 'Examen blanc n° ' + X.numero }));
    app.appendChild(el('h1', { texte: 'Les sept épreuves d\'admissibilité' }));
    app.appendChild(el('p', { texte: 'Faites les épreuves dans l\'ordre de votre choix, sans livre ni notes. Le chronomètre démarre quand vous ouvrez une épreuve et continue même si vous quittez la page.' }));
    var opt = el('input', { type: 'checkbox', id: 'opt-chrono' });
    opt.checked = chronoActif();
    opt.addEventListener('change', function () { setChrono(opt.checked); });
    app.appendChild(el('div', { classe: 'option-chrono' }, [opt, el('label', { 'for': 'opt-chrono', texte: 'Chronométrer les épreuves, comme le jour de l\'examen' })]));

    var tb = el('tbody');
    ORDRE.forEach(function (L) {
      var E = X.epreuves[L], S = st.ep[L], etat, lien;
      var detail = E.duree + ' min · coef. ' + E.coef + ' · ' + E.qcm.length + ' QCM' + (E.qrc.length ? ', ' + E.qrc.length + ' QRC' : '');
      if (S.termine) {
        var nt = note(L);
        etat = nt.aNoter ? 'Corrigée, ' + nt.aNoter + ' QRC à noter' : fmt(nt.pts) + ' / 20';
        lien = el('a', { classe: 'bouton second', href: '#corr-' + L, texte: 'Correction' });
        lien.setAttribute('aria-label', ty('Correction de l\'épreuve ' + L + ', ' + E.nom));
      } else {
        etat = S.ouverte ? 'En cours' : 'À faire';
        lien = el('a', { classe: 'bouton', href: '#ep-' + L, texte: S.ouverte ? 'Reprendre' : 'Commencer' });
        lien.setAttribute('aria-label', ty((S.ouverte ? 'Reprendre' : 'Commencer') + ' l\'épreuve ' + L + ', ' + E.nom));
      }
      tb.appendChild(el('tr', {}, [el('th', { scope: 'row', texte: L + ' · ' + E.nom }), el('td', { texte: detail }), el('td', { texte: etat }), el('td', {}, [lien])]));
    });
    app.appendChild(el('h2', { texte: 'Les épreuves' }));
    app.appendChild(el('div', { classe: 'defile' }, [el('table', { classe: 'epreuves' }, [
      el('thead', {}, [el('tr', {}, ['Épreuve', 'Format', 'État', 'Action'].map(function (h) { return el('th', { scope: 'col', texte: h }); }))]), tb])]));
    app.appendChild(tableauNotes());
    var raz = el('button', { classe: 'bouton second', type: 'button', texte: 'Effacer mes réponses et recommencer' });
    raz.addEventListener('click', function () {
      if (raz.dataset.confirme) { st = neuf(); sauver(); sommaire(); focusTitre(); dire('Réponses effacées.'); }
      else { raz.dataset.confirme = '1'; raz.textContent = ty('Confirmer : effacer toutes mes réponses'); }
    });
    app.appendChild(el('div', { classe: 'actions' }, [raz, el('a', { classe: 'bouton second', href: 'examens.html', texte: 'Retour aux examens' })]));
  }

  function tableauNotes() {
    var bloc = el('section', { 'aria-labelledby': 'titre-notes' }, [el('h2', { id: 'titre-notes', texte: 'Mes notes' })]);
    var tb = el('tbody'), total = 0, complet = true, elimine = false;
    ORDRE.forEach(function (L) {
      var E = X.epreuves[L], S = st.ep[L], nt = note(L), ok = S.termine && !nt.aNoter;
      if (!ok) complet = false;
      if (ok) { total += nt.pts * E.coef; if (nt.pts < E.elim) elimine = true; }
      tb.appendChild(el('tr', {}, [
        el('th', { scope: 'row', texte: L + ' · ' + E.nom }),
        el('td', { classe: 'nombre', texte: ok ? fmt(nt.pts) + ' / 20' : '—' }),
        el('td', { classe: 'nombre', texte: String(E.coef) }),
        el('td', { classe: 'nombre', texte: ok ? fmt(nt.pts * E.coef) : '—' }),
        el('td', { classe: 'nombre', texte: 'sous ' + E.elim })
      ]));
    });
    var entetes = [['Épreuve', ''], ['Note', 'nombre'], ['Coef.', 'nombre'], ['Points', 'nombre'], ['Éliminatoire', 'nombre']];
    bloc.appendChild(el('div', { classe: 'defile' }, [el('table', {}, [
      el('thead', {}, [el('tr', {}, entetes.map(function (h) { return el('th', { scope: 'col', classe: h[1], texte: h[0] }); }))]), tb])]));
    if (complet) {
      var moy = total / 17, adm = moy >= 10 && !elimine;
      bloc.appendChild(el('p', { classe: 'resultat ' + (adm ? 'ok' : 'ko'), texte: 'Moyenne : ' + fmt(moy) + ' / 20. ' + (adm ? 'Vous seriez admissible.' : (elimine ? 'Non admissible : au moins une note éliminatoire.' : 'Non admissible.')) }));
    } else {
      bloc.appendChild(el('p', { classe: 'meta', texte: 'La moyenne s\'affiche quand les sept épreuves sont corrigées et toutes les QRC notées. Moyenne = total des points divisé par 17. Admissible avec 10 / 20 de moyenne et aucune note éliminatoire (sous 6, sous 4 en anglais).' }));
    }
    return bloc;
  }

  // ---------------------------------------------------------------- une épreuve
  function epreuve(L) {
    var E = X.epreuves[L], S = st.ep[L];
    if (S.termine) { location.hash = '#corr-' + L; return; }
    if (!S.ouverte) { S.ouverte = true; S.fin = chronoActif() ? Date.now() + E.duree * 60000 : null; sauver(); }
    app.innerHTML = '';
    app.appendChild(el('p', { classe: 'surtitre', texte: 'Examen blanc n° ' + X.numero + ' · épreuve ' + L }));
    app.appendChild(el('h1', { texte: E.nom }));
    app.appendChild(el('p', { classe: 'note', texte: E.duree + ' minutes. ' + E.qcm.length + ' QCM notées sur ' + E.pq + ' point' + (E.pq > 1 ? 's' : '') + ' chacune (une seule bonne réponse dans cet examen blanc)' +
      (E.qrc.length ? ' ; ' + E.qrc.length + ' QRC notées sur ' + E.pr + ' points, à rédiger en quelques lignes.' : '.') }));
    if (L === 'D') {
      var td = el('section', { classe: 'texte-d', 'aria-labelledby': 'titre-texte' }, [el('h2', { id: 'titre-texte', texte: 'Texte : ' + E.titre_texte })]);
      E.texte.forEach(function (p, i) { td.appendChild(el('p', {}, [el('b', { classe: 'lettre', texte: '§ ' + (i + 1) + ' ' }), p])); });
      app.appendChild(td);
    }
    E.qcm.forEach(function (q, i) {
      var fs = el('fieldset', { classe: 'question' }, [el('legend', {}, [el('span', { classe: 'num', texte: 'QCM ' + (i + 1) + ' sur ' + E.qcm.length }), q.q])]);
      var ch = el('div', { classe: 'choix' });
      q.o.forEach(function (o, j) {
        var id = L + '-q' + i + '-' + j;
        var inp = el('input', { type: 'radio', name: L + '-q' + i, id: id, value: String(j) });
        if (S.qcm[i] === j) inp.checked = true;
        inp.addEventListener('change', function () { S.qcm[i] = j; sauver(); });
        ch.appendChild(el('label', { 'for': id }, [inp, el('span', { classe: 'lettre', 'aria-hidden': 'true', texte: 'ABCD'[j] }), el('span', { texte: o })]));
      });
      fs.appendChild(ch);
      app.appendChild(fs);
    });
    E.qrc.forEach(function (r, i) {
      var id = L + '-r' + i;
      var ta = el('textarea', { id: id });
      ta.value = S.qrc[i] || '';
      ta.addEventListener('input', function () { S.qrc[i] = ta.value; sauver(); });
      app.appendChild(el('div', { classe: 'question-bloc' }, [
        el('label', { 'for': id }, [el('span', { classe: 'num', texte: 'QRC ' + (i + 1) + ' · ' + E.pr + ' points' }), el('span', { style: 'display:block;font-family:var(--serif);font-weight:400;font-size:1.1875rem', texte: r.q })]), ta]));
    });
    var fin = el('button', { classe: 'bouton', type: 'button', texte: 'Terminer l\'épreuve et voir la correction' });
    fin.addEventListener('click', function () {
      var vides = S.qcm.filter(function (x) { return x == null; }).length;
      if (vides && !fin.dataset.confirme) { fin.dataset.confirme = '1'; fin.textContent = ty(vides + ' QCM sans réponse : terminer quand même'); dire(vides + ' QCM sans réponse. Appuyez de nouveau pour terminer quand même.'); return; }
      terminer(L, false);
    });
    app.appendChild(el('div', { classe: 'actions' }, [fin, el('a', { classe: 'bouton second', href: '#sommaire', texte: S.fin ? 'Revenir au sommaire (le temps continue)' : 'Revenir au sommaire' })]));
    lancerChrono(L);
  }

  function terminer(L, tempsEcoule) {
    var S = st.ep[L];
    if (S.termine) return;
    S.termine = true; S.tempsEcoule = !!tempsEcoule; sauver();
    arreterChrono();
    if (location.hash === '#corr-' + L) { correction(L); focusTitre(); } else location.hash = '#corr-' + L;
  }

  // ---------------------------------------------------------------- correction
  function correction(L) {
    arreterChrono();
    var E = X.epreuves[L], S = st.ep[L];
    if (!S.termine) { location.hash = '#ep-' + L; return; }
    app.innerHTML = '';
    app.appendChild(el('p', { classe: 'surtitre', texte: 'Examen blanc n° ' + X.numero + ' · correction de l\'épreuve ' + L }));
    app.appendChild(el('h1', { texte: E.nom }));
    if (S.tempsEcoule) app.appendChild(el('p', { classe: 'note', texte: 'Le temps était écoulé : l\'épreuve a été arrêtée automatiquement.' }));
    var resume = el('p', { classe: 'resultat', 'aria-live': 'polite' });
    app.appendChild(resume);
    function majResume() {
      var nt = note(L);
      resume.className = 'resultat ' + (nt.aNoter ? '' : (nt.pts >= 10 ? 'ok' : 'ko'));
      resume.textContent = ty(nt.aNoter ? 'QCM corrigées. Notez vos ' + nt.aNoter + ' QRC pour obtenir votre note.' : 'Note : ' + fmt(nt.pts) + ' / 20' + (nt.pts < E.elim ? ', note éliminatoire.' : '.'));
    }
    E.qcm.forEach(function (q, i) {
      var rep = S.qcm[i], juste = rep === q.r;
      var ch = el('ul', { classe: 'choix', style: 'list-style:none;padding:0;margin:0' });
      q.o.forEach(function (o, j) {
        var c = j === q.r ? 'juste' : (j === rep ? 'faux' : '');
        var etiq = j === q.r ? (j === rep ? 'Bonne réponse, votre choix' : 'Bonne réponse') : (j === rep ? 'Votre choix' : '');
        ch.appendChild(el('li', { classe: 'rep ' + c, style: 'margin:0' }, [el('span', { classe: 'lettre', texte: 'ABCD'[j] }), el('span', { texte: o }), etiq ? el('span', { classe: 'etiq', texte: etiq }) : null]));
      });
      app.appendChild(el('section', { classe: 'question-bloc', 'aria-label': ty('QCM ' + (i + 1)) }, [
        el('span', { classe: 'num', texte: 'QCM ' + (i + 1) }), el('p', { style: 'font-size:1.1875rem;margin:0 0 .75rem', texte: q.q }), ch,
        el('div', { classe: 'correction' }, [
          el('p', { classe: 'verdict ' + (juste ? 'ok' : 'ko'), texte: rep == null ? 'Sans réponse. Bonne réponse : ' + 'ABCD'[q.r] + '.' : (juste ? 'Juste : ' + E.pq + ' point' + (E.pq > 1 ? 's' : '') + '.' : 'Faux. Bonne réponse : ' + 'ABCD'[q.r] + '.') }),
          el('p', { style: 'margin:0', texte: q.e }), el('p', { classe: 'renvoi', style: 'margin-bottom:0', texte: 'À revoir dans le livre : fiche ' + q.ref })])
      ]));
    });
    E.qrc.forEach(function (r, i) {
      var ul = el('ul', { style: 'margin:.25rem 0 0' });
      r.c.forEach(function (c) { ul.appendChild(el('li', { texte: c })); });
      var sel = el('select', { id: L + '-auto' + i });
      sel.appendChild(el('option', { value: '', texte: 'Choisir' }));
      for (var p = 0; p <= E.pr; p += 0.5) sel.appendChild(el('option', { value: String(p), texte: fmt(p) + ' sur ' + E.pr }));
      if (S.auto[i] != null) sel.value = String(S.auto[i]);
      sel.addEventListener('change', function () { S.auto[i] = sel.value === '' ? null : parseFloat(sel.value); sauver(); majResume(); });
      app.appendChild(el('section', { classe: 'question-bloc', 'aria-label': ty('QRC ' + (i + 1)) }, [
        el('span', { classe: 'num', texte: 'QRC ' + (i + 1) + ' · ' + E.pr + ' points' }), el('p', { style: 'font-size:1.1875rem;margin:0 0 .75rem', texte: r.q }),
        el('p', { classe: 'note' }, [el('b', { texte: 'Ma réponse : ' }), S.qrc[i] ? S.qrc[i] : 'aucune réponse']),
        el('div', { classe: 'correction' }, [
          el('p', { classe: 'verdict', texte: 'Corrigé type' }), ul,
          el('p', { style: 'margin:.5rem 0 0' }, [el('b', { texte: 'Barème : ' }), r.b]),
          el('p', { classe: 'renvoi', style: 'margin-bottom:0', texte: 'À revoir dans le livre : fiche ' + r.ref })]),
        el('div', { classe: 'option-chrono' }, [el('label', { 'for': L + '-auto' + i, style: 'margin:0', texte: 'Mes points, selon le barème' }), sel])
      ]));
    });
    majResume();
    app.appendChild(el('div', { classe: 'actions' }, [el('a', { classe: 'bouton', href: '#sommaire', texte: 'Retour au sommaire et à mes notes' })]));
  }

  // ---------------------------------------------------------------- navigation
  function route() {
    var m = location.hash.match(/^#(ep|corr)-([A-G])$/);
    if (m && X.epreuves[m[2]]) (m[1] === 'ep' ? epreuve : correction)(m[2]);
    else sommaire();
    focusTitre();
  }
  document.title = ty('Examen blanc n° ' + X.numero + ' · Révision VTC');
  window.addEventListener('hashchange', route);
  route();
})();
