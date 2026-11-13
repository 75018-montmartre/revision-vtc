/* revision-vtc.fr · simulateur « coût de revient de la voiture VTC et revenu net »
   Les hypothèses par défaut et leurs sources sont dans contenu/simulateur.json, injectées dans la page
   (balise <script id="simu-donnees" type="application/json">). Rien n'est envoyé : tout est calculé ici. */
(function (racine) {
  'use strict';

  /* ---------- le calcul (aussi utilisé par les tests) ---------- */
  /* TVA (régime de croisière, année complète) :
     - chiffre d'affaires au-delà du seuil majoré (41 250 €) : plus de franchise ; TVA de 10 % comprise dans le prix des courses,
       à reverser, moins la TVA récupérable (20 %) sur le loyer, l'achat, l'entretien et le carburant d'un véhicule affecté au VTC ;
       cotisations et abattement sur le chiffre d'affaires hors taxe ; la TVA autoliquidée sur la commission est collectée et déduite ;
     - entre 37 500 € et 41 250 € : franchise cette année, TVA due l'année suivante (alerte seulement) ;
     - en franchise : rien à facturer, mais la TVA de 20 % sur une commission facturée depuis l'étranger (Uber, Bolt) est due sans déduction. */
  function calculer(e, d, sansSeuil) {
    var v = d.valeurs, semaines = e.semaines, c = e.commission / 100;
    var verse = e.verse_semaine * semaines;                 // montant versé par les plateformes sur l'année
    var prixClients = c < 1 ? verse / (1 - c) : verse;      // prix payé par les clients, commission comprise
    var commission = prixClients - verse;
    var caBrut = e.base === 'verse' ? verse : prixClients;   // chiffre d'affaires retenu, taxes comprises
    var redevable = caBrut > v.seuil_tva.majore;
    var tN = v.taux_tva_normal.valeur / 100, tT = v.taux_tva_transport.valeur / 100;
    var tvaCollectee = redevable ? caBrut * tT / (1 + tT) : 0;
    var ca = caBrut - tvaCollectee;                          // chiffre d'affaires hors taxe : base des cotisations
    var etranger = e.etranger !== false;
    var tauxCma = e.cma === 'moselle' ? v.taux_cma.moselle : e.cma === 'rhin' ? v.taux_cma.bas_haut_rhin : v.taux_cma.valeur;
    var tauxCotis = e.acre ? v.taux_acre.valeur : v.taux_cotisations.valeur;   // Acre : cotisations sociales seulement
    var tauxSocial = tauxCotis + v.taux_formation.valeur + tauxCma;
    var social = ca * tauxSocial / 100;
    var vl = e.vl ? ca * v.taux_vl.valeur / 100 : 0;

    var loyer = 0, amortissement = 0;
    if (e.mode === 'location') loyer = e.loyer_semaine * 52;
    else if (e.mode === 'lld') loyer = e.loyer_mois * 12;
    else amortissement = e.duree_ans > 0 ? Math.max(e.prix_achat - e.revente, 0) / e.duree_ans : 0;
    var electrique = e.energie === 'electricite';
    var energie = e.km_an * (electrique ? e.conso_elec : e.conso_thermique) / 100 * e.prix_energie;
    var assurance = e.assurance;
    var entretien = e.entretien_mois * 12;
    var voiture = loyer + amortissement + energie + assurance + entretien;   // montants payés, TVA comprise
    var reglementaire = v.reglementaire_5ans.valeur / 5;
    var autres = e.autres_mois * 12;
    var cfe = e.cfe || 0;
    var frais = voiture + reglementaire + autres + cfe;

    // TVA récupérable (redevable seulement) : loyer, achat (et TVA due à la revente, d'où le prix net), entretien, carburant ;
    // pas l'électricité rechargée à domicile (facture au nom du particulier), ni l'assurance (sans TVA), ni les autres frais (inconnus)
    var tvaRecuperee = 0, tvaCommission = 0;
    if (redevable) {
      tvaRecuperee = (loyer + amortissement + entretien + (electrique ? 0 : energie)) * tN / (1 + tN);
      if (!etranger) tvaRecuperee += commission * tN / (1 + tN);     // commission d'une plateforme française, TVA facturée
    } else if (etranger) {
      tvaCommission = commission * tN;                                // autoliquidée, sans droit à déduction en franchise
    }
    var tva = tvaCollectee - tvaRecuperee + tvaCommission;
    var net = verse - social - vl - tva - frais;

    // seuil de rentabilité : plus petit montant versé par semaine qui donne un revenu net positif (calcul pas à pas)
    var seuilSemaine = Infinity, seuilSaut = false;   // seuilSaut : le revenu passe d'un coup sous zéro juste en dessous du seuil
    if (!sansSeuil && semaines > 0) {
      var essai = function (x) { var o = {}; for (var k in e) o[k] = e[k]; o.verse_semaine = x; return calculer(o, d, true).net; };
      for (var bas = 0, haut = 10; haut <= 20000; bas = haut, haut += 10) {
        if (essai(haut) >= 0) {
          for (var i = 0; i < 40; i++) { var m = (bas + haut) / 2; if (essai(m) >= 0) haut = m; else bas = m; }
          seuilSemaine = haut; seuilSaut = essai(haut - 0.5) < -100; break;
        }
      }
    }
    var abattement = Math.max(ca * v.abattement.valeur / 100, Math.min(305, ca));

    return {
      verse: verse, prixClients: prixClients, commission: commission, caBrut: caBrut, ca: ca, tauxSocial: tauxSocial,
      social: social, vl: vl, tvaCollectee: tvaCollectee, tvaRecuperee: tvaRecuperee, tvaCommission: tvaCommission, tvaNette: tva,
      loyer: loyer, amortissement: amortissement, energie: energie, assurance: assurance,
      entretien: entretien, voiture: voiture, reglementaire: reglementaire, autres: autres, cfe: cfe, frais: frais, net: net,
      netMois: net / 12, voitureKm: e.km_an > 0 ? voiture / e.km_an : null, voitureMois: voiture / 12,
      netHeure: e.heures > 0 && semaines > 0 ? net / (e.heures * semaines) : null,
      seuilSemaine: seuilSemaine, seuilSaut: seuilSaut,
      imposable: e.vl ? null : Math.max(ca - abattement, 0),
      tva: redevable ? 'redevable' : caBrut > v.seuil_tva.valeur ? 'base' : null,
      horsMicro: ca > v.seuil_micro.valeur
    };
  }
  racine.SimuVTC = { calculer: calculer };
  if (typeof document === 'undefined') return;

  /* ---------- la page ---------- */
  var form = document.getElementById('simu');
  var source = document.getElementById('simu-donnees');
  if (!form || !source) return;
  var D = JSON.parse(source.textContent), V = D.valeurs;
  // nombres à la française, comme le reste du site : espace fine entre les milliers dès 1 000, virgule décimale
  function fr(x, dec) {
    var s = Math.abs(x).toFixed(dec), p = s.split('.');
    return (x < 0 && Number(s) !== 0 ? '\u2212\u00A0' : '') + p[0].replace(/\B(?=(\d{3})+(?!\d))/g, '\u202F') + (p[1] ? ',' + p[1] : '');
  }
  var euro = { format: function (x) { return fr(x, 0) + '\u00A0€'; } };
  var euroCts = { format: function (x) { return fr(x, 2) + '\u00A0€'; } };
  var nombre = { format: function (x) { return fr(x, 2).replace(/,00$/, '').replace(/(,\d)0$/, '$1'); } };
  var $ = function (id) { return document.getElementById(id); };
  var CHAMPS = ['verse_semaine', 'commission', 'semaines', 'heures', 'km_an', 'loyer_semaine', 'loyer_mois', 'prix_achat', 'duree_ans',
                'revente', 'assurance', 'entretien_mois', 'conso_thermique', 'conso_elec', 'prix_energie', 'autres_mois', 'cfe'];
  var CHOIX = ['base', 'mode', 'energie', 'cma'];
  var touche = {};   // champs modifiés par la personne : on ne les remplace plus par une valeur par défaut

  function lireNombre(id) {
    var c = $(id), brut = c.value.replace(/\s| | |€|%/g, '').replace(',', '.');
    var n = brut === '' ? 0 : /^\d+(\.\d+)?$/.test(brut) ? Number(brut) : NaN, err = $('err-' + id);   // pas de « 1e3 » ni de signe
    var min = Number(c.dataset.min || 0), max = Number(c.dataset.max || 1e9);
    var ok = isFinite(n) && n >= min && n <= max;
    err.textContent = ok ? '' : 'Indiquez un nombre entre ' + nombre.format(min) + ' et ' + nombre.format(max) + '.';
    if (ok) c.removeAttribute('aria-invalid'); else c.setAttribute('aria-invalid', 'true');
    return ok ? n : null;
  }
  function choix(nom) { var r = form.querySelector('input[name="' + nom + '"]:checked'); return r ? r.value : null; }
  function poser(id, val) { if (!touche[id]) $(id).value = String(val).replace('.', ','); }

  // valeurs par défaut qui dépendent d'un choix : assurance selon la formule, prix selon l'énergie
  function defautsLies() {
    var mode = choix('mode'), en = choix('energie');
    poser('assurance', mode === 'location' ? V.assurance_rc.valeur : V.assurance_complete.valeur);
    poser('prix_energie', en === 'electricite' ? V.prix_kwh.valeur : en === 'gazole' ? V.prix_gazole.valeur : V.prix_e10.valeur);
    document.querySelectorAll('[data-mode]').forEach(function (b) { b.hidden = b.dataset.mode.split(' ').indexOf(mode) < 0; });
    document.querySelectorAll('[data-energie]').forEach(function (b) { b.hidden = (b.dataset.energie === 'electricite') !== (en === 'electricite'); });
    $('unite-prix_energie').textContent = en === 'electricite' ? '(€ par kWh)' : '(€ par litre)';
    $('aide-assurance-location').hidden = mode !== 'location';
    $('aide-assurance-complete').hidden = mode === 'location';
  }

  function ligne(t, libelle, montant, classe) {
    var tr = document.createElement('tr');
    if (classe) tr.className = classe;
    var th = document.createElement('th'); th.scope = 'row'; th.textContent = libelle;
    var td = document.createElement('td'); td.className = 'nombre'; td.textContent = montant;
    tr.appendChild(th); tr.appendChild(td); t.appendChild(tr);
  }

  var minuterie = null, caches = {};   // caches : champs masqués par le choix en cours, comptés à 0 et absents du lien
  function calculerEtAfficher(annoncer) {
    var e = {}, valide = true;
    caches = {};
    CHAMPS.forEach(function (id) {
      var bloc = $(id).closest('[hidden]');
      if (bloc) caches[id] = true;
      var n = bloc ? 0 : lireNombre(id);
      if (n === null) valide = false;
      e[id] = n;
    });
    CHOIX.forEach(function (n) { e[n] = choix(n); });
    e.vl = $('vl').checked;
    e.etranger = $('etranger').checked;
    e.acre = $('acre').checked;
    if (!valide) {   // jamais d'ancien résultat à côté d'une saisie fausse
      $('simu-etat').textContent = 'Corrigez les champs signalés pour voir le résultat.';
      ['res-net', 'barre-res-net', 'res-km', 'res-voiture-mois', 'res-seuil'].forEach(function (id) { $(id).textContent = '\u2014'; });
      ['res-net-an', 'barre-texte', 'res-impot'].forEach(function (id) { $(id).textContent = ''; });
      $('res-detail').textContent = ''; $('res-alertes').textContent = ''; $('res-heure-bloc').hidden = true;
      return;
    }
    var r = calculer(e, D), mois = function (x) { return euro.format(x / 12); };

    $('res-net').textContent = euro.format(r.netMois);
    $('barre-res-net').textContent = euro.format(r.netMois);
    $('res-net-an').textContent = euro.format(r.net) + ' par an, avant impôt sur le revenu' + (e.vl ? ' (versement libératoire déduit)' : '');
    var corps = $('res-detail'); corps.textContent = '';
    if (e.base !== 'verse') ligne(corps, 'Prix payé par les clients', mois(r.prixClients));
    ligne(corps, 'Commission des plateformes', '\u2212\u00A0' + mois(r.commission));
    ligne(corps, 'Versé par les plateformes', mois(r.verse), 'sous-total');
    if (r.tva === 'redevable') ligne(corps, 'TVA à reverser (10 % des courses, moins la TVA récupérée)', '\u2212\u00A0' + mois(r.tvaNette));
    else if (r.tvaCommission) ligne(corps, 'TVA sur la commission (autoliquidée, 20 %)', '\u2212\u00A0' + mois(r.tvaCommission));
    ligne(corps, 'Cotisations et contributions (' + nombre.format(r.tauxSocial) + ' %' + (r.tva === 'redevable' ? ' du hors taxe' : '') + (e.acre ? ', avec l’Acre' : '') + ')', '\u2212\u00A0' + mois(r.social));
    if (e.vl) ligne(corps, 'Impôt : versement libératoire', '\u2212\u00A0' + mois(r.vl));
    if (r.loyer) ligne(corps, e.mode === 'location' ? 'Location de la voiture' : 'Loyer LLD ou LOA', '\u2212\u00A0' + mois(r.loyer));
    if (r.amortissement) ligne(corps, 'Achat de la voiture (étalé)', '\u2212\u00A0' + mois(r.amortissement));
    ligne(corps, e.energie === 'electricite' ? 'Électricité' : 'Carburant', '\u2212\u00A0' + mois(r.energie));
    ligne(corps, 'Assurance', '\u2212\u00A0' + mois(r.assurance));
    if (r.entretien) ligne(corps, 'Entretien et pneus', '\u2212\u00A0' + mois(r.entretien));
    ligne(corps, 'Carte, registre, visite médicale', '\u2212\u00A0' + mois(r.reglementaire));
    if (r.autres) ligne(corps, 'Autres frais', '\u2212\u00A0' + mois(r.autres));
    if (r.cfe) ligne(corps, 'Cotisation foncière des entreprises (CFE)', '\u2212\u00A0' + mois(r.cfe));
    ligne(corps, 'Revenu net', mois(r.net), 'total');

    $('res-km').textContent = r.voitureKm === null ? '\u2014' : euroCts.format(r.voitureKm);
    $('res-voiture-mois').textContent = euro.format(r.voitureMois);
    $('res-seuil').textContent = isFinite(r.seuilSemaine) ? euro.format(Math.ceil(r.seuilSemaine)) : '\u2013';   // arrondi au-dessus : au seuil affiché, le revenu est positif
    $('res-heure-bloc').hidden = r.netHeure === null;
    if (r.netHeure !== null) $('res-heure').textContent = euroCts.format(r.netHeure);

    // où vont 100 € versés par les plateformes (barre empilée, doublée d'un texte)
    var parts = [['social', r.social + r.vl + r.tvaNette], ['voiture', r.voiture], ['autres', r.reglementaire + r.autres]], reste = Math.max(r.net, 0);
    var total = Math.max(r.verse, 1);
    parts.forEach(function (p) { $('barre-' + p[0]).style.flexBasis = Math.min(p[1] / total * 100, 100) + '%'; });
    $('barre-net').style.flexBasis = (reste / total * 100) + '%';
    var pc = function (x) { return Math.round(x / total * 100); };
    $('barre-texte').textContent = 'Sur 100 € versés par les plateformes : ' + pc(r.social + r.vl + r.tvaNette) + ' € de prélèvements (cotisations' + (r.tvaNette ? ' et TVA' : '') + '), ' + pc(r.voiture) +
      ' € pour la voiture, ' + pc(r.reglementaire + r.autres) + ' € d’autres frais, ' + (r.net > 0 ? pc(r.net) + ' € de revenu net.' : 'rien ne reste : les frais dépassent les recettes.');

    // alertes
    var al = [];
    if (r.net < 0) al.push('Avec ces chiffres, l’activité perd de l’argent : les frais dépassent ce que versent les plateformes.');
    if (r.tva === 'redevable') al.push('Votre chiffre d’affaires annuel (' + euro.format(r.caBrut) + ') dépasse 41 250 € : vous n’êtes plus en franchise de TVA. Le résultat, calculé pour une année complète, déduit la TVA de 10 % comprise dans le prix des courses et compte la TVA récupérable sur la voiture et le carburant. La première année, la TVA n’est due qu’à partir du jour du dépassement.');
    else if (r.tva === 'base') al.push('Votre chiffre d’affaires annuel (' + euro.format(r.caBrut) + ') dépasse 37 500 € : vous restez en franchise de TVA cette année, mais la TVA sera due l’année suivante. Ce résultat est celui d’une année en franchise.');
    if (r.seuilSaut) al.push('Le seuil de rentabilité tombe sur la sortie de la franchise de TVA : juste en dessous, la TVA sur la commission, qui ne se récupère pas en franchise, fait passer le revenu sous zéro.');
    if (r.horsMicro) al.push('Au-delà de 83 600 € de chiffre d’affaires, le régime micro ne s’applique plus après deux années de dépassement : demandez conseil à un expert-comptable.');
    if (!e.autres_mois) al.push('Les autres frais (téléphone, banque, lavage, péages, comptable…) sont à 0 € : indiquez-les pour un résultat complet, le revenu réel est plus bas.');
    if (e.acre) al.push('Avec l’Acre, le taux réduit ne dure que jusqu’à la fin du 3e trimestre civil qui suit le début d’activité : le résultat, calculé sur une année entière au taux réduit, est un maximum.');
    if (e.mode !== 'location' && !e.entretien_mois) al.push('L’entretien et les pneus ne sont pas comptés : indiquez un montant mensuel pour un résultat complet.');
    var zone = $('res-alertes'); zone.textContent = '';
    al.forEach(function (t) { var p = document.createElement('p'); p.className = 'note'; p.textContent = t; zone.appendChild(p); });
    $('res-impot').textContent = e.vl ? 'L’impôt sur le revenu est déjà payé par le versement libératoire.' :
      'Impôt sur le revenu non compté : il dépend de votre foyer. Revenu imposable après l’abattement de 50 % : ' + euro.format(r.imposable) + ' par an.';

    $('simu-etat').textContent = '';
    if (annoncer) {
      clearTimeout(minuterie);
      minuterie = setTimeout(function () { $('simu-annonce').textContent = 'Revenu net estimé : ' + euro.format(r.netMois) + ' par mois.'; }, 900);
    }
    try { history.replaceState(null, '', '?' + parametres(e)); } catch (x) { /* adresse inchangée */ }
  }

  // la simulation tient dans l'adresse de la page : on peut la garder en favori ou l'envoyer
  function parametres(e) {
    var p = new URLSearchParams();
    CHAMPS.concat(CHOIX).forEach(function (k) { if (!caches[k] && e[k] !== null && e[k] !== undefined) p.set(k, e[k]); });
    if (e.vl) p.set('vl', '1');
    if (!e.etranger) p.set('etranger', '0');
    if (e.acre) p.set('acre', '1');
    return p.toString();
  }
  function lireAdresse() {
    var p = new URLSearchParams(location.search);
    CHOIX.forEach(function (n) { var r = form.querySelector('input[name="' + n + '"][value="' + p.get(n) + '"]'); if (r) r.checked = true; });
    if (p.get('vl') === '1') $('vl').checked = true;
    if (p.get('etranger') === '0') $('etranger').checked = false;
    if (p.get('acre') === '1') $('acre').checked = true;
    CHAMPS.forEach(function (id) { if (p.has(id) && isFinite(Number(p.get(id)))) { $(id).value = String(p.get(id)).replace('.', ','); touche[id] = true; } });
  }

  lireAdresse();
  defautsLies();
  form.addEventListener('input', function (ev) {
    if (ev.target.type === 'text') touche[ev.target.id] = true;
    if (ev.target.type === 'radio') defautsLies();
    calculerEtAfficher(true);
  });
  form.addEventListener('submit', function (ev) { ev.preventDefault(); calculerEtAfficher(true); $('resultat').focus(); });
  $('simu-raz').addEventListener('click', function () {
    touche = {};
    form.reset();
    CHAMPS.forEach(function (id) { $(id).value = $(id).defaultValue; $(id).removeAttribute('aria-invalid'); $('err-' + id).textContent = ''; });
    defautsLies(); calculerEtAfficher(false);
    $('simu-annonce').textContent = 'Valeurs par défaut rétablies.';
  });
  $('simu-lien').addEventListener('click', function () {
    var ok = function () { $('simu-annonce').textContent = 'Lien de cette simulation copié.'; $('lien-etat').textContent = 'Lien copié.'; };
    if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(ok, function () { $('lien-etat').textContent = location.href; });
    else $('lien-etat').textContent = location.href;
  });
  form.hidden = false;
  $('resultat').hidden = false;
  $('detail-resultat').hidden = false;
  $('simu-sans-js').hidden = true;
  calculerEtAfficher(false);

  /* ---------- barre de résultat collante (téléphone et tablette, quand le résultat est sous le formulaire) ----------
     Elle ne masque jamais un champ ni le clavier : elle s'efface dès qu'un champ du formulaire a le focus,
     quand le clavier du téléphone réduit l'écran, et quand le résultat complet est déjà visible.
     Elle glisse depuis le bas, sauf si l'appareil demande moins d'animations (CSS). */
  var barre = $('barre-resultat'), petit = window.matchMedia('(max-width: 64rem)');
  var resultatVu = false;
  function clavierOuvert() {
    var vv = window.visualViewport;
    return !!vv && vv.height < window.innerHeight - 120;
  }
  function majBarre() {
    var champ = document.activeElement && form.contains(document.activeElement) && document.activeElement.matches('input, select, textarea');
    var montrer = petit.matches && !champ && !clavierOuvert() && !resultatVu;
    barre.classList.toggle('cachee', !montrer);
    document.documentElement.classList.toggle('avec-barre', montrer);
  }
  if (barre) {
    barre.hidden = false;
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { resultatVu = es[0].isIntersecting; majBarre(); }).observe($('resultat'));
    }
    form.addEventListener('focusin', majBarre);
    form.addEventListener('focusout', function () { setTimeout(majBarre, 0); });
    if (window.visualViewport) window.visualViewport.addEventListener('resize', majBarre);
    if (petit.addEventListener) petit.addEventListener('change', majBarre);
    barre.querySelector('a').addEventListener('click', function (ev) { ev.preventDefault(); $('resultat').scrollIntoView(); $('resultat').focus({ preventScroll: true }); });
    majBarre();
  }
})(typeof window !== 'undefined' ? window : globalThis);
