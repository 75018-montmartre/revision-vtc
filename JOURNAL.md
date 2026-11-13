# Journal des mises à jour de revision-vtc.fr

Chaque publication sur le site ajoute ici une entrée, la plus récente en haut : ce qui a été fait, les pages concernées et le lien vers le détail des changements.

Adresse à garder en favori : https://github.com/75018-montmartre/revision-vtc/blob/main/JOURNAL.md

---

## Vendredi 13 novembre 2026, 12 h 45 · Plus de rythme de publication promis, sur tout le site

- « Chaque semaine » retiré partout où il annonçait un rythme de publication : résumés de l'accueil et de la page À propos pour les moteurs de recherche, titre et résumé de l'Actualité VTC, flux RSS, page À propos, colonne « Je roule déjà » de l'accueil (« Ce qui change pour vous, au fil des textes »).
  - https://revision-vtc.fr/actualite/index.html
  - https://revision-vtc.fr/a-propos.html
- Gardé, car exact et sans promesse de publication : la comparaison des textes avec Légifrance chaque semaine, la veille du Journal officiel, les conseils aux chauffeurs (« notez chaque semaine… »).
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Vendredi 13 novembre 2026, 12 h 40 · Accueil : plus de rythme de publication promis

- Bandeau d'accueil : « tenu à jour chaque semaine » devient « tenu à jour régulièrement ».
- Bande des preuves : « Mis à jour chaque semaine : actualité le lundi, question-réponse le jeudi » devient « Mis à jour régulièrement : actualité, questions et guides » (la question est désormais quotidienne, et Benjamin ne veut plus de rythme promis sur le site).
  - https://revision-vtc.fr/
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Vendredi 13 novembre 2026, 12 h 30 · Audit visuel, lot 4 (finitions)

- 4.a Retours à la ligne équilibrés sur les titres et surtitres (`text-wrap:balance`), pas de mot seul en fin de paragraphe (`text-wrap:pretty`) ; jamais sur les pastilles, badges et boutons. Exemple : le titre du simulateur ne se coupe plus après « de ».
- 4.b Thème sombre : le bandeau d'accueil passe sur `--nuit-2` et se détache du fond de page ; la carte du simulateur du bandeau passe sur `--doux`.
- 4.c Bloc « Le livre Machine à Réussite » retiré du bandeau d'accueil (quatre propositions en concurrence) ; le livre reste en bas de page, dans le pied de page, dans les colonnes des pages intérieures et via « Préparer l'examen 2027 ». Règles CSS du bloc retirées.
- 4.d Quadrillage « plan de ville » réservé aux en-têtes de page et un peu plus visible (lignes à .18 au lieu de .12 ; .10 en sombre) ; les bandes grises de l'accueil gardent leur fond, sans quadrillage.
  - https://revision-vtc.fr/
- Vérifié : axe sans erreur sur 12 pages à 320, 768 et 1 366 px, en clair et en sombre, aucun débordement.
- Fin de l'audit visuel du 13 novembre 2026 (lots 1 à 4).
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Vendredi 13 novembre 2026, 10 h 32 · Article n° 9 (tâche tous les deux jours)

- Titre : « Le VTC en chiffres : combien de chauffeurs VTC en France, de courses, de candidats à l'examen ? »
- Page : https://revision-vtc.fr/dossiers/vtc-en-chiffres-nombre-chauffeurs-france.html (2 416 mots, épreuve F, sans photo)
- En bref : environ 71 300 chauffeurs VTC actifs sur les plateformes en 2024 (+27 %), plus de 100 millions de courses (+16 %), donc environ 9 % de courses en moins par chauffeur (notre calcul) ; près de 63 000 taxis (France entière) ; 74 % des VTC en Île-de-France ; près de 36 000 candidats aux examens taxi et VTC en 2025 (−33 %) ; 45 % des candidats VTC inscrits en 2024 avaient tout réussi en janvier 2026 ; 19 % de voitures VTC hybrides rechargeables, électriques ou à hydrogène, 11 % de diesel.
- Sources lues le jour même : SDES, rapports 2026 (29 juin 2026) et 2025 (18 juin 2025) de l'Observatoire national des T3P ; « Les chauffeurs des plateformes de VTC en 2024 » (13 novembre 2025) et « … en 2023 » (25 novembre 2024), pages HTML. PDF et fichiers de données non lus (outil refusé).
- Relecture indépendante : 51 points relevés, 46 confirmés, 0 contredit, 7 calculs refaits exacts ; 1 non trouvé retiré (CMA France comme source des données) ; 5 formulations précisées (date du minimum de 9 € ramenée à « début 2024 » car les deux publications du SDES divergent, période septembre-octobre 2024, taxis « France entière », « plus de 71 000 » pour le rapport 2026, lien de cause hybride nuancé).
- Écarté faute de certitude : nombre de cartes VTC valides et d'exploitants inscrits au registre (absents des pages lues), taux de réussite par épreuve, régions détaillées (PDF non lu), cartes délivrées en 2024 (texte et infographie du rapport 2025 divergent).
- Vérifié : axe sans erreur en clair et en sombre à 320 et 1 366 px (article et index des guides), aucun débordement ; page dans sitemap.xml, llms.txt et l'index des guides.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Vendredi 13 novembre 2026, 9 h 00 · Question VTC du jour

- Question : « TVA VTC : quel taux sur une course ? »
- Page : https://revision-vtc.fr/questions/2026-11-13-tva-vtc-taux-course.html
- Réponse courte : 10 %, le taux réduit que l'article 279 du Code général des impôts (point b quater) applique aux transports de voyageurs. Ce taux ne concerne que le chauffeur redevable de la TVA : en franchise en base, la course est facturée sans TVA.
- Apport : calcul de la TVA comprise (prix TTC divisé par 11, erreur des 10 % du TTC chiffrée), formules à l'heure soumises au taux normal selon le BOFiP, mention de facture en franchise et passage au CIBS au 1er janvier 2027.
- Sources lues le jour même : Légifrance, CGI articles 279 (version du 1er mars 2026) et 278 ; BOFiP BOI-TVA-LIQ-30-20-60 et ACTU-2026-00126 (7 octobre 2026) ; impots.gouv.fr (page modifiée le 14 octobre 2026) ; WebLex (9 septembre 2026) et LégiFiscal (26 août 2026). L3120-1 : texte du wiki, concordant avec le recueil T3P du ministère.
- Relecture indépendante : 33 affirmations confirmées, aucune retirée ; 1 citation corrigée (« de véritables contrats de transports », au pluriel) ; 5 formulations précisées (titre BOFiP, mention L.233-3 « peut aussi s'écrire », date du 30 juin 2028 attribuée au BOFiP, L3120-1, perte de la franchise).
- Écarté faute de certitude : le numéro de l'article du CIBS qui reprendra le taux de 10 % au 1er janvier 2027 (non trouvé) ; l'amendement du PLF 2027 sur la TVA à 5,5 % des transports publics (projet, texte non lu, taxis et VTC non mentionnés) ; l'arrêt de la CAA de Lyon du 26 mars 2026 (lu seulement via WebLex).
- Vérifié : axe sans erreur en clair et en sombre à 320 et 1 366 px sur la page et l'index FAQ VTC, aucun débordement ; page dans sitemap.xml, llms.txt, l'index FAQ VTC et l'accueil. Accueil : alerte axe « landmark-complementary-is-top-level » déjà présente avant.
- Script du réel : reseaux/reels/2026-11-13-tva-vtc-taux-course.txt
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Vendredi 13 novembre 2026, 2 h 10 · Audit visuel, lot 3 (relief unique, accueil, badge d'article)

- 3.a Relief : choix tranché par Benjamin, suivre l'audit. Tout ce qui se clique a désormais le même relief bleu nuit de 4 px (nouvelle partie 12 de `site.css`, jeton `--ombre-relief`) : boutons, bouton « Le livre », cartes des questions, guides, fiches et numéros, cartes-liens, sommaire du wiki, liens « Tous les… », carte du livre de l'accueil. Survol : +1 px ; clic : enfoncé ; immobile si l'appareil demande moins d'animations. L'ombre douce ne reste que sur les encadrés non cliquables. Les choix des formulaires restent sans relief. Remplace les décisions du 7 novembre (boutons à plat) et du 8 novembre (tuiles sans relief noir).
  - Nettoyage : anciennes règles de relief (partie 8), boutons à plat (partie 9), ombres douces et mouvements des tuiles cliquables (parties 10 et 11), animation de l'ancienne pastille fléchée, jeton `--ombre-tuile-survol`, variable `--hover` et espace vide réservé à la pastille sur les cartes de l'Actualité, tous retirés.
- 3.b Accueil : « Par où commencer ? » n'a plus qu'un niveau de cadre (liens en liste simple, filet, flèche →) ; « Je roule déjà » renvoie au guide du précompte des cotisations au lieu d'un 4e « Calculer mon revenu net ». « Réglementation VTC : l'essentiel » devient une liste sur deux colonnes avec le numéro d'article en pastille jaune (section de 1 158 à 880 px sur téléphone).
  - https://revision-vtc.fr/
- 3.c Pages du wiki (73) : le badge « Article L… » passe sur sa propre ligne au-dessus du titre ; il reste dans le `h1` (référencement inchangé).
- Vérifié : axe sans erreur sur 12 pages à 320, 768 et 1 366 px, en clair et en sombre, aucun débordement ; survol et clic mesurés, aucun déplacement en mouvement réduit ; contour clavier de 3 px sur les cartes.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Vendredi 13 novembre 2026, 1 h 30 · Audit visuel, lot 2 (simulateurs : formulaire en premier)

- Ordre des deux simulateurs : titre, chapeau d'une phrase (raccourci, aucune information perdue : l'idée « l'argent versé n'est pas un salaire » reste dans l'exemple chiffré), mention « rien n'est envoyé », puis directement le formulaire. « Comment ça marche » (étapes et glossaire), l'exemple (renommé « Un exemple chiffré », il ne vient plus « pour commencer ») ; « Comment s'en servir » et « La règle en bref » sont déplacés après le résultat. Rien n'est supprimé.
  - Premier champ du simulateur de revenu net : 763 px du haut sur ordinateur (environ 1 900 px avant), dans le premier écran sur téléphone.
  - https://revision-vtc.fr/simulateurs/cout-revient-revenu-net-vtc.html
  - https://revision-vtc.fr/simulateurs/calcul-note-examen-vtc.html
- Barre de résultat collante sur téléphone : ajoutée au calcul de la note (verdict) ; reste affichée quand on coche un choix (avant, elle disparaissait dès qu'un bouton radio avait le focus) ; toujours effacée quand on tape (clavier ouvert). Logique déplacée de `js/simulateur.js` vers `js/site.js`, commune aux deux.
- Choix coché (simulateurs, fiches et QCM) : bordure jaune de 2 px et fond jaune très pâle (nouveau jeton `--jaune-pale`, #FDF5DE en clair, #2C2615 en sombre) au lieu du jaune plein. Contraste du texte : 16,7:1 en clair, 12,8:1 en sombre.
- Vérifié : axe sans erreur sur 12 pages à 320, 768 et 1 366 px, en clair et en sombre, aucun débordement ; tests du simulateur et de la note passés.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Vendredi 13 novembre 2026, 1 h 05 · Audit visuel, lot 1 (défauts visibles)

- 1.a Panneau « Votre résultat » des deux simulateurs : il ne garde plus que l'essentiel et tient en entier à l'écran, sans barre de défilement interne (revenu net : 486 px de haut au lieu de 852 px coupés ; note : 467 px au plus au lieu de 1 395 px avec des notes faibles). Le détail (alertes TVA, seuil, autres frais à 0 €, tableau, impôt, « Copier le lien » ; conseils et tableau par épreuve) passe dans « Le détail de votre résultat », sous le formulaire. Le panneau collant s'arrête désormais sous l'en-tête collé (son titre passait dessous) et cesse d'être collant sous 38rem de hauteur d'écran.
  - https://revision-vtc.fr/simulateurs/cout-revient-revenu-net-vtc.html
  - https://revision-vtc.fr/simulateurs/calcul-note-examen-vtc.html
- 1.b Alignement : sur toutes les pages intérieures, fil d'Ariane, titre et contenu commencent au bord gauche du logo (115 px sur un écran de 1 366 px), et l'encadré de droite finit sur le bord du bouton « Le livre ». Le décalage était de 16 px (wiki, questions, simulateurs, QCM, index) et de 200 px sur les pages à une colonne (Contact, À propos, Le livre, mentions…), point non relevé par l'audit.
- 1.c Flèches : → pour les liens vers une page du site (boutons, « Le livre » de l'en-tête, tuiles, cartes-liens, « Tous les… »), ↗ seulement vers un autre site (Amazon, Légifrance…), choisi automatiquement selon l'adresse du lien. Nouveau jeton `--fleche-interne`. Annule la règle du 7 novembre 2026 « ↗ sur tous les boutons ».
- Fichiers : `docs/css/site.css`, `outils/generer.py`, `docs/js/simulateur.js`, `docs/js/calcul-note.js`, README (charte). Aucune page supprimée, aucune adresse changée.
- Vérifié : axe sans erreur sur 12 pages (accueil, wiki, deux simulateurs, QCM, FAQ, Contact, Le livre, index) à 320, 768 et 1 366 px, en clair et en sombre, aucun débordement horizontal ; tests du simulateur et du calcul de la note passés (401 cas Python / JavaScript identiques) ; focus sur le résultat après « Voir le résultat » ; flèches immobiles si l'appareil demande moins d'animations.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Jeudi 12 novembre 2026, 9 h 05 · Question VTC du jour

- Question : « Casier judiciaire VTC : quelles condamnations empêchent d'être chauffeur ? »
- Page : https://revision-vtc.fr/questions/2026-11-12-casier-judiciaire-vtc-condamnations.html
- Réponse courte : Trois familles de condamnations inscrites au bulletin n° 2 du casier judiciaire (article R3120-8 du Code des transports) : un délit routier puni de la perte de 6 points, la conduite sans permis ou malgré son annulation, et une peine criminelle ou d'au moins six mois de prison pour vol, escroquerie, violences, stupéfiants ou quelques autres infractions.
- Apport : la distinction délit / contravention (l'alcool sous 0,8 g/l coûte aussi 6 points mais n'est pas visé, les contraventions ne figurent pas au bulletin n° 2), quatre cas comparés, qui voit le bulletin n° 2, restitution de la carte en cours de carrière.
- Sources lues le jour même : Légifrance (R3120-8, R3120-6, L3120-2-1) ; Entreprendre.Service-Public.fr F31027 (vérifiée le 12 août 2026) ; Service-Public.fr F2881 « Alcool au volant » (27 août 2026) ; Justice.fr : « Devenir chauffeur VTC » (1er janvier 2026), « Casier judiciaire : présentation des trois bulletins » (20 octobre 2025), « barème des points retirés » (27 février 2026).
- Relecture indépendante : 24 affirmations confirmées, aucune retirée ; 1 contredite corrigée (mention « Légifrance non lisible » dans les sources : le relecteur l'a lu) ; 3 formulations précisées (conditions de la carte complétées par l'avis médical, « notamment » pour les professions visées, atteinte volontaire à la personne).
- Écarté faute de certitude : les délits routiers autres que l'alcool (stupéfiants, refus d'obtempérer, grand excès de vitesse : une seule source lue) ; l'effet du sursis sur le seuil de six mois ; les délais d'effacement du bulletin n° 2.
- Vérifié : axe sans erreur en clair et en sombre à 320 et 1 366 px sur la page et l'index FAQ VTC, aucun débordement ; page dans sitemap.xml, llms.txt, l'index FAQ VTC et l'accueil. Remarque : l'accueil garde une alerte axe « landmark-complementary-is-top-level » (règle de bonne pratique, déjà présente avant cette publication).
- Script du réel : reseaux/reels/2026-11-12-casier-judiciaire-vtc-condamnations.txt
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 11 novembre 2026, 10 h 40 · Article n° 8 (tâche tous les deux jours)

- Titre : « Épreuve pratique de l'examen VTC : déroulé étape par étape, grille sur 20 et causes d'ajournement »
- Page : https://revision-vtc.fr/dossiers/epreuve-pratique-examen-vtc.html (2 378 mots, épreuve X, sans photo)
- En bref : l'épreuve pratique est une mission de transport de 45 minutes au plus, dont 20 minutes au moins de conduite ; notée sur 20 (parcours 3, conduite 10, prise en charge et relation client 5, facturation 2, arrêté du 6 avril 2017, article 3) ; reçu à 12 sur 20 ; 6 minutes pour le GPS, le plan et le devis ; une intervention sur la double commande ou le volant arrête l'épreuve ; trois essais en un an, 120 € par nouveau passage en 2027.
- Sources lues le jour même : Légifrance, arrêté du 6 avril 2017 (articles 1, 2 et 3 ; annexes II et III bis non lisibles, publiées en image) ; arrêté du 11 août 2017 (copie CMA PACA) ; règlement d'examen des CMA de décembre 2024 (copie CMA Alsace) ; référentiel VTC de France compétences ; exament3p.fr, CMA Hauts-de-France, CMA Île-de-France (mise à jour du 30 octobre 2026).
- Relecture indépendante : 44 affirmations confirmées, aucune contredite, calculs refaits exacts ; 1 non trouvée reformulée (question touristique « sans doute posée » devient « le jury peut poser ») ; 3 formulations précisées (adresse lue « au plus » deux fois, ajournement « possible » pour les conditions non remplies, « minute par minute » retiré du titre).
- Écarté faute de certitude : la grille officielle détaillée de l'annexe III bis (image non lisible) ; le terminal de paiement (le référentiel le cite, le règlement ne l'impose pas au VTC) ; l'avis motivé sous quinze jours et la communication du jury trois jours ouvrés avant (décret n° 2021-202, version en vigueur non vérifiée).
- Page modifiée (lien seulement) : article n° 5, la section sur l'épreuve pratique renvoie au nouvel article.
- Vérifié : axe sans erreur en clair et en sombre à 320 et 1 366 px (article, index des guides, article n° 5), aucun débordement ; sitemap.xml et llms.txt contiennent la page.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 11 novembre 2026, 9 h 03 · Question VTC du jour

- Question : « Justificatif de réservation VTC : quelles sont les mentions obligatoires ? »
- Page : https://revision-vtc.fr/questions/2026-11-11-justificatif-reservation-vtc-mentions.html
- Réponse courte : Sept mentions, fixées par l'arrêté du 6 août 2025 : nom et coordonnées de l'exploitant, son numéro d'inscription au registre des VTC, son numéro unique d'identification (Siren), nom et téléphone du client, date et heure de la réservation, date et heure de prise en charge souhaitées, lieu de prise en charge. Le justificatif peut être sur papier ou sur écran.
- Sources lues le jour même : Entreprendre.Service-Public.fr F31027 (vérifiée le 12 août 2026) ; Légifrance : article 3 de l'arrêté du 6 août 2025, sommaire du JORF n° 200 du 29 août 2025, R3120-2, R3122-12, L3120-2, L3122-1, L3124-12, D3120-3 ; page du ministère « Taxi, VTC, VMDTR et CPA » (3 février 2026). Article 1er de l'arrêté : Légifrance refusé, texte du wiki (25 octobre 2026) concordant avec service-public.fr et deux sources secondaires.
- Relecture indépendante : 27 affirmations confirmées, aucune contredite ; 3 non trouvées, retirées ou reformulées (précision « délivré à l'immatriculation », phrase sur la carte professionnelle ; « désormais » nuancé pour Atout France).
- Écarté faute de certitude : date d'application de l'arrêté (29 octobre 2025 selon trois sources secondaires, « 30 août 2025 » dans le wiki, article 2 non lu) ; comparaison avec le justificatif des taxis (arrêté taxis non lu).
- Vérifié : axe sans erreur en clair et en sombre à 320 et 1 366 px sur la page et l'index FAQ VTC ; aucun débordement ; page dans sitemap.xml, llms.txt, l'index FAQ VTC et l'accueil.
- Script du réel : reseaux/reels/2026-11-11-justificatif-reservation-vtc-mentions.txt
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 11 novembre 2026, 7 h 55 · Veille du wiki (tâche du mercredi)

- **PROBLÈME : 50 articles sur 78 confirmés dans leur version en vigueur au 11 novembre 2026.** Légifrance a encore refusé de nombreuses pages (client_error) et l'outil de lecture ne recopie que 125 caractères à la fois (textes relus par morceaux puis recollés). Date « vérifié » laissée au 25 octobre 2026.
- Confirmés, texte identique : L3120-1, L3120-2, L3120-2-1, L3120-2-2, L3120-4, L3120-5, L3120-7, L3122-1, L3122-3, L3122-4, L3122-4-1, L3122-9, R3120-1, R3120-2, R3120-4, R3120-6, R3120-7, R3120-8, R3120-8-1, R3120-8-2, R3120-9, R3120-10, D3120-3, D3120-5, D3120-38, R3122-1, R3122-2, R3122-3, R*3122-5, R3122-6, R3122-7, R3122-8, R3122-9, R3122-12, L1326-1 à L1326-4, L3124-7, L3124-11, L3124-12, L3124-13, R3124-5, L3141-1, L3141-2, L3142-3, L3143-1, L3143-2, L3143-4, R3141-1.
- Texte identique, mais lu seulement sur une version datée (non confirmé au jour) : L3142-1, L3142-2, L3142-4 (17 juillet 2026), R3124-6, R3124-7 (26 juin 2025), R3124-1 (23 avril 2022), R3141-2 à R3141-7 (20 août 2022), R3124-4, R3124-11, R3124-12, R3124-13 (1er mai 2020), R3122-4, R3122-10 (3 octobre 2020), R3122-5-1 (décret de création de 2021).
- Non lus : D3120-21, D3120-32, L3143-3, L3143-5 (pages introuvables ou refusées) ; les 5 arrêtés n'ont pas pu être recopiés mot à mot (4 comparés par l'outil, sans écart de fond ni de date ; arrêté du 6 août 2025 non lu).
- Texte corrigé (découpage seulement, mots inchangés) : https://revision-vtc.fr/wiki/r3122-9.html, les quatre « -soit » deviennent quatre alinéas, comme sur Légifrance.
- Explications améliorées (première phrase reprise par Google) :
  - https://revision-vtc.fr/wiki/l3124-12.html : « Maraude, client pris sans réservation, démarchage ou conducteur sans carte VTC : c'est un délit puni de trois ans de prison et 45 000 € d'amende. »
  - https://revision-vtc.fr/wiki/r3120-8.html : « Casier judiciaire : certaines condamnations inscrites au bulletin n° 2 interdisent d'exercer… » ; ajout des peines criminelles, des condamnations étrangères et du refus de restituer le permis, oubliés jusqu'ici.
  - https://revision-vtc.fr/wiki/l3122-1.html : première phrase en forme de définition (« Exploitant VTC : celui qui met à la disposition de ses clients… »).
- Repéré sur Légifrance, hors wiki : R3122-11 abrogé par le décret n° 2026-764 du 5 août 2026 (depuis le 12 août 2026) ; L3142-5 en vigueur mais sans page ; L3141-3 et L3141-4 créés par la loi n° 2026-534 du 25 juin 2026, pas encore applicables.
- Contrôle technique : génération réussie, pages présentes dans le sitemap avec description et données structurées, llms.txt et llms-full.txt à jour, aucun lien interne cassé, axe sans erreur en clair et en sombre à 320 et 1366 px.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mardi 10 novembre 2026, 8 h 56 · Question VTC du jour

- Question : « Micro-entreprise VTC : quel est le plafond de chiffre d'affaires ? »
- Page : https://revision-vtc.fr/questions/2026-11-10-plafond-micro-entreprise-vtc.html
- Réponse courte : 83 600 € hors taxes par an, le seuil des prestations de services, fixé pour 2026, 2027 et 2028. Le dépasser une seule année ne fait pas sortir de la micro-entreprise : il faut le dépasser deux années civiles de suite, et la sortie a lieu le 1er janvier suivant.
- Sources lues le jour même : Entreprendre.Service-Public.fr F31027 (12 août 2026), F32353 (21 février 2026), A18813 (26 février 2026), F32887 (1er septembre 2024) ; CCI Paris Île-de-France (9 mars 2026) ; Bpifrance Création (février 2026).
- Relecture indépendante : 36 affirmations confirmées, aucune contredite ; 1 non trouvée retirée (cotisations « en pourcentage », remplacée par un simple renvoi) ; 1 nuance retirée (TVA non récupérable, vraie seulement en franchise).
- Écarté faute de certitude : article 50-0 du CGI et arrêté du 27 janvier 2026 non lus sur Légifrance (montants confirmés par service-public.fr et deux sources publiques concordantes) ; quel montant compte comme chiffre d'affaires pour les courses via plateforme.
- Vérifié : axe sans erreur en clair et en sombre à 320 et 1 366 px sur la page et l'index FAQ VTC ; aucun débordement ; page dans sitemap.xml et llms.txt.
- Script du réel : reseaux/reels/2026-11-10-plafond-micro-entreprise-vtc.txt
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Lundi 9 novembre 2026, 10 h 30 · Article n° 7 (tâche tous les deux jours)

- Titre : « Précompte des cotisations au 1er janvier 2027 : ce que les plateformes VTC prélèveront à votre place »
- Page : https://revision-vtc.fr/dossiers/precompte-cotisations-vtc-plateformes-2027.html (2 248 mots, épreuve B, sans photo)
- En bref : à partir du 1er janvier 2027, les plateformes retiennent les cotisations sociales des chauffeurs VTC en micro-entreprise sur les sommes qu'elles leur versent et les reversent à l'Urssaf (article L613-6-1 du Code de la sécurité sociale) ; ce n'est pas le prélèvement à la source de l'impôt, seul le versement libératoire est retenu en plus ; clients directs et CFE restent à la charge du chauffeur.
- Sources lues le jour même : Légifrance L613-6-1 et section L613-1 à L613-11 (notes d'entrée en vigueur) ; Entreprendre.Service-Public.fr A18550 (15 septembre 2026) et F36232 ; collectivites-locales.gouv.fr (CFE).
- Relecture indépendante : aucune affirmation contredite ; 9 précisions apportées (date du 1er janvier 2027 attribuée à la loi n° 2023-1250 art. 6, montants « hors petites taxes », réserve sur les plateformes volontaires, destinataire des données, sûretés).
- Écarté faute de certitude : délai exact pour un nouvel inscrit (arrêté non lu), traitement de l'Acre, taux 2027, contenu des pages Urssaf (refusées aux robots).
- Page modifiée : https://revision-vtc.fr/dossiers/cout-pour-devenir-chauffeur-vtc.html (l'annonce « un prochain article » devient un lien).
- Vérifié : axe sans erreur en clair et en sombre à 320 et 1 366 px (article et index des guides), aucun débordement ; sitemap.xml et llms.txt contiennent la page.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Lundi 9 novembre 2026, 8 h 57 · Question VTC du jour

- Question : « Carte VTC : où la placer dans la voiture ? »
- Page : https://revision-vtc.fr/questions/2026-11-09-carte-vtc-ou-la-placer.html
- Réponse courte : Sur le pare-brise ou, à défaut, sur le véhicule, de telle façon que la photographie soit facilement visible de l'extérieur, dès que le chauffeur utilise la voiture à titre professionnel (article R3120-6 du Code des transports). Quand il n'exerce pas son activité, il peut l'enlever.
- Sources lues le jour même : Code des transports R3120-6 (Légifrance, version en vigueur depuis le 12 août 2026, décret n° 2026-764) ; Entreprendre.Service-Public.fr F31027 (vérifiée le 12 août 2026) ; pages VTC des préfectures de l'Ardèche et des Hautes-Pyrénées.
- Relecture indépendante : 26 affirmations confirmées ; 1 corrigée (le délai de trois mois vaut pour toute demande, pas seulement la première) ; 2 précisions (« en substance » pour les préfectures, « Hors service ? » au lieu de « En week-end ? » dans le réel) ; la nature de la vignette, non relue aujourd'hui, est renvoyée à la question du 3 novembre.
- Écarté faute de certitude : les classes de contravention de l'article R3124-12 (Légifrance refusé aujourd'hui pour cet article) ; la page renvoie à l'article du wiki sans les citer.
- Vérifié : axe sans erreur en clair et en sombre à 320 et 1 366 px sur la page et l'index FAQ VTC ; aucun débordement. Accueil : 1 alerte axe déjà présente avant (landmark-complementary-is-top-level).
- Script du réel : reseaux/reels/2026-11-09-carte-vtc-ou-la-placer.txt
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Lundi 9 novembre 2026, 7 h 47 · Actualité VTC n° 6 (tâche du lundi)

- Page : https://revision-vtc.fr/actualite/2026-11-09.html
- Titre : « Accidents du travail des plateformes : projet au Sénat, examen VTC inchangé » (période du 8 au 9 novembre 2026).
- Textes officiels : aucun nouveau texte VTC repéré au Journal officiel n° 262 du 8 novembre 2026 (sommaire complet non lisible sur Légifrance ; deux textes lus et recherches par mots-clés). La page le dit.
- Examen : aucune nouveauté ; tarifs 2027 inchangés sur exament3p.fr (246 €, 171 €, 120 €) et sur la page de la CMA Île-de-France.
- Cotisations et statut : PLFSS 2027, la commission des affaires sociales du Sénat (4 novembre 2026) propose d'affilier les travailleurs des plateformes à la branche AT-MP au 1er janvier 2029, avec une contribution des plateformes (projet ; séance publique du 9 au 18 novembre 2026).
- Simulateur : prix des carburants à jour (7 novembre 2026, mise à jour automatique).
- Vérifié : axe sans erreur en clair et en sombre à 320 et 1 366 px, aucun débordement ; sitemap.xml et llms.txt contiennent le numéro.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Dimanche 8 novembre 2026, 8 h 55 · Question VTC du jour

- Question : « Chien guide d'aveugle en VTC : le chauffeur peut-il refuser ? »
- Page : https://revision-vtc.fr/questions/2026-11-08-chien-guide-vtc-refus.html
- Réponse courte : Non. La loi autorise l'accès aux transports des chiens guides d'aveugle et des chiens d'assistance qui accompagnent une personne handicapée titulaire de la carte prévue par la loi, et leur présence ne doit pas entraîner de facturation supplémentaire (article 88 de la loi n° 87-588 du 30 juillet 1987).
- Sources lues le jour même : loi n° 87-588, article 88 (version en vigueur depuis le 19 août 2026) ; CASF R241-23 ; Code rural L211-30 ; service-public.fr F35787 ; guide ministériel de mai 2025. R3120-1 recoupé avec Légifrance par la relecture.
- Relecture indépendante : toutes les affirmations confirmées, aucune contredite ; 2 précisions (auteur du guide, mention de la carte dans l'accroche du réel).
- Écarté faute de certitude : un montant d'amende présenté comme certain pour un VTC (le texte de sanction vise les « lieux ouverts au public » sans nommer les transports) ; la page le dit.
- Vérifié : axe sans erreur en clair et en sombre à 320 et 1 366 px sur la page et l'index FAQ VTC ; aucun débordement. Accueil : 1 alerte axe déjà présente avant cette publication (landmark-complementary-is-top-level).
- Script du réel : reseaux/reels/2026-11-08-chien-guide-vtc-refus.txt
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Dimanche 8 novembre 2026, 0 h 55 · QCM VTC : données structurées complétées

- Les 21 pages https://revision-vtc.fr/qcm/… : données structurées « Quiz » complétées (texte complet de chaque question avec sa situation, réponses numérotées, corrigé en commentaire, règle évaluée, alignement sur l'épreuve), après l'alerte « Champ text manquant » de Google Search Console. Contenu visible inchangé.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Dimanche 8 novembre 2026, 0 h 45 · Nouvelle rubrique QCM VTC (21 fiches du livre) et tuiles arrondies sur tout le site

- Nouvelle rubrique https://revision-vtc.fr/qcm/ (deuxième du menu) : 21 fiches d'entraînement tirées du livre, trois par épreuve écrite (A3.4, A3.2, A8.2 · B1.2, B3.2, B3.4 · C7.2, C4.2, C6.1 · D1.1, D1.3, D3.1 · E1.5, E3.1, E3.4 · F3.1, F3.4, F3.6 · G4.1, G3.1, G2.1), chacune jouable sur sa page (situation, confiance, QCM corrigé, réponse rédigée et barème, bilan, dates de révision). Texte recopié mot pour mot du livre et vérifié contre une seconde extraction : aucun écart. Fiches écartées faute de certitude aujourd'hui : B5.1, B5.2, B4.3 (chiffres 2027 à surveiller, sources en cours de correction), C5.6 (ZFE), D1.2 (dépend du texte d'une autre fiche), F4.2 (corrigé au passé pour une règle du 1er janvier 2027).
- Encadré « Testez-vous » sur les questions, guides et articles du wiki liés à une fiche ; lien vers la rubrique sur l'accueil (« Par où commencer ? ») et sous la fiche de la page du livre.
- Tout le site : tuiles arrondies à ombre douce à la place du relief noir, toutes de la même hauteur dans une liste, action en bas (« Lire la réponse », « Lire le guide », « Faire la fiche ») ; FAQ VTC et Guides VTC sur trois colonnes ; nouveau jaune #EDB321 ; pictogrammes en carré plein sans liseré ; menu à six rubriques sur une ligne.
- Vérifié : axe sans erreur en clair et en sombre à 320 et 1 366 px sur 21 pages ; aucun débordement ; deux fiches jouées jusqu'au bilan sans erreur de script.
- Règles du livre touchées : aucune.
- URL à indexer :
  https://revision-vtc.fr/qcm/
  https://revision-vtc.fr/qcm/a3-2-maraude-reservee-taxi.html
  https://revision-vtc.fr/qcm/a3-4-gares-aeroports.html
  https://revision-vtc.fr/qcm/a8-2-revenu-minimal-desactivation.html
  https://revision-vtc.fr/qcm/b1-2-micro-entreprise-regime-societe.html
  https://revision-vtc.fr/qcm/b3-2-cout-revient.html
  https://revision-vtc.fr/qcm/b3-4-seuil-rentabilite-point-mort.html
  https://revision-vtc.fr/qcm/c4-2-enfants-siege-place.html
  https://revision-vtc.fr/qcm/c6-1-proteger-alerter-secourir.html
  https://revision-vtc.fr/qcm/c7-2-periode-probatoire-activite-vtc.html
  https://revision-vtc.fr/qcm/d1-1-lire-texte-quatre-etapes.html
  https://revision-vtc.fr/qcm/d1-3-pieges-qcm-comprehension.html
  https://revision-vtc.fr/qcm/d3-1-fautes-orthographe-coutent-points.html
  https://revision-vtc.fr/qcm/e1-5-aeroport-gare-hotel.html
  https://revision-vtc.fr/qcm/e3-1-nombres-prix-heures.html
  https://revision-vtc.fr/qcm/e3-4-faux-amis-pieges-qcm.html
  https://revision-vtc.fr/qcm/f3-1-formule-monome-cout-revient.html
  https://revision-vtc.fr/qcm/f3-4-marge-taux-marge-taux-marque.html
  https://revision-vtc.fr/qcm/f3-6-forfaits-aeroport-mises-disposition.html
  https://revision-vtc.fr/qcm/g2-1-taille-puissance-lire-carte-grise.html
  https://revision-vtc.fr/qcm/g3-1-deux-vignettes-ou-quoi-comment.html
  https://revision-vtc.fr/qcm/g4-1-justificatif-reservation-sept-mentions.html
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 7 novembre 2026, 22 h 45 · Rythme vertical harmonisé sous les titres de bloc

- Tout le site : le premier texte d'un bloc tombe toujours à la même distance de son titre (19 px entre le bas du titre et la première ligne), qu'il s'agisse d'un paragraphe, d'étapes numérotées ou d'une liste de questions ; les encadrés (cartes, texte officiel, brèves) commencent tous à 16 px ; 48 px entre deux blocs partout.
- Vérifié par mesure sur les pages d'index, la page du livre, une question, un article du wiki et une Actualité ; axe sans erreur en clair et en sombre à 320 et 1 366 px.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 7 novembre 2026, 22 h 35 · Pages d'index : blocs les uns sous les autres, sur toute la largeur

- https://revision-vtc.fr/questions/, https://revision-vtc.fr/dossiers/, https://revision-vtc.fr/actualite/, https://revision-vtc.fr/wiki/, https://revision-vtc.fr/simulateurs/ : l'en-tête, les paragraphes et les blocs prennent toute la largeur de la grille de cartes (fini la colonne étroite collée à gauche). FAQ VTC et Guides VTC : blocs les uns sous les autres (présentation dans l'en-tête, étapes de lecture côte à côte, légende des épreuves sur toute la largeur), et non plus en deux colonnes. Guides VTC : le bloc des épreuves explique d'abord les pictogrammes, puis les mises à jour.
- Vérifié : aucun bloc plus étroit que la grille à 1 440 px ; axe sans erreur en clair et en sombre à 320 et 1 366 px ; aucun débordement.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 7 novembre 2026, 22 h 25 · FAQ VTC et Guides VTC : introduction alignée sur la grille

- https://revision-vtc.fr/questions/ et https://revision-vtc.fr/dossiers/ : l'introduction occupait une colonne étroite collée à gauche au-dessus d'une grille pleine largeur. Elle passe sur deux colonnes calées exactement sur les deux colonnes de cartes (à gauche : présentation et mode de lecture ; à droite : légende des épreuves). Une colonne sur téléphone. La page des guides reçoit aussi la légende des épreuves.
- Vérifié : bords des colonnes identiques à ceux des cartes (1 440 et 390 px) ; axe sans erreur en clair et en sombre à 320 et 1 366 px ; aucun débordement.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 7 novembre 2026, 22 h 10 · Pictogrammes des épreuves en panneaux

- Tout le site : les pictogrammes des épreuves (cartes de la FAQ VTC et des guides, légende des épreuves) passent en panneaux : plaque bleu nuit, liseré blanc, dessin jaune, sans lettre. Mêmes dessins qu'avant.
- Vérifié : axe sans nouvelle erreur en clair et en sombre à 320 et 1 366 px (FAQ VTC, guides, accueil).
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 7 novembre 2026, 22 h 30 · Encadrés « À retenir » en panneau, situation des fiches en bon de course

- Tout le site : les encadrés « À retenir » (FAQ VTC, guides, Actualité VTC, fiches) deviennent un panneau jaune à double filet bleu nuit, titre en onglet. Texte inchangé.
- https://revision-vtc.fr/le-livre.html : la situation de la fiche A3.4 passe en « bon de course » clair (en-tête gris, horaires en étiquettes, réplique dans une bulle) ; fin de la barre noire à gauche.
- Vérifié : axe sans nouvelle erreur en clair et en sombre à 320 et 1 366 px (page du livre, une question, un guide, une Actualité) ; aucun débordement.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 7 novembre 2026, 22 h 10 · Nouvelle barre de navigation, boutons à flèche, corrections de la page du livre

- Tout le site : nouvelle barre de navigation d'après la maquette « propal » (fond blanc, nom en capitales condensées, liens sobres soulignés de jaune, « Le livre » en bouton à contour avec flèche ↗). Libellés inchangés. En-tête toujours collé en haut, jauge de lecture et menu défilant sur téléphone conservés.
- Tout le site : boutons à plat, coins de 6 px, flèche ↗ intégrée ; couleurs inchangées (jaune pour l'achat).
- https://revision-vtc.fr/le-livre.html : « Déjà lecteur ? » sur une ligne à part, sous un filet, avec deux liens (mises à jour, signalement) ; formulaire de signalement : les deux champs du haut sont alignés (aide placée au-dessus du champ) ; exemple corrigé « A3.4, page 66 ».
- Vérifié : axe sans nouvelle erreur en clair et en sombre à 320 et 1 366 px (accueil, page du livre, contact, simulateur, wiki) ; aucun débordement.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 7 novembre 2026, 21 h 20 · Nouvelle page du livre, avec une fiche à essayer

- https://revision-vtc.fr/le-livre.html devient une vraie page de présentation du livre : présentation et achat, la fiche A3.4 « Gares et aéroports » à essayer (situation, confiance, QCM corrigé au clic, réponse rédigée comparée au corrigé type, bilan et dates de révision), trois visuels des pages du livre, la méthode, les engagements de vérification, les questions des acheteurs. L'inscription aux mises à jour et le signalement d'erreurs sont regroupés en bas, dans l'« Espace lecteurs » (mêmes ancres `#inscription` et `#signaler`).
- Premier schéma de règle : frise horaire de la fiche A3.4 (stationnement au plus une heure avant la prise en charge), qui se décale de deux heures dans « Pour aller plus loin ».
- En-tête : le bouton jaune « Le livre » mène directement à cette page (plus de menu déroulant). Pied de page : liens « Le livre », « Mises à jour du livre », « Examens blancs n° 4 et 5 ».
- Texte de la fiche recopié du livre (page 66, corrigé page 72) ; aucune règle nouvelle. Titre de la page pour la recherche : « Livre examen VTC 2027 ».
- Vérifié : axe sans erreur en clair et en sombre à 320 et 1 366 px, avant et après avoir joué la fiche ; aucun débordement ; page lisible sans JavaScript.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 7 novembre 2026, 19 h 25 · Article n° 6 (tâche tous les deux jours)

- Titre : « Taxi ou VTC : quelles différences pour devenir chauffeur en 2027 ? » (épreuve A, réglementation T3P).
- Page : https://revision-vtc.fr/dossiers/taxi-ou-vtc-differences.html (2 500 mots, sans photo).
- En bref : seul le taxi, titulaire d'une autorisation de stationnement (licence), peut prendre un client sans réservation et chercher des clients sur la voie publique ; en échange, ses prix sont plafonnés (2026 : 4,48 € de prise en charge, 1,30 € du kilomètre au plus, 8 € minimum) et sa voiture porte compteur et lumineux. La licence est gratuite en mairie après une longue attente, ou achetée de 30 000 € à 300 000 €. Le VTC travaille uniquement sur réservation, à prix libres. Les deux examens ont cinq épreuves écrites communes ; un admissible depuis moins de 3 ans ne passe que les deux épreuves propres à l'autre métier, puis la pratique.
- Sources lues le jour même (recherche web puis lecture) : fiches Entreprendre Service Public F21907, F22127, F31027, actualité A15396, arrêté du 6 avril 2017 (Légifrance). Textes du wiki (L3120-2, R3122-7, R3120-8-2, arrêtés du 26 mars 2015 et du 11 août 2017) recoupés avec ces fiches. Légifrance a refusé les pages du chapitre « Les taxis » (L3121-1 et suivants) : rien n'en est cité directement.
- Relecture indépendante : tout confirmé, calculs justes ; 9 précisions apportées (carte de taxi départementale et carte VTC nationale, 4 à 9 places attribué à la fiche officielle, formation continue attribuée à l'arrêté du 11 août 2017, secourisme PSC1 exigé pour le taxi, forfaits aéroports « taxis parisiens, course directe », nuances du revenu minimum des plateformes, frais VTC chiffrés).
- Vérifié : axe sans erreur en clair et en sombre à 320 et 1 366 px, aucun débordement.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 7 novembre 2026, 19 h 21 · Actualité VTC n° 5 (tâche du lundi)

- Page : https://revision-vtc.fr/actualite/2026-11-07.html
- Titre : « Chauffeurs VTC : 10 heures par jour selon l'ARPE, aucun nouveau texte officiel » (période du 3 au 7 novembre 2026).
- Textes officiels : aucun nouveau texte VTC au Journal officiel du 3 au 7 novembre 2026 (sommaires des JO n° 257 à 261 lus sur Légifrance).
- Examen : aucune nouveauté ; tarifs 2027 inchangés sur exament3p.fr ; résultats de la session d'admission d'octobre 2026 publiés le 5 novembre 2026 par la CMA Hauts-de-France.
- Rémunération et plateformes : enquête de l'ARPE publiée le 6 novembre 2026 (593 chauffeurs VTC, 10 heures par jour travaillé, 2 736 € de revenus bruts déclarés par mois avant charges, 1 563 € de charges, 65 % ont augmenté leur temps de travail).
- Simulateur : prix des carburants à jour (6 novembre 2026, mise à jour automatique).
- Vérifié : axe sans erreur en clair et en sombre à 320 et 1 366 px, aucun débordement ; sitemap.xml et llms.txt contiennent le numéro.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 7 novembre 2026, 19 h 10 · Menu renommé : Simulateurs, Réglementation VTC, FAQ VTC, Guides VTC

- Menu de toutes les pages : « Simulateur » devient « Simulateurs », « Textes réglementaires » devient « Réglementation VTC », « Questions VTC » devient « FAQ VTC », « Articles » devient « Guides VTC » ; « Actualité VTC » inchangé. Adresses inchangées (`simulateurs/`, `wiki/`, `questions/`, `dossiers/`).
- Repris partout : titres `h1` et `<title>`, fils d'Ariane (pages et données structurées), surtitres (« Textes officiels expliqués », « Guides pratiques », « Guide n° … »), liens dans les textes (accueil, contact, à propos, simulateur, deux guides), llms.txt.
- https://revision-vtc.fr/questions/ a pour titre « FAQ VTC : les questions des chauffeurs et des candidats à l'examen, réponses sourcées ».
- Vérifié : axe sans erreur en clair et en sombre à 320 et 1 366 px, menu lisible et sans débordement.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 7 novembre 2026, 19 h 30 · Menu « Textes réglementaires », index des Questions VTC et des Articles refaits

- Menu et toutes les pages : la rubrique « Textes du métier » s'appelle désormais « Textes réglementaires » (menu, titre de https://revision-vtc.fr/wiki/, liens dans les textes, accueil, llms.txt). Adresses inchangées (`wiki/`).
- https://revision-vtc.fr/questions/ : introduction plus pédagogique (exemples de questions, « Comment se lit une réponse » en trois étapes, légende des sept épreuves avec leurs pictogrammes, lien « Posez-la » vers le contact) ; plus de promesse « une question chaque semaine ». Cartes numérotées (n° 1 = la plus ancienne), mois et année seulement, épreuve concernée avec pictogramme sous le titre. Mêmes cartes sur l'accueil (surtitre « Réponses sourcées » au lieu de « Chaque jeudi »).
- https://revision-vtc.fr/dossiers/ : introduction plus vivante, « Ce que vous trouvez dans chaque article » en trois étapes, « De nouveaux articles sont mis en ligne régulièrement » au lieu de « Un nouvel article chaque semaine » ; cartes numérotées, mois et année, épreuve avec pictogramme.
- Pages des questions et des articles : « Publiée en novembre 2026, vérifiée en novembre 2026 » (plus le jour), précédé de l'épreuve. Les dates exactes restent dans les données structurées.
- Épreuve rattachée : lettre de la première fiche du livre citée (questions) ; champ `domaine` ajouté aux cinq articles (B, F, B, B, X). README mis à jour.
- Vérifié : axe sans erreur en clair et en sombre à 320 et 1 366 px (index questions, articles, accueil, textes, une question, un article), aucun débordement horizontal.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 7 novembre 2026, 14 h 30 · Question VTC du jour (relance avec la nouvelle méthode de lecture)

- Question : « Contrôle technique VTC : tous les combien ? »
- Page : https://revision-vtc.fr/questions/2026-11-07-controle-technique-vtc-tous-les-combien.html
- Réponse courte : Tous les ans. Une voiture de VTC passe son premier contrôle technique au plus tard un an après sa première mise en circulation, puis chaque année (article R323-24 du Code de la route), au lieu de quatre ans puis tous les deux ans pour une voiture particulière.
- Méthode testée à la demande de Benjamin : chaque page est d'abord trouvée par une recherche web, puis lue à l'adresse donnée dans les résultats (l'outil de lecture refuse désormais les adresses tapées directement). Résultat : Légifrance (Code de la route, R323-22 à R323-26, version en vigueur au 7 novembre 2026) et entreprendre.service-public.fr (F22299) lus en entier.
- Relecture indépendante : toutes les affirmations confirmées, aucune contredite ; 2 formulations précisées (« véhicule léger », exemple compté « d'ici le 15 mars 2032 »).
- Script du réel : `reseaux/reels/2026-11-07-controle-technique-vtc-tous-les-combien.txt`.
- Les deux entrées PROBLÈME de ce jour (9 h 05 et 13 h 40) sont levées pour la Question VTC.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 7 novembre 2026, 13 h 40 · Question VTC du jour (second passage)

- **PROBLÈME : aucune question publiée, même blocage que ce matin.** Le réseau de la tâche refuse toujours la connexion directe (refus 403 du proxy) à legifrance.gouv.fr, service-public.fr, urssaf.fr et ecologie.gouv.fr. La lecture par l'outil web a été refusée pour 3 pages sur 3 (service-public.fr F33801 et deux pages Légifrance du Code de la route : « PROVENANCE_REQUIRED », demande d'autorisation restée sans réponse). Aucune source officielle lue le jour même : rien n'est publié.
- Sujet toujours en attente, non rédigé : « Contrôle technique VTC : tous les combien ? » (famille Véhicule ; contrôle des doublons fait ce matin). Aucune question préparée et restée non publiée.
- À faire : autoriser legifrance.gouv.fr et service-public.fr dans les accès réseau de la tâche (claude.ai, Paramètres > Capacités), ou accepter les lectures web de la tâche, ou la faire tourner depuis l'ordinateur (« Exiger cet ordinateur »).
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 7 novembre 2026, 10 h 25 · Article n° 6 (tâche tous les deux jours)

- **PROBLÈME : aucun article publié, faute de pouvoir lire une seule source officielle.** Le réseau de la tâche refuse la connexion directe (refus 403 du proxy) à legifrance.gouv.fr, service-public.fr, entreprendre.service-public.fr, urssaf.fr, impots.gouv.fr, bofip.impots.gouv.fr, ecologie.gouv.fr, data.gouv.fr, insee.fr, senat.fr, assemblee-nationale.fr et pixabay.com. La lecture par l'outil web a été refusée pour 4 pages sur 4 (« PROVENANCE_REQUIRED » : demande d'autorisation restée sans réponse, la tâche tournant sans personne pour l'accepter). La recherche web ne renvoie que des titres et des liens, sans le texte des pages : rien n'a pu être vérifié, donc rien n'est publié.
- Contrôle des doublons fait (5 articles publiés, aucun brouillon, 8 questions). Sujet retenu pour le prochain passage, non rédigé : « Taxi ou VTC en 2027 : ce qui change vraiment » (thème réglementation, après l'article n° 5 sur l'examen). Sujet de repli : le précompte des cotisations sociales par les plateformes (à ne pas confondre avec le prélèvement à la source de l'impôt).
- Même blocage que la Question VTC de ce matin et la veille du wiki du 4 novembre.
- À faire : autoriser legifrance.gouv.fr, service-public.fr, urssaf.fr, impots.gouv.fr, ecologie.gouv.fr et pixabay.com dans les accès réseau des tâches (claude.ai, Paramètres > Capacités), ou accepter les lectures web des tâches, ou les faire tourner depuis l'ordinateur (« Exiger cet ordinateur »).
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 7 novembre 2026, 9 h 05 · Question VTC du jour

- **PROBLÈME : aucune question publiée, faute de pouvoir lire une source officielle.** Le réseau de la tâche refuse la connexion directe à legifrance.gouv.fr et à service-public.fr (refus 403 du proxy). La lecture par l'outil web a été refusée trois fois (« PROVENANCE_REQUIRED » : demande d'autorisation restée sans réponse, la tâche tournant sans personne pour l'accepter) ; un livret de préfecture (bas-rhin.gouv.fr) a renvoyé une erreur du serveur.
- Sujet préparé, non rédigé : « Contrôle technique VTC : tous les combien ? » (famille Véhicule). Contrôle des doublons fait : proche du wiki R3120-10 et d'une ligne de l'article « Combien coûte vraiment le lancement en VTC ? », mais aucune question ne donne le calendrier du premier contrôle d'une voiture neuve utilisée en VTC. Sources à lire : Code de la route R323-24 et R323-26, Code des transports R3120-10, service-public.fr F33801.
- Aucune question préparée et restée non publiée lors des passages précédents.
- À faire : autoriser legifrance.gouv.fr et service-public.fr dans les accès réseau de la tâche (claude.ai, Paramètres > Capacités), ou accepter les lectures web de la tâche, ou la faire tourner depuis l'ordinateur (« Exiger cet ordinateur »).
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 4 novembre 2026, 12 h 20 · Toutes les pages : carreaux estompés dans l'en-tête

- Les en-têtes quadrillés des pages intérieures (Questions VTC, Textes du métier, Articles, Actualité VTC, Simulateurs, le livre, pages fixes) prennent le même traitement que les bandes de l'accueil : fond `--doux` éclairci de moitié par `--fond`, quadrillage net en haut qui s'estompe vers le bas. Une seule règle pour tous les fonds quadrillés du site (`.bloc-doux,.tete-page` dans `docs/css/site.css`).
- Vérifié sur l'accueil, la liste et une page des Questions VTC, un texte du wiki, un article, le simulateur, l'Actualité VTC et la page du livre : axe sans erreur en clair et en sombre, aucun débordement à 320 et 1 366 px.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 4 novembre 2026, 12 h 10 · Accueil : fond des carreaux ramené aux neutres de la charte

- https://revision-vtc.fr/ : le voile de jaune sous les carreaux est retiré (jeton `--lavis` supprimé), pour ne pas ajouter de couleur à la charte. Le fond des bandes quadrillées est maintenant le gris bleuté des bandes (`--doux`) éclairci de moitié par le blanc du fond (`--fond`), avec `color-mix()` : le même gris, plus léger, sans couleur nouvelle. En sombre, le même mélange des deux jetons sombres.
- Quadrillage estompé et alternance des bandes inchangés.
- Vérifié : axe sans erreur en clair et en sombre à 320 et 1 366 px, aucun débordement.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 4 novembre 2026, 12 h 00 · Accueil : carreaux estompés sur un voile de jaune

- https://revision-vtc.fr/ : les bandes quadrillées de l'accueil changent d'aspect. Le quadrillage est net en haut de la bande et s'estompe progressivement vers le bas, au lieu de couvrir toute la bande. Le fond derrière les carreaux n'est plus gris bleuté : c'est un voile très clair du jaune signal de la charte (nouveau jeton `--lavis`, #FEF9EC en clair, #181B1C en sombre). Les bandes blanches n'ont plus de filet.
- Alternance inversée : sous la bande des preuves, « Par où commencer ? » est maintenant blanc, puis « Réglementation VTC : l'essentiel » quadrillé, Questions VTC blanc et Actualité VTC quadrillé.
- L'en-tête quadrillé des pages intérieures ne change pas.
- Vérifié : axe sans erreur en clair et en sombre à 320 et 1 366 px, aucun débordement ; quadrillage masqué à l'impression.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 4 novembre 2026, 11 h 50 · Simulateur : champs côte à côte alignés

- https://revision-vtc.fr/simulateurs/cout-revient-revenu-net-vtc.html : quand deux champs sont côte à côte (commission et semaines travaillées, kilomètres et heures de travail, etc.), les deux cases de saisie sont maintenant à la même hauteur, même si leurs textes d'aide n'ont pas le même nombre de lignes. Avant, la case dont l'aide était plus courte remontait.
- Règle commune `.champs-2` dans `docs/css/site.css` (s'applique aussi aux formulaires du contact et de la page du livre, sans changement visible quand les aides ont la même longueur). Calcul inchangé.
- Vérifié : écart nul entre les cases de chaque rangée à 1 366 px, axe sans erreur en clair et en sombre à 320 et 1 366 px, aucun débordement.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 4 novembre 2026, 11 h 15 · Accueil : simulateur en format horizontal

- https://revision-vtc.fr/ : la carte « Simulateur gratuit » est plus large et moins haute (311 px au lieu de 403) : les deux curseurs sont côte à côte (« Versé par semaine », « Location par semaine ») et le relevé mensuel tient sur une ligne de trois colonnes (versé, TVA-cotisations-voiture-frais, reste avant impôt). La colonne de droite du premier écran est un peu plus large. La carte du livre est entièrement visible sans défiler, même sur un écran de 1 366 × 657.
- Sur téléphone (sous 480 px), curseurs et relevé repassent l'un sous l'autre. Calcul inchangé.
- Vérifié : axe sans erreur en clair et en sombre à 320 et 1 366 px, aucun débordement, 1 500 € versés et 200 € de location donnent toujours 2 398 € par mois, comme la page du simulateur ; tests du simulateur justes.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 4 novembre 2026, 11 h 00 · Accueil : carte du simulateur resserrée

- https://revision-vtc.fr/ : la carte « Simulateur gratuit » passe de 531 à 403 px de haut (marges, espacement des curseurs, taille des montants, phrase d'hypothèses raccourcie : « Par mois, sur 47 semaines par an, voiture louée. »), et le premier écran commence un peu plus haut. La carte du livre est de nouveau visible sans faire défiler : entièrement à partir de 1 536 × 730, et en grande partie sur un écran de 1 366 × 657.
- Les curseurs gardent une zone tactile de 44 px. Calcul inchangé.
- Vérifié : axe sans erreur en clair et en sombre à 320 et 1 366 px, aucun débordement horizontal, 1 500 € versés et 200 € de location donnent toujours 2 398 € par mois, comme la page du simulateur.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 4 novembre 2026, 10 h 40 · Accueil : simulateur à curseurs et premier écran aligné

- https://revision-vtc.fr/ : le texte du premier écran et la carte « Simulateur gratuit » commencent maintenant à la même hauteur ; avant, le texte était centré face aux deux cartes et descendait plus bas que le simulateur.
- La carte « Simulateur gratuit » a deux curseurs : montant versé par les plateformes par semaine (200 à 2 500 €) et location de la voiture par semaine (0 à 600 €). Le relevé mensuel (versé, TVA, cotisations, voiture et frais, reste avant impôt) se recalcule à chaque cran avec le calcul du simulateur complet et ses valeurs par défaut (47 semaines, hybride essence, cotisations sur le prix payé par les clients). Exemple contrôlé : 1 500 € versés et 200 € de location par semaine donnent 2 398 € par mois, comme la page du simulateur avec les mêmes valeurs. Le lien « Faire ma simulation avec mes chiffres » ouvre le simulateur avec ces deux valeurs.
- La carte n'est plus un lien entier : elle est à plat, seul le lien du bas se clique (charte : ce qui ne se clique pas reste à plat). Sans JavaScript, l'exemple pour 1 000 € par semaine reste affiché.
- Nouveau script `docs/js/accueil-simu.js` ; `outils/generer.py` (accueil), `docs/css/site.css` (curseurs, alignement, relief réservé aux cartes-liens), README (accueil).
- Vérifié : tests du simulateur (calculs justes, Python et JavaScript identiques sur 401 cas), axe sans erreur en clair et en sombre à 320 et 1 366 px, aucun débordement horizontal.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 4 novembre 2026, 9 h 06 · Question VTC du jour

- Question : « Siège auto en VTC : est-il obligatoire pour un enfant ? »
- Page : https://revision-vtc.fr/questions/2026-11-04-siege-auto-vtc-obligatoire.html
- Réponse courte : Oui. Un enfant de moins de 10 ans doit être attaché dans un siège auto homologué adapté à sa morphologie et à son poids, en VTC comme dans une voiture particulière. La dispense prévue par le Code de la route vise seulement le taxi et les transports en commun : elle ne s'applique pas au VTC.
- Sources lues le jour même : Code de la route R412-1, R412-2, R412-3 (Légifrance, page de section, version au 31 octobre 2026) ; service-public.fr F628 (vérifiée le 2 novembre 2026) ; Code des transports R3120-1 (Légifrance). Relecture indépendante : 32 affirmations confirmées, 0 contredite ; 3 nuances apportées (passager mineur, chute du réel, intitulés de sources).
- Script du réel : `reseaux/reels/2026-11-04-siege-auto-vtc-obligatoire.txt`.
- À noter : l'accueil signale une alerte axe déjà présente avant cette publication (« landmark-complementary-is-top-level », un élément `aside` imbriqué), relevée avec axe-core 4.10.2.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 4 novembre 2026, 7 h 57 · Veille du wiki (tâche du mercredi)

- **PROBLÈME : Légifrance n'a laissé lire que 9 articles sur 78.** La connexion directe reste refusée (403) et la lecture par l'outil web a échoué 15 fois sur 18 (refus du site), même en espaçant les essais de 4 minutes.
- Articles vérifiés : 9 sur 78, tous identiques au texte officiel : L3120-1, L3120-2, L3120-2-1, L3120-2-2, L3120-4, L3120-5, L3120-7 (page Légifrance en vigueur au 30 octobre 2026), R3122-2 (en vigueur au 4 novembre 2026), L3142-2 (copie Légifrance du 19 août 2026, version en vigueur depuis le 31 décembre 2016).
- Articles non lus : les 69 autres (dont les 5 arrêtés). Aucun texte modifié. Date « vérifié » laissée au 25 octobre 2026.
- Explications améliorées (première phrase plus directe, reprise telle quelle par Google, 158 caractères au plus) :
  - https://revision-vtc.fr/wiki/l3120-1.html : « Le T3P (transport public particulier de personnes) : transport payant de personnes en véhicule de moins de dix places, hors bus, cars et transport privé. »
  - https://revision-vtc.fr/wiki/l3120-2-2.html : ajout du mot « carte VTC ».
  - https://revision-vtc.fr/wiki/l3120-2.html : ajout du mot « maraude » dans la première phrase.
- Contrôle technique : génération réussie, sitemap complet (79 adresses du wiki), descriptions et données structurées présentes, aucun lien interne cassé, axe sans erreur en clair et en sombre à 320 et 1366 px.
- À faire : autoriser legifrance.gouv.fr dans les accès réseau de la tâche, ou la faire tourner depuis l'ordinateur (option « Exiger cet ordinateur », navigateur intégré).
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mardi 3 novembre 2026, 23 h 15 · Moins d'arrondis, liens « Tous les… » en rectangle

- Toutes les pages : coins des cartes, des cartes-liens et des touches ramenés à 4 px (au lieu de 10 et 12 px) ; sommaire du wiki et barre de répartition du simulateur moins arrondis.
- https://revision-vtc.fr/ : les liens « Tous les textes expliqués », « Toutes les questions » et « Tous les numéros » deviennent des rectangles sobres, à plat, avec une flèche, remplis de bleu nuit au survol (au lieu de pilules en relief).
- Vérifié : axe en clair et en sombre à 320 et 1366 px, aucun débordement. README (charte) mis à jour.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mardi 3 novembre 2026, 23 h 05 · En-tête collant, jauge de lecture et menu animé

- Toutes les pages (https://revision-vtc.fr/ et les autres) : l'en-tête reste collé en haut de l'écran au défilement. Il se resserre dès qu'on quitte le haut de la page, une jauge jaune en bas montre la part de la page déjà lue, et sur téléphone il se range quand on descend et revient dès qu'on remonte. Au survol du menu, un trait jaune s'étire sous la rubrique.
- Les liens vers un titre de la page (sommaires, « Aller au résultat ») tiennent compte de la hauteur de l'en-tête.
- Fichiers : `docs/css/site.css` (partie 8), `docs/js/site.js`, README (charte, en-tête).
- Vérifié : ordinateur et téléphone (390 px), axe en clair et en sombre à 320 et 1366 px sur l'accueil, le simulateur et le wiki, aucun débordement, aucune erreur JavaScript ; mouvements coupés si l'appareil demande moins d'animations.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mardi 3 novembre 2026, 22 h 50 · Simulateur : corrections de l'audit, Acre et CFE

- https://revision-vtc.fr/simulateurs/cout-revient-revenu-net-vtc.html, suite à l'audit des outils du 3 novembre 2026 (rapport dans Notion, « QUESTION A CLAUDE » > « Audit des outils, 3 novembre 2026 ») :
  - seuil de rentabilité arrondi à l'euro supérieur (659 € au lieu de 658 €, montant auquel le revenu était encore négatif) ;
  - une saisie fausse remplace le résultat par « — » au lieu de laisser l'ancien chiffre affiché ;
  - « 1e3 » et les signes ne sont plus acceptés comme nombres ;
  - coût au kilomètre « — » quand les kilomètres sont à 0 ;
  - mention « montants arrondis » sous le détail et l'exemple chiffré (les lignes peuvent différer du total de 1 €) ;
  - alerte tant que les autres frais sont à 0 € ;
  - nouvelle case « Première année avec l'Acre » (15,9 % au lieu de 21,2 % pour une micro-entreprise créée depuis le 1er juillet 2026 ; sources : Bpifrance Création, juillet 2026, et L'Essentiel de l'Éco, 20 février 2026, décret n° 2026-69) et nouveau champ facultatif CFE.
- Résultat par défaut inchangé : 908 € par mois. Accueil et articles inchangés.
- Vérifié : tests du calcul (cas Acre, CFE, seuil, 0 km ajoutés), calculs Python et JavaScript identiques sur 401 cas, recalcul indépendant de l'audit sur 2 008 cas sans écart, axe en clair et en sombre à 320 et 1366 px, aucune erreur JavaScript.
- À trancher : chauffeur VTC artisan ou commerçant (taux de formation 0,3 % et taxe de chambre de métiers 0,48 % comptés aujourd'hui), à vérifier sur une fiche officielle.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mardi 3 novembre 2026, 19 h 45 · Simulateur : la TVA est désormais calculée

- https://revision-vtc.fr/simulateurs/cout-revient-revenu-net-vtc.html : le simulateur calcule la TVA au lieu de seulement la signaler.
  - Au-delà de 41 250 € de chiffre d'affaires par an (seuil majoré de la franchise) : TVA de 10 % comprise dans le prix des courses, à reverser, moins la TVA de 20 % récupérable sur le loyer, l'achat, l'entretien et le carburant d'une voiture affectée au VTC ; cotisations calculées sur le hors taxe ; année complète.
  - En franchise : TVA de 20 % sur la commission facturée depuis l'étranger (Uber, Bolt), due même en franchise et sans déduction. Nouvelle case « Ma plateforme facture sa commission depuis l'étranger », cochée par défaut.
  - Entre 37 500 € et 41 250 € : année en franchise, alerte « TVA due l'année suivante ».
  - Seuil de rentabilité recalculé pas à pas ; alerte quand il tombe sur la sortie de la franchise.
- Exemple par défaut (1 000 € versés par semaine, 62 667 € de chiffre d'affaires) : 908 € par mois au lieu de 991 € (1 287 € au lieu de 1 278 € avec les cotisations sur le montant versé).
- Mis à jour avec ces chiffres : accueil (carte « Simulateur gratuit »), https://revision-vtc.fr/dossiers/combien-gagne-chauffeur-vtc-par-heure.html (8,20 € et 11,63 € par heure au lieu de 8,90 € et 11,50 €, 0,35 € par km), https://revision-vtc.fr/dossiers/chauffeur-vtc-salarie-ou-independant.html, https://revision-vtc.fr/dossiers/erreurs-chauffeur-vtc-debutant.html (ces trois articles citaient encore 983 € et 1 270 €, chiffres d'un ancien prix du carburant).
- Sources : BOFiP BOI-TVA-LIQ-20 (taux normal), BOI-TVA-LIQ-30-20-60 (10 %), BOI-TVA-DECLA-10-10-20 § 130 et 140 (autoliquidation même en franchise ; version du 11 mars 2020 lue, la version du 9 septembre 2026 n'a pas pu être ouverte), BOI-TVA-DED-30-30-20 § 120 à 140 (véhicules VTC), BOI-TVA-DED-30-30-40 (carburants), BOI-TVA-DECLA-40-10-20 § 160 (fin de franchise au jour du dépassement) ; Dhraagi Conseil et Hayot Expertise (commissions facturées depuis l'étranger). La fiche F21746 de service-public.fr n'a pas pu être relue aujourd'hui (seuils inchangés, déjà vérifiés le 28 octobre).
- Nouveau contrôle : `outils/test_coherence_simulateur.py` compare le calcul Python des exemples au calcul JavaScript de la page sur 401 cas (lancé aussi chaque matin avec la mise à jour des carburants).
- À trancher : la TVA sur la commission en franchise est un coût de 20 % de la commission (131 € par mois pour 500 € versés par semaine) que beaucoup de chauffeurs ignorent ; un article ou une Question VTC sur ce sujet serait utile.
- Vérifié : tests du calcul, axe en clair et en sombre à 320 et 1366 px (accueil, simulateur, article), aucun débordement horizontal, aucune erreur JavaScript.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mardi 3 novembre 2026, 13 h 20 · Accueil : carte « Simulateur gratuit » refaite

- https://revision-vtc.fr/ : la carte du simulateur est refaite. « Simulateur gratuit » devient un vrai titre (condensé, grand). Dessous, un petit relevé mensuel en trois lignes : versé par les plateformes (3 917 €), cotisations, voiture et frais (− 2 926 €), il vous reste avant impôt (991 €), sous un trait épais. Les trois montants ont la même taille et sont alignés à droite, dans la même unité (par mois) ; avant, un montant était par semaine et l'autre par mois, en deux tailles différentes. Lien « Faire ma simulation avec mes chiffres » avec la pastille fléchée des cartes.
- Montants calculés par le générateur avec les valeurs par défaut du simulateur (1 000 € versés par semaine, 47 semaines par an) ; résultat net inchangé (991 € par mois).
- Vérifié : axe en clair et en sombre à 320, 768 et 1366 px (seule remarque, antérieure : « landmark-complementary-is-top-level » sur le bloc Actualité), aucun débordement horizontal.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mardi 3 novembre 2026, 14 h 10 · Simulateur : prix des carburants mis à jour chaque jour

- https://revision-vtc.fr/simulateurs/cout-revient-revenu-net-vtc.html : les prix du SP95-E10 et du gazole sont désormais ceux de la veille, mis à jour chaque matin par GitHub Actions (`.github/workflows/carburants.yml`, script `outils/carburants.py`), au lieu de la moyenne hebdomadaire de la DGEC reprise le lundi (qui s'arrêtait encore au 23 octobre).
- Nouvelle source : flux quotidien officiel de prix-carburants.gouv.fr (ministère de l'Économie, Licence Ouverte 2.0). Moyenne nationale TTC des prix relevés la veille, une valeur par station, prix à plus de 20 % de la médiane écartés (erreurs de saisie, par exemple du gazole à 1,25 €).
- Méthode contrôlée sur le vendredi 23 octobre 2026 : SP95-E10 2,106 € et gazole 2,355 €, contre 2,116 € et 2,352 € pour la DGEC. Résultat identique sur le fichier du 2 novembre déposé par Benjamin.
- Prix du lundi 2 novembre 2026 : SP95-E10 2,082 € (3 743 stations), gazole 2,232 € (5 413 stations), contre 2,116 € et 2,352 € au 23 octobre. L'exemple chiffré du simulateur et la carte de l'accueil sont recalculés.
- La tâche du lundi (Actualité VTC) ne touche plus aux prix des carburants. Les mises à jour quotidiennes n'ajoutent pas d'entrée à ce journal (commits « Simulateur : prix des carburants du … »).
- Vérifications : `node outils/test_simulateur.js` (tous les calculs justes), générateur sans erreur, axe en clair et en sombre à 320 et 1 280 px (aucune nouvelle alerte ; l'alerte « landmark-complementary-is-top-level » à 320 px existait déjà), aucun débordement ; seuls les prix, leur date, la source et le texte de bas de page changent sur la page.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mardi 3 novembre 2026, 10 h 47 · Article n° 5 (tâche tous les deux jours)

- Titre : « Réussir l'examen VTC du premier coup : coefficients, notes éliminatoires et calendrier 2027 »
- Page publiée : https://revision-vtc.fr/dossiers/reussir-examen-vtc-premier-coup.html (2 491 mots, sans photo)
- En bref : à l'écrit, 10 sur 20 de moyenne pondérée sur sept épreuves (170 points sur 340), au moins 6 sur 20 à chaque épreuve sauf l'anglais (4 sur 20), puis 12 sur 20 à la pratique. Les épreuves de coefficient 3 (A, C, F, G) font 70,6 % de la note.
- Apport : poids réel de chaque épreuve, valeur pondérée de chaque question (une réponse courte en G vaut douze QCM d'anglais), temps par question, taux de réussite officiels (SDES : 51 % des inscrits VTC de 2023 admis en janvier 2025 ; 58 % à l'écrit et 68 % à la pratique au premier passage pour les inscrits de 2022), règles en cas d'échec (règlement CMA de décembre 2024), coût d'un échec aux tarifs 2027 (246 €, 120 €), calendrier 2027 des Hauts-de-France, règles pratiques de l'épreuve de conduite.
- Sources lues le 3 novembre 2026 : arrêté du 6 avril 2017 (Légifrance), règlement d'examen des CMA, CMA Hauts-de-France, exament3p.fr, rapports 2025 et 2024 de l'Observatoire national du T3P (SDES). R3120-7 d'après le wiki (vérifié le 25 octobre 2026), concordant avec le règlement CMA. Relecture indépendante : 46 points contrôlés, 7 corrigés (dont un nombre de notes sous 10 faux), calculs refaits.
- Doublons évités : simulateur « calcul de la note » (outil, mêmes règles ; l'article a des exemples différents et le relie), article n° 1 (seul le prix de l'examen), question « permis probatoire » (reliée).
- Accessibilité : axe sans erreur en clair et en sombre, à 320 et 1 280 px, sur la page et l'index des articles ; l'accueil garde l'alerte « landmark-complementary-is-top-level » déjà signalée.
- À noter : la mention de bas de page commune aux articles parle de « fourchettes » de formation, d'assurance et de véhicule, absentes de cet article (texte du générateur, non modifié).
- Règles du livre touchées : aucune (la fiche A2.4 cite le tarif 2026 de 241 €, déjà signalé le 2 novembre).
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mardi 3 novembre 2026, 9 h 05 · Question VTC du jour

- Question : « Vignette VTC : où la coller sur la voiture ? »
- Page publiée : https://revision-vtc.fr/questions/2026-11-03-vignette-vtc-ou-la-coller.html
- Réponse courte : en bas à gauche du pare-brise avant, côté conducteur, et en bas à droite de la lunette arrière, à l'opposé du conducteur. Depuis le 2 août 2025, les deux vignettes doivent être « collées de manière inamovible » : une vignette simplement posée ou glissée dans un support amovible ne suffit plus.
- Apport : emplacement exact des deux vignettes, changement du 2 août 2025 (arrêté du 24 juillet 2025 : « apposées » devient « collées de manière inamovible »), vignette temporaire (une seule, 30 jours ouvrés au plus), quatre informations propres au véhicule, trois cas de fin de validité, sanction (4e classe, 750 € au plus pour une personne physique). L'article sur le budget ne citait que le prix des vignettes ; il est relié depuis la page.
- Sources lues le 3 novembre 2026 : arrêté du 6 avril 2017 (articles 1 à 4 et annexe) et arrêté du 24 juillet 2025 sur Légifrance ; R3122-8 et R3124-6 sur Légifrance ; Code pénal 131-13 (service-public.fr F32803 et Juritravail) ; L'Officiel des métiers. Relecture indépendante : 32 affirmations confirmées, 1 retirée (définition de l'exploitant), 2 attributions précisées.
- Accessibilité : axe sans erreur en clair et en sombre, à 320 et 1 280 px, sur la page. À noter : l'accueil signale une alerte axe « landmark-complementary-is-top-level » (déjà présente avant cette publication, règle de bonne pratique).
- Script du réel : `reseaux/reels/2026-11-03-vignette-vtc-ou-la-coller.txt`.
- Règles du livre touchées : aucune modifiée ; à vérifier par Benjamin : la fiche G3.1 mentionne-t-elle le collage inamovible exigé depuis le 2 août 2025 ?.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Lundi 2 novembre 2026, 14 h 45 · Mises à jour du livre : un encadré par correction, avec la page du livre

- https://revision-vtc.fr/mises-a-jour.html : chaque correction du livre s'affiche désormais dans un encadré (titre de la fiche, date, **page du livre et page du corrigé**, ce que dit le livre, ce qu'il faut retenir, texte officiel cliquable, exemplaires concernés), au lieu d'un tableau. La page n'a encore aucune correction : rien ne change pour le lecteur tant qu'il n'y en a pas.
- Nouvelle rubrique « Quelle version du livre avez-vous ? » : version 1.0 (page 2 blanche) ou 1.1 (page 2 « Ce livre est tenu à jour », prête pour KDP le 2 novembre 2026). Même pagination dans les deux versions.
- Nouveau fichier `contenu/livre_pages.json` : la page des 213 fiches du livre et de leur corrigé, relevée dans le PDF du livre. Le générateur y prend la page tout seul ; il refuse une correction sans fiche connue ou à laquelle il manque un champ. Format documenté dans `README.md` (« Format d'une correction du livre »).
- Page « Le livre tenu à jour » : la phrase sur les corrections mentionne la page du livre.
- Vérifié : aucune erreur axe en clair et en sombre, à 320 px et 1 280 px, avec un encadré d'essai (retiré avant publication).
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Lundi 2 novembre 2026, 10 h 44 · Question VTC du jour

- Question : « Visite médicale VTC : tous les combien d'années ? »
- Page publiée : https://revision-vtc.fr/questions/2026-11-02-visite-medicale-vtc-tous-les-combien.html
- Réponse courte : tous les 5 ans jusqu'à 60 ans, tous les 2 ans de 60 à 76 ans, puis chaque année après 76 ans. La visite se passe chez un médecin agréé par le préfet, jamais chez son médecin traitant, et coûte 36 €, non remboursés par l'Assurance maladie.
- Apport : calendrier complet par tranche d'âge (dont la validité arrêtée aux 60 ans entre 55 et 60 ans), exemple à 57 ans, calcul sur une carrière (14 visites de 30 à 75 ans, 504 €), déroulé du contrôle. L'article sur le budget ne disait que « tous les cinq ans jusqu'à 55 ans, puis plus souvent avec l'âge ».
- Sources : service-public.fr (F36483) et entreprendre.service-public.fr (F31027) lus le 2 novembre 2026 ; D3120-5 d'après le wiki (vérifié le 25 octobre 2026) ; R221-11 non lu sur Légifrance (vérification anti-robot), durées concordantes d'après l'OPPBTP. Relecture indépendante : 30 affirmations confirmées, 0 retirée.
- Non publiée : la question « Formation continue VTC » préparée ce matin (correctif `claude/a_publier/2026-11-02-question-vtc-formation-continue.patch` dans le projet Claude) n'est toujours pas en ligne ; sujet non repris.
- Maillage : pas de lien vers l'article sur le budget dans le texte, le générateur actuel n'acceptant pas encore les liens dans les Questions VTC (changement contenu dans le correctif non appliqué).
- Script du réel : `reseaux/reels/2026-11-02-visite-medicale-vtc-tous-les-combien.txt`.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Lundi 2 novembre 2026, 9 h 05 (publiée à 10 h 55) · Question VTC du jour

- Question : « Formation continue VTC : combien d'heures et tous les combien d'années ? »
- Page publiée : https://revision-vtc.fr/questions/2026-11-02-formation-continue-vtc-duree.html
- Réponse courte : 14 heures, tous les cinq ans. Le stage se suit en présentiel dans un centre de formation agréé, en quatre modules de 3 h 30, et l'attestation remise à la fin, valable cinq ans, est demandée pour renouveler la carte professionnelle VTC.
- Préparée et vérifiée à 9 h 05 par la tâche planifiée, qui n'a pas pu l'envoyer sur GitHub ; publiée à 10 h 55 depuis le correctif, sans changement de contenu.
- Apport : programme des quatre modules, fractionnement possible (quatre fois 3 h 30 sur deux mois au plus), présentiel obligatoire, calendrier daté du renouvellement. L'article sur le budget ne citait que « 14 heures tous les cinq ans » ; il est relié depuis la page.
- Sources : R3120-8-2 lu sur Légifrance le 2 novembre 2026 ; arrêté du 11 août 2017 et R3124-12 d'après le wiki (vérifié le 25 octobre 2026), Légifrance renvoyant une vérification anti-robot pour ces pages ; service-public.fr (F31027, R73497) et fiche CMA Alsace-Moselle Grand Est lus le 2 novembre 2026. Relecture indépendante : 48 affirmations confirmées, 8 corrigées puis confirmées.
- Générateur : les paragraphes des Questions VTC acceptent les liens `[texte](adresse)` (comme les articles) ; README mis à jour. La question « Visite médicale VTC » du jour est maintenant reliée à l'article sur le budget et à cette question.
- Script du réel : `reseaux/reels/2026-11-02-formation-continue-vtc-duree.txt`.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Lundi 2 novembre 2026, 7 h 55 (publiée à 11 h 05) · Actualité VTC n° 4 (tâche du lundi)

- Préparée et vérifiée à 7 h 55 par la tâche planifiée, qui n'a pas pu l'envoyer sur GitHub ; publiée à 11 h 05 depuis le correctif, sans changement de contenu. Tarifs 2027 de l'examen revérifiés le 2 novembre 2026 sur la page de la CMA Hauts-de-France.
- PROBLÈME : prix des carburants non mis à jour (le fichier « Prix HTT et TTC depuis janvier 2020 » de la DGEC, lu le 2 novembre 2026 à 7 h 40, s'arrêtait encore au vendredi 23 octobre 2026, déjà repris dans le simulateur).
- Page publiée : https://revision-vtc.fr/actualite/2026-11-02.html
- Titre : « Examen VTC 2027 : inscription à 246 €, aucun nouveau texte au Journal officiel »
- Textes officiels : aucun nouveau texte VTC au Journal officiel du 29 octobre au 2 novembre 2026 (vérifié directement sur Légifrance).
- Examen : droits d'inscription 2027, 246 € pour l'examen complet (241 € en 2026), 171 € pour la mobilité professionnelle, 120 € pour l'admission seule, à partir du 1er janvier 2027 (exament3p.fr et CMA Hauts-de-France).
- Simulateur : prix des carburants inchangés, ceux du 23 octobre 2026 (SP95-E10 2,116 €, gazole 2,352 €).
- Contenu à corriger : https://revision-vtc.fr/dossiers/cout-pour-devenir-chauffeur-vtc.html indique que le tarif 2027 de l'examen « n'est pas encore publié » (246 € désormais).
- Livre : le livre cite 241 € (tarif 2026) pour l'examen complet (fiche A2.4) ; signalé dans « Ce que ça change pour le livre », pas de correction ajoutée (tarif publié par les CMA, pas par un texte du Journal officiel).
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Dimanche 1er novembre 2026, 22 h 10 · Accueil : carte « Simulateur gratuit » réalignée

- https://revision-vtc.fr/ : dans la carte de l'exemple du simulateur, les deux légendes (« Versé par les plateformes », « Il vous reste, avant impôt ») sont maintenant sur la même ligne, et les deux montants sur la même ligne de base ; avant, les légendes étaient décalées en hauteur. Quand la carte est étroite (téléphone, tablette), les deux blocs s'empilent proprement. « 1 000 € » est écrit avec le même format que « 983 € ». Chiffres inchangés.
- `docs/css/site.css` (`.carte-calcul`, grille à deux colonnes, requête de conteneur sous 22rem) ; `outils/generer.py` (montant versé formaté par `_euros`).
- Vérifications : axe sans erreur en clair et en sombre à 320 et 1 366 px ; aucun débordement à 320, 700, 900 et 1 366 px.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Dimanche 1er novembre 2026, 20 h 30 · E-mail de récapitulatif envoyé une fois le site à jour

- Aucune page du site modifiée.
- `outils/recap_mail.py` et `.github/workflows/recap.yml` : l'e-mail de récapitulatif attend désormais que GitHub Pages serve la nouvelle version (15 minutes au plus) avant de partir. Avant, il pouvait arriver avant la fin du déploiement : un lien ouvert aussitôt affichait « Page introuvable », et GoatCounter comptait une visite 404 (deux sur le simulateur, les 29 octobre et 1er novembre, aux heures de publication). Si le site n'est pas à jour au bout de 15 minutes, l'e-mail part quand même et le signale.
- README, « Récapitulatif par e-mail » : mis à jour.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Dimanche 1er novembre 2026, 1 h 40 · Simulateur, page du livre, page 404 (refonte design et UX, 3/3)

- https://revision-vtc.fr/simulateurs/cout-revient-revenu-net-vtc.html : sur téléphone et tablette, barre collante en bas de l'écran avec le revenu net mensuel et « Voir le détail ». Elle s'efface quand un champ a le focus, quand le clavier du téléphone est ouvert et quand le résultat complet est à l'écran ; lisible en clair et en sombre ; sans glissement si l'appareil demande moins d'animations ; absente sans JavaScript et sur grand écran. Calcul inchangé (`node outils/test_simulateur.js` : tous les calculs justes).
- https://revision-vtc.fr/le-livre.html : bloc de présentation en tête (couverture, 540 pages, 213 fiches, 1 191 questions corrigées, test diagnostic, 3 examens blancs plus 2 sur le site, à jour de la loi du 25 juin 2026), bouton « Acheter le livre sur Amazon » et « Déjà lecteur : recevoir les mises à jour ». Adresse inchangée ; engagements, formulaires et FAQ inchangés.
- https://revision-vtc.fr/404.html : pages proposées en petites cartes-liens en relief.
- README, « Charte graphique » : barre de résultat, page du livre, page 404.
- Vérifications sur les 109 pages : W3C (Nu) sans erreur, HTML et CSS ; axe sans erreur en clair et en sombre, à 320, 768 et 1 366 px, sur les 22 types de page ; aucun débordement ; barre testée en clair et en sombre, avec et sans réduction des animations.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Dimanche 1er novembre 2026, 1 h 15 · Corrections communes à toutes les pages (refonte design et UX, 2/3)

- Toutes les pages :
  - en-tête sur téléphone : nom du site sur une ligne, sous-titre masqué (l'en-tête passe de 165 px à environ 120 px) ; logo en cible de 44 px ;
  - fil d'Ariane : zone cliquable de 44 px, aspect inchangé ;
  - un seul bouton d'achat du livre (jaune, 44 px) dans le pied de page, l'encadré « Dans le livre » et la page du livre, au lieu de trois styles ;
  - feuille de style : plus aucune couleur en dur hors des jetons (nouveaux jetons `--jaune-survol`, `--lien-sur-nuit`, `--focus-sur-nuit`) ; règles mortes retirées (anciens boutons, tuiles de l'ancien accueil) ;
  - touches du sommaire, liens de l'encadré latéral et petits boutons : 44 px au moins.
- https://revision-vtc.fr/wiki/ : « Les lois d'origine et les autres références » en petites cartes-liens en relief (toute la carte est le lien) au lieu de liens à plat.
- https://revision-vtc.fr/textes.html (redirection) : adresse canonique alignée sur celle du wiki, `https://revision-vtc.fr/wiki/`.
- Numéros de l'Actualité VTC (https://revision-vtc.fr/actualite/2026-10-22.html, 2026-10-26.html, 2026-10-28.html) : « Numéro précédent », « Numéro suivant » et « Tous les numéros » en boutons secondaires, sans points médians.
- Déjà faits dans la publication 1 : menu illisible de 761 à 832 px, menu « Le livre » et liens du pied à 44 px.
- Inchangés volontairement : liens de sources du simulateur et crédits photo des articles (liens dans le texte, à plat).
- Adresses, titres, descriptions et données structurées inchangés.
- README, « Charte graphique » : jetons, bouton d'achat unique, téléphone, cartes-liens, navigation entre numéros.
- Vérifications sur les 109 pages : W3C (Nu) sans erreur, HTML et CSS ; axe sans erreur en clair et en sombre, à 320, 768 et 1 366 px, sur les 22 types de page ; aucun débordement.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Dimanche 1er novembre 2026, 0 h 55 · Accueil sans carrousel, menu réordonné, « Le livre » en bouton jaune (refonte design et UX, 1/3)

- https://revision-vtc.fr/ : le carrousel et son script sont supprimés. À la place :
  - un premier écran fixe sur fond nuit : surtitre « Examen VTC 2027, règles vérifiées en octobre 2026 » (mois tiré automatiquement de la dernière vérification du wiki), titre visible en `h1` « Réussir l'examen VTC 2027, et savoir ce que vous gagnerez vraiment », chapeau, bouton principal « Préparer l'examen 2027 », bouton secondaire « Calculer mon revenu net », mention « Gratuit, sans inscription, sans publicité. » ;
  - deux cartes-liens en relief : l'exemple du simulateur (1 000 € versés par semaine, 983 € nets par mois, chiffre recalculé par le générateur) et le livre ;
  - une bande de trois preuves (78 articles de loi, chiffres sourcés et datés, mise à jour chaque semaine) ;
  - « Par où commencer ? » (je prépare l'examen, je me lance, je roule déjà) remplace le bloc « Quatre rubriques », qui répétait le menu ;
  - ordre de la suite : réglementation essentielle, Questions VTC (2 × 2), Actualité VTC.
- Toutes les pages :
  - menu dans l'ordre Simulateur, Textes du métier, Questions VTC, Articles, Actualité VTC ; sur téléphone, dégradé et flèche sur le bord droit tant que le menu continue ;
  - « Le livre » en bouton jaune plein en relief ; la page du livre en cours est marquée dans la liste ;
  - cibles tactiles de 44 px : entrées du menu « Le livre », liens et bouton du pied de page ;
  - menu illisible entre 761 et 832 px en thème clair (texte blanc sur fond clair) : corrigé, les deux règles ont maintenant le même point de rupture (avancé de la publication 2 pour que axe passe sans erreur).
- Couverture du pied de page : déjà `alt=""` (décorative, le titre du livre est écrit à côté), inchangée.
- Adresses, titres, descriptions, balises de partage et données structurées inchangés.
- README, « Charte graphique » : en-tête, accueil, relief sur fond nuit, cibles de 44 px.
- Vérifications sur les 109 pages : W3C (Nu) sans erreur, HTML et CSS ; axe sans erreur en clair et en sombre, à 320, 768 et 1 366 px, sur les 22 types de page ; aucun débordement ; un seul `h1` visible par page.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 31 octobre 2026, 23 h 25 · Question VTC (tâche du jeudi)

- Question : « Quelles sont les voitures hybrides les moins chères pour faire VTC ? »
- Page publiée : https://revision-vtc.fr/questions/2026-10-31-voitures-hybrides-vtc-moins-cheres.html
- Réponse courte : au 31 octobre 2026, les hybrides non rechargeables les moins chères au prix catalogue sont la Dacia Sandero hybrid 155 (19 900 €) et la MG3 Hybrid+ (19 990 €), devant la Sandero Stepway (21 400 €) et la nouvelle Renault Clio full hybrid E-Tech (24 600 €). Une hybride peut servir de VTC sans respecter les critères de taille et de puissance.
- Classement de neuf modèles (prix catalogue des constructeurs, consommation WLTP), méthode écrite dans la page. Toyota et Honda non classés : seuls des prix remisés étaient affichés.
- Légifrance toujours inaccessible depuis l'outil : les textes viennent du wiki (vérifié le 25 octobre 2026) et de service-public.fr (lu le 31 octobre 2026).
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 31 octobre 2026, 23 h 30 · Nouvelle charte graphique « signalétique en relief »

- Tout le site (toutes les pages) : nouvelle apparence choisie par l'auteur parmi trois prototypes, avec la rubrique Actualités du LaboINSPIRE comme inspiration pour le relief.
  - en-tête du site en bandeau bleu nuit, rubrique en cours soulignée en jaune ; titres en Barlow Condensed, texte en Barlow (polices hébergées sur le site ; Inter et EB Garamond retirées) ;
  - fond quadrillé (plan de ville) dans l'en-tête des pages et les bandes claires de l'accueil ;
  - tout ce qui se clique a un relief bleu nuit, se soulève au survol et s'enfonce au clic : cartes de l'accueil, Actualité VTC, Questions VTC, articles, listes d'articles du wiki, « Voir aussi », sommaire, boutons, choix du simulateur (la touche choisie est enfoncée et jaune) ; ce qui ne se clique pas reste à plat ;
  - numéros d'article, étapes et numéros de l'Actualité en pastilles jaunes ; « En clair » en bandeau nuit ; « À retenir » sur fond clair avec bande jaune.
- Contenu, adresses, balises de référencement et données structurées inchangés : seules la feuille de style, les polices et le préchargement des polices changent.
- README : section « Charte graphique » réécrite.
- Vérifications sur les 108 pages : W3C (Nu) sans erreur, HTML et CSS ; axe sans erreur en clair et en sombre, à 320 et 1 366 px ; aucun débordement ; titres, descriptions, canoniques et liens internes en ordre ; animations coupées si l'appareil demande moins de mouvement ; contour de focus contrasté sur les cartes.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 31 octobre 2026, 20 h 50 · Formulaire de signalement : champs alignés

- https://revision-vtc.fr/le-livre.html : l'exemple « A3.4, page 65 » passe sous le champ « Fiche ou page », qui s'aligne sur la liste « Type de signalement » ; les listes déroulantes du site ont la même hauteur que les champs de saisie (44 px).
- Vérifications : W3C (Nu) sans erreur ; axe sans erreur en clair et en sombre ; aucun débordement à 320 px ; simulateurs inchangés.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 31 octobre 2026, 19 h 00 · Nouvelle page « Le livre tenu à jour » : inscription des lecteurs et signalement d'erreur

- Page publiée : https://revision-vtc.fr/le-livre.html
  - cinq engagements de l'auteur (vérifier chaque règle sur sa source, revérifier le livre toutes les trois semaines, publier chaque correction, l'envoyer aux lecteurs avec la page corrigée en PDF, répondre à chaque signalement) ;
  - inscription aux mises à jour, réservée aux lecteurs (mot de la fiche G2.6), avec double confirmation par e-mail ;
  - formulaire de signalement d'une erreur ou d'une critique (Web3Forms) ;
  - méthode de vérification et questions fréquentes (FAQPage, WebPage, Book).
- Pages de retour (non indexées) : https://revision-vtc.fr/le-livre-confirmation.html et https://revision-vtc.fr/le-livre-desinscription.html
- Modifiés : menu « Le livre » de toutes les pages (nouvelle entrée en premier) ; https://revision-vtc.fr/mises-a-jour.html (renvoi vers l'inscription) ; https://revision-vtc.fr/mentions-legales.html (deux paragraphes sur les données personnelles : inscription des lecteurs, signalements) ; sitemap.xml ; formulaires : liste déroulante et champs sur deux colonnes qui ne débordent plus à 320 px.
- n8n (serveur de l'auteur) : workflows « Lecteurs du livre : inscription aux mises à jour », « envoyer une mise à jour » (formulaire réservé au compte n8n) et « effacer les inscriptions non confirmées » (chaque lundi) ; table `lecteurs_livre`. E-mails envoyés par benjamin@revision-vtc.fr (Gandi), sans adresse postale. Testés de bout en bout ; envoi réel vérifié vers benjamin@revision-vtc.fr.
- README : section « Le livre tenu à jour ».
- Vérifications sur les 108 pages : W3C (Nu) sans erreur, HTML et CSS ; axe sans erreur en clair et en sombre, à 320 et 1 366 px ; aucun débordement ; titres, descriptions, canoniques, données structurées et liens internes en ordre.
- Points à trancher : le contrôle complet du livre toutes les trois semaines attend le dépôt privé contenant le PDF du livre.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 31 octobre 2026, 14 h 20 · Liens sans flèche, mentions sans points médians, arrondis réduits

- Charte graphique, sur tout le site :
  - plus de flèche « → » ajoutée aux liens « Tous les… » ni aux cartes-liens du wiki et de l'accueil ;
  - mentions de date en phrase (« Publié le 28 octobre 2026, chiffres vérifiés le 27 octobre 2026. Lecture : 9 min. ») au lieu des points médians, dans les actualités, questions, articles et simulateurs ;
  - arrondis de 8 px pour les cartes et 6 px pour les petits encarts (au lieu de 14 et 10 px) ; boutons inchangés ;
  - accueil, diapositive du simulateur : encart d'exemple sans bord rouge à gauche.
- Pages modifiées (mentions seulement) : accueil https://revision-vtc.fr/ ; actualités https://revision-vtc.fr/actualite/ et les 3 numéros ; articles https://revision-vtc.fr/dossiers/ et les 4 articles ; les 3 questions de https://revision-vtc.fr/questions/ ; les 2 simulateurs de https://revision-vtc.fr/simulateurs/.
- Inchangés volontairement : balises `<title>`, titre du livre, ligne « En vigueur depuis… · Modifié par… » du wiki (présentation de Légifrance), photos des articles (à revoir plus tard).
- README, « Charte graphique » : règles des arrondis, des liens et des mentions.
- Vérifications sur les 105 pages : W3C (Nu) sans erreur, HTML et CSS ; axe sans erreur en clair et en sombre, à 320 et 1 366 px ; aucun débordement ; titres, descriptions, canoniques, données structurées et liens internes en ordre. Adresses inchangées.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 31 octobre 2026, 14 h 10 · Cartes sans ombre, surtitres en casse normale

- Charte graphique, sur tout le site (feuille de style seulement, aucune page HTML modifiée) :
  - cartes et encadrés latéraux sans ombre, filet gris seul ; au survol, le filet et le titre passent au rouge, sans soulèvement ; l'ombre reste sous le menu déroulant « Le livre » ;
  - accueil : pastilles numérotées 01 à 04 retirées des quatre tuiles des rubriques (ce n'est pas une suite d'étapes) ;
  - surtitres (« Chaque lundi », « Code des transports »…) et titres des encadrés latéraux (« Sommaire », « Dans le livre ») en casse normale, sans lettres espacées.
- Jetons retirés de `site.css` : `--ombre` et les pastilles `--p1` à `--p4`, devenus inutiles.
- README, « Charte graphique » : règles mises à jour (cartes, surtitres, tuiles de l'accueil).
- Vérifications sur les 105 pages : feuille de style validée par le W3C (Nu) sans erreur ; aucune erreur d'accessibilité (axe) en clair et en sombre, à 320 et 1 366 px ; aucun débordement ; référencement inchangé. Adresses inchangées.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Samedi 31 octobre 2026, 13 h 05 · Fond blanc et nouveau bloc Actualité sur l'accueil

- Charte graphique : le fond crème et les encarts beiges passent au blanc et au gris neutre, sur tout le site (jetons de `docs/css/site.css` uniquement : `--fond`, `--doux`, `--filet`, `--gris`, couleurs posées sur fond foncé, et leurs équivalents du thème sombre, désormais gris anthracite neutre). Deux couleurs écrites en dur remplacées (pied de page, survol du bouton clair). Le rouge du livre ne change pas.
- Accueil, bloc « Le dernier numéro de l'Actualité VTC » : plus de boîte à filet rouge collée à gauche ; le dernier numéro à gauche, les numéros précédents (trois au plus, mis à jour automatiquement chaque lundi) à droite ; une seule colonne sur tablette et téléphone. Page modifiée : https://revision-vtc.fr/
- Validation W3C : trois erreurs anciennes corrigées. Formulaire de contact, attribut `autocomplete` retiré de la case anti-robots (https://revision-vtc.fr/contact.html) ; accueil, rôle `region` ajouté au carrousel ; feuille de style, propriété `mask` écrite en propriétés détaillées (rendu identique).
- README, « Charte graphique » : mentions du beige remplacées, bloc Actualité documenté.
- Vérifications sur les 105 pages : validateur W3C (Nu) sans erreur pour le HTML et la CSS ; aucune erreur d'accessibilité (axe) en clair et en sombre, à 320 et 1 366 px ; aucun débordement ; référencement inchangé (un seul `h1`, titre, description, adresse canonique, Open Graph, données structurées valides, aucun lien interne cassé). Adresses des pages inchangées.
- Règles du livre touchées : aucune.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Vendredi 30 octobre 2026, 22 h 35 · Nouvel outil : calcul de la note de l'examen VTC

- Page publiée (validée par l'auteur) : https://revision-vtc.fr/simulateurs/calcul-note-examen-vtc.html
  - après un examen blanc : admissible ou non, pourquoi, et quoi travailler (note éliminatoire à rattraper, épreuve où combler la moyenne, notes à moins de 2 points du seuil, marge de moyenne) ;
  - notes partielles : ce qu'il faut aux épreuves restantes ; mode « F et G seulement » pour les candidats admissibles au taxi depuis moins de 3 ans (article 5) ;
  - barème officiel avec le poids de chaque épreuve, deux exemples, épreuve pratique, limites de l'outil, questions fréquentes (FAQPage).
- Modifiés : https://revision-vtc.fr/simulateurs/ (deux outils), sitemap.xml, llms.txt.
- Sources : arrêté du 6 avril 2017, articles 2 (version du 1er avril 2024), 3 et 5, Légifrance, consulté le 30 octobre 2026 ; CMA Alsace, fiche V1.4 du 26 janvier 2026 (seuils concordants).
- Garde-fou : le générateur compare le barème (`contenu/calcul_note.json`) au texte de l'arrêté recopié dans le wiki ; si la veille du mercredi met à jour ce texte et que le barème change, la génération s'arrête.
- Vérifications : `node outils/test_calcul_note.js` (cas faits à la main, 200 000 tirages, 20 000 tirages pour les conseils) ; aucune erreur d'accessibilité (axe) en clair et en sombre de 320 à 1 920 px ; aucun débordement ; aucun lien interne cassé.
- Règles du livre touchées : aucune. Le menu affiche toujours « Simulateur » (au singulier) : à trancher par l'auteur.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Jeudi 29 octobre 2026, 14 h 30 · Publication des articles n° 2, 3 et 4

- Publiés (relus par l'auteur) :
  - n° 2 « Chauffeur VTC : combien gagne-t-on vraiment de l'heure sur Uber, Bolt et Heetch ? » : https://revision-vtc.fr/dossiers/combien-gagne-chauffeur-vtc-par-heure.html
  - n° 3 « Chauffeur VTC débutant : 10 erreurs qui coûtent cher (et comment les éviter) » : https://revision-vtc.fr/dossiers/erreurs-chauffeur-vtc-debutant.html
  - n° 4 « Chauffeur VTC salarié ou indépendant : que choisir pour débuter ? » : https://revision-vtc.fr/dossiers/chauffeur-vtc-salarie-ou-independant.html
- Une photo d'en-tête Pixabay par article, avec crédit et lien : REDioACTIVE (conduite de nuit, n° 1929135), dbelkin (remise des clés, n° 5235220), MULTIMEDIOSDS (chauffeur au volant, n° 4786555). Fichiers WebP 640 et 1200 + JPEG 1200 pour le partage dans `docs/images/dossiers/`.
- Index des articles : à date égale, le numéro le plus récent passe en premier.
- Entrées ajoutées dans sitemap.xml, llms.txt et llms-full.txt ; IndexNow signalera les nouvelles pages à Bing.
- Vérifications : aucune erreur d'accessibilité (axe) en clair et en sombre de 320 à 1 920 px ; aucun débordement ; aucun lien interne cassé.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Jeudi 29 octobre 2026, 12 h 25 · « Dossiers » devient « Articles » ; trois articles en brouillon

- La rubrique s'affiche désormais « Articles » partout : menu de toutes les pages, accueil, fil d'Ariane, page d'index (« Articles VTC »), surtitre « Article n° », encadré « Autres articles », données structurées, llms.txt. **Adresses inchangées** (https://revision-vtc.fr/dossiers/ …), conformément à la règle « jamais de changement d'adresse ».
- Trois articles rédigés à partir de l'audit « métier de chauffeur VTC fin 2026 », ton de blog pédagogique, **en brouillon** (non publiés, à relire) :
  - n° 2 « Chauffeur VTC : combien gagne-t-on vraiment de l'heure sur Uber, Bolt et Heetch ? » → https://revision-vtc.fr/dossiers/combien-gagne-chauffeur-vtc-par-heure.html (après publication)
  - n° 3 « Chauffeur VTC débutant : 10 erreurs qui coûtent cher (et comment les éviter) » → https://revision-vtc.fr/dossiers/erreurs-chauffeur-vtc-debutant.html (après publication)
  - n° 4 « Chauffeur VTC salarié ou indépendant : que choisir pour débuter ? » → https://revision-vtc.fr/dossiers/chauffeur-vtc-salarie-ou-independant.html (après publication)
- Chiffres revérifiés sur les sources primaires (rapport ARPE avril 2026, accord du 19 décembre 2023, rapport ARPE de juin 2025 sur les désactivations, fiches Service-Public F31027, F23547, F21746, F2258, SMIC au 1er juin 2026, Cour de cassation 4 mars 2020, directive (UE) 2024/2831). Corrigé par rapport à l'audit : revenu moyen Uber 2025 = 17,30 € (et non « ≈ 17 € »), d'où 35,40 €/h attente comprise.
- Écartés faute de vérification suffisante : la baisse de revenu INSEE taxis-VTC, l'autoliquidation de TVA sur les commissions facturées depuis l'étranger, les chiffres d'offres d'emploi salariées.
- Ajouté : minimum horaire relevé à 32 € en octobre et novembre 2026 (Economie Matin et Entrevue, 30 septembre 2026) ; temps d'attente publié par Uber pour 2024 (41,35 min entre deux courses effectuées).
- Générateur : `**texte**` affiche du gras dans les articles. README mis à jour (« Publier un article »).
- Vérifications : aucune erreur d'accessibilité (axe) en clair et en sombre à 320, 375, 768, 1 280 et 1 920 px (index, quatre articles, accueil, simulateur) ; aucun débordement horizontal.
- Pour publier : retirer la ligne `"brouillon": true` des trois fichiers de `contenu/dossiers/`, puis `python3 outils/generer.py`.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Jeudi 29 octobre 2026, 7 h 45 · Question VTC (tâche du jeudi)

- Question : « Peut-on devenir chauffeur VTC avec un permis probatoire ? »
- Page publiée : https://revision-vtc.fr/questions/2026-10-29-vtc-permis-probatoire.html
- Réponse courte : Non. Pour s'inscrire à l'examen VTC, le délai probatoire du permis B doit être terminé à la date du dépôt de la candidature : en général 3 ans après l'obtention du permis, 2 ans après un apprentissage anticipé de la conduite (conduite accompagnée).
- À noter : Légifrance toujours inaccessible depuis la tâche ; l'article R3120-7 est cité d'après le texte du wiki (vérifié le 25 octobre 2026) et le règlement général des CMA qui le reprend mot pour mot.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 28 octobre 2026, 21 h 40 · Charte graphique : contrôle de tout le site après la refonte

- Tour complet des 16 types de pages (accueil, actualité, questions, dossiers, wiki, simulateur, mises à jour, examens, contact, à propos, mentions légales, 404), sur ordinateur et téléphone : même en-tête, mêmes composants partout.
- Corrigé : couleurs des surfaces foncées (pied de page et diapositive « Le site ») passées en jetons (`--fonce`, `--sur-fonce`…) au lieu de valeurs écrites en dur ; rendu inchangé.
- Corrigé sur téléphone : la rubrique en cours est amenée à l'écran dans le menu qui défile (elle était cachée pour Textes du métier et Simulateur) ; marge gauche du menu respectée.
- README, « Charte graphique » : en-tête et menu « Le livre », carrousel de l'accueil, étapes numérotées, jetons des surfaces foncées.
- Vérifications : aucune erreur d'accessibilité (axe) en clair et en sombre de 320 à 1 920 px ; aucun débordement.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 28 octobre 2026, 21 h 20 · Refonte de l'accueil, du menu et de l'introduction du simulateur

- **Sauvegarde avant refonte** : branche `sauvegarde-2026-10-28` (état du site au commit 5b12445) : https://github.com/75018-montmartre/revision-vtc/tree/sauvegarde-2026-10-28 . Pour revenir en arrière : remettre `main` sur ce commit (ou annuler le commit de la refonte, 052ab2b).
- Toutes les pages : en-tête refait (logo agrandi, sous-titre « Examen, réglementation et métier de chauffeur VTC »), menu réduit à cinq rubriques (Actualité VTC, Questions VTC, Dossiers, Textes du métier, Simulateur) ; « Mises à jour du livre », « Examens blancs n° 4 et 5 » et l'achat Amazon regroupés dans un menu déroulant « Le livre » ; « Accueil » retiré du menu (le logo y mène).
- Accueil : https://revision-vtc.fr/ : carrousel de trois diapositives (le site, gratuit et sourcé ; le simulateur, avec l'exemple recalculé à 983 € nets par mois ; le livre), détaché de l'en-tête ; défilement toutes les 8 s avec bouton de pause, arrêté au survol, au clavier et si l'appareil demande moins d'animations. Tuiles : Actualité, Textes du métier, Dossiers, Simulateur.
- Simulateur : https://revision-vtc.fr/simulateurs/cout-revient-revenu-net-vtc.html : nouveau chapeau, « Comment ça marche » en trois étapes, lexique (montant versé, coût de revient, seuil de rentabilité, revenu net) ; page d'index https://revision-vtc.fr/simulateurs/ : chapeau réécrit. Aucun chiffre ni calcul modifié.
- Nouveaux fichiers fixes : `docs/js/site.js` (menu « Le livre », carrousel) ; composant CSS « .etapes ».
- Vérifications : aucune erreur d'accessibilité (axe) en clair et en sombre à 320, 375, 768, 1 100, 1 280 et 1 920 px (accueil avec chaque diapositive, simulateur, mises à jour, examens, wiki, actualité, dossier, 404) ; aucun débordement horizontal ; aucun lien interne cassé ; calcul du simulateur testé.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 28 octobre 2026, 20 h 10 · Simulateur « coût de revient de la voiture VTC et revenu net »

- Nouvelle rubrique « Simulateur » (lien ajouté au menu de toutes les pages) : https://revision-vtc.fr/simulateurs/
- Publié : https://revision-vtc.fr/simulateurs/cout-revient-revenu-net-vtc.html
  - Pour un chauffeur en micro-entreprise : montant versé par les plateformes, commission, location à la semaine / LLD-LOA / achat, essence, gazole ou électricité, assurance, entretien, autres frais, Alsace-Moselle, versement libératoire.
  - Résultats : revenu net par mois et par an, détail poste par poste, coût de revient de la voiture au km et par mois, seuil de rentabilité par semaine, revenu net par heure, revenu imposable ; alertes TVA (37 500 / 41 250 €), plafond micro (83 600 €), perte, entretien non saisi. Lien partageable (la simulation est dans l'adresse) ; rien n'est envoyé.
  - Exemple publié (valeurs par défaut) : 1 000 € versés par semaine, 47 semaines, hybride louée 280 €/semaine, 60 000 km → 983 € net par mois si cotisations sur le prix payé par les clients, 1 270 € si sur le montant versé ; voiture 0,36 €/km.
  - 26 sources : fiches Service-Public (cotisations, formation, CMA, régime fiscal, TVA, seuils micro), DGEC (carburants du 23 octobre 2026), ADEME Car Labelling, SDES (38 € par heure en 2024), Uber, Bolt, CRE via deux sources (électricité), courtiers et loueurs du dossier n° 1.
- **Point à trancher** : aucun texte officiel ne dit si le chiffre d'affaires d'un chauffeur de plateforme est le prix payé par le client ou le montant versé après commission ; le simulateur propose les deux (« prudent » par défaut). La TVA au-delà de 41 250 € est signalée mais pas calculée (règles de déduction à vérifier sur le BOFiP avant de l'ajouter).
- Maillage : lien depuis le dossier n° 1 (section « Le budget total ») et encadré « Simulateur gratuit » sur chaque dossier ; index des dossiers ; sitemap, llms.txt, données structurées WebApplication.
- À mettre à jour : prix des carburants chaque mois, taux et seuils au 1er janvier 2027, électricité au 1er février 2027 (procédure dans README, « Mettre à jour le simulateur »).
- Vérifications : calcul testé (node outils/test_simulateur.js, même résultat que le générateur) ; aucune erreur d'accessibilité (axe) en clair et en sombre à 320, 768, 1 280 et 1 920 px sur le simulateur, les dossiers et l'accueil ; aucun débordement horizontal ; aucun lien interne cassé.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 28 octobre 2026, 19 h 20 · Actualité VTC n° 3 (tâche du lundi)

- **PROBLÈME : Légifrance toujours inaccessible** (refus 403). Journal officiel vérifié seulement par les pages indexées ; exament3p.fr non lu cette fois (lecture non autorisée à temps).
- Publié : https://revision-vtc.fr/actualite/2026-10-28.html
- Titre : « Examen VTC 2027 : 11 dates publiées, aucun nouveau texte officiel » (période du 27 au 28 octobre 2026, tâche lancée le mercredi).
- Textes officiels : aucun nouveau texte VTC repéré au Journal officiel du 27 au 28 octobre 2026.
- Examen : calendrier national 2027 de CMA France, 11 épreuves d'admissibilité (mardis, du 26 janvier au 7 décembre 2027) ; Hauts-de-France : inscription avant le 18 décembre 2026 à 12 h pour le 26 janvier 2027.
- Livre : rien à corriger.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 28 octobre 2026, 16 h 10 · Rubrique Dossiers, dossier n° 1 et IndexNow

- Nouvelle rubrique « Dossiers » (articles longs, un par semaine, relus par l'auteur) : https://revision-vtc.fr/dossiers/ , lien « Dossiers » ajouté au menu de toutes les pages.
- Dossier n° 1 publié : « Combien coûte vraiment le lancement en VTC ? Le budget complet 2026-2027 » : https://revision-vtc.fr/dossiers/cout-pour-devenir-chauffeur-vtc.html
  - Frais obligatoires 2026 : 539,60 € plus l'envoi de la carte (examen 241 €, visite médicale 36 €, carte 57,60 €, registre 170 €, vignette 35 € environ, micro-entreprise gratuite).
  - Trois budgets : de 2 730 € à 4 040 € (candidat libre, voiture louée à la semaine), de 3 130 € à 7 040 € (avec formation), de 37 600 € à 45 320 € (voiture neuve achetée comptant).
  - 13 sources, dont la fiche officielle « Devenir chauffeur de VTC » vérifiée le 12 août 2026 ; 5 photos Pixabay choisies par l'auteur, avec crédit.
  - À mettre à jour en janvier 2027 : tarif de l'examen (réévalué chaque 1er janvier).
- Données structurées Article, image de partage propre au dossier, entrées dans sitemap.xml, llms.txt et llms-full.txt.
- IndexNow pour Bing : clé publique en ligne (https://revision-vtc.fr/ffb463a3b58a4d6f80ea5043c02886aa.txt) ; à chaque publication, une tâche GitHub signale à Bing les pages ajoutées ou modifiées (onglet Actions, « IndexNow (Bing) »). Premier envoi : toutes les pages, puisque le menu a changé partout.
- Vérifications : aucune erreur d'accessibilité (axe) en clair et en sombre, de 320 px au grand écran ; aucun lien interne cassé.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 28 octobre 2026, 15 h 47 · Question VTC (tâche du jeudi)

- Question : « Quelles cotisations paie un chauffeur VTC en micro-entreprise ? »
- Publié : https://revision-vtc.fr/questions/2026-10-28-cotisations-vtc-micro-entreprise.html
- Réponse courte : en 2026, 21,2 % du chiffre d'affaires en cotisations sociales, plus 0,3 % de formation professionnelle et, hors Alsace-Moselle, 0,48 % de taxe de chambre de métiers, soit près de 22 % au total, calculés sur le chiffre d'affaires et non sur le bénéfice.
- Sources : fiches officielles d'Entreprendre.Service-Public.fr et guide Urssaf (Légifrance toujours inaccessible depuis la tâche : sujet choisi pour reposer sur des sources lisibles).
- Publication anticipée d'un jour (tâche lancée le mercredi).
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 28 octobre 2026, 15 h · Veille du wiki (tâche du mercredi)

- **PROBLÈME : Légifrance toujours inaccessible (troisième passage de la journée).** Connexion directe refusée (403) à legifrance.gouv.fr, aux données ouvertes de la DILA, à l'API PISTE et à data.gouv.fr. L'outil web ne renvoie qu'un résumé d'une version datée du 20 septembre 2024 : impossible de comparer mot à mot.
- Articles vérifiés : 0 sur 78. Articles non lus : les 78 (73 articles de code et 5 arrêtés).
- Aucun texte modifié, aucune explication réécrite (chaque réécriture exige de relire l'article officiel).
- Date « vérifié » laissée au 25 octobre 2026.
- Contrôle technique : génération réussie, aucune différence avec les pages en ligne, sitemap complet (79 adresses du wiki).
- À faire : autoriser legifrance.gouv.fr dans les accès réseau de la tâche, ou la faire tourner depuis l'ordinateur (option « Exiger cet ordinateur », navigateur intégré). Inutile de relancer la tâche avant ce réglage : le résultat sera le même.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 28 octobre 2026, 14 h 50 · Veille du wiki (tâche du mercredi)

- **PROBLÈME : Légifrance toujours inaccessible (deuxième passage de la journée).** Le réseau de la tâche refuse encore la connexion à legifrance.gouv.fr (refus 403), et la lecture par l'outil web a été bloquée faute d'autorisation.
- Articles vérifiés : 0 sur 78. Articles non lus : les 78 (73 articles de code et 5 arrêtés).
- Aucun texte modifié, aucune explication réécrite (chaque réécriture exige de relire l'article officiel).
- Date « vérifié » laissée au 25 octobre 2026.
- Contrôle technique : génération réussie, aucune différence avec les pages en ligne, sitemap complet (79 adresses du wiki).
- À faire : autoriser legifrance.gouv.fr dans les accès réseau de la tâche, ou la faire tourner depuis l'ordinateur (option « Exiger cet ordinateur », navigateur intégré).
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mercredi 28 octobre 2026, 7 h 45 · Veille du wiki (tâche du mercredi)

- **PROBLÈME : Légifrance inaccessible depuis l'environnement de la tâche.** Le réseau de la tâche refuse toute connexion à legifrance.gouv.fr (et aux données ouvertes de la DILA). Seule une lecture résumée passe, et elle affiche une version datée du 20 septembre 2024 : elle ne permet pas de comparer mot à mot.
- Articles vérifiés : 0 sur 78. Articles non lus : les 78 (73 articles de code et 5 arrêtés).
- Aucun texte modifié, aucune explication réécrite (chaque réécriture exige de relire l'article officiel).
- Date « vérifié » laissée au 25 octobre 2026.
- Contrôle technique : génération réussie, aucune différence avec les pages en ligne, sitemap complet (79 adresses du wiki).
- Pour la semaine prochaine : faire tourner la tâche depuis l'ordinateur (option « Exiger cet ordinateur », navigateur intégré) ou autoriser legifrance.gouv.fr dans les accès réseau.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mardi 27 octobre 2026, 19 h 10 · Prix de lancement du livre

- Prix du livre broché passé de 27,90 € à 24,90 € (prix de lancement, à remonter après les premiers avis).
- Prix mis à jour dans les données structurées du livre (Google, assistants d'IA).
- Campagne Amazon Ads « A - VTC Mots-cles » lancée ce soir (25 mots-clés, 14 négatifs, 10 €/jour, enchères à la baisse uniquement).
- Campagne Amazon Ads « B - VTC Livres concurrents » lancée ce soir (18 livres concurrents ciblés, 0,40 € par clic, 5 €/jour).
- Campagne Amazon Ads « C - Auto » lancée ce soir (ciblage automatique, 0,40 € par défaut, 14 négatifs, 3 €/jour).
- Premier bilan des campagnes prévu le mardi 3 novembre 2026.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Mardi 27 octobre 2026, 9 h · Le livre est en vente : liens Amazon activés

- Tous les boutons « Bientôt disponible sur Amazon » deviennent « Acheter le livre sur Amazon » : https://www.amazon.fr/dp/B0HPCMRKDR (accueil, pied de toutes les pages, encadrés « Dans le livre » du wiki et des questions).
- Données structurées du livre complétées (lien Amazon, prix 27,90 €) pour Google et les assistants d'IA.
- Détail : https://github.com/75018-montmartre/revision-vtc/commits/main

## Lundi 26 octobre 2026, fin d'après-midi · Journal et récapitulatifs

- Création de ce journal.
- Mise en place d'un envoi de récapitulatif par e-mail (inactif tant que les identifiants ne sont pas enregistrés dans GitHub).

## Lundi 26 octobre 2026, 17 h 37 · Formulaire de contact activé

- Nouvelle page : https://revision-vtc.fr/contact.html (prénom, nom, e-mail, message de 1 000 caractères au plus), lien « Contact » dans le pied de page.
- Mentions légales complétées (traitement des messages, durée de conservation, droits).
- Détail : https://github.com/75018-montmartre/revision-vtc/commit/79223f4

## Lundi 26 octobre 2026, 7 h 51 · Actualité VTC n° 2 (tâche du lundi)

- Publié : https://revision-vtc.fr/actualite/2026-10-26.html
- Titre : « Directive européenne plateformes en retard, examen VTC inchangé ».
- Détail : https://github.com/75018-montmartre/revision-vtc/commit/a152946

## Dimanche 25 octobre 2026 · Refonte du site

- Wiki « Textes du métier » : 78 pages (texte officiel Légifrance expliqué en clair) : https://revision-vtc.fr/wiki/
- Rubrique « Questions VTC » et première question : https://revision-vtc.fr/questions/2026-10-25-vtc-attente-gare-aeroport.html
- Référencement (Google, Bing, assistants d'IA), page « À propos et méthode », page 404.
- Nouvelle charte graphique, mise en page centrée.
