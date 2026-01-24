# Partie 4 - Base de données graphe - Neo4j (Cypher)

## Introduction à Cypher

Cypher est le langage de requêtage de Neo4j. Il utilise des **patterns visuels** pour représenter les graphes :
- `()` = Nœuds (nodes)
- `-->` = Relations (relationships)
- `[]` = Propriétés des relations

## Modèle de données graphe

Dans Neo4j, les données SQL sont transformées en graphe :

**Nœuds (Labels) :**
- `:Artist` - Artistes avec propriétés (idArtist, primaryName, birthYear)
- `:Film` - Films avec propriétés (idFilm, primaryTitle, startYear, runtimeMinutes)
- `:Genre` - Genres avec propriétés (idGenre, genre)

**Relations :**
- `[:ACTED_IN]` - Un artiste a joué dans un film
- `[:DIRECTED]` - Un artiste a réalisé un film
- `[:PRODUCED]` - Un artiste a produit un film
- `[:COMPOSED]` - Un artiste a composé la musique d'un film
- `[:HAS_GENRE]` - Un film appartient à un genre

---

## Requêtes Cypher

### Exercice 1 (¼ pt): Ajouter une personne dans le graphe

**Question:** Ajoutez une personne ayant votre prénom et votre nom dans le graphe. Vérifiez que le nœud a bien été créé.

**Requête Cypher:**
```cypher
// Créer le nœud
CREATE (me:Artist {
    idArtist: 'nm9999999',
    primaryName: 'TAZI',
    birthYear: 2002
})
RETURN me;

// Vérifier
MATCH (me:Artist {primaryName: 'TAZI'})
RETURN me;
```

**Explication:**

CREATE crée un nouveau nœud avec le label Artist et des propriétés (équivalent INSERT en SQL). MATCH recherche ensuite ce nœud pour vérifier qu'il existe bien. Le pattern (variable:Label {propriétés}) est la syntaxe de base de Cypher.

---

### Exercice 2 (¼ pt): Ajouter un film

**Question:** Ajoutez un film nommé `L'histoire de mon 20 au cours Infrastructure de données`

**Requête Cypher:**
```cypher
CREATE (f:Film {
    idFilm: 'tt9999999',
    primaryTitle: 'L\'histoire de mon 20 au cours Infrastructure de données',
    startYear: 2026
})
RETURN f;
```

**Explication:**

CREATE crée un nœud Film avec les propriétés spécifiées.


---

### Exercice 3 (½ pt): Ajouter une relation ACTED_IN

**Question:** Ajoutez la relation `ACTED_IN` qui modélise votre participation à ce film en tant qu'acteur/actrice

**Requête Cypher:**
```cypher
MATCH (a:Artist {primaryName: 'TAZI'}),
      (f:Film {primaryTitle: 'L\'histoire de mon 20 au cours Infrastructure de données'})
CREATE (a)-[r:ACTED_IN]->(f)
RETURN a, r, f;
```

**Explication:**

MATCH trouve les deux nœuds existants (artiste et film), puis CREATE crée la relation ACTED_IN entre eux. La syntaxe (a)-[r:Type]->(f) représente une relation dirigée.


---

### Exercice 4 (½ pt): Ajouter des professeurs comme réalisateurs

**Question:** Ajoutez deux de vos professeurs/enseignants comme réalisateurs/réalisatrices de ce film.

**Requête Cypher:**
```cypher
MATCH (f:Film {primaryTitle: 'L\'histoire de mon 20 au cours Infrastructure de données'})
CREATE (p1:Artist {idArtist: 'nm9999001', primaryName: 'Prof1', birthYear: 1975}),
       (p2:Artist {idArtist: 'nm9999002', primaryName: 'Prof2', birthYear: 1980}),
       (p1)-[:DIRECTED]->(f),
       (p2)-[:DIRECTED]->(f)
RETURN p1, p2, f;
```

**Explication:**

MATCH trouve le film, puis CREATE crée les deux professeurs et leurs relations DIRECTED en une seule requête.


---

### Exercice 5 (½ pt): Afficher Nicole Kidman et son année de naissance

**Question:** Affichez le nœud représentant l'actrice nommée `Nicole Kidman`, et visualisez son année de naissance.

**Requête Cypher:**
```cypher
MATCH (a:Artist {primaryName: 'Nicole Kidman'})
RETURN a.primaryName, a.birthYear;
```

**Explication:**

MATCH trouve l'artiste Nicole Kidman et RETURN affiche son nom et année de naissance.


---

### Exercice 6 (½ pt): Visualiser tous les films

**Question:** Visualisez l'ensemble des films.

**Requête Cypher:**
```cypher
MATCH (f:Film)
RETURN f;
```

**Explication:**

MATCH (f:Film) sélectionne tous les nœuds de type Film sans condition.


---

### Exercice 7 (½ pt): Artistes nés en 1963

**Question:** Trouvez les noms des artistes nés en `1963`, affichez ensuite leur nombre.

**Requête Cypher:**
```cypher
// Liste des noms
MATCH (a:Artist)
WHERE a.birthYear = 1963
RETURN a.primaryName;

// Nombre total
MATCH (a:Artist)
WHERE a.birthYear = 1963
RETURN COUNT(a) AS NombreArtistes;
```

**Explication:**

WHERE filtre les artistes nés en 1963. La première requête retourne les noms, la seconde utilise COUNT pour compter le total.


---

### Exercice 8 (1 pt): Acteurs ayant joué dans plus d'un film

**Question:** Trouver l'ensemble des acteurs (sans entrées doublons) qui ont joué dans plus d'un film.

**Requête Cypher:**
```cypher
MATCH (a:Artist)-[:ACTED_IN]->(f:Film)
WITH a, COUNT(DISTINCT f) AS NombreFilms
WHERE NombreFilms > 1
RETURN a.idArtist, a.primaryName, NombreFilms
ORDER BY NombreFilms DESC;
```

**Explication:**

MATCH traverse les relations ACTED_IN entre artistes et films. WITH regroupe par artiste et compte les films distincts. WHERE filtre ceux ayant joué dans plus d'un film (équivalent HAVING en SQL).


---

### Exercice 9 (1 pt): Artistes avec plusieurs responsabilités (carrière)

**Question:** Trouvez les artistes ayant eu plusieurs responsabilités au cours de leur carrière (acteur, directeur, producteur...).

**Requête Cypher:**
```cypher
MATCH (a:Artist)-[r]->(f:Film)
WITH a, COLLECT(DISTINCT type(r)) AS Responsabilites
WHERE SIZE(Responsabilites) > 1
RETURN a.idArtist, a.primaryName, Responsabilites, SIZE(Responsabilites) AS NombreResponsabilites
ORDER BY NombreResponsabilites DESC;
```

**Explication:**

MATCH avec [r] capture toutes les relations (ACTED_IN, DIRECTED, etc.). COLLECT regroupe les types de relations distincts par artiste, et SIZE compte combien chaque artiste en a. WHERE garde seulement ceux avec plusieurs types de responsabilités.


---

### Exercice 10 (1 pt): Artistes avec plusieurs responsabilités dans un même film

**Question:** Montrez les artistes ayant eu plusieurs responsabilités dans un même film (ex: à la fois acteur et directeur, ou toute autre combinaison) et les titres de ces films.

**Requête Cypher:**
```cypher
MATCH (a:Artist)-[r]->(f:Film)
WITH a, f, COLLECT(DISTINCT type(r)) AS Responsabilites
WHERE SIZE(Responsabilites) > 1
RETURN a.idArtist, a.primaryName, f.primaryTitle, Responsabilites, SIZE(Responsabilites) AS NombreResponsabilites
ORDER BY NombreResponsabilites DESC;
```

**Explication:**

Similaire à l'exercice 9 mais WITH garde à la fois l'artiste ET le film, ce qui regroupe par couple (artiste, film). Cela détecte les cas où un artiste a plusieurs rôles dans UN MÊME film (ex: Ben Affleck acteur+réalisateur dans Argo).


---

### Exercice 11 (2 pt): Film(s) avec le plus d'acteurs

**Question:** Trouver le nom du ou des film(s) ayant le plus d'acteurs.

**Requête Cypher:**
```cypher
MATCH (a:Artist)-[:ACTED_IN]->(f:Film)
WITH f, COUNT(DISTINCT a) AS NombreActeurs
ORDER BY NombreActeurs DESC
LIMIT 1
RETURN f.idFilm, f.primaryTitle, NombreActeurs;
```

**Explication:**

MATCH traverse les relations ACTED_IN. WITH regroupe par film et compte les acteurs distincts. ORDER BY DESC + LIMIT 1 retourne le film avec le plus d'acteurs. Note : retourne un seul film en cas d'ex-aequo.


---
