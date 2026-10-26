# -*- coding: utf-8 -*-
"""Récapitulatif d'une mise à jour du site, envoyé par e-mail (lancé par GitHub Actions à chaque push sur main).

Le message contient : le récapitulatif écrit par la tâche (corps des messages de commit), la liste exacte
des pages ajoutées, modifiées ou supprimées avec leur adresse en ligne, et le lien vers les changements sur GitHub.
Les identifiants SMTP viennent des secrets GitHub ; ils ne sont jamais écrits dans le dépôt.
"""
import os, subprocess, smtplib, ssl, sys
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

SITE = "https://revision-vtc.fr/"
env = os.environ.get
if not (env("SMTP_UTILISATEUR") and env("SMTP_MOT_DE_PASSE") and env("RECAP_DESTINATAIRE")):
    print("Secrets SMTP absents : aucun e-mail envoyé.")
    sys.exit(0)

avant, apres = env("AVANT", ""), env("APRES", "HEAD")
if not avant or set(avant) == {"0"}:
    avant = apres + "~1"
plage = f"{avant}..{apres}"


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout


commits = git("log", "--reverse", "--format=%H%x1f%s%x1f%b%x1e", plage).strip("\x1e\n").split("\x1e")
commits = [c.strip("\n").split("\x1f") for c in commits if c.strip()]
changements = [l.split("\t") for l in git("diff", "--name-status", "--no-renames", plage).splitlines() if l]


def url(chemin):
    p = chemin[len("docs/"):]
    return SITE + (p[:-10] if p.endswith("index.html") else p)


import re


def principal(rev, chemin):
    """Le contenu propre de la page (balise <main>), sans l'en-tête ni le pied communs à tout le site."""
    try:
        t = git("show", f"{rev}:{chemin}")
    except subprocess.CalledProcessError:
        return ""
    m = re.search(r"<main.*?</main>", t, re.S)
    return re.sub(r"\s+", " ", m.group(0) if m else t)


pages = {"A": [], "M": [], "D": []}
mise_en_forme = 0
for etat, chemin in changements:
    if chemin.startswith("docs/") and chemin.endswith(".html") and not chemin.endswith("404.html") and etat[0] in pages:
        if etat[0] == "M" and principal(avant, chemin) == principal(apres, chemin):
            mise_en_forme += 1
            continue
        pages[etat[0]].append(chemin)

titre = commits[-1][1] if commits else "Mise à jour du site"
lignes = [f"Mise à jour de revision-vtc.fr, {formatdate(localtime=True)}", ""]
for _, sujet, corps in commits:
    lignes += ["=" * 70, sujet, "=" * 70]
    if corps.strip():
        lignes += [l for l in corps.strip().splitlines() if not l.startswith(("Co-Authored-By:", "Claude-Session:"))]
    lignes.append("")
noms = {"A": "Pages ajoutées", "M": "Pages dont le contenu a changé", "D": "Pages supprimées"}
for k in "AMD":
    if pages[k]:
        lignes.append(f"{noms[k]} ({len(pages[k])}) :")
        lignes += [f"  - {url(c)}" for c in sorted(pages[k])]
        lignes.append("")
if mise_en_forme:
    lignes += [f"Et {mise_en_forme} page(s) dont seuls la présentation, le menu ou le pied de page ont changé.", ""]
if not any(pages.values()) and not mise_en_forme:
    lignes += ["Aucune page du site n'a changé (modification technique ou de contenu source).", ""]
lignes += [f"Détail technique des changements : https://github.com/{env('DEPOT')}/compare/{avant[:12]}...{apres[:12]}", "",
           "Message envoyé automatiquement par le dépôt revision-vtc (GitHub Actions)."]

m = EmailMessage()
m["Subject"] = f"[revision-vtc.fr] {titre}"
m["From"] = f"Révision VTC <{env('SMTP_UTILISATEUR')}>"
m["To"] = env("RECAP_DESTINATAIRE")
m["Date"] = formatdate(localtime=True)
m["Message-ID"] = make_msgid(domain="revision-vtc.fr")
m.set_content("\n".join(lignes))
with smtplib.SMTP_SSL(env("SMTP_SERVEUR", "mail.gandi.net"), int(env("SMTP_PORT", "465")), context=ssl.create_default_context(), timeout=30) as s:
    s.login(env("SMTP_UTILISATEUR"), env("SMTP_MOT_DE_PASSE"))
    s.send_message(m)
print("Récapitulatif envoyé :", m["Subject"])
