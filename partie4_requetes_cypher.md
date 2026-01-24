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
// ============================================================================
// Exercice 1 : Créer un nœud Artist avec votre nom
// ============================================================================
// Cette requête crée un nouveau nœud de type Artist avec des propriétés
// ============================================================================

// Partie 1 : Créer le nœud
CREATE (me:Artist {
    idArtist: 'nm9999999',           -- Identifiant unique (fictif)
    primaryName: 'Votre Prénom Nom',  -- Remplacer par votre nom
    birthYear: 2000                   -- Remplacer par votre année de naissance
})
RETURN me;

// Partie 2 : Vérifier que le nœud a été créé
MATCH (me:Artist {primaryName: 'Votre Prénom Nom'})
RETURN me;
```

**Explication:**

**Partie 1 - CREATE :**
1. **CREATE** : Statement pour créer un nouveau nœud dans le graphe
2. **(me:Artist {...})** :
   - `me` : Variable temporaire pour référencer le nœud créé
   - `:Artist` : Label (type) du nœud - équivalent à une table en SQL
   - `{...}` : Propriétés du nœud (équivalent aux colonnes)
3. **Propriétés** :
   - `idArtist` : Identifiant unique (utiliser un ID fictif comme 'nm9999999')
   - `primaryName` : Votre nom complet
   - `birthYear` : Votre année de naissance
4. **RETURN me** : Retourne le nœud créé pour visualisation

**Partie 2 - MATCH (Vérification) :**
1. **MATCH** : Statement pour rechercher des nœuds existants
2. **(me:Artist {...})** : Pattern de recherche
   - Cherche un nœud avec le label `:Artist`
   - Ayant la propriété `primaryName` correspondante
3. **RETURN me** : Affiche le nœud trouvé

**Concepts Cypher utilisés :**
- **CREATE** : Création de nœuds
- **Label** : Type/catégorie d'un nœud (`:Artist`)
- **Propriétés** : Attributs stockés dans le nœud (format JSON)
- **MATCH** : Pattern matching pour rechercher des nœuds
- **RETURN** : Projection des résultats

**Exemple concret :**
```cypher
// Créer un étudiant fictif
CREATE (me:Artist {
    idArtist: 'nm9999999',
    primaryName: 'Jean Dupont',
    birthYear: 2002
})
RETURN me;

// Vérifier
MATCH (me:Artist {primaryName: 'Jean Dupont'})
RETURN me.idArtist, me.primaryName, me.birthYear;
```

**Différence avec SQL :**
| Aspect | SQL | Cypher |
|--------|-----|--------|
| Créer | INSERT INTO tArtist VALUES (...) | CREATE (a:Artist {...}) |
| Lire | SELECT * FROM tArtist WHERE ... | MATCH (a:Artist {...}) RETURN a |
| Structure | Table avec lignes/colonnes | Graphe avec nœuds/relations |

---

### Exercice 2 (¼ pt): Ajouter un film

**Question:** Ajoutez un film nommé `L'histoire de mon 20 au cours Infrastructure de données`

**Requête Cypher:**
```cypher
// Création d'un nœud Film avec les propriétés nécessaires
CREATE (f:Film {
    idFilm: 'tt9999999',
    primaryTitle: 'L\'histoire de mon 20 au cours Infrastructure de données',
    startYear: 2026
})
RETURN f;
```

**Explication:**

On utilise CREATE pour insérer un nouveau nœud de type Film dans le graphe avec les propriétés idFilm, primaryTitle et startYear. Le RETURN permet de visualiser le nœud créé et vérifier que l'insertion s'est bien déroulée.


---

### Exercice 3 (½ pt): Ajouter une relation ACTED_IN

**Question:** Ajoutez la relation `ACTED_IN` qui modélise votre participation à ce film en tant qu'acteur/actrice

**Requête Cypher:**
```cypher
// On matche d'abord les deux nœuds existants (artiste TAZI et le film)
// puis on crée la relation ACTED_IN entre eux
MATCH (a:Artist {primaryName: 'TAZI'}),
      (f:Film {primaryTitle: 'L\'histoire de mon 20 au cours Infrastructure de données'})
CREATE (a)-[r:ACTED_IN]->(f)
RETURN a, r, f;
```

**Explication:**

MATCH permet de rechercher les deux nœuds existants (l'artiste TAZI créé en exercice 1 et le film créé en exercice 2). Ensuite CREATE établit la relation ACTED_IN entre l'artiste et le film avec la syntaxe de flèche `(a)-[r:ACTED_IN]->(f)` qui représente visuellement la direction de la relation.


---

### Exercice 4 (½ pt): Ajouter des professeurs comme réalisateurs

**Question:** Ajoutez deux de vos professeurs/enseignants comme réalisateurs/réalisatrices de ce film.

**Requête Cypher:**
```cypher
// Création des deux professeurs et des relations DIRECTED en une seule requête
MATCH (f:Film {primaryTitle: 'L\'histoire de mon 20 au cours Infrastructure de données'})
CREATE (p1:Artist {idArtist: 'nm9999001', primaryName: 'Prof1', birthYear: 1975}),
       (p2:Artist {idArtist: 'nm9999002', primaryName: 'Prof2', birthYear: 1980}),
       (p1)-[:DIRECTED]->(f),
       (p2)-[:DIRECTED]->(f)
RETURN p1, p2, f;
```

**Explication:**

On commence par matcher le film cible, puis on crée simultanément les deux nœuds Artist (Prof1 et Prof2) et leurs relations DIRECTED vers le film. Cette syntaxe permet de créer plusieurs nœuds et relations en une seule requête de manière efficace.


---

### Exercice 5 (½ pt): Afficher Nicole Kidman et son année de naissance

**Question:** Affichez le nœud représentant l'actrice nommée `Nicole Kidman`, et visualisez son année de naissance.

**Requête Cypher:**
```cypher
// Pattern matching simple pour trouver Nicole Kidman
MATCH (a:Artist {primaryName: 'Nicole Kidman'})
RETURN a.primaryName, a.birthYear;
```

**Explication:**

MATCH recherche un nœud Artist ayant comme propriété primaryName la valeur 'Nicole Kidman'. Le RETURN projette les propriétés demandées (nom et année de naissance) du nœud trouvé.


---

### Exercice 6 (½ pt): Visualiser tous les films

**Question:** Visualisez l'ensemble des films.

**Requête Cypher:**
```cypher
// Récupération de tous les nœuds de type Film
MATCH (f:Film)
RETURN f;
```

**Explication:**

Le pattern MATCH (f:Film) sélectionne tous les nœuds ayant le label Film sans aucune condition de filtrage. Le RETURN retourne l'ensemble des nœuds Film trouvés dans le graphe.


---

### Exercice 7 (½ pt): Artistes nés en 1963

**Question:** Trouvez les noms des artistes nés en `1963`, affichez ensuite leur nombre.

**Requête Cypher:**
```cypher
// Partie 1 : Liste des noms
MATCH (a:Artist)
WHERE a.birthYear = 1963
RETURN a.primaryName;

// Partie 2 : Nombre total
MATCH (a:Artist)
WHERE a.birthYear = 1963
RETURN COUNT(a) AS NombreArtistes;
```

**Explication:**

La première requête utilise WHERE pour filtrer les artistes nés en 1963 et retourne leurs noms. La seconde requête applique la fonction d'agrégation COUNT sur le même pattern pour obtenir le nombre total d'artistes correspondants.


---

### Exercice 8 (1 pt): Acteurs ayant joué dans plus d'un film

**Question:** Trouver l'ensemble des acteurs (sans entrées doublons) qui ont joué dans plus d'un film.

**Requête Cypher:**
```cypher
// Pattern de traversée pour compter les films par acteur
MATCH (a:Artist)-[:ACTED_IN]->(f:Film)
WITH a, COUNT(DISTINCT f) AS NombreFilms
WHERE NombreFilms > 1
RETURN a.idArtist, a.primaryName, NombreFilms
ORDER BY NombreFilms DESC;
```

**Explication:**

On matche le pattern (acteur)-[:ACTED_IN]->(film) pour traverser les relations, puis WITH regroupe par artiste et compte les films distincts. La clause WHERE filtre ensuite pour ne garder que les acteurs ayant joué dans plus d'un film.


---

### Exercice 9 (1 pt): Artistes avec plusieurs responsabilités (carrière)

**Question:** Trouvez les artistes ayant eu plusieurs responsabilités au cours de leur carrière (acteur, directeur, producteur...).

**Requête Cypher:**
```cypher
// On collecte tous les types de relations pour chaque artiste
MATCH (a:Artist)-[r]->(f:Film)
WITH a, COLLECT(DISTINCT type(r)) AS Responsabilites
WHERE SIZE(Responsabilites) > 1
RETURN a.idArtist, a.primaryName, Responsabilites, SIZE(Responsabilites) AS NombreResponsabilites
ORDER BY NombreResponsabilites DESC;
```

**Explication:**

Le pattern matche toutes les relations entre artistes et films (peu importe le type). COLLECT récupère les types de relations distincts (ACTED_IN, DIRECTED, etc.) pour chaque artiste, et SIZE compte leur nombre. On filtre pour ne garder que ceux ayant plusieurs types de responsabilités différentes.


---

### Exercice 10 (1 pt): Artistes avec plusieurs responsabilités dans un même film

**Question:** Montrez les artistes ayant eu plusieurs responsabilités dans un même film (ex: à la fois acteur et directeur, ou toute autre combinaison) et les titres de ces films.

**Requête Cypher:**
```cypher
// Regroupement par couple (artiste, film) pour détecter les cumuls de rôles
MATCH (a:Artist)-[r]->(f:Film)
WITH a, f, COLLECT(DISTINCT type(r)) AS Responsabilites
WHERE SIZE(Responsabilites) > 1
RETURN a.idArtist, a.primaryName, f.primaryTitle, Responsabilites, SIZE(Responsabilites) AS NombreResponsabilites
ORDER BY NombreResponsabilites DESC;
```

**Explication:**

Cette requête matche les relations artiste-film et regroupe par couple (artiste, film) grâce au WITH qui garde les deux variables. COLLECT récupère les types de relations pour chaque paire, permettant d'identifier les cas où un artiste a plusieurs rôles dans un même film (ex: acteur et réalisateur).


---

### Exercice 11 (2 pt): Film(s) avec le plus d'acteurs

**Question:** Trouver le nom du ou des film(s) ayant le plus d'acteurs.

**Requête Cypher:**
```cypher
// Comptage des acteurs par film, puis sélection du maximum
MATCH (a:Artist)-[:ACTED_IN]->(f:Film)
WITH f, COUNT(DISTINCT a) AS NombreActeurs
ORDER BY NombreActeurs DESC
LIMIT 1
RETURN f.idFilm, f.primaryTitle, NombreActeurs;
```

**Explication:**

On traverse les relations ACTED_IN pour compter le nombre d'acteurs distincts par film. ORDER BY DESC trie les films par nombre d'acteurs décroissant et LIMIT 1 retourne uniquement le film ayant le casting le plus large. Note : cette approche retourne un seul film en cas d'égalité, pour retourner tous les ex-aequo il faudrait utiliser une sous-requête avec MAX.


---
