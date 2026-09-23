# Portfolio Francisco — site statique extrait de Wix

Site source : <https://fran6pereira.wixsite.com/portfolio-francisco>  
Extraction : 2026-09-23  
Sortie : `C:\Users\Fran6\Desktop\Portfolio`

Ce dossier est un site **statique autonome** : HTML pré-rendu, CSS, images et
polices téléchargés localement, **aucune dépendance au runtime Wix**, **aucune URL
absolue** vers `wix.com`, `wixstatic.com` ou `parastorage.com`. Les chemins sont
relatifs : le site fonctionne en double-cliquant sur `index.html` et sur GitHub Pages.

## Méthode d'extraction

1. `sitemap.xml` → index vers `pages-sitemap.xml` : **20 URLs**.
2. `robots.txt` récupéré (aucune page interdite en dehors de `*?lightbox=` et `_partials`).
3. Rendu **Chromium headless** de chaque page (viewport 1440×900) puis sérialisation du
   **DOM après exécution JavaScript**, et non du HTML source.
4. Inspection du **JSON embarqué** (`warmupData`, `masterPage`) et des `pageUriSEO` pour
   retrouver les pages absentes de la navigation : **2 pages cachées découvertes**
   (`fullscreen-page`, `copie-de-portfolio`) → **22 pages au total**.
5. Crawl de tous les liens internes du DOM rendu : **0 page supplémentaire** trouvée
   au-delà du sitemap et des 2 pages cachées.

Chaque page a été capturée avec son manifeste réseau complet (requêtes, codes, types)
afin d'identifier les assets réellement chargés, y compris le lazy-loading (scroll
complet déclenché avant capture).

## Fidélité de mise en page

La mise en page a été comparée au site d'origine en mesurant, pour chaque page, la
hauteur totale du document (`scrollHeight`) à viewport identique (1440×900) :

- **Les 22 pages sur 22 ont une hauteur identique au pixel près à celle du site en ligne.**
- Contrôle complémentaire : les 73 composants identifiés de la page `about-9` ont tous
  exactement la même géométrie en local et en ligne (0 écart).
- 0 image cassée sur l'ensemble du site.

Deux points ont dû être corrigés pour y parvenir, et méritent d'être connus :

1. **`data-mesh-id` est indispensable.** Le CSS Wix contient des milliers de sélecteurs
   `[data-mesh-id=...]` : c'est la grille de positionnement des composants. Retirer cet
   attribut « pour nettoyer » fait s'empiler le contenu et triple la hauteur des pages.
   Il est donc conservé tel quel.
2. **`crossorigin` doit être retiré.** Ouvert en `file://`, un attribut `crossorigin`
   résiduel faisait bloquer les vidéos par la politique CORS du navigateur.

## Pages récupérées

| # | Page | Fichier | Statut | Images |
|---|------|---------|--------|--------|
| 1 | `projects-8` | `projects-8.html` | OK | 8 |
| 2 | `fully-automated-blender-render-pipeline` | `fully-automated-blender-render-pipeline.html` | OK | 4 |
| 3 | `main-skills` | `main-skills.html` | OK | 1 |
| 4 | `s-projects-side-by-side` | `s-projects-side-by-side.html` | partielle | 140 |
| 5 | `copie-de-cvpropsartist` | `copie-de-cvpropsartist.html` | OK | 1 |
| 6 | `copie-de-rubber-1` | `copie-de-rubber-1.html` | OK | 82 |
| 7 | `jeanne-la-faussaire` | `jeanne-la-faussaire.html` | partielle | 10 |
| 8 | `about-9` | `about-9.html` | OK | 22 |
| 9 | `home` | `home.html` | OK | 183 |
| 10 | `contact-6` | `contact-6.html` | OK | 2 |
| 11 | `general-8` | `general-8.html` | OK | 107 |
| 12 | `nouvellepagemaison` | `nouvellepagemaison.html` | OK | 1 |
| 13 | `dietemna` | `dietemna.html` | OK | 7 |
| 14 | `automated-render-pipeline` | `automated-render-pipeline.html` | OK | 8 |
| 15 | `portfolio-francisco` | `index.html` | OK | 152 |
| 16 | `cvpropsartist` | `cvpropsartist.html` | OK | 1 |
| 17 | `general-8-1` | `general-8-1.html` | partielle | 107 |
| 18 | `projects-6` | `projects-6.html` | OK | 55 |
| 19 | `copie-de-environement` | `copie-de-environement.html` | OK | 50 |
| 20 | `projects-6-1` | `projects-6-1.html` | partielle | 56 |
| 21 | `fullscreen-page` | `fullscreen-page.html` | OK | 0 |
| 22 | `copie-de-portfolio` | `copie-de-portfolio.html` | OK | 152 |

22 pages, dont 18 complètes.

### Correspondance URL → fichier

- <https://fran6pereira.wixsite.com/portfolio-francisco/projects-8> → `projects-8.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco/fully-automated-blender-render-pipeline> → `fully-automated-blender-render-pipeline.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco/main-skills> → `main-skills.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco/s-projects-side-by-side> → `s-projects-side-by-side.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco/copie-de-cvpropsartist> → `copie-de-cvpropsartist.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco/copie-de-rubber-1> → `copie-de-rubber-1.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco/jeanne-la-faussaire> → `jeanne-la-faussaire.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco/about-9> → `about-9.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco/home> → `home.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco/contact-6> → `contact-6.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco/general-8> → `general-8.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco/nouvellepagemaison> → `nouvellepagemaison.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco/dietemna> → `dietemna.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco/automated-render-pipeline> → `automated-render-pipeline.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco> → `index.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco/cvpropsartist> → `cvpropsartist.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco/general-8-1> → `general-8-1.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco/projects-6> → `projects-6.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco/copie-de-environement> → `copie-de-environement.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco/projects-6-1> → `projects-6-1.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco/fullscreen-page> → `fullscreen-page.html`
- <https://fran6pereira.wixsite.com/portfolio-francisco/copie-de-portfolio> → `copie-de-portfolio.html`

### Pages sans lien entrant

Ces pages existent mais ne sont atteignables depuis aucune autre page du site
(elles ont été retrouvées via le sitemap et le JSON embarqué) :

- `/projects-8`
- `/main-skills`
- `/jeanne-la-faussaire`
- `/about-9`
- `/contact-6`
- `/nouvellepagemaison`
- `/dietemna`
- `/fullscreen-page`
- `/copie-de-portfolio`

## Éléments manquants

12 élément(s) non récupérable(s). Chacun a été remplacé par un
placeholder **de mêmes dimensions** portant un texte visible, conformément à la règle
demandée (`<img>` avec `src` local, `width` et `height` explicites, marqué `data-cw-missing="1"`).

| Élément | Dimensions | Type | Page |
|---------|-----------|------|------|
| `Image manquante : maxresdefault.jpg — 501x282 px` | 501×282 px | image | `s-projects-side-by-side.html` |
| `Media manquant : maxresdefault.jpg` | 0×0 px | media | `projects-6-1.html` |
| `Image manquante : maxresdefault.jpg — 245x138 px` | 245×138 px | image | `jeanne-la-faussaire.html` |
| `Image manquante : 2ec010_f4c156df55ef4d08ac19098eefec3397~mv2.gif — 430x312 px` | 430×312 px | image | `general-8-1.html` |
| `Image manquante : 2ec010_db698d52cb094910afacee4e6ca088f9~mv2.gif — 430x312 px` | 430×312 px | image | `general-8-1.html` |
| `Image manquante : 2ec010_379758865cfd4604adea42eac43e0bd9~mv2.gif — 477x312 px` | 477×312 px | image | `general-8-1.html` |
| `Image manquante : 2ec010_48664706e8884e479f708bcde2d1fee3~mv2.gif — 284x305 px` | 284×305 px | image | `general-8-1.html` |
| `Media manquant : 2ec010_f4c156df55ef4d08ac19098eefec3397~mv2.gif` | 0×0 px | media | `general-8-1.html` |
| `Media manquant : 2ec010_db698d52cb094910afacee4e6ca088f9~mv2.gif` | 0×0 px | media | `general-8-1.html` |
| `Media manquant : 2ec010_379758865cfd4604adea42eac43e0bd9~mv2.gif` | 0×0 px | media | `general-8-1.html` |
| `Media manquant : 2ec010_48664706e8884e479f708bcde2d1fee3~mv2.gif` | 0×0 px | media | `general-8-1.html` |
| `Image manquante : maxresdefault.jpg — 756x425 px` | 756×425 px | image | `projects-6-1.html` |

Échecs de téléchargement bruts :

- `https://fran6pereira.wixsite.com/portfolio-francisco/media/emptystate.85a4add5.svg` — HTTP 404
- `https://static.wixstatic.com/media/maxresdefault.jpg/v1/fit/w_501,h_282,q_90,enc_avif,quality_auto/maxresdefault.jpg` — HTTP 403
- `https://static.wixstatic.com/media/maxresdefault.jpg/v1/fit/w_1919,h_1080,q_90,enc_avif,quality_auto/maxresdefault.jpg` — HTTP 403
- `https://static.wixstatic.com/media/maxresdefault.jpg/v1/fill/w_245,h_138,q_90,enc_avif,quality_auto/maxresdefault.jpg` — HTTP 403
- `https://static.wixstatic.com/media/maxresdefault.jpg/v1/fill/w_1225,h_690,q_90,enc_avif,quality_auto/maxresdefault.jpg` — HTTP 403
- `https://fran6pereira.wixsite.com/media/emptystate.85a4add5.svg` — HTTP 404
- `https://static.wixstatic.com/media/2ec010_f4c156df55ef4d08ac19098eefec3397~mv2.gif/v1/fit/w_430,h_312,q_90,enc_avif,quality_auto/2ec010_f4c156df55ef4d08ac19098eefec3397~mv2.gif` — HTTP 403
- `https://static.wixstatic.com/media/2ec010_db698d52cb094910afacee4e6ca088f9~mv2.gif/v1/fit/w_430,h_312,q_90,enc_avif,quality_auto/2ec010_db698d52cb094910afacee4e6ca088f9~mv2.gif` — HTTP 403
- `https://static.wixstatic.com/media/2ec010_379758865cfd4604adea42eac43e0bd9~mv2.gif/v1/fit/w_477,h_312,q_90,enc_avif,quality_auto/2ec010_379758865cfd4604adea42eac43e0bd9~mv2.gif` — HTTP 403
- `https://static.wixstatic.com/media/2ec010_48664706e8884e479f708bcde2d1fee3~mv2.gif/v1/fit/w_284,h_305,q_90,enc_avif,quality_auto/2ec010_48664706e8884e479f708bcde2d1fee3~mv2.gif` — HTTP 403
- `https://static.wixstatic.com/media/2ec010_f4c156df55ef4d08ac19098eefec3397~mv2.gif/v1/fit/w_1138,h_825,q_90,enc_avif,quality_auto/2ec010_f4c156df55ef4d08ac19098eefec3397~mv2.gif` — HTTP 403
- `https://static.wixstatic.com/media/2ec010_db698d52cb094910afacee4e6ca088f9~mv2.gif/v1/fit/w_1138,h_825,q_90,enc_avif,quality_auto/2ec010_db698d52cb094910afacee4e6ca088f9~mv2.gif` — HTTP 403
- `https://static.wixstatic.com/media/2ec010_379758865cfd4604adea42eac43e0bd9~mv2.gif/v1/fit/w_1126,h_736,q_90,enc_avif,quality_auto/2ec010_379758865cfd4604adea42eac43e0bd9~mv2.gif` — HTTP 403
- `https://static.wixstatic.com/media/2ec010_48664706e8884e479f708bcde2d1fee3~mv2.gif/v1/fit/w_651,h_699,q_90,enc_avif,quality_auto/2ec010_48664706e8884e479f708bcde2d1fee3~mv2.gif` — HTTP 403
- `https://static.wixstatic.com/media/2ec010_15b232510b5a40bbbd7daec156581dd3~mv2.gif?formatterValues=2ec010_15b232510b5a40bbbd7daec156581dd3~mv2.gif,701,485` — HTTP 403
- `https://static.wixstatic.com/media/2ec010_27380275f5b2470daaa07169229cc6d5~mv2.gif?formatterValues=2ec010_27380275f5b2470daaa07169229cc6d5~mv2.gif,1079,806` — HTTP 403
- `https://static.wixstatic.com/media/maxresdefault.jpg/v1/fit/w_756,h_425,q_90,enc_avif,quality_auto/maxresdefault.jpg` — HTTP 403
- `https://static.wixstatic.com/media/maxresdefault.jpg/v1/fit/w_1920,h_1079,q_90,enc_avif,quality_auto/maxresdefault.jpg` — HTTP 403

## Contenu du dossier

- `index.html` — page d'accueil (ex `https://fran6pereira.wixsite.com/portfolio-francisco`)
- `<slug>.html` — une page par fichier, à la racine
- `assets/css/` — feuilles de style (références `url()` réécrites en relatif)
- `assets/img/` — images
- `assets/fonts/` — polices web
- `assets/media/` — vidéos / audio
- `assets/files/` — fichiers hébergés chez Wix localisés : le CV (PDF) des boutons « Download CV » et les documents/visionneuses HTML embarqués
- `assets/missing/` — placeholders SVG générés pour les éléments non récupérables
- `README.md` — ce fichier

| Dossier | Fichiers | Poids |
|---------|----------|-------|
| `assets/css` | 1 | 0 Ko |
| `assets/files` | 7 | 74 Ko |
| `assets/fonts` | 156 | 5.7 Mo |
| `assets/img` | 782 | 473.8 Mo |
| `assets/media` | 3 | 19.3 Mo |

Total : 949 fichiers pour 498.9 Mo.

## Déploiement sur GitHub Pages

1. Pousser le contenu de ce dossier à la racine du dépôt.
2. `Settings` → `Pages` → `Source` : `Deploy from a branch`, branche `main`, dossier `/ (root)`.
3. Aucune configuration supplémentaire : aucun chemin absolu, aucun backend, aucun
   build. Le site est servi tel quel.

## Limites connues

1. **JavaScript retiré.** Tous les `<script>` ont été supprimés : plus de runtime Wix.
   Les contenus révélés uniquement par interaction (lightbox, onglets, carrousels) sont
   présents dans le DOM capturé à leur état initial, mais ne sont plus interactifs.
2. **Formulaires.** Le formulaire de contact Wix ne peut pas fonctionner sans backend ;
   les champs sont visibles mais l'envoi est inopérant.
3. **Liens externes** conservés tels quels (voir liste ci-dessous).
4. **Animations** d'entrée pilotées par JS : les éléments concernés restent affichés
   dans leur état final, sans transition.

### Liens externes présents dans le site

- https://certaingorgon.itch.io/cheats-of-honor
- https://daunan-hortense.itch.io/roots
- https://edouard-mordant.itch.io/hangry-monkey
- https://fittingbox.com/fr/#vto
- https://github.com/LeBoFran6
- https://github.com/LeBoFran6/ESMA-JAM-2023
- https://github.com/LeBoFran6/Espace__Temps
- https://github.com/LeBoFran6/HangryMonkey
- https://github.com/LeBoFran6/JeanneProjet
- https://github.com/LeBoFran6/Roots
- https://github.com/LeBoFran6/gacha2022
- https://lefran6.itch.io/
- https://lefran6.itch.io/dietemna
- https://lefran6.itch.io/holytaxi
- https://lefran6.itch.io/miamis-lifeguard
- https://lefran6.itch.io/rubber
- https://loudebwa.itch.io/espace-temps
- https://nolwenna.itch.io/catch-nip
- https://store.steampowered.com/app/1611600/WARNO/?l=french&v=
- https://voxler.thqnordic.com/
- https://www.artstation.com/artwork/14q6P8
- https://www.artstation.com/artwork/5vWnyA
- https://www.artstation.com/artwork/8bV6Gm
- https://www.artstation.com/artwork/9E88ER
- https://www.artstation.com/artwork/Xgwzea
- https://www.artstation.com/artwork/blgaQa
- https://www.artstation.com/artwork/elo4a6
- https://www.artstation.com/artwork/obed2B
- https://www.artstation.com/lefran6
- https://www.linkedin.com/feed/update/urn:li:activity:7487827704906571776/
- https://www.linkedin.com/in/francisco-de-carvalho-pereira-aa0458196/
- https://www.linkedin.com/in/franciscodecarvalhopereira/
