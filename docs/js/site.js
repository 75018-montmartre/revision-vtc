/* revision-vtc.fr : scripts communs à toutes les pages.
   0. Menu sur téléphone (défilement horizontal) : la rubrique en cours est amenée à l'écran, et la flèche
      du bord droit (« il reste des rubriques ») disparaît quand on arrive au bout (classe « au-bout »).
   1. En-tête collant : classe « defile » dès qu'on a quitté le haut de la page (en-tête resserré), jauge de lecture
      (variable --lu, de 0 à 1) et, sur téléphone, en-tête rangé en descendant et rappelé en remontant (« entete-cachee »),
      jamais quand un élément de l'en-tête a le focus. */
(function () {
  "use strict";

  var nav = document.querySelector(".nav"), liste = document.querySelector(".nav ul"),
      courante = document.querySelector('.nav a[aria-current="page"]');
  if (liste && courante && liste.scrollWidth > liste.clientWidth) {
    var marge = parseFloat(getComputedStyle(liste).paddingLeft) || 0;
    var cible = courante.parentNode.offsetLeft - marge;
    if (courante.parentNode.offsetLeft + courante.offsetWidth > liste.clientWidth) liste.scrollLeft = cible;
  }
  if (nav && liste) {
    var auBout = function () {
      nav.classList.toggle("au-bout", liste.scrollLeft + liste.clientWidth >= liste.scrollWidth - 2);
    };
    liste.addEventListener("scroll", auBout, { passive: true });
    window.addEventListener("resize", auBout);
    auBout();
  }

  var entete = document.querySelector(".entete"), racine = document.documentElement;
  if (entete) {
    var avant = window.scrollY, petit = window.matchMedia("(max-width: 52rem)"), prevu = false;
    var hauteur = function () { racine.style.setProperty("--haut-entete", entete.offsetHeight + "px"); };
    var maj = function () {
      prevu = false;
      var y = Math.max(window.scrollY, 0), max = racine.scrollHeight - window.innerHeight;
      racine.classList.toggle("defile", y > 24);
      entete.style.setProperty("--lu", max > 0 ? Math.min(y / max, 1).toFixed(4) : 0);
      var ouvert = entete.contains(document.activeElement);
      if (!petit.matches || ouvert || y < 120) racine.classList.remove("entete-cachee");
      else if (y > avant + 6) racine.classList.add("entete-cachee");
      else if (y < avant - 6) racine.classList.remove("entete-cachee");
      avant = y;
    };
    window.addEventListener("scroll", function () { if (!prevu) { prevu = true; requestAnimationFrame(maj); } }, { passive: true });
    window.addEventListener("resize", function () { hauteur(); maj(); });
    entete.addEventListener("focusin", function () { racine.classList.remove("entete-cachee"); });
    hauteur(); maj();
  }

  /* barre de résultat collante des simulateurs (téléphone et tablette, sous 64rem ; #barre-resultat, #resultat, form.simu).
     Chaque simulateur remplit sa valeur ; ici, seulement quand la montrer. Elle ne masque jamais un champ ni le clavier :
     elle s'efface quand un champ de saisie a le focus (le clavier s'ouvre), quand le clavier réduit l'écran et quand le
     résultat est déjà visible ; elle reste affichée quand on coche un choix. Mouvement coupé si l'appareil le demande (CSS). */
  var barre = document.getElementById("barre-resultat"), formSimu = document.querySelector("form.simu"), res = document.getElementById("resultat");
  if (barre && formSimu && res) {
    var etroit = window.matchMedia("(max-width: 64rem)"), resultatVu = false;
    var clavierOuvert = function () { var vv = window.visualViewport; return !!vv && vv.height < window.innerHeight - 120; };
    var majBarre = function () {
      var a = document.activeElement;
      var saisie = a && formSimu.contains(a) && a.matches("input:not([type=radio]):not([type=checkbox]), select, textarea");
      var montrer = etroit.matches && !saisie && !clavierOuvert() && !resultatVu;
      barre.classList.toggle("cachee", !montrer);
      racine.classList.toggle("avec-barre", montrer);
    };
    barre.hidden = false;
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { resultatVu = es[0].isIntersecting; majBarre(); }).observe(res);
    formSimu.addEventListener("focusin", majBarre);
    formSimu.addEventListener("focusout", function () { setTimeout(majBarre, 0); });
    if (window.visualViewport) window.visualViewport.addEventListener("resize", majBarre);
    if (etroit.addEventListener) etroit.addEventListener("change", majBarre);
    barre.querySelector("a").addEventListener("click", function (ev) { ev.preventDefault(); res.scrollIntoView(); res.focus({ preventScroll: true }); });
    majBarre();
  }
})();
