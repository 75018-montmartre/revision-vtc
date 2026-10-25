# revision-vtc.fr

Site compagnon du livre *Machine à Réussite · Examen VTC 2027* (Benjamin Blondin).

## Organisation du dépôt

| Dossier | Contenu |
|---|---|
| `contenu/actualite/AAAA-MM-JJ.json` | Un numéro de l'Actualité VTC (un fichier par semaine, nommé par sa date de publication) |
| `contenu/mises-a-jour.json` | Les corrections du livre après impression et les points à surveiller |
| `contenu/wiki.json` | Le wiki « Textes du métier » (`docs/wiki/`) : pour chaque article, le thème, l'explication « En clair », l'exemple « Concrètement », les fiches du livre, le texte officiel recopié de Légifrance (`texte`, `vigueur`, `modif`) et son lien ; plus les lois d'origine et références externes (`autres`). Date de vérification : `verifie`. |
| `contenu/questions/AAAA-MM-JJ-adresse.json` | Une « Question VTC » (une par semaine, publiée le jeudi) : question, réponse courte, développement, à retenir, liens vers le wiki, fiches du livre, sources |
| `contenu/fiches.json` | Codes et titres des fiches du livre, pour les renvois « Dans le livre » |
| `contenu/livre.json` | L'adresse de la page Amazon du livre (`amazon`) ; vide, le site affiche « Bientôt disponible sur Amazon » |
| `outils/generer.py` | Génère tout le site dans `docs/` à partir de `contenu/` |
| `outils/gabarit.py` | En-tête, menu et pied de page communs |
| `docs/` | Le site publié par GitHub Pages (ne pas modifier les pages HTML à la main : elles sont régénérées) |

Les fichiers fixes de `docs/` (feuille de style, polices, scripts et données des examens, PDF, `CNAME`) ne sont pas régénérés.

## Publier un numéro de l'Actualité VTC

1. Créer `contenu/actualite/AAAA-MM-JJ.json` sur le modèle du numéro précédent (format ci-dessous).
2. Si une règle du livre change : ajouter une ligne dans `contenu/mises-a-jour.json` (`corrections`).
   Si un article du wiki est modifié ou abrogé sur Légifrance : recopier le nouveau texte dans `contenu/wiki.json`, revoir « En clair » et « Concrètement », mettre à jour `verifie`. Le texte officiel n'est jamais réécrit : il est recopié tel quel.
3. Lancer `python3 outils/generer.py` depuis la racine du dépôt : il vérifie que chaque brève a au moins une source.
4. Publier directement sur `main` (commit puis push) : le site est mis à jour en quelques minutes. L'auteur reçoit ensuite un récapitulatif.

Calendrier des publications automatiques : lundi, Actualité VTC ; mercredi, veille du wiki ; jeudi, Question VTC.

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

## Charte graphique

Une seule feuille de style, `docs/css/site.css`, organisée en sept parties (jetons, base, structure, typographie, composants, pages, adaptations). Règles à respecter pour garder un site homogène :

- **Couleurs** : uniquement les jetons de `:root` (`--fond`, `--carte`, `--doux`, `--encre`, `--gris`, `--filet`, `--rouge`, `--accent`). Jamais de couleur écrite en dur dans une page. Le thème sombre est géré par les mêmes jetons.
- **Typographie** : Inter pour les titres, menus, boutons et mentions ; EB Garamond pour le texte de lecture. Pas d'autre police.
- **Structure d'une page intérieure** (automatique, faite par `outils/gabarit.py`) : bande d'en-tête blanche avec fil d'Ariane (s'il y en a un), surtitre rouge en capitales, titre, chapeau ; puis la colonne de lecture (46rem), alignée à gauche sur le logo. Chaque page commence donc par `<p class="surtitre">` (facultatif : sinon celui de la rubrique), `<h1>`, puis `<p class="chapeau">` ou `<p class="meta">`.
- **Trois mises en page, choisies automatiquement et toujours centrées dans l'écran** : une colonne de lecture (pages simples) ; colonne + encadré à droite « Dans le livre », « Voir aussi » (`.deux-col`, pages du wiki et Questions VTC ; l'encadré passe sous le texte sur tablette et téléphone) ; pages d'index avec grilles de cartes. L'en-tête de page prend toujours la même largeur que le contenu.
- **Deux niveaux de titres de section** : l'en-tête de bloc (`.tete-bloc` : surtitre, titre, lien « Tous les… » à droite, trait noir épais) pour les blocs de l'accueil et les thèmes du wiki ; l'intertitre de contenu (`h2`, petit trait rouge au-dessus) dans les pages.
- **Une seule forme de boîte, la carte** : fond blanc, filet, coins arrondis (14 px), ombre légère. Variante « mise en avant » : filet rouge épais à gauche (`.en-clair`, `.retenir`, `.une-actu`). Carte cliquable : toute la surface est un lien, elle se soulève au survol. Encart secondaire : fond beige (`.concretement`, `.impact`, `.note`).
- **Boutons** en pilule (`.bouton`, `.bouton.second`, `.bouton.petit`) ; liens « voir tout » avec `.lien-fleche`.
- **Grilles** : tuiles de l'accueil 4 / 2 / 1 colonnes ; cartes-liens en grille automatique. Jamais de tuile orpheline.
- **Accessibilité** : contraste AA minimum, cibles tactiles de 40 px au moins, focus visible, aucune information portée par la couleur seule, animations coupées si l'appareil le demande.
- Avant d'ajouter une règle CSS, chercher un composant existant. Toute nouvelle règle va dans la bonne partie du fichier, avec un commentaire.
