/* revision-vtc.fr : fiches d'entraînement tirées du livre (rubrique QCM VTC et page du livre).
   Sans ce script, la fiche et tout son corrigé restent lisibles (et indexés par les moteurs).
   Avec lui, la fiche se joue comme dans le livre : confiance, un ou plusieurs QCM corrigés au clic,
   réponse rédigée comparée au corrigé type (l'élève compte ses points) quand la fiche en a une,
   puis bilan et dates de révision J+1, J+3, J+7, J+21.
   « Pour aller plus loin » décale la frise horaire du corrigé (schéma « frise-attente »).
   Rien n'est enregistré : la fiche repart de zéro à chaque visite. */
(function () {
  "use strict";

  function heure(mn) { var h = Math.floor(mn / 60), m = mn % 60; return h + " h" + (m ? " " + (m < 10 ? "0" : "") + m : ""); }
  function dateJ(n) {
    var d = new Date(); d.setDate(d.getDate() + n);
    return d.toLocaleDateString("fr-FR", { weekday: "long", day: "numeric", month: "long" });
  }
  var CONF = { sur: "sûr", hesitant: "hésitant", hasard: "au hasard" };
  var reduit = function () { return matchMedia("(prefers-reduced-motion: reduce)").matches; };

  document.querySelectorAll(".fiche-essai").forEach(function (fiche) {
    var code = fiche.dataset.code, etat = { conf: null, rep: {}, pts: 0 };
    var q = function (sel) { return fiche.querySelector(sel); };
    var ouvrir = function (nom) { var e = q('[data-etape="' + nom + '"]'); if (e) e.classList.add("ouvert"); return e; };
    var amener = function (el) { if (!el) return; el.setAttribute("tabindex", "-1"); el.focus({ preventScroll: true }); el.scrollIntoView({ behavior: reduit() ? "auto" : "smooth", block: "start" }); };
    var groupes = fiche.querySelectorAll("fieldset[data-qcm]");
    var aQrc = !!q('[data-etape="qrc"]');

    fiche.classList.add("fiche-js");
    fiche.querySelectorAll("[data-js]").forEach(function (e) { e.hidden = false; });
    var rep = q('[data-role="plus-loin"]'); if (rep) rep.hidden = true;

    fiche.querySelectorAll('input[name$="-conf"]').forEach(function (r) {
      r.addEventListener("change", function () { etat.conf = r.value; });
    });

    groupes.forEach(function (g) {
      var i = g.dataset.qcm, juste = g.dataset.juste, options = g.querySelectorAll('input[type="radio"]');
      options.forEach(function (r) {
        r.addEventListener("change", function () {
          if (etat.rep[i]) return;
          etat.rep[i] = r.value;
          options.forEach(function (o) {
            var lab = o.closest("label"), v = lab.querySelector(".verdict");
            o.disabled = true;
            if (o.value === juste) { lab.classList.add("rep", "juste"); v.textContent = o === r ? "Votre réponse : juste" : "La bonne réponse"; }
            else if (o === r) { lab.classList.add("rep", "faux"); v.textContent = "Votre réponse : fausse"; }
          });
          var bloc = ouvrir("qcm-" + i), verdict = bloc.querySelector('[data-role="verdict"]');
          verdict.textContent = (r.value === juste ? "Juste. " : "Pas cette fois. ") + verdict.textContent.replace(/^(Juste|Pas cette fois)\. /, "");
          if (Object.keys(etat.rep).length === groupes.length) ouvrir(aQrc ? "qrc-question" : "suite");
          amener(verdict);
        });
      });
    });

    var cases = fiche.querySelectorAll('input[name$="-pt"]'), score = q('[data-role="score"]');
    cases.forEach(function (c) {
      c.addEventListener("change", function () {
        etat.pts = 0;
        cases.forEach(function (x) { if (x.checked) etat.pts += +(x.dataset.valeur || 1); });
        score.textContent = etat.pts;
      });
    });

    fiche.addEventListener("click", function (ev) {
      var b = ev.target.closest("[data-action]"); if (!b) return;
      var action = b.dataset.action;
      if (action === "qrc") { amener(ouvrir("qrc").querySelector(".fiche-verdict")); }
      if (action === "bilan") {
        ouvrir("bilan");
        var nbQ = groupes.length, justes = 0;
        groupes.forEach(function (g) { if (etat.rep[g.dataset.qcm] === g.dataset.juste) justes++; });
        var tousJustes = justes === nbQ, total = aQrc ? +q('[data-etape="qrc"]').dataset.total : 0, qrcOk = !aQrc || etat.pts === total;
        var resume = (nbQ > 1 ? "QCM : " + justes + " sur " + nbQ + " justes." : "QCM : " + (tousJustes ? "juste." : "faux."));
        if (aQrc) resume += " Réponse rédigée : " + etat.pts + " / " + total + ".";
        resume += " Confiance : " + (etat.conf ? CONF[etat.conf] : "non indiquée") + ".";
        q('[data-role="resume"]').textContent = resume;
        var conseil;
        if (tousJustes && etat.conf === "sur" && qrcOk) conseil = "Règle acquise. Les révisions espacées servent à la garder jusqu'au jour de l'examen.";
        else if (!tousJustes && etat.conf === "sur") conseil = "Vous étiez sûr, et ce n'était pas juste : c'est la fiche à revoir en priorité, car ce genre d'erreur se répète le jour de l'examen.";
        else if (tousJustes && etat.conf !== "sur") conseil = "Bonne réponse, mais sans certitude : relisez la règle à retenir jusqu'à ce qu'elle devienne un réflexe.";
        else if (!qrcOk) conseil = "Il manque un élément à votre réponse rédigée : à l'examen, chaque élément de la règle rapporte des points.";
        else conseil = "Relisez le corrigé et la règle à retenir, puis refaites la fiche demain.";
        q('[data-role="conseil"]').textContent = conseil;
        var ul = q('[data-role="revisions"]'); ul.textContent = "";
        [1, 3, 7, 21].forEach(function (n) {
          var li = document.createElement("li"), b2 = document.createElement("b");
          b2.textContent = "J+" + n; li.appendChild(b2); li.appendChild(document.createTextNode(dateJ(n))); ul.appendChild(li);
        });
        amener(q(".fiche-bilan h4"));
        try { if (window.goatcounter && window.goatcounter.count) window.goatcounter.count({ path: "fiche-" + code + "-bilan", title: "Fiche " + code + " terminée", event: true }); } catch (e) {}
      }
      if (action === "plus-loin") {
        rep.hidden = false; b.closest("p").hidden = true;
        var svg = q("svg.frise");
        if (svg && +svg.dataset.retard) {
          var d = +svg.dataset.debut, f = +svg.dataset.fin, x0 = +svg.dataset.x0, x1 = +svg.dataset.x1;
          var x = function (mn) { return x0 + (mn - d) * (x1 - x0) / (f - d); };
          var prise = +svg.dataset.prise + +svg.dataset.retard, lim = prise - +svg.dataset.avance;
          var zi = svg.querySelector('[data-role="interdit"]'), zp = svg.querySelector('[data-role="permis"]');
          zi.style.width = (x(lim) - x0) + "px"; zi.setAttribute("width", x(lim) - x0);
          zp.style.x = x(lim) + "px"; zp.setAttribute("x", x(lim));
          zp.style.width = (x(prise) - x(lim)) + "px"; zp.setAttribute("width", x(prise) - x(lim));
          svg.querySelector('[data-role="limite"]').style.transform = "translateX(" + x(lim) + "px)";
          svg.querySelector('[data-role="prise"]').style.transform = "translateX(" + x(prise) + "px)";
          svg.querySelector('[data-role="t-limite"]').textContent = heure(lim);
          svg.querySelector('[data-role="t-prise"]').textContent = heure(prise);
          var note = document.createElement("span");
          note.textContent = " La frise du corrigé ci-dessus montre le nouvel horaire : prise en charge à " + heure(prise) + ", stationnement aux abords permis à partir de " + heure(lim) + ".";
          rep.appendChild(note);
        }
      }
    });
  });
})();
