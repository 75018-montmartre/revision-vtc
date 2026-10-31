# revision-vtc.fr

Site compagnon du livre *Machine à Réussite · Examen VTC 2027* (Benjamin Blondin).

## Organisation du dépôt

| Dossier | Contenu |
|---|---|
| `contenu/actualite/AAAA-MM-JJ.json` | Un numéro de l'Actualité VTC (un fichier par semaine, nommé par sa date de publication) |
| `contenu/mises-a-jour.json` | Les corrections du livre après impression et les points à surveiller |
| `contenu/wiki.json` | Le wiki « Textes du métier » (`docs/wiki/`) : pour chaque article, le thème, l'explication « En clair », l'exemple « Concrètement », les fiches du livre, le texte officiel recopié de Légifrance (`texte`, `vigueur`, `modif`) et son lien ; plus les lois d'origine et références externes (`autres`). Date de vérification : `verifie`. |
| `contenu/questions/AAAA-MM-JJ-adresse.json` | Une « Question VTC » (une par semaine, publiée le jeudi) : question, réponse courte, développement, à retenir, liens vers le wiki, fiches du livre, sources |
| `contenu/dossiers/adresse.json` | Un article de la rubrique « Articles » (1 500 à 2 500 mots, ton pédagogique de blog, publié dans `docs/dossiers/`) : voir « Publier un article » |
| `contenu/simulateur.json` | Les hypothèses du simulateur « coût de revient et revenu net » (`docs/simulateurs/`) : chaque valeur, ses sources et la date de vérification ; voir « Mettre à jour le simulateur » |
| `contenu/indexnow.json` | La clé publique IndexNow (`cle`), servie à la racine du site sous `docs/<clé>.txt` |
| `contenu/fiches.json` | Codes et titres des fiches du livre, pour les renvois « Dans le livre » |
| `contenu/contact.json` | La clé d'accès Web3Forms du formulaire de contact (`web3forms_cle`) ; vide, la page Contact affiche l'adresse e-mail à la place du formulaire |
| `contenu/livre.json` | L'adresse de la page Amazon du livre (`amazon`) ; vide, le site affiche « Bientôt disponible sur Amazon ». Et l'adresse n8n qui reçoit les inscriptions des lecteurs (`inscription_url`) |
| `outils/generer.py` | Génère tout le site dans `docs/` à partir de `contenu/` |
| `outils/indexnow.py` | Signale à Bing (IndexNow) les pages ajoutées ou modifiées, lancé par `.github/workflows/indexnow.yml` |
| `outils/test_simulateur.js` | Vérifie le calcul du simulateur sur des cas faits à la main (`node outils/test_simulateur.js`) |
| `contenu/calcul_note.json` | Le barème de l'examen pour le « calcul de la note » (`docs/simulateurs/`) : voir « Calcul de la note de l'examen » |
| `outils/test_calcul_note.js` | Vérifie le calcul de la note sur des cas faits à la main et 200 000 tirages (`node outils/test_calcul_note.js`) |
| `outils/gabarit.py` | En-tête, menu et pied de page communs |
| `docs/` | Le site publié par GitHub Pages (ne pas modifier les pages HTML à la main : elles sont régénérées) |

Les fichiers fixes de `docs/` (feuille de style, polices, scripts communs `js/site.js` et des examens, données des examens, PDF, `CNAME`) ne sont pas régénérés.

## Publier un numéro de l'Actualité VTC

1. Créer `contenu/actualite/AAAA-MM-JJ.json` sur le modèle du numéro précédent (format ci-dessous).
2. Si une règle du livre change : ajouter une ligne dans `contenu/mises-a-jour.json` (`corrections`).
   Si un article du wiki est modifié ou abrogé sur Légifrance : recopier le nouveau texte dans `contenu/wiki.json`, revoir « En clair » et « Concrètement », mettre à jour `verifie`. Le texte officiel n'est jamais réécrit : il est recopié tel quel.
3. Lancer `python3 outils/generer.py` depuis la racine du dépôt : il vérifie que chaque brève a au moins une source.
4. Publier directement sur `main` (commit puis push) : le site est mis à jour en quelques minutes. L'auteur reçoit ensuite un récapitulatif.

Calendrier des publications automatiques : lundi, Actualité VTC ; mercredi, veille du wiki ; jeudi, Question VTC.

## Le livre tenu à jour (lecteurs inscrits)

Page `docs/le-livre.html` (générée par `livre_vivant()`) : engagements de l'auteur, inscription des lecteurs aux mises à jour, signalement d'une erreur, méthode de vérification. Pages de retour : `le-livre-confirmation.html` et `le-livre-desinscription.html` (non indexées).

- **Inscription** : le formulaire envoie l'adresse, le mot de la fiche G2.6 et la case cochée au workflow n8n « Lecteurs du livre : inscription aux mises à jour » (adresse `inscription_url` de `contenu/livre.json`). Il vérifie la demande, enregistre l'adresse « en_attente » dans la table n8n `lecteurs_livre` et envoie un lien de confirmation depuis benjamin@revision-vtc.fr (identifiant n8n « SMTP Gandi benjamin@revision-vtc.fr »). Le lien passe l'adresse en « confirme » ; le lien de désinscription l'efface. Le workflow « effacer les inscriptions non confirmées » supprime chaque lundi celles de plus de trois mois.
- **Signalement** : formulaire Web3Forms (même clé que la page Contact), reçu dans la boîte de l'auteur.
- **Envoyer une correction aux lecteurs** : 1) ajouter la correction dans `contenu/mises-a-jour.json` et publier ; 2) ouvrir le formulaire n8n « Lecteurs du livre : envoyer une mise à jour » (connecté à n8n), écrire le message, joindre les pages corrigées en PDF, cocher la case, envoyer. Seules les adresses confirmées le reçoivent, chacune avec son lien de désinscription.
- Les engagements de la page (vérification complète toutes les trois semaines, réponse à chaque signalement, envoi des corrections) doivent rester vrais : ne pas les modifier sans l'accord de l'auteur.

### Format d'un numéro

```json
{
  "date": "AAAA-MM-JJ",
  "numero": 2,
  "titre": "Titre du numéro, factuel, sans point final",
  "periode": "du JJ mois au JJ mois AAAA",
  "a_retenir": ["Une phrase par information importante (3 au plus)."],
  "rubriques": [
    {"titre": "Textes officiels", "breves": [
      {"titre": "Titre de la brève", "texte": ["Paragraphe 1.", "Paragraphe 2."],
       "sources": [{"nom": "Nom de la source", "url": "https://...", "date": "JJ mois AAAA"}]}
    ]}
  ],
  "impact_livre": ["Ce que ça change pour le livre, avec les codes des fiches (par exemple A3.6)."],
  "verifie": "JJ mois AAAA"
}
```

Rubriques possibles, dans cet ordre : « Textes officiels », « Examen », « Rémunération et plateformes », « Cotisations et statut », « Sécurité routière », « Contrôles et sanctions », « Europe ». Une rubrique sans nouvelle est omise, sauf « Textes officiels » et « Examen », qui disent explicitement « aucune nouveauté » avec la date de vérification.

### Format d'une correction du livre

```json
{"date": "JJ mois AAAA", "fiche": "A3.6", "avant": "Ce que dit le livre", "apres": "Ce qu'il faut retenir", "texte": "Texte officiel qui fonde la nouvelle règle"}
```

## Accès aux examens blancs

Réservé aux lecteurs : le site demande le dernier mot du titre de la fiche G2.6 (page 160). Seule l'empreinte SHA-256 de la réponse est dans `docs/js/acces.js`.

## Référencement (SEO) et citations par les assistants d'IA (GEO)

Tout est automatique : `outils/generer.py` ajoute à chaque page indexable l'adresse canonique, les balises de partage (Open Graph, image `docs/partage.jpg`) et les données structurées schema.org (livre, articles du wiki rattachés au texte officiel, numéros de l'Actualité, fil d'Ariane). Il produit aussi `sitemap.xml` (avec dates de mise à jour), `robots.txt` (moteurs et assistants d'IA explicitement autorisés), `llms.txt` (plan du site pour les IA) et `llms-full.txt` (tout le wiki en texte brut, avec ses sources).

Règles pour tout nouveau contenu :
- chaque page a un titre unique et une description de 50 caractères au moins (le générateur s'arrête sinon) ;
- une idée par paragraphe, la réponse d'abord, puis le détail : c'est ce que reprennent les moteurs et les assistants ;
- chiffres exacts, avec leur unité, leur date et leur source ;
- relier les brèves aux pages du wiki concernées.

## Publier une Question VTC

Fichier `contenu/questions/AAAA-MM-JJ-adresse.json` (l'adresse est en minuscules, mots séparés par des tirets, avec le mot-clé principal : `vtc-attente-gare-aeroport`). Modèle : la première question publiée.

```json
{"date": "AAAA-MM-JJ", "slug": "adresse-de-la-page",
 "question": "La question telle qu'un chauffeur la taperait dans Google ?",
 "reponse_courte": "La réponse en une ou deux phrases, autonome (50 à 400 caractères).",
 "sections": [{"titre": "Intertitre", "texte": ["Paragraphe."]}],
 "a_retenir": ["Trois phrases autonomes au plus."],
 "wiki": ["l3120-2"], "fiches": [["A3.4", "Gares et aéroports"]],
 "sources": [{"nom": "Nom de la source", "url": "https://...", "date": "JJ mois AAAA"}],
 "verifie": "JJ mois AAAA"}
```

Le générateur refuse une question sans source, sans point d'interrogation, ou qui renvoie vers une page du wiki inexistante.

## Publier un article (rubrique « Articles »)

Fichier `contenu/dossiers/adresse.json`, nommé par l'adresse de la page (minuscules, tirets, mots-clés principaux : `cout-pour-devenir-chauffeur-vtc`). La rubrique s'appelait « Dossiers » jusqu'au 29 octobre 2026 ; elle s'affiche désormais « Articles », mais le dossier technique et les adresses restent `dossiers/` (règle : jamais de changement d'adresse). La page est publiée à `https://revision-vtc.fr/dossiers/adresse.html` ; l'adresse ne change plus ensuite (un article se met à jour, avec `mis_a_jour`). Modèles : l'article n° 1 (budget, ton de référence chiffré) et les articles n° 2 à 4 (ton de blog pédagogique : un exemple concret pour commencer, phrases courtes, « vous », listes en gras).

```json
{"numero": 1, "slug": "adresse", "date": "AAAA-MM-JJ", "brouillon": true,
 "titre": "Le titre affiché, avec les mots que les gens tapent",
 "titre_page": "Le titre de l'onglet et de Google (facultatif)",
 "image": {"fichier": "...", "alt": "...", "legende": "...", "credit": "...", "lien": "..."},
 "description": "50 à 160 caractères, avec les chiffres clés.",
 "mots_cles": ["..."],
 "chapeau": "Une ou deux phrases.",
 "en_bref": ["La réponse d'abord, autonome, chiffrée."],
 "sections": [{"id": "ancre", "titre": "Intertitre", "blocs": [
   "Paragraphe ; lien : [texte](../wiki/r3120-6.html)",
   {"liste": ["élément"]},
   {"note": "Encart gris clair"},
   {"tableau": {"legende": "Légende obligatoire", "colonnes": ["Poste", "Montant"], "nombres": [1],
                "lignes": [["Examen", "241 €"]], "total": [["Total", "241 €"]]}},
   {"image": {"fichier": "nom-de-la-photo", "alt": "Ce que montre la photo", "legende": "Phrase utile au lecteur",
              "credit": "auteur Pixabay", "lien": "https://pixabay.com/fr/photos/..."}}]}],
 "a_retenir": ["Phrases autonomes."],
 "wiki": ["r3120-6"], "fiches": [["A2.6", "La carte professionnelle au quotidien"]],
 "sources": [{"nom": "Nom de la source", "url": "https://...", "date": "consulté le JJ mois AAAA"}],
 "verifie": "JJ mois AAAA", "mis_a_jour": "JJ mois AAAA (facultatif)"}
```

- **Brouillon** : tant que `"brouillon": true`, l'article n'est pas publié. `python3 outils/generer.py --apercu` construit une copie complète du site avec les brouillons dans `apercu/` (jamais versionné) pour la relecture par l'auteur. Pour publier : retirer la ligne `brouillon`, mettre la date de publication, lancer `python3 outils/generer.py`.
- Mise en forme dans les textes : `[texte](adresse)` pour un lien, `**texte**` pour du gras.
- Le générateur refuse un article sans source, de moins de 1 200 ou de plus de 3 000 mots (hors brouillon), qui renvoie vers une page du wiki inexistante ou dont la description est trop courte ou trop longue.
- **Photos** (Pixabay ou équivalent, jamais d'image générée par IA) : recadrées en 3:2 et enregistrées dans `docs/images/dossiers/` sous un nom qui décrit la photo, en deux tailles WebP (`<nom>-640.webp`, `<nom>-1200.webp`) ; la photo d'en-tête (`image`) a aussi un `<nom>-1200.jpg`, utilisé pour le partage sur les réseaux sociaux et dans les données structurées. Une photo par section au plus, placée en tête de section. Le texte alternatif décrit ce qu'on voit ; la légende dit ce que le lecteur doit retenir. Le générateur refuse une photo dont un fichier manque ou sans texte alternatif.
- Données structurées : `Article` (avec `wordCount`, `citation`, `abstract` = la réponse en bref) et fil d'Ariane ; le dossier entre dans `sitemap.xml` et `llms.txt`.
- Chaque chiffre a sa source : texte officiel ou deux sources concordantes. Les prix libres (formation, assurance, véhicule) sont donnés en fourchettes publiées, avec leurs sources, jamais comme un tarif.

## Mettre à jour le simulateur

Page : https://revision-vtc.fr/simulateurs/cout-revient-revenu-net-vtc.html (adresse définitive), avec la page d'accueil de la rubrique `simulateurs/`. Le calcul se fait dans le navigateur (`docs/js/simulateur.js`) ; les valeurs par défaut viennent de `contenu/simulateur.json`, injecté dans la page par le générateur, qui recalcule aussi l'exemple chiffré publié dans la page (`calcul_simulateur`, même formule que le script).

- Chaque valeur a des `sources` (identifiants de la liste `sources`) ou est marquée `"exemple": true` (hypothèse à remplacer par l'utilisateur, jamais présentée comme un chiffre de référence). Le générateur refuse une valeur sans l'un ou l'autre.
- **Chaque lundi (tâche « Actualité VTC »)** : prix des carburants. Dans `contenu/simulateur.json`, changer `valeur` et `date` de `prix_e10` et `prix_gazole` (prix moyens TTC du dernier vendredi, fichier « Prix HTT et TTC depuis janvier 2020 » de la DGEC, onglet « Carburants routiers », colonnes T.T.C.) et la date citée dans le nom de la source `dgec` et dans sa date de consultation ; rien d'autre : la page reprend ces valeurs partout. Le générateur refuse deux dates différentes ou une source qui ne cite pas la date. **Chaque 1er janvier** : taux de cotisations, seuils de TVA et de la micro-entreprise. **Au 1er août et au 1er février** : tarif réglementé de l'électricité. Mettre à jour `verifie`, puis les textes d'aide de `simulateur()` dans `outils/generer.py` qui citent ces valeurs.
- Après toute modification du calcul : `node outils/test_simulateur.js`, puis vérifier la page en clair et en sombre, de 320 px au grand écran.

## Calcul de la note de l'examen

Page : https://revision-vtc.fr/simulateurs/calcul-note-examen-vtc.html (adresse définitive), listée dans `simulateurs/`. Le barème est dans `contenu/calcul_note.json` (épreuves A à G : durée, coefficient, note éliminatoire, composition ; deux exemples ; sources), injecté dans la page ; le calcul se fait dans le navigateur (`docs/js/calcul-note.js`), en centièmes de point entiers (une moyenne de 9,999 n'est jamais affichée 10).

- **Recoupement automatique** : le générateur compare la durée et le coefficient de chaque épreuve, les seuils (10, 6, 4) et la note de l'épreuve pratique (12) au texte de l'arrêté du 6 avril 2017 recopié dans `contenu/wiki.json`. Si la veille du mercredi met à jour ce texte et que le barème change, le générateur s'arrête jusqu'à ce que `calcul_note.json` soit corrigé (puis `verifie` mis à jour).
- Le mode « seulement F et G » applique l'article 5 de l'arrêté (candidat admissible à l'examen de taxi depuis moins de 3 ans).
- Après toute modification : `node outils/test_calcul_note.js`, puis vérifier la page en clair et en sombre, de 320 px au grand écran.

## IndexNow (Bing)

À chaque mise à jour de `main` qui touche `docs/`, GitHub Actions (`.github/workflows/indexnow.yml`) attend que GitHub Pages serve la nouvelle version, puis envoie à IndexNow la liste des pages HTML ajoutées ou modifiées (pages `noindex` et redirections exclues). Aucun secret : la clé est publique. Envoi complet du sitemap : onglet Actions > « IndexNow (Bing) » > Run workflow, case « Envoyer toutes les adresses ». Essai sans envoi : `python3 outils/indexnow.py --essai`.

## Charte graphique

Une seule feuille de style, `docs/css/site.css`, organisée en sept parties (jetons, base, structure, typographie, composants, pages, adaptations). Règles à respecter pour garder un site homogène :

- **Couleurs** : uniquement les jetons de `:root` (`--fond`, `--carte`, `--doux`, `--encre`, `--gris`, `--filet`, `--rouge`, `--accent`). Surfaces foncées (pied de page, diapositives foncées de l'accueil) : `--fonce` pour le fond, `--sur-fonce`, `--sur-fonce-doux`, `--sur-fonce-gris` et `--sur-fonce-filet` pour ce qui est posé dessus. Jamais de couleur écrite en dur dans une page. Le thème sombre est géré par les mêmes jetons. Fond général blanc et gris neutres (ni crème ni beige, depuis le 31 octobre 2026) : `--fond` blanc, `--doux` gris très clair pour les encarts et les bandes ; le rouge du livre reste la seule couleur de marque.
- **Typographie** : Inter pour les titres, menus, boutons et mentions ; EB Garamond pour le texte de lecture. Pas d'autre police.
- **En-tête du site** (toutes les pages, `outils/gabarit.py`) : logo et nom du site à gauche ; menu des cinq rubriques (`NAV` : Actualité VTC, Questions VTC, Articles, Textes du métier, Simulateur) ; à droite, le menu déroulant « Le livre » (`MENU_LIVRE` : mises à jour, examens blancs, achat), pilule à contour rouge, noire quand on est sur une de ses pages. Pas d'« Accueil » dans le menu : le logo y mène. Une nouvelle rubrique s'ajoute à `NAV` seulement si elle est de même niveau que les cinq autres ; tout ce qui concerne le livre va dans `MENU_LIVRE`. Sur une seule ligne sur grand écran, menu sous le logo sur écran moyen, menu qui défile horizontalement sur téléphone (la rubrique en cours est amenée à l'écran par `docs/js/site.js`).
- **Accueil** : carrousel de trois diapositives en panneaux à coins arrondis, détachés de l'en-tête (le site sur fond foncé, le simulateur sur fond gris clair avec un exemple en carte, le livre sur fond rouge) ; commandes en pilules numérotées et bouton de pause ; défilement automatique arrêté au survol, au clavier, au choix d'une diapositive et si l'appareil demande moins d'animations (`docs/js/site.js`). Le titre principal de la page (`h1`) est permanent et caché visuellement ; les titres des diapositives sont des `h2`. Bloc « Le dernier numéro de l'Actualité VTC » sur deux colonnes, sans boîte : le dernier numéro à gauche (titre et points à retenir), les numéros précédents à droite (trois au plus, `.actu-une`, `.actu-precedents`) ; une seule colonne sur tablette et téléphone.
- **Structure d'une page intérieure** (automatique, faite par `outils/gabarit.py`) : bande d'en-tête blanche avec fil d'Ariane (s'il y en a un), surtitre rouge en casse normale, titre, chapeau ; puis la colonne de lecture (46rem), alignée à gauche sur le logo. Chaque page commence donc par `<p class="surtitre">` (facultatif : sinon celui de la rubrique), `<h1>`, puis `<p class="chapeau">` ou `<p class="meta">`.
- **Trois mises en page, choisies automatiquement et toujours centrées dans l'écran** : une colonne de lecture (pages simples) ; colonne + encadré à droite « Dans le livre », « Voir aussi » (`.deux-col`, pages du wiki et Questions VTC ; l'encadré passe sous le texte sur tablette et téléphone) ; pages d'index avec grilles de cartes. L'en-tête de page prend toujours la même largeur que le contenu.
- **Surtitres et petits titres** (`.surtitre`, titres des encadrés latéraux) : en casse normale, jamais en capitales ni en lettres espacées ; les textes s'écrivent normalement dans le contenu.
- **Deux niveaux de titres de section** : l'en-tête de bloc (`.tete-bloc` : surtitre, titre, lien « Tous les… » à droite, trait noir épais) pour les blocs de l'accueil et les thèmes du wiki ; l'intertitre de contenu (`h2`, petit trait rouge au-dessus) dans les pages.
- **Une seule forme de boîte, la carte** : fond blanc, filet, coins arrondis (8 px ; 6 px pour les petits encarts `--rayon-p`), sans ombre (l'ombre `--ombre-h` est réservée au menu déroulant « Le livre »). Variante « mise en avant » : filet rouge épais à gauche (`.en-clair`, `.retenir`). Carte cliquable : toute la surface est un lien ; au survol, le filet et le titre passent au rouge, sans ombre ni mouvement. Encart secondaire : fond gris clair `--doux` (`.concretement`, `.impact`, `.note`).
- **Étapes numérotées** (`.etapes`, mode d'emploi d'un outil) : pastille foncée numérotée, titre court en gras, explication ; un petit lexique se met dans un encart gris clair (`.note` avec une liste `dl`).
- **Boutons** en pilule (`.bouton`, `.bouton.second`, `.bouton.petit`) ; liens « voir tout » avec `.lien-fleche` (souligné rouge, sans flèche ajoutée). Pas de flèche « → » ajoutée aux liens ni aux cartes-liens.
- **Mentions** (`.meta` : date, numéro, vérification, durée de lecture) : en phrase, avec des virgules ou des points, jamais une suite d'éléments séparés par des points médians « · ». Exception : la ligne « En vigueur depuis… · Modifié par… » du wiki, qui reprend la présentation de Légifrance, et les balises `<title>`.
- **Grilles** : tuiles de l'accueil 4 / 2 / 1 colonnes, sans pastille numérotée (une numérotation 01, 02… seulement pour une vraie suite d'étapes, voir `.etapes`) ; cartes-liens en grille automatique. Jamais de tuile orpheline.
- **Accessibilité** : contraste AA minimum, cibles tactiles de 40 px au moins, focus visible, aucune information portée par la couleur seule, animations coupées si l'appareil le demande.
- Avant d'ajouter une règle CSS, chercher un composant existant. Toute nouvelle règle va dans la bonne partie du fichier, avec un commentaire.

## Récapitulatif par e-mail

À chaque mise à jour de `main`, GitHub Actions (`.github/workflows/recap.yml`) lance `outils/recap_mail.py`, qui envoie un e-mail au destinataire configuré : le récapitulatif écrit dans le corps des messages de commit, la liste des pages ajoutées, de celles dont le contenu a changé et de celles supprimées (avec leur adresse en ligne), et le lien vers le détail sur GitHub.

**Toute publication doit donc avoir un message de commit complet** : une première ligne courte (le titre), une ligne vide, puis le récapitulatif en texte simple (ce qui a été publié, les sources consultées et celles non lues, ce qui n'a pas été retenu, les règles du livre touchées, les points à trancher).

L'envoi passe par la boîte benjamin@revision-vtc.fr (serveur mail.gandi.net, port 465). Les identifiants sont dans les secrets GitHub du dépôt (`SMTP_UTILISATEUR`, `SMTP_MOT_DE_PASSE`, `RECAP_DESTINATAIRE`), jamais dans les fichiers.

## Journal des mises à jour

`JOURNAL.md` (à la racine, hors du site publié) garde la trace de chaque publication, la plus récente en haut. **Toute publication y ajoute une entrée** : jour, heure de Paris, titre, pages publiées ou modifiées avec leur adresse en ligne, points importants (règle du livre modifiée, problème), et lien vers le commit (`https://github.com/75018-montmartre/revision-vtc/commit/<identifiant>`, identifiant du commit précédent si besoin, ou la page des commits). L'auteur le consulte à l'adresse https://github.com/75018-montmartre/revision-vtc/blob/main/JOURNAL.md
