# gluther-data

Données téléchargées par l'application GlutHer (aide pour personnes coeliaques).

## Liste de courses générale

`courses.json` : produits courants par rayon.

- `version` : numéro de version (l'appli propose la mise à jour quand il augmente) ;
- `items[]` : `n` (nom), `k` (rayon), `h` (indication gluten pour la version classique du produit :
  `g` contient du gluten, `f` naturellement sans gluten, `c` dépend de la marque / à vérifier).

Rayons : `pates`, `pain`, `biscuits`, `chocolat`, `cereales`, `farines`, `sauces`, `soupes`,
`snacks`, `boissons`, `viandes`, `poissons`, `laitiers`, `fruits_legumes`, `riz`, `plats`, `epicerie`.

## Base de produits hors ligne

`catalog.json` décrit les fichiers disponibles (`tiers[]` : identifiant, fichier, nombre de produits,
taille en Mo) et leur `version`. Chaque fichier `products_*.jsonl.gz` est un JSON par ligne, compressé en gzip,
classé du produit le plus scanné au moins scanné :

```json
{"c":"3017620422003","n":"Nutella","b":"Ferrero","t":["sweet-spreads","spreads"],"i":"Sucre, huile de palme, ..."}
```

`c` code-barres, `n` nom, `b` marque, `t` étiquettes de catégorie Open Food Facts (sans le préfixe `en:`),
`i` texte des ingrédients.

Sélection : produits de l'export Open Food Facts vendus en France (`countries_tags` contient `en:france`),
codes-barres commençant par 3, 4, 5 ou 8, avec un nom et un texte d'ingrédients. Le script est dans
`tools/extract.py` (export du 10/10/2026 : 293 059 produits).

## Recettes sans gluten

`recipes.json` : recettes originales GlutHer, libres de droits (CC0 1.0).

- `version` : numéro de version (l'appli adopte une version plus récente) ;
- `recipes[]` : `id`, `t` titre, `c` plat (`entree`, `plat`, `dessert`, `petitdej`), `s` nombre de personnes,
  `m` minutes, `i` ingrédients, `st` étapes ;
- ingrédient : `n` nom, `q` quantité, `u` unité, `k` rayon (voir la liste de courses), `v` = 1 si l'ingrédient
  est **à risque** pour un coeliaque (sauce ou bouillon du commerce, produit pouvant contenir du gluten ou être
  contaminé : farines, chocolat, charcuterie…). Le « mode strict » de l'appli masque les recettes qui en contiennent.

Chaque ingrédient est contrôlé par l'analyseur de gluten de GlutHer (aucun terme de gluten, les ambigus sont signalés).
Ce contrôle automatique ne remplace pas la lecture de l'étiquette des produits utilisés.

## Licence et attribution

Les données de produits proviennent d'[Open Food Facts](https://world.openfoodfacts.org) et sont publiées
sous licence [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/) ; les contenus individuels sous
[Database Contents License](https://opendatacommons.org/licenses/dbcl/1-0/). Ce jeu de données dérivé est
redistribué sous la même licence ODbL, avec attribution à Open Food Facts et ses contributeurs.

Ces informations ne remplacent pas la lecture de l'étiquette : les ingrédients peuvent être incomplets
ou obsolètes.
