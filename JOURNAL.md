# Journal des mises à jour de revision-vtc.fr

Chaque publication sur le site ajoute ici une entrée, la plus récente en haut : ce qui a été fait, les pages concernées et le lien vers le détail des changements.

Adresse à garder en favori : https://github.com/75018-montmartre/revision-vtc/blob/main/JOURNAL.md

---

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
