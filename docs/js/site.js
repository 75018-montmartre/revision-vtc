/* revision-vtc.fr : scripts communs à toutes les pages.
   0. Menu sur téléphone (défilement horizontal) : la rubrique en cours est amenée à l'écran, et la flèche
      du bord droit (« il reste des rubriques ») disparaît quand on arrive au bout (classe « au-bout »).
   1. Menu « Le livre » (balise details) : se ferme avec Échap ou un clic ailleurs. */
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
