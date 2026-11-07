# revision-vtc.fr

Site compagnon du livre *Machine à Réussite · Examen VTC 2027* (Benjamin Blondin).

## Organisation du dépôt

| Dossier | Contenu |
|---|---|
| `contenu/actualite/AAAA-MM-JJ.json` | Un numéro de l'Actualité VTC (un fichier par semaine, nommé par sa date de publication) |
| `contenu/mises-a-jour.json` | Les corrections du livre après impression et les points à surveiller |
| `contenu/wiki.json` | Le wiki « Textes réglementaires » (`docs/wiki/`) : pour chaque article, le thème, l'explication « En clair », l'exemple « Concrètement », les fiches du livre, le texte officiel recopié de Légifrance (`texte`, `vigueur`, `modif`) et son lien ; plus les lois d'origine et références externes (`autres`). Date de vérification : `verifie`. |
| `contenu/questions/AAAA-MM-JJ-adresse.json` | Une « Question VTC » (une par semaine, publiée le jeudi) : question, réponse courte, développement, à retenir, liens vers le wiki, fiches du livre, sources |
| `contenu/dossiers/adresse.json` | Un article de la rubrique « Articles » (1 500 à 2 500 mots, ton pédagogique de blog, publié dans `docs/dossiers/`) : voir « Publier un article » |
| `contenu/simulateur.json` | Les hypothèses du simulateur « coût de revient et revenu net » (`docs/simulateurs/`) : chaque valeur, ses sources et la date de vérification ; voir « Mettre à jour le simulateur » |
| `contenu/indexnow.json` | La clé publique IndexNow (`cle`), servie à la racine du site sous `docs/<clé>.txt` |
| `contenu/fiches.json` | Codes et titres des fiches du livre, pour les renvois « Dans le livre » |
| `contenu/livre_pages.json` | Page de chaque fiche du livre imprimé et de son corrigé (encadrés de `mises-a-jour.html`) |
| `contenu/contact.json` | La clé d'accès Web3Forms du formulaire de contact (`web3forms_cle`) ; vide, la page Contact affiche l'adresse e-mail à la place du formulaire |
| `contenu/livre.json` | L'adresse de la page Amazon du livre (`amazon`) ; vide, le site affiche « Bientôt disponible sur Amazon ». Et l'adresse n8n qui reçoit les inscriptions des lecteurs (`inscription_url`) |
| `outils/generer.py` | Génère tout le site dans `docs/` à partir de `contenu/` |
| `outils/indexnow.py` | Signale à Bing (IndexNow) les pages ajoutées ou modifiées, lancé par `.github/workflows/indexnow.yml` |
| `outils/carburants.py` | Met à jour chaque matin les prix moyens des carburants du simulateur (lancé par `.github/workflows/carburants.yml`) ; voir « Mettre à jour le simulateur » |
| `outils/test_simulateur.js` | Vérifie le calcul du simulateur sur des cas faits à la main (`node outils/test_simulateur.js`) |
| `outils/test_coherence_simulateur.py` | Vérifie que le calcul Python des exemples chiffrés (accueil, page du simulateur) donne exactement le même résultat que le calcul JavaScript de la page, sur 401 cas (`python3 outils/test_coherence_simulateur.py`, nécessite node) |
| `contenu/calcul_note.json` | Le barème de l'examen pour le « calcul de la note » (`docs/simulateurs/`) : voir « Calcul de la note de l'examen » |
| `outils/test_calcul_note.js` | Vérifie le calcul de la note sur des cas faits à la main et 200 000 tirages (`node outils/test_calcul_note.js`) |
| `outils/gabarit.py` | En-tête, menu et pied de page communs |
| `docs/` | Le site publié par GitHub Pages (ne pas modifier les pages HTML à la main : elles sont régénérées) |

Les fichiers fixes de `docs/` (feuille de style, polices, scripts communs `js/site.js`, `js/accueil-simu.js` et des examens, données des examens, PDF, `CNAME`) ne sont pas régénérés.

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
{"date": "JJ mois AAAA", "fiche": "A3.6", "avant": "Ce que dit le livre", "apres": "Ce qu'il faut retenir", "texte": "Texte officiel qui fonde la nouvelle règle", "url": "https://www.legifrance.gouv.fr/…"}
```

La correction la plus récente se place **en tête** de `corrections`. Chacune devient un encadré sur `mises-a-jour.html` : titre de la fiche, date, **page du livre** (et page du corrigé), ce que dit le livre, ce qu'il faut retenir, texte officiel (cliquable si `url` est donné), exemplaires concernés.

- La page vient toute seule de `contenu/livre_pages.json` (les 213 fiches, page de la fiche et de son corrigé, tirées du PDF du livre ; même pagination dans les versions 1.0 et 1.1). Ne pas l'écrire à la main. Seulement si la correction porte sur une autre page que celle de la fiche (corrigé, examen blanc, page « Ce qui change en 2027 »…), ajouter `"page": 72`.
- `"corrigee_dans": "1.2"` : seulement quand une nouvelle version du livre, qui intègre la correction, a été envoyée sur KDP. Sans ce champ, l'encadré dit « Toutes les versions imprimées ».
- Le générateur refuse une correction à laquelle il manque un champ, ou dont la fiche n'existe pas dans `contenu/livre_pages.json`.
- Versions du livre : 1.0 (octobre 2026, page 2 blanche) ; 1.1 (novembre 2026, page 2 « Ce livre est tenu à jour », version écrite en bas de la page 2 et en page 4).

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

**Épreuve, numéro et date affichés** (depuis le 7 novembre 2026) : chaque question est rattachée à une épreuve de l'examen (A à G, intitulés courts de `contenu/calcul_note.json`), affichée avec son pictogramme sous le titre de la carte. Par défaut, c'est la lettre de la première fiche du livre citée dans `fiches` ; le champ facultatif `"domaine": "A"` la remplace (`"X"` pour l'examen lui-même : méthode, inscription). Les cartes sont numérotées dans l'ordre de publication (la plus ancienne est la n° 1). Les pages n'affichent plus le jour de publication ni de vérification, seulement le mois et l'année ; les dates exactes restent dans le JSON et les données structurées. Pas de rythme de publication promis sur les pages (« régulièrement »).

Dans les paragraphes des sections, `[texte](adresse)` fait un lien (par exemple vers un article : `[le budget complet](../dossiers/cout-pour-devenir-chauffeur-vtc.html)`) et `**texte**` met en gras, comme dans les articles.

## Publier un article (rubrique « Articles »)

Fichier `contenu/dossiers/adresse.json`, nommé par l'adresse de la page (minuscules, tirets, mots-clés principaux : `cout-pour-devenir-chauffeur-vtc`). La rubrique s'appelait « Dossiers » jusqu'au 29 octobre 2026 ; elle s'affiche désormais « Articles », mais le dossier technique et les adresses restent `dossiers/` (règle : jamais de changement d'adresse). La page est publiée à `https://revision-vtc.fr/dossiers/adresse.html` ; l'adresse ne change plus ensuite (un article se met à jour, avec `mis_a_jour`). Modèles : l'article n° 1 (budget, ton de référence chiffré) et les articles n° 2 à 4 (ton de blog pédagogique : un exemple concret pour commencer, phrases courtes, « vous », listes en gras).

Chaque article a un champ `"domaine"` (épreuve A à G, ou `"X"` pour l'examen), affiché avec son pictogramme sur la carte de la page d'index et dans la ligne de date de l'article ; même règle de date que les Questions VTC (mois et année seulement).

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
- **Chaque matin, automatiquement (GitHub Actions, `.github/workflows/carburants.yml`, 6 h 17 à Paris l'hiver)** : prix des carburants. `outils/carburants.py` télécharge le flux quotidien officiel de la veille (prix-carburants.gouv.fr, `https://donnees.roulez-eco.fr/opendata/jour/AAAAMMJJ`, Licence Ouverte 2.0), prend pour chaque station le dernier prix du SP95-E10 et du gazole relevé ce jour-là, écarte les prix à plus de 20 % de la médiane, fait la moyenne et l'écrit dans `prix_e10`, `prix_gazole` et la source `prix_carburants` de `contenu/simulateur.json` ; puis il régénère le site, lance `node outils/test_simulateur.js` et publie sur main (commit « Simulateur : prix des carburants du … », sans entrée au journal ni e-mail de récapitulatif). Si le fichier manque ou compte moins de 1 500 stations par carburant, la tâche échoue sans rien modifier et GitHub prévient par e-mail : le simulateur garde les prix précédents et leur date. Lancement à la main : onglet Actions, « Prix des carburants (simulateur) », avec un jour au choix et l'option « essai » pour calculer sans publier. Méthode contrôlée le 3 novembre 2026 sur le vendredi 23 octobre 2026 : SP95-E10 2,106 € et gazole 2,355 €, contre 2,116 € et 2,352 € dans le fichier hebdomadaire de la DGEC. Ne pas modifier ces prix à la main. **Chaque 1er janvier** : taux de cotisations, seuils de TVA et de la micro-entreprise. **Au 1er août et au 1er février** : tarif réglementé de l'électricité. Mettre à jour `verifie`, puis les textes d'aide de `simulateur()` dans `outils/generer.py` qui citent ces valeurs.
- **TVA** (depuis le 3 novembre 2026) : le simulateur calcule une année complète. Au-delà du seuil majoré de la franchise (41 250 €), TVA de 10 % comprise dans le prix des courses, moins la TVA de 20 % récupérable sur le loyer, l'achat (net de la revente), l'entretien et le carburant (pas l'électricité, ni l'assurance, ni les autres frais) ; cotisations sur le hors taxe. En franchise, TVA de 20 % sur la commission facturée depuis l'étranger (Uber, Bolt), due sans déduction (case « Ma plateforme facture sa commission depuis l'étranger », cochée par défaut). Entre 37 500 € et 41 250 €, année en franchise et alerte pour l'année suivante. Les articles qui citent l'exemple du simulateur (accueil, « Combien gagne-t-on vraiment de l'heure ? », « Salarié ou indépendant », « Les erreurs du débutant ») sont à mettre à jour si le calcul change.
- **Acre et CFE** (depuis le 3 novembre 2026) : case « Première année avec l'Acre » (`taux_acre`, 15,9 % au lieu de 21,2 %, cotisations sociales seulement, résultat sur une année entière donc maximal) et champ facultatif CFE (€ par an, 0 par défaut). Alerte tant que les autres frais sont à 0 €. Seuil de rentabilité affiché arrondi à l'euro supérieur ; résultat remplacé par « — » tant qu'un champ est faux.
- Après toute modification du calcul : `node outils/test_simulateur.js` et `python3 outils/test_coherence_simulateur.py`, puis vérifier la page en clair et en sombre, de 320 px au grand écran.

## Calcul de la note de l'examen

Page : https://revision-vtc.fr/simulateurs/calcul-note-examen-vtc.html (adresse définitive), listée dans `simulateurs/`. Le barème est dans `contenu/calcul_note.json` (épreuves A à G : durée, coefficient, note éliminatoire, composition ; deux exemples ; sources), injecté dans la page ; le calcul se fait dans le navigateur (`docs/js/calcul-note.js`), en centièmes de point entiers (une moyenne de 9,999 n'est jamais affichée 10).

- **Recoupement automatique** : le générateur compare la durée et le coefficient de chaque épreuve, les seuils (10, 6, 4) et la note de l'épreuve pratique (12) au texte de l'arrêté du 6 avril 2017 recopié dans `contenu/wiki.json`. Si la veille du mercredi met à jour ce texte et que le barème change, le générateur s'arrête jusqu'à ce que `calcul_note.json` soit corrigé (puis `verifie` mis à jour).
- Le mode « seulement F et G » applique l'article 5 de l'arrêté (candidat admissible à l'examen de taxi depuis moins de 3 ans).
- Après toute modification : `node outils/test_calcul_note.js`, puis vérifier la page en clair et en sombre, de 320 px au grand écran.

## IndexNow (Bing)

À chaque mise à jour de `main` qui touche `docs/`, GitHub Actions (`.github/workflows/indexnow.yml`) attend que GitHub Pages serve la nouvelle version, puis envoie à IndexNow la liste des pages HTML ajoutées ou modifiées (pages `noindex` et redirections exclues). Aucun secret : la clé est publique. Envoi complet du sitemap : onglet Actions > « IndexNow (Bing) » > Run workflow, case « Envoyer toutes les adresses ». Essai sans envoi : `python3 outils/indexnow.py --essai`.

## Charte graphique

Direction « signalétique en relief », en place depuis le 31 octobre 2026 : bandeaux bleu nuit et jaune signal, comme l'information routière ; **tout ce qui se clique a une épaisseur bleu nuit (le relief), se soulève au survol et s'enfonce au clic ; ce qui ne se clique pas reste à plat.** Une seule feuille de style, `docs/css/site.css`, en huit parties (jetons, base, structure, typographie, composants, pages, adaptations, puis « 8. Habillage signalétique en relief », qui doit rester en fin de fichier). Règles :

- **Couleurs** : uniquement les jetons de `:root`. Neutres : `--fond` (blanc), `--carte`, `--doux` (gris bleuté clair), `--encre`, `--gris`, `--filet`. Signalétique : `--nuit` (en-tête du site, bandeaux, « En clair », relief), `--nuit-2`, `--jaune` (numéros d'article, étapes, numéros de l'Actualité, choix actif, soulignement du menu, boutons principaux sur fond nuit, menu « Le livre » et bouton d'achat), `--jaune-ombre` (relief sur fond nuit), `--jaune-survol`. Sur fond nuit : `--lien-sur-nuit` (liens de « En clair »), `--focus-sur-nuit` (focus du pied de page) ; flèche du menu sur téléphone : `--chevron-nav`. Liens : `--accent` (bleu). Le rouge du livre (`--rouge`) ne sert qu'à la marque. Surfaces foncées : `--fonce`, `--sur-fonce*`. Relief : `--relief`, `--pastille`, `--pastille-fleche` ; quadrillage : `--quadrille`. Jamais de couleur en dur dans une page ; le thème sombre redéfinit les mêmes jetons (relief bleu gris, pastille jaune).
- **Typographie** : Barlow (texte, interface) et Barlow Condensed (titres `h1`-`h3`, numéros, résultats chiffrés), hébergées dans `docs/fonts/`. Pas d'autre police.
- **Fond quadrillé** (plan de ville, carrés de 56 px) : uniquement sur l'en-tête des pages intérieures (`.tete-page`) et les bandes claires de l'accueil (`.bloc-doux`), avec le même traitement partout depuis le 4 novembre 2026 : fond `--doux` éclairci de moitié par `--fond` avec `color-mix()` (aucune couleur nouvelle), quadrillage net en haut, qui s'estompe vers le bas (masque sur `::before`), masqué à l'impression. Les bandes blanches (`.bloc-blanc`) n'ont plus de filet.
- **En-tête du site** (`outils/gabarit.py`) : bandeau bleu nuit, logo et nom à gauche ; menu des cinq rubriques (`NAV`, dans cet ordre : Simulateur, Textes réglementaires, Questions VTC, Articles, Actualité VTC), rubrique en cours soulignée en jaune ; à droite, le menu déroulant « Le livre » (`MENU_LIVRE`) : bouton jaune plein en relief sur toutes les pages, la page du livre en cours est marquée dans la liste (`aria-current`, trait jaune à gauche). Pas d'« Accueil » dans le menu : le logo y mène. **L'en-tête reste collé en haut de l'écran** au défilement (depuis le 3 novembre 2026) : il se resserre dès qu'on quitte le haut de la page (sous-titre masqué), une jauge jaune de 3 px en bas montre la part de la page déjà lue, et sur téléphone il se range quand on descend et revient dès qu'on remonte (jamais quand le menu « Le livre » est ouvert ou qu'un de ses éléments a le focus). Au survol, un trait jaune s'étire sous la rubrique. Les ancres tiennent compte de sa hauteur (`--haut-entete`, `js/site.js`). Mouvements coupés si l'appareil demande moins d'animations. Sur téléphone (sous 52rem), le menu défile horizontalement : un dégradé et une flèche sur le bord droit (jeton `--chevron-nav`) montrent qu'il continue, et disparaissent au bout de la liste (classe `au-bout`, `js/site.js`).
- **Accueil** (`accueil()` dans `outils/generer.py`), de haut en bas :
  - **premier écran fixe** sur fond nuit (`.hero.fond-nuit`), sans carrousel : surtitre « Examen VTC 2027, règles vérifiées en <mois année> » (mois tiré de `verifie` dans `contenu/wiki.json`), `h1` visible, chapeau, bouton principal jaune « Préparer l'examen 2027 » (vers `le-livre.html`), bouton secondaire à contour « Calculer mon revenu net » (vers le simulateur), mention « Gratuit, sans inscription, sans publicité. » ; texte et cartes alignés en haut (`align-items:start`) ; à droite (dessous sous 64rem), deux cartes : **le simulateur interactif** (`.carte-simu`, depuis le 4 novembre 2026), à plat parce que la carte n'est plus un lien : titre « Simulateur gratuit », format horizontal (colonne de droite élargie, `1.2fr`) : deux curseurs côte à côte (« Versé par semaine », 200 à 2 500 € ; « Location par semaine », 0 à 600 €), puis le relevé mensuel sur une ligne de trois colonnes (versé, TVA-cotisations-voiture-frais, reste avant impôt derrière un trait épais) ; sous 30rem, curseurs et relevé repassent l'un sous l'autre recalculé à chaque cran par `SimuVTC.calculer` (`docs/js/simulateur.js` + `docs/js/accueil-simu.js`, avec les valeurs par défaut du simulateur injectées par le générateur) ; le lien « Faire ma simulation avec mes chiffres » ouvre le simulateur avec les deux valeurs choisies ; sans JavaScript, les curseurs restent cachés et l'exemple pour 1 000 € par semaine, **calculé par le générateur**, reste affiché ; et la carte-lien en relief du livre (`.carte-hero`, couverture décorative `alt=""`, chiffres du livre) ;
  - **bande de trois preuves** (`.preuves`), à plat : nombre d'articles du wiki (compté), chiffres sourcés et datés, mise à jour chaque semaine ;
  - **« Par où commencer ? »** (`.parcours`) : trois panneaux à plat (je prépare l'examen, je me lance, je roule déjà), chacun avec trois petites cartes-liens ;
  - puis « Réglementation VTC : l'essentiel », les quatre dernières Questions VTC (2 × 2, une colonne sur téléphone), et le dernier numéro de l'Actualité VTC (grande carte, petites cartes des numéros précédents : `.actu-une`, `.une-actu`, `.actu-precedents`). Les bandes alternent blanc et quadrillé, à partir du blanc sous la bande des preuves : « Par où commencer ? » blanc, « l'essentiel » quadrillé, Questions VTC blanc, Actualité VTC quadrillé.
- **Achat du livre** : un seul composant, `achat()` dans `outils/gabarit.py`, classe `.bouton.achat` (jaune plein, 44 px au moins) : pied de page, encadré « Dans le livre » du wiki et des Questions VTC, page du livre. Ne pas créer d'autre bouton d'achat.
- **Sur téléphone** (sous 52rem) : nom du site sur une ligne, sous-titre masqué (le nom suffit) ; fil d'Ariane avec une zone cliquable de 44 px sans changer son aspect.
- **Structure d'une page intérieure** (automatique) : en-tête quadrillé avec fil d'Ariane, surtitre, titre, chapeau ; puis la colonne de lecture (46rem). Chaque page commence par `<p class="surtitre">` (facultatif), `<h1>`, puis `<p class="chapeau">` ou `<p class="meta">`.
- **Trois mises en page** : une colonne ; colonne + encadré à droite (`.deux-col`, wiki et Questions VTC) ; pages d'index avec grilles de cartes.
- **Titres** : surtitres en casse normale, jamais en capitales ni espacés. En-tête de bloc (`.tete-bloc`) : surtitre gris, grand titre condensé posé sur la page, trait épais dessous, lien « Tous les… » en rectangle sobre à plat (bord 1,5 px, flèche à droite, rempli de bleu nuit au survol). Intertitre de contenu (`h2`) : petit carré jaune devant.
- **Éléments cliquables, en relief** (bord 1,5 px nuit + relief plein décalé en bas à droite) :
  - grandes cartes (`.questions`, `.numeros`, `.une-actu`, `.actu-precedents`) : coins de 4 px, relief de 7 px, pastille ronde fléchée en bas à droite, toute la carte est le lien ;
  - petites cartes-liens (`.essentiel-liens`, `.wiki-liste`, et les lois d'origine du wiki, `.wiki-liste.textes-ref`) : coins de 4 px, relief de 4 px, petite pastille à droite, toute la carte est le lien ;
  - liens de l'encadré latéral (`.cote-bloc .voir-aussi` : sommaire, voir aussi, autres questions) : relief de 3 px, sans pastille, 44 px de haut au moins ;
  - navigation entre numéros de l'Actualité VTC (précédent, suivant, tous les numéros) : boutons secondaires (`.bouton.second`) ;
  - boutons (`.bouton`, `.second`, `.petit`) : relief de 4 px ; touches (`.sommaire`, choix du simulateur `.choix label`) : relief de 3 à 4 px, la touche choisie est enfoncée (et jaune pour les choix).
  - **sur fond nuit** (`.fond-nuit`, menu « Le livre ») : un relief bleu nuit y serait invisible, le relief y est donc jaune foncé (`--jaune-ombre`) pour le bouton jaune et les cartes-liens (`.carte-hero`, relief de 6 px), et `--nuit-2` pour le bouton à contour ; mêmes mouvements qu'ailleurs.
  - Survol : la carte monte de 2 ou 3 px et le relief s'épaissit, la flèche de la pastille file ; clic : la carte s'enfonce ; clavier : contour `--focus` autour de toute la carte. Tout mouvement est coupé si l'appareil demande moins d'animations ; pas de relief à l'impression.
- **Éléments à plat** (non cliquables) : « En clair » et « La réponse courte » en bandeau nuit, titre jaune ; « À retenir » sur fond `--doux` avec bande jaune à gauche ; texte officiel, brèves et encadrés latéraux à filet fin ; encarts secondaires sur `--doux` (`.concretement`, `.note`). L'ombre `--ombre-h` est réservée au menu déroulant « Le livre ».
- **Simulateur, barre de résultat collante** (`.barre-resultat`, téléphone et tablette, sous 64rem) : bandeau nuit à filet jaune en bas de l'écran, revenu net mensuel et bouton « Voir le détail ». Elle ne masque jamais un champ ni le clavier : elle s'efface quand un champ du formulaire a le focus, quand le clavier réduit l'écran (`visualViewport`) et quand le résultat complet est visible ; la page garde une marge en bas tant qu'elle est affichée. Sans JavaScript, elle n'existe pas ; si l'appareil demande moins d'animations, elle apparaît sans glisser.
- **Page du livre** (`le-livre.html`) : en tête, bloc de présentation à plat (`.presentation-livre` : couverture, chiffres du livre en liste à coches `.liste-coches`, bouton d'achat et « Déjà lecteur : recevoir les mises à jour »). Les chiffres viennent du livre imprimé : les changer seulement s'ils changent dans le livre.
- **Page 404** : les pages proposées sont des petites cartes-liens (`.essentiel-liens`).
- **Pastilles jaunes** : numéros d'article (`.num-art`, aussi le numéro des cartes des Questions VTC et des articles), étapes (`.etapes`, seulement pour une vraie suite d'étapes), numéros de l'Actualité VTC.
- **Cartes des Questions VTC et des articles** (`carte()` dans `outils/generer.py`) : en tête, numéro en pastille jaune et mois (`.carte-tete`) ; titre ; ligne de l'épreuve avec pictogramme (`.domaine`, `.picto` : pictogrammes au trait de `_PICTOS`, décoratifs, couleur du texte sur carré `--doux`) ; résumé. La légende des épreuves (`.legende-domaines`) est à plat, sur la page d'index des Questions VTC.
- **Mentions** (`.meta`) : en phrase, avec des virgules ou des points, jamais une suite séparée par des points médians « · » (sauf la ligne Légifrance du wiki et les `<title>`).
- **Grilles** : panneaux « Par où commencer ? » 3 / 1 colonnes, questions de l'accueil 2 / 1 ; cartes-liens en grille automatique ; jamais de tuile orpheline.
- **Accessibilité** : contraste AA minimum dans les deux thèmes, cibles tactiles de 44 px au moins (menu, menus déroulants, cartes-liens, liens du pied de page compris), focus visible (`--focus`, jaune dans l'en-tête), aucune information portée par la couleur seule, animations coupées si l'appareil le demande. Avant chaque publication : validateur W3C (HTML et CSS), axe en clair et en sombre à 320 et 1366 px, aucun débordement horizontal.
- Avant d'ajouter une règle CSS, chercher un composant existant. Toute nouvelle règle va dans la bonne partie du fichier, avec un commentaire.

## Récapitulatif par e-mail

À chaque mise à jour de `main`, GitHub Actions (`.github/workflows/recap.yml`) lance `outils/recap_mail.py`, qui attend que GitHub Pages serve la nouvelle version (15 minutes au plus, sinon le message le signale) puis envoie un e-mail au destinataire configuré : le récapitulatif écrit dans le corps des messages de commit, la liste des pages ajoutées, de celles dont le contenu a changé et de celles supprimées (avec leur adresse en ligne), et le lien vers le détail sur GitHub.

**Toute publication doit donc avoir un message de commit complet** : une première ligne courte (le titre), une ligne vide, puis le récapitulatif en texte simple (ce qui a été publié, les sources consultées et celles non lues, ce qui n'a pas été retenu, les règles du livre touchées, les points à trancher).

L'envoi passe par la boîte benjamin@revision-vtc.fr (serveur mail.gandi.net, port 465). Les identifiants sont dans les secrets GitHub du dépôt (`SMTP_UTILISATEUR`, `SMTP_MOT_DE_PASSE`, `RECAP_DESTINATAIRE`), jamais dans les fichiers.

## Journal des mises à jour

`JOURNAL.md` (à la racine, hors du site publié) garde la trace de chaque publication, la plus récente en haut. **Toute publication y ajoute une entrée** : jour, heure de Paris, titre, pages publiées ou modifiées avec leur adresse en ligne, points importants (règle du livre modifiée, problème), et lien vers le commit (`https://github.com/75018-montmartre/revision-vtc/commit/<identifiant>`, identifiant du commit précédent si besoin, ou la page des commits). L'auteur le consulte à l'adresse https://github.com/75018-montmartre/revision-vtc/blob/main/JOURNAL.md
