// Accès réservé aux lecteurs : une question dont la réponse est dans le livre.
// La réponse n'est pas écrite ici, seulement son empreinte SHA-256.
(function () {
  var CLE = 'mar-vtc-2027-acces';
  var EMPREINTE = '9f60d83e92d7ca4f038d58765514e5a84ddfa3ab9629cfb38e3f6c2ab5691202';

  function lire() {
    try { if (localStorage.getItem(CLE) === 'oui') return true; } catch (e) {}
    try { if (sessionStorage.getItem(CLE) === 'oui') return true; } catch (e) {}
    return false;
  }
  function ecrire() {
    try { localStorage.setItem(CLE, 'oui'); } catch (e) {}
    try { sessionStorage.setItem(CLE, 'oui'); } catch (e) {}
  }
  function normaliser(t) {
    return (t || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z]/g, '');
  }
  async function empreinte(t) {
    var d = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(t));
    return Array.from(new Uint8Array(d)).map(function (b) { return b.toString(16).padStart(2, '0'); }).join('');
  }
  async function verifier(reponse) {
    var ok = (await empreinte(normaliser(reponse))) === EMPREINTE;
    if (ok) ecrire();
    return ok;
  }
  window.Acces = { ouvert: lire, verifier: verifier };
})();
