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
// Création
g.addV('Artist')
  .property('idArtist', 'nm9999999')
  .property('primaryName', 'TAZI')
  .property('birthYear', 2002)

// Vérification
g.V().has('Artist', 'primaryName', 'TAZI').valueMap()
```

**Explication:**

addV crée un vertex, property() ajoute les propriétés en chaînage. Pour vérifier : g.V() parcourt les vertices, has() filtre, valueMap() retourne les propriétés.

---

### Exercice 2 (0 pt): Ajouter un film

**Question:** Ajoutez un film nommé `L'histoire de mon 20 au cours Infrastructure de données`

**Requête Gremlin:**
```groovy
g.addV('Film')
  .property('idFilm', 'tt9999999')
  .property('primaryTitle', 'L\'histoire de mon 20 au cours Infrastructure de données')
  .property('startYear', 2026)
```

**Explication:**

addV('Film') crée un vertex Film avec les propriétés spécifiées.

---

### Exercice 3 (0 pt): Ajouter une relation ACTED_IN

**Question:** Ajoutez la relation `ACTED_IN` qui modélise votre participation à ce film en tant qu'acteur/actrice

**Requête Gremlin:**
```groovy
g.V().has('Artist', 'primaryName', 'TAZI').as('artist')
  .V().has('Film', 'primaryTitle', 'L\'histoire de mon 20 au cours Infrastructure de données').as('film')
  .addE('ACTED_IN').from('artist').to('film')
```

**Explication:**

Trouve l'artiste et le marque avec as('artist'), trouve le film et le marque avec as('film'), puis addE crée l'arête dirigée avec from() et to().

---

### Exercice 4 (1 pt): Ajouter des professeurs comme réalisateurs

**Question:** Ajoutez deux de vos professeurs/enseignants comme réalisateurs/réalisatrices de ce film.

**Requête Gremlin:**
```groovy
// Prof1
g.addV('Artist')
  .property('idArtist', 'nm9999001')
  .property('primaryName', 'Prof1')
  .property('birthYear', 1975).as('prof1')
  .V().has('Film', 'primaryTitle', 'L\'histoire de mon 20 au cours Infrastructure de données').as('film')
  .addE('DIRECTED').from('prof1').to('film')

// Prof2
g.addV('Artist')
  .property('idArtist', 'nm9999002')
  .property('primaryName', 'Prof2')
  .property('birthYear', 1980).as('prof2')
  .V().has('Film', 'primaryTitle', 'L\'histoire de mon 20 au cours Infrastructure de données').as('film')
  .addE('DIRECTED').from('prof2').to('film')
```

**Explication:**

Crée chaque professeur, le marque avec as(), trouve le film, puis crée l'arête DIRECTED. Deux requêtes séparées nécessaires.

---

### Exercice 5 (1 pt): Afficher Nicole Kidman et son année de naissance

**Question:** Affichez le nœud représentant l'actrice nommée `Nicole Kidman`, et visualisez son année de naissance.

**Requête Gremlin:**
```groovy
g.V().has('Artist', 'primaryName', 'Nicole Kidman')
  .valueMap('primaryName', 'birthYear')
```

**Explication:**

g.V() parcourt les vertices, has() filtre Nicole Kidman, valueMap() retourne les propriétés demandées.

---

### Exercice 6 (1 pt): Visualiser tous les films

**Question:** Visualisez l'ensemble des films.

**Requête Gremlin:**
```groovy
g.V().hasLabel('Film')
```

**Explication:**

g.V() parcourt tous les vertices, hasLabel('Film') filtre par label.

---

### Exercice 7 (1 pt): Artistes nés en 1963

**Question:** Trouvez les noms des artistes nés en `1963`, affichez ensuite leur nombre.

**Requête Gremlin:**
```groovy
// Liste des noms
g.V().has('Artist', 'birthYear', 1963)
  .values('primaryName')

// Nombre total
g.V().has('Artist', 'birthYear', 1963)
  .count()
```

**Explication:**

has() filtre sur birthYear = 1963. values() projette les noms, count() retourne le total.

---

### Exercice 8 (1 pt): Acteurs ayant joué dans plus d'un film

**Question:** Trouver l'ensemble des acteurs (sans entrées doublons) qui ont joué dans plus d'un film.

**Requête Gremlin:**
```groovy
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

Traverse les arêtes ACTED_IN (outE + inV), groupe par acteur avec comptage des films distincts (dedup), filtre avec where(gt(1)) ceux ayant plus d'un film.

---

### Exercice 9 (1.5 pt): Artistes avec plusieurs responsabilités (carrière)

**Question:** Trouvez les artistes ayant eu plusieurs responsabilités au cours de leur carrière (acteur, directeur, producteur...).

**Requête Gremlin:**
```groovy
g.V().hasLabel('Artist').as('artist')
  .outE().label().dedup().fold().as('roles')
  .select('artist', 'roles')
  .where(select('roles').count(local).is(gt(1)))
  .by(valueMap('idArtist', 'primaryName'))
  .by()
```

**Explication:**

Collecte les labels des arêtes sortantes avec outE().label().dedup().fold(), filtre les artistes ayant plusieurs types de relations distinctes.

---

### Exercice 10 (2 pt): Artistes avec plusieurs responsabilités dans un même film

**Question:** Montrez les artistes ayant eu plusieurs responsabilités dans un même film (ex: à la fois acteur et directeur, ou toute autre combinaison) et les titres de ces films.

**Requête Gremlin:**
```groovy
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

Part des films, remonte vers artistes (inE + outV), groupe par couple (artiste, film) en collectant les types d'arêtes, filtre ceux ayant plusieurs rôles dans un même film.

---

### Exercice 11 (5 pt bonus): Film(s) avec le plus d'acteurs

**Question:** Trouver le nom du ou des film(s) ayant le plus d'acteurs.

**Requête Gremlin:**
```groovy
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

Compte les acteurs distincts par film (inE + outV + dedup + count), trie par ordre décroissant, limit(1) retourne le film avec le plus d'acteurs.

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
