# Partie 1 - Base de données relationnelle - Azure SQL Database

## Requêtes SQL

### Exercice 0 (Description des tables et attributs)

La base de données contient 5 tables décrivant des films, des artistes et leurs relations :

#### 1. **tArtist** - Table des artistes
Stocke les informations sur les personnes impliquées dans les films (acteurs, réalisateurs, etc.)

| Attribut | Type | Description |
|----------|------|-------------|
| idArtist | nvarchar(10) | **Clé primaire** - Identifiant unique de l'artiste |
| primaryName | nvarchar(max) | Nom complet de l'artiste |
| birthYear | smallint | Année de naissance de l'artiste (peut être NULL) |

#### 2. **tFilm** - Table des films
Contient les informations principales sur chaque film

| Attribut | Type | Description |
|----------|------|-------------|
| idFilm | nvarchar(10) | **Clé primaire** - Identifiant unique du film |
| primaryTitle | nvarchar(max) | Titre principal du film |
| startYear | smallint | Année de sortie du film (peut être NULL) |
| runtimeMinutes | smallint | Durée du film en minutes (peut être NULL) |

#### 3. **tGenre** - Table des genres
Liste des genres cinématographiques

| Attribut | Type | Description |
|----------|------|-------------|
| idGenre | nvarchar(35) | **Clé primaire** - Identifiant unique du genre |
| genre | nvarchar(20) | Nom du genre (Action, Drama, Comedy, etc.) |

#### 4. **tFilmGenre** - Table de liaison Film-Genre
Table d'association permettant à un film d'avoir plusieurs genres (relation many-to-many)

| Attribut | Type | Description |
|----------|------|-------------|
| idFilm | nvarchar(10) | **Clé étrangère** vers tFilm - Identifiant du film |
| idGenre | nvarchar(35) | **Clé étrangère** vers tGenre - Identifiant du genre |

**Clé primaire composite** : (idFilm, idGenre)

#### 5. **tJob** - Table des rôles/responsabilités
Associe les artistes aux films avec leur rôle spécifique (relation many-to-many avec attribut)

| Attribut | Type | Description |
|----------|------|-------------|
| idArtist | nvarchar(10) | **Clé étrangère** vers tArtist - Identifiant de l'artiste |
| idFilm | nvarchar(10) | **Clé étrangère** vers tFilm - Identifiant du film |
| category | nvarchar(20) | Type de responsabilité (actor, director, producer, etc.) |

**Clé primaire composite** : (idArtist, idFilm, category)

---

**Schéma relationnel :**
- Un **artiste** peut travailler sur plusieurs **films** (via tJob)
- Un **film** peut avoir plusieurs **artistes** (via tJob) avec différentes responsabilités
- Un **film** peut appartenir à plusieurs **genres** (via tFilmGenre)
- Un **genre** peut être associé à plusieurs **films** (via tFilmGenre)


---

### Exercice 1 (¼ pt): Année de naissance de Jude Law

**Requête SQL:**
```sql
-- ============================================================================
-- Exercice 1 : Visualiser l'année de naissance de l'artiste Jude Law
-- ============================================================================
-- Cette requête effectue une simple sélection (projection) sur un attribut
-- spécifique en filtrant sur le nom de l'artiste.
-- ============================================================================

SELECT
    birthYear           -- Projection : on sélectionne uniquement l'année de naissance
FROM
    tArtist            -- Table source contenant les informations des artistes
WHERE
    primaryName = 'Jude Law';  -- Restriction : filtre pour ne garder que l'artiste recherché
```

**Explication:**

Cette requête effectue une **projection-restriction** simple :

1. **SELECT birthYear** : On projette uniquement la colonne `birthYear` car c'est la seule information demandée

2. **FROM tArtist** : La source de données est la table `tArtist` qui contient tous les artistes

3. **WHERE primaryName = 'Jude Law'** : Clause de restriction permettant de filtrer les lignes
   - On utilise l'opérateur d'égalité `=` pour faire une correspondance exacte
   - Le nom est entre apostrophes car c'est une chaîne de caractères (nvarchar)
   - Cette condition limite le résultat à un seul artiste

**Concepts SQL utilisés :**
- **Projection** : Sélection de colonnes spécifiques (birthYear)
- **Restriction** : Filtrage de lignes selon une condition (WHERE)
- **Comparaison de chaînes** : Utilisation de l'opérateur `=` avec des valeurs textuelles


---

### Exercice 2 (¼ pt): Nombre d'artistes dans la base

**Requête SQL:**
```sql
-- ============================================================================
-- Exercice 2 : Compter le nombre d'artistes présents dans la base de données
-- ============================================================================
-- Cette requête utilise la fonction d'agrégation COUNT pour compter le nombre
-- total de lignes dans la table tArtist.
-- ============================================================================

SELECT
    COUNT(*) AS NombreArtistes    -- Fonction d'agrégation qui compte toutes les lignes
FROM
    tArtist;                      -- Table contenant tous les artistes
```

**Explication:**

Cette requête utilise une **fonction d'agrégation** pour obtenir un résultat statistique :

1. **COUNT(*)** : Fonction d'agrégation qui compte le nombre total de lignes dans la table
   - L'astérisque `*` signifie "toutes les lignes"
   - COUNT compte même les valeurs NULL dans les colonnes
   - Retourne un seul nombre entier représentant le total

2. **AS NombreArtistes** : Alias pour rendre le résultat plus lisible
   - Renomme la colonne de résultat
   - Facultatif mais améliore la compréhension du résultat

3. **FROM tArtist** : La table source sur laquelle on effectue le comptage

**Concepts SQL utilisés :**
- **Fonction d'agrégation** : COUNT(*) pour calculer un résultat sur l'ensemble des lignes
- **Alias de colonne** : AS pour renommer le résultat
- **Pas de WHERE** : On compte toutes les lignes sans restriction

**Alternative possible :**
```sql
SELECT COUNT(idArtist) AS NombreArtistes FROM tArtist;
```
Cette version compte uniquement les valeurs non-NULL de `idArtist`, mais comme c'est une clé primaire (jamais NULL), le résultat est identique.


---

### Exercice 3 (¼ pt): Artistes nés en 1960

**Requête SQL:**
```sql
-- ============================================================================
-- Exercice 3 : Trouver les noms des artistes nés en 1960 et leur nombre
-- ============================================================================
-- Cette requête combine une restriction sur l'année de naissance et
-- un comptage pour obtenir à la fois la liste et le total.
-- ============================================================================

-- Partie 1 : Liste des noms des artistes nés en 1960
SELECT
    primaryName        -- Projection du nom de l'artiste
FROM
    tArtist           -- Table des artistes
WHERE
    birthYear = 1960; -- Restriction : uniquement les artistes nés en 1960

-- Partie 2 : Nombre total d'artistes nés en 1960
SELECT
    COUNT(*) AS NombreArtistesNes1960    -- Comptage avec alias explicite
FROM
    tArtist
WHERE
    birthYear = 1960;                     -- Même condition de filtrage
```

**Explication:**

Cette question demande **deux informations distinctes**, donc nous utilisons **deux requêtes séparées** :

**Requête 1 - Liste des noms :**
1. **SELECT primaryName** : On projette uniquement le nom des artistes
2. **WHERE birthYear = 1960** : Filtre pour ne garder que les artistes nés en 1960
3. Cette requête retourne une ligne par artiste trouvé

**Requête 2 - Comptage :**
1. **COUNT(*)** : Fonction d'agrégation pour compter les lignes
2. **WHERE birthYear = 1960** : Même condition de filtrage
3. Cette requête retourne un seul nombre : le total

**Concepts SQL utilisés :**
- **Restriction avec égalité numérique** : `birthYear = 1960` (pas de quotes car c'est un nombre)
- **Projection simple** : Sélection d'un seul attribut
- **Agrégation avec condition** : COUNT(*) combiné avec WHERE

**Alternative - Requête combinée (avancé) :**
```sql
SELECT
    primaryName,
    COUNT(*) OVER() AS Total
FROM tArtist
WHERE birthYear = 1960;
```
Cette version utilise une **fonction fenêtre** pour afficher à la fois les noms et le total dans un seul résultat, mais nécessite SQL Server 2012+.


---

### Exercice 4 (1 pt): Année de naissance la plus représentée

**Requête SQL:**
```sql
-- ============================================================================
-- Exercice 4 : Année de naissance la plus représentée parmi les acteurs
-- ============================================================================
-- Cette requête utilise une jointure, un regroupement, une agrégation,
-- un filtrage et un tri pour trouver l'année avec le plus d'acteurs.
-- ============================================================================

SELECT TOP 1
    birthYear,                                  -- L'année de naissance
    COUNT(DISTINCT tArtist.idArtist) AS NombreActeurs  -- Nombre d'acteurs distincts
FROM
    tArtist
INNER JOIN
    tJob ON tArtist.idArtist = tJob.idArtist   -- Jointure pour lier artistes et rôles
WHERE
    tJob.category = 'actor'                     -- Restriction : uniquement les acteurs
    AND birthYear != 0                          -- Exclure l'année 0 (donnée invalide)
    AND birthYear IS NOT NULL                   -- Exclure les NULL
GROUP BY
    birthYear                                   -- Regroupement par année de naissance
ORDER BY
    NombreActeurs DESC;                         -- Tri décroissant pour avoir le max en premier
```

**Explication:**

Cette requête est plus complexe et combine plusieurs concepts avancés :

**1. INNER JOIN (Jointure interne) :**
   - Lie la table `tArtist` avec `tJob` via la clé `idArtist`
   - Permet d'accéder à l'attribut `category` pour filtrer les acteurs
   - Ne garde que les artistes qui ont au moins un rôle enregistré

**2. WHERE (Multiple conditions) :**
   - `category = 'actor'` : Filtre uniquement les acteurs (pas les directors, producers, etc.)
   - `birthYear != 0` : Exclut les valeurs aberrantes (année 0 invalide)
   - `birthYear IS NOT NULL` : Exclut les valeurs manquantes

**3. GROUP BY (Regroupement) :**
   - Regroupe toutes les lignes ayant la même `birthYear`
   - Permet ensuite d'appliquer une fonction d'agrégation sur chaque groupe

**4. COUNT(DISTINCT idArtist) (Agrégation) :**
   - Compte le nombre d'artistes **distincts** pour chaque année
   - DISTINCT est important car un acteur peut avoir joué dans plusieurs films
   - Sans DISTINCT, on compterait le nombre de rôles, pas le nombre d'acteurs

**5. ORDER BY ... DESC (Tri décroissant) :**
   - Trie les résultats par nombre d'acteurs du plus grand au plus petit
   - Place l'année la plus représentée en première position

**6. TOP 1 (Limitation) :**
   - Limite le résultat à la première ligne seulement
   - Combiné avec ORDER BY DESC, retourne l'année avec le maximum d'acteurs

**Concepts SQL utilisés :**
- **Jointure interne** : INNER JOIN pour relier deux tables
- **Agrégation avec regroupement** : GROUP BY + COUNT
- **Fonction DISTINCT** : Éviter les doublons dans le comptage
- **Tri et limitation** : ORDER BY + TOP pour trouver le maximum
- **Conditions multiples** : AND pour combiner plusieurs filtres

**Ordre d'exécution logique :**
1. FROM + JOIN : Combiner tArtist et tJob
2. WHERE : Filtrer les acteurs et années valides
3. GROUP BY : Regrouper par année
4. COUNT : Compter pour chaque groupe
5. ORDER BY : Trier par comptage décroissant
6. TOP 1 : Ne garder que le premier résultat


---

### Exercice 5 (½ pt): Artistes ayant joué dans plus d'un film

**Requête SQL:**
```sql
-- A COMPLETER
```

**Explication:**


---

### Exercice 6 (½ pt): Artistes avec plusieurs responsabilités

**Requête SQL:**
```sql
-- A COMPLETER
```

**Explication:**


---

### Exercice 7 (¾ pt): Film(s) avec le plus d'acteurs

**Requête SQL:**
```sql
-- A COMPLETER
```

**Explication:**


---

### Exercice 8 (1 pt): Artistes avec plusieurs responsabilités dans un même film

**Requête SQL:**
```sql
-- A COMPLETER
```

**Explication:**


