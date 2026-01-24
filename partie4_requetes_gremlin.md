# Partie 4 - Base de données graphe - Cosmos DB (Gremlin)

## Introduction à Gremlin

Gremlin est un langage de traversée de graphe open source développé par Apache TinkerPop. Contrairement à Cypher qui est déclaratif, Gremlin est un langage **impératif** basé sur le chaînage de méthodes (steps).

**Différences avec Cypher :**
- **Cypher** : Patterns visuels `(a)-[:REL]->(b)` → Déclaratif
- **Gremlin** : Chaînage de traversées `g.V().has().out().count()` → Impératif

## Modèle de données graphe

Dans Cosmos DB (Gremlin), les données sont représentées comme :

**Vertices (Sommets) :**
- Label `Artist` - Artistes avec propriétés (idArtist, primaryName, birthYear)
- Label `Film` - Films avec propriétés (idFilm, primaryTitle, startYear, runtimeMinutes)

**Edges (Arêtes) :**
- Label `ACTED_IN` - Un artiste a joué dans un film
- Label `DIRECTED` - Un artiste a réalisé un film
- Label `PRODUCED` - Un artiste a produit un film
- Label `COMPOSED` - Un artiste a composé la musique d'un film

---

## Requêtes Gremlin

### Exercice 1 (0 pt): Ajouter une personne dans le graphe

**Question:** Ajoutez une personne ayant votre prénom et votre nom dans le graphe. Vérifiez que le nœud a bien été créé.

**Requête Gremlin:**
```groovy
// Création d'un vertex Artist avec les propriétés
g.addV('Artist')
  .property('idArtist', 'nm9999999')
  .property('primaryName', 'TAZI')
  .property('birthYear', 2002)

// Vérification : recherche du vertex créé
g.V().has('Artist', 'primaryName', 'TAZI').valueMap()
```

**Explication:**

La méthode `addV('Artist')` crée un nouveau vertex avec le label Artist, puis on chaîne les `.property()` pour ajouter les propriétés. Pour vérifier, `g.V()` démarre une traversée sur tous les vertices, `has()` filtre par label et propriété, et `valueMap()` retourne toutes les propriétés.

---

### Exercice 2 (0 pt): Ajouter un film

**Question:** Ajoutez un film nommé `L'histoire de mon 20 au cours Infrastructure de données`

**Requête Gremlin:**
```groovy
// Création d'un vertex Film
g.addV('Film')
  .property('idFilm', 'tt9999999')
  .property('primaryTitle', 'L\'histoire de mon 20 au cours Infrastructure de données')
  .property('startYear', 2026)
```

**Explication:**

Similaire à l'exercice 1, on utilise `addV('Film')` pour créer un vertex de type Film avec les propriétés idFilm, primaryTitle et startYear.

---

### Exercice 3 (0 pt): Ajouter une relation ACTED_IN

**Question:** Ajoutez la relation `ACTED_IN` qui modélise votre participation à ce film en tant qu'acteur/actrice

**Requête Gremlin:**
```groovy
// Création d'une arête ACTED_IN entre l'artiste TAZI et le film
g.V().has('Artist', 'primaryName', 'TAZI').as('artist')
  .V().has('Film', 'primaryTitle', 'L\'histoire de mon 20 au cours Infrastructure de données').as('film')
  .addE('ACTED_IN').from('artist').to('film')
```

**Explication:**

On recherche d'abord le vertex Artist (avec `.as('artist')` pour le marquer), puis le vertex Film (marqué comme 'film'), et enfin on crée l'arête ACTED_IN avec `addE()` en spécifiant la direction avec `from()` et `to()`.

---

### Exercice 4 (1 pt): Ajouter des professeurs comme réalisateurs

**Question:** Ajoutez deux de vos professeurs/enseignants comme réalisateurs/réalisatrices de ce film.

**Requête Gremlin:**
```groovy
// Création du Prof1 et relation DIRECTED
g.addV('Artist')
  .property('idArtist', 'nm9999001')
  .property('primaryName', 'Prof1')
  .property('birthYear', 1975).as('prof1')
  .V().has('Film', 'primaryTitle', 'L\'histoire de mon 20 au cours Infrastructure de données').as('film')
  .addE('DIRECTED').from('prof1').to('film')

// Création du Prof2 et relation DIRECTED
g.addV('Artist')
  .property('idArtist', 'nm9999002')
  .property('primaryName', 'Prof2')
  .property('birthYear', 1980).as('prof2')
  .V().has('Film', 'primaryTitle', 'L\'histoire de mon 20 au cours Infrastructure de données').as('film')
  .addE('DIRECTED').from('prof2').to('film')
```

**Explication:**

Pour chaque professeur, on crée un vertex Artist, on le marque avec `.as()`, puis on recherche le film et on crée l'arête DIRECTED. Gremlin nécessite deux requêtes séparées pour créer deux artistes distincts avec leurs relations.

---

### Exercice 5 (1 pt): Afficher Nicole Kidman et son année de naissance

**Question:** Affichez le nœud représentant l'actrice nommée `Nicole Kidman`, et visualisez son année de naissance.

**Requête Gremlin:**
```groovy
// Recherche de Nicole Kidman et projection des propriétés
g.V().has('Artist', 'primaryName', 'Nicole Kidman')
  .valueMap('primaryName', 'birthYear')
```

**Explication:**

`g.V()` parcourt tous les vertices, `has()` filtre pour trouver l'artiste Nicole Kidman, et `valueMap()` projette uniquement les propriétés primaryName et birthYear.

---

### Exercice 6 (1 pt): Visualiser tous les films

**Question:** Visualisez l'ensemble des films.

**Requête Gremlin:**
```groovy
// Récupération de tous les vertices Film
g.V().hasLabel('Film')
```

**Explication:**

`g.V()` démarre la traversée sur tous les vertices, et `hasLabel('Film')` filtre pour ne garder que ceux ayant le label Film. C'est l'équivalent du `MATCH (f:Film)` en Cypher.

---

### Exercice 7 (1 pt): Artistes nés en 1963

**Question:** Trouvez les noms des artistes nés en `1963`, affichez ensuite leur nombre.

**Requête Gremlin:**
```groovy
// Partie 1 : Liste des noms
g.V().has('Artist', 'birthYear', 1963)
  .values('primaryName')

// Partie 2 : Nombre total
g.V().has('Artist', 'birthYear', 1963)
  .count()
```

**Explication:**

La première requête utilise `has()` pour filtrer sur birthYear = 1963 et `values('primaryName')` pour projeter les noms. La seconde applique `.count()` sur le même pattern pour obtenir le nombre total.

---

### Exercice 8 (1 pt): Acteurs ayant joué dans plus d'un film

**Question:** Trouver l'ensemble des acteurs (sans entrées doublons) qui ont joué dans plus d'un film.

**Requête Gremlin:**
```groovy
// Traversée des arêtes ACTED_IN et comptage des films par acteur
g.V().hasLabel('Artist').as('actor')
  .outE('ACTED_IN')
  .inV().dedup()
  .group()
    .by(select('actor'))
    .by(count())
  .unfold()
  .where(select(values).is(gt(1)))
  .select(keys)
  .valueMap('idArtist', 'primaryName')
```

**Explication:**

On part des vertices Artist, on traverse les arêtes ACTED_IN vers les films avec `outE().inV()`, puis on groupe par acteur en comptant les films distincts. `where(select(values).is(gt(1)))` filtre pour ne garder que ceux ayant plus d'un film.

---

### Exercice 9 (1.5 pt): Artistes avec plusieurs responsabilités (carrière)

**Question:** Trouvez les artistes ayant eu plusieurs responsabilités au cours de leur carrière (acteur, directeur, producteur...).

**Requête Gremlin:**
```groovy
// Comptage des types d'arêtes sortantes par artiste
g.V().hasLabel('Artist').as('artist')
  .outE().label().dedup().fold().as('roles')
  .select('artist', 'roles')
  .where(select('roles').count(local).is(gt(1)))
  .by(valueMap('idArtist', 'primaryName'))
  .by()
```

**Explication:**

On parcourt les artistes, on collecte les labels des arêtes sortantes (ACTED_IN, DIRECTED, etc.) avec `outE().label().dedup().fold()`, puis on filtre avec `where()` pour ne garder que les artistes ayant plusieurs types d'arêtes distinctes.

---

### Exercice 10 (2 pt): Artistes avec plusieurs responsabilités dans un même film

**Question:** Montrez les artistes ayant eu plusieurs responsabilités dans un même film (ex: à la fois acteur et directeur, ou toute autre combinaison) et les titres de ces films.

**Requête Gremlin:**
```groovy
// Regroupement par couple (artiste, film) pour détecter les cumuls
g.V().hasLabel('Film').as('film')
  .inE().as('edge')
  .outV().hasLabel('Artist').as('artist')
  .select('artist', 'film', 'edge')
  .group()
    .by(select('artist', 'film'))
    .by(select('edge').label().dedup().fold())
  .unfold()
  .where(select(values).count(local).is(gt(1)))
  .project('artist', 'film', 'roles')
    .by(select(keys).select('artist').valueMap('primaryName'))
    .by(select(keys).select('film').valueMap('primaryTitle'))
    .by(select(values))
```

**Explication:**

On part des films, on remonte vers les artistes via les arêtes entrantes, puis on groupe par couple (artiste, film) en collectant les types d'arêtes. Le filtre `where()` garde uniquement les couples ayant plusieurs types de relations, révélant les artistes polyvalents sur un même projet.

---

### Exercice 11 (5 pt bonus): Film(s) avec le plus d'acteurs

**Question:** Trouver le nom du ou des film(s) ayant le plus d'acteurs.

**Requête Gremlin:**
```groovy
// Comptage des acteurs par film et sélection du maximum
g.V().hasLabel('Film').as('film')
  .inE('ACTED_IN')
  .outV().dedup()
  .count().as('actorCount')
  .select('film', 'actorCount')
  .order().by(select('actorCount'), desc)
  .limit(1)
  .project('idFilm', 'primaryTitle', 'NombreActeurs')
    .by(select('film').values('idFilm'))
    .by(select('film').values('primaryTitle'))
    .by(select('actorCount'))
```

**Explication:**

On parcourt les films, on compte les artistes distincts reliés par ACTED_IN avec `inE('ACTED_IN').outV().dedup().count()`, puis on trie par ordre décroissant et limite à 1 résultat avec `order().by(desc).limit(1)`. Cette approche retourne le film avec le casting le plus large.

---

## Syntaxe Gremlin - Aide-mémoire

### Steps de base
- `g.V()` : Tous les vertices
- `g.E()` : Toutes les arêtes
- `addV(label)` : Créer un vertex
- `addE(label)` : Créer une arête
- `property(key, value)` : Ajouter une propriété

### Traversée
- `out(label)` / `in(label)` : Traverser les arêtes sortantes/entrantes
- `outE(label)` / `inE(label)` : Récupérer les arêtes sortantes/entrantes
- `outV()` / `inV()` : Vertex source/destination d'une arête
- `both()` / `bothE()` : Traversée bidirectionnelle

### Filtrage
- `has(label, key, value)` : Filtrer par label et propriété
- `hasLabel(label)` : Filtrer par label uniquement
- `where(predicate)` : Condition personnalisée
- `is(predicate)` : Comparaison (gt, lt, eq, etc.)

### Projection
- `values(key)` : Extraire les valeurs d'une propriété
- `valueMap()` : Toutes les propriétés d'un vertex/edge
- `select(keys)` : Sélectionner des variables marquées
- `project()` : Créer une projection custom

### Agrégation
- `count()` : Compter les éléments
- `group()` : Grouper par critère
- `fold()` : Collecter en liste
- `unfold()` : Déplier une collection
- `dedup()` : Éliminer les doublons

### Utilitaires
- `as(label)` : Marquer un point dans la traversée
- `by(projection)` : Modulateur pour group/order/project
- `order()` : Trier les résultats
- `limit(n)` : Limiter le nombre de résultats

---
