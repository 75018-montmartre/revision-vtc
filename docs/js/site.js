/* revision-vtc.fr : scripts communs à toutes les pages.
   0. Menu sur téléphone (défilement horizontal) : la rubrique en cours est amenée à l'écran.
   1. Menu « Le livre » (balise details) : se ferme avec Échap ou un clic ailleurs.
   2. Carrousel de l'accueil : trois diapositives ; défilement automatique toutes les 8 s,
      arrêté au survol, quand le clavier est dedans, dès que l'on choisit une diapositive,
      avec le bouton « Mettre en pause », et jamais si l'appareil demande moins d'animations.
      Sans JavaScript, les trois diapositives s'affichent l'une sous l'autre. */
(function () {
  "use strict";

  var liste = document.querySelector(".nav ul"), courante = document.querySelector('.nav a[aria-current="page"]');
  if (liste && courante && liste.scrollWidth > liste.clientWidth) {
    var marge = parseFloat(getComputedStyle(liste).paddingLeft) || 0;
    var cible = courante.parentNode.offsetLeft - marge;
    if (courante.parentNode.offsetLeft + courante.offsetWidth > liste.clientWidth) liste.scrollLeft = cible;
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

  var c = document.querySelector(".carrousel");
  if (!c) return;
  var diapos = [].slice.call(c.querySelectorAll(".diapo"));
  var choix = [].slice.call(c.querySelectorAll(".carrousel-choix button"));
  var pause = c.querySelector(".carrousel-pause");
  var zone = c.querySelector(".diapos");
  var reduit = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var i = 0, arrete = reduit, survol = false, dedans = false;

  c.classList.add("js");
  c.querySelector(".carrousel-commandes").hidden = false;
  if (reduit) pause.hidden = true;

  function montre(n, annonce) {
    i = (n + diapos.length) % diapos.length;
    diapos.forEach(function (d, k) {
      d.classList.toggle("active", k === i);
      if ("inert" in d) d.inert = k !== i;
    });
    choix.forEach(function (b, k) {
      if (k === i) b.setAttribute("aria-current", "true");
      else b.removeAttribute("aria-current");
    });
    zone.setAttribute("aria-live", annonce ? "polite" : "off");
  }

  function arreter() {
    arrete = true;
    pause.textContent = "Reprendre le défilement";
  }

  choix.forEach(function (b, k) {
    b.addEventListener("click", function () { arreter(); montre(k, true); });
  });
  pause.addEventListener("click", function () {
    if (arrete) { arrete = false; pause.textContent = "Mettre en pause"; montre(i + 1, false); }
    else arreter();
  });
  c.addEventListener("mouseenter", function () { survol = true; });
  c.addEventListener("mouseleave", function () { survol = false; });
  c.addEventListener("focusin", function () { dedans = true; });
  c.addEventListener("focusout", function (e) { if (!c.contains(e.relatedTarget)) dedans = false; });

  montre(0, false);
  if (!reduit) {
    setInterval(function () {
      if (!arrete && !survol && !dedans && !document.hidden) montre(i + 1, false);
    }, 8000);
  }
})();
