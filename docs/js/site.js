/* revision-vtc.fr : scripts communs à toutes les pages.
   0. Menu sur téléphone (défilement horizontal) : la rubrique en cours est amenée à l'écran, et la flèche
      du bord droit (« il reste des rubriques ») disparaît quand on arrive au bout (classe « au-bout »).
   1. Menu « Le livre » (balise details) : se ferme avec Échap ou un clic ailleurs.
   2. En-tête collant : classe « defile » dès qu'on a quitté le haut de la page (en-tête resserré), jauge de lecture
      (variable --lu, de 0 à 1) et, sur téléphone, en-tête rangé en descendant et rappelé en remontant (« entete-cachee »),
      jamais quand le menu « Le livre » est ouvert ou qu'un élément de l'en-tête a le focus. */
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
      var ouvert = entete.querySelector("details[open]") || entete.contains(document.activeElement);
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

  var menu = document.querySelector(".menu-livre");
  if (menu) {
    document.addEventListener("click", function (e) {
      if (menu.open && !menu.contains(e.target)) menu.open = false;
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.open) {
        menu.open = false;
        menu.querySelector("summary").focus();
      }
    });
  }
})();
