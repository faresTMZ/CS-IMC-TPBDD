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
// A COMPLETER
```

**Explication:**


---

### Exercice 3 (½ pt): Ajouter une relation ACTED_IN

**Question:** Ajoutez la relation `ACTED_IN` qui modélise votre participation à ce film en tant qu'acteur/actrice

**Requête Cypher:**
```cypher
// A COMPLETER
```

**Explication:**


---

### Exercice 4 (½ pt): Ajouter des professeurs comme réalisateurs

**Question:** Ajoutez deux de vos professeurs/enseignants comme réalisateurs/réalisatrices de ce film.

**Requête Cypher:**
```cypher
// A COMPLETER
```

**Explication:**


---

### Exercice 5 (½ pt): Afficher Nicole Kidman et son année de naissance

**Question:** Affichez le nœud représentant l'actrice nommée `Nicole Kidman`, et visualisez son année de naissance.

**Requête Cypher:**
```cypher
// A COMPLETER
```

**Explication:**


---

### Exercice 6 (½ pt): Visualiser tous les films

**Question:** Visualisez l'ensemble des films.

**Requête Cypher:**
```cypher
// A COMPLETER
```

**Explication:**


---

### Exercice 7 (½ pt): Artistes nés en 1963

**Question:** Trouvez les noms des artistes nés en `1963`, affichez ensuite leur nombre.

**Requête Cypher:**
```cypher
// A COMPLETER
```

**Explication:**


---

### Exercice 8 (1 pt): Acteurs ayant joué dans plus d'un film

**Question:** Trouver l'ensemble des acteurs (sans entrées doublons) qui ont joué dans plus d'un film.

**Requête Cypher:**
```cypher
// A COMPLETER
```

**Explication:**


---

### Exercice 9 (1 pt): Artistes avec plusieurs responsabilités (carrière)

**Question:** Trouvez les artistes ayant eu plusieurs responsabilités au cours de leur carrière (acteur, directeur, producteur...).

**Requête Cypher:**
```cypher
// A COMPLETER
```

**Explication:**


---

### Exercice 10 (1 pt): Artistes avec plusieurs responsabilités dans un même film

**Question:** Montrez les artistes ayant eu plusieurs responsabilités dans un même film (ex: à la fois acteur et directeur, ou toute autre combinaison) et les titres de ces films.

**Requête Cypher:**
```cypher
// A COMPLETER
```

**Explication:**


---

### Exercice 11 (2 pt): Film(s) avec le plus d'acteurs

**Question:** Trouver le nom du ou des film(s) ayant le plus d'acteurs.

**Requête Cypher:**
```cypher
// A COMPLETER
```

**Explication:**


---
