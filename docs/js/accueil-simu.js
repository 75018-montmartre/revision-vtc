/* revision-vtc.fr · accueil : carte « Simulateur gratuit » avec deux curseurs.
   Même calcul que la page du simulateur (SimuVTC.calculer, js/simulateur.js), avec ses valeurs par défaut
   (balises simu-donnees et simu-defauts, écrites par outils/generer.py). Sans JavaScript, la carte garde l'exemple
   chiffré calculé par le générateur et les curseurs restent cachés. Rien n'est envoyé : tout est calculé ici. */
(function () {
  'use strict';
  var carte = document.getElementById('carte-simu');
  var donnees = document.getElementById('simu-donnees'), defauts = document.getElementById('simu-defauts');
  if (!carte || !donnees || !defauts || !window.SimuVTC) return;
  var D = JSON.parse(donnees.textContent), base = JSON.parse(defauts.textContent);
  var $ = function (id) { return document.getElementById(id); };
  var verse = $('cs-verse'), loyer = $('cs-loyer'), lien = $('cs-lien'), adresse = lien.getAttribute('href');
  var minuterie;

  // nombres à la française, comme le reste du site : espace fine entre les milliers, signe moins typographique
  function euros(x) {
    var s = Math.round(Math.abs(x)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
    return (Math.round(x) < 0 ? '− ' : '') + s + ' €';
  }

  function maj() {
    var e = {};
    for (var k in base) e[k] = base[k];
    e.verse_semaine = Number(verse.value);
    e.loyer_semaine = Number(loyer.value);
    var r = window.SimuVTC.calculer(e, D, true);
    $('cs-verse-val').textContent = euros(e.verse_semaine);
    $('cs-loyer-val').textContent = euros(e.loyer_semaine);
    verse.setAttribute('aria-valuetext', euros(e.verse_semaine) + ' par semaine');
    loyer.setAttribute('aria-valuetext', euros(e.loyer_semaine) + ' par semaine');
    $('cs-m-verse').textContent = euros(r.verse / 12);
    $('cs-m-retenues').textContent = '− ' + euros((r.verse - r.net) / 12);
    $('cs-m-net').textContent = euros(r.netMois);
    lien.setAttribute('href', adresse + '?verse_semaine=' + e.verse_semaine + '&loyer_semaine=' + e.loyer_semaine);
    clearTimeout(minuterie);   // une seule annonce quand le curseur s'arrête, pas une par cran
    minuterie = setTimeout(function () { $('cs-annonce').textContent = 'Il vous reste ' + euros(r.netMois) + ' par mois, avant impôt.'; }, 900);
  }

  $('cs-texte').textContent = 'Par mois, sur ' + base.semaines + ' semaines par an, voiture louée.';
  carte.querySelector('.carte-curseurs').hidden = false;
  verse.addEventListener('input', maj);
  loyer.addEventListener('input', maj);
  maj();
  clearTimeout(minuterie);   // pas d'annonce au chargement : seulement quand la personne bouge un curseur
})();
