# gluther-data

Liste de produits courants par rayon, téléchargée par l'application GlutHer
pour préparer une liste de courses.

`courses.json` :

- `version` : numéro de version de la liste (l'appli propose la mise à jour quand il augmente) ;
- `items[]` : `n` (nom), `k` (rayon), `h` (indication gluten pour la version classique du produit :
  `g` contient du gluten, `f` naturellement sans gluten, `c` dépend de la marque / à vérifier).

Rayons : `pates`, `pain`, `biscuits`, `chocolat`, `cereales`, `farines`, `sauces`, `soupes`,
`snacks`, `boissons`, `viandes`, `poissons`, `laitiers`, `fruits_legumes`, `riz`, `plats`, `epicerie`.

Ces indications sont générales et ne remplacent pas la lecture de l'étiquette.
