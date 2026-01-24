# Partie 1 - Base de données relationnelle - Azure SQL Database

## Requêtes SQL

### Exercice 0 (Description des tables et attributs)

La base de données contient 5 tables décrivant des films, des artistes et leurs relations :

**1. tArtist** - Table des artistes stockant les personnes impliquées dans les films
- idArtist (nvarchar(10)) : Clé primaire - Identifiant unique de l'artiste
- primaryName (nvarchar(max)) : Nom complet de l'artiste
- birthYear (smallint) : Année de naissance de l'artiste (peut être NULL)

**2. tFilm** - Table des films avec les informations principales
- idFilm (nvarchar(10)) : Clé primaire - Identifiant unique du film
- primaryTitle (nvarchar(max)) : Titre principal du film
- startYear (smallint) : Année de sortie du film (peut être NULL)
- runtimeMinutes (smallint) : Durée du film en minutes (peut être NULL)

**3. tGenre** - Table des genres cinématographiques
- idGenre (nvarchar(35)) : Clé primaire - Identifiant unique du genre
- genre (nvarchar(20)) : Nom du genre (Action, Drama, Comedy, etc.)

**4. tFilmGenre** - Table de liaison Film-Genre (relation many-to-many)
- idFilm (nvarchar(10)) : Clé étrangère vers tFilm
- idGenre (nvarchar(35)) : Clé étrangère vers tGenre
- Clé primaire composite : (idFilm, idGenre)

**5. tJob** - Table des rôles/responsabilités des artistes dans les films
- idArtist (nvarchar(10)) : Clé étrangère vers tArtist
- idFilm (nvarchar(10)) : Clé étrangère vers tFilm
- category (nvarchar(20)) : Type de responsabilité (acted in, directed, produced, composed)
- Clé primaire composite : (idArtist, idFilm, category)

**Schéma relationnel :**
Un artiste peut travailler sur plusieurs films (via tJob), un film peut avoir plusieurs artistes avec différentes responsabilités, un film peut appartenir à plusieurs genres (via tFilmGenre).


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
    tJob.category = 'acted in'                  -- Restriction : uniquement les acteurs
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
   - `category = 'acted in'` : Filtre uniquement les acteurs (pas les directors, producers, etc.)
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
-- ============================================================================
-- Exercice 5 : Trouver les artistes ayant joué dans plus d'un film
-- ============================================================================
-- Cette requête utilise un regroupement avec la clause HAVING pour filtrer
-- les groupes selon une condition d'agrégation.
-- ============================================================================

SELECT
    tArtist.idArtist,                             -- Identifiant de l'artiste
    tArtist.primaryName,                          -- Nom de l'artiste
    COUNT(DISTINCT tJob.idFilm) AS NombreFilms    -- Nombre de films distincts
FROM
    tArtist
INNER JOIN
    tJob ON tArtist.idArtist = tJob.idArtist     -- Jointure artiste-rôle
WHERE
    tJob.category = 'acted in'                    -- Restriction : uniquement acteurs
GROUP BY
    tArtist.idArtist, tArtist.primaryName         -- Regroupement par artiste
HAVING
    COUNT(DISTINCT tJob.idFilm) > 1               -- Filtre sur agrégat : plus d'1 film
ORDER BY
    NombreFilms DESC;                             -- Tri : les plus prolifiques d'abord
```

**Explication:**

Cette requête introduit la clause **HAVING**, qui permet de filtrer des groupes après agrégation :

**1. INNER JOIN :**
   - Relie `tArtist` et `tJob` pour accéder aux rôles de chaque artiste
   - Permet de compter les films par artiste

**2. WHERE category = 'acted in' :**
   - Filtre avant le regroupement
   - Ne garde que les lignes où l'artiste a agi (pas réalisé, produit, etc.)

**3. GROUP BY idArtist, primaryName :**
   - Regroupe les lignes par artiste
   - On doit inclure `primaryName` dans le GROUP BY car on le sélectionne (règle SQL)
   - Chaque groupe représente un artiste unique avec tous ses films

**4. COUNT(DISTINCT idFilm) :**
   - Compte le nombre de films **distincts** pour chaque artiste
   - DISTINCT est essentiel : un acteur peut avoir plusieurs catégories dans un même film
   - Sans DISTINCT, on compterait les lignes de tJob, pas les films uniques

**5. HAVING COUNT(DISTINCT idFilm) > 1 :**
   - **Différence avec WHERE** : HAVING filtre **après** le regroupement et agrégation
   - WHERE filtre des lignes individuelles, HAVING filtre des groupes entiers
   - Ne garde que les artistes ayant joué dans **plus d'un film** (≥ 2)

**6. ORDER BY NombreFilms DESC :**
   - Trie les résultats par nombre de films décroissant
   - Les acteurs les plus prolifiques apparaissent en premier

**Concepts SQL utilisés :**
- **HAVING** : Clause de filtrage sur les résultats d'agrégation
- **Différence WHERE vs HAVING** :
  - WHERE : Filtre les lignes avant regroupement
  - HAVING : Filtre les groupes après regroupement
- **GROUP BY multiple** : Regroupement sur plusieurs colonnes
- **COUNT(DISTINCT)** : Comptage sans doublons

**Exemple de résultat attendu :**
```
idArtist   | primaryName      | NombreFilms
-----------|------------------|-------------
nm0000123  | Tom Hanks        | 45
nm0000456  | Meryl Streep     | 38
...
```


---

### Exercice 6 (½ pt): Artistes avec plusieurs responsabilités

**Requête SQL:**
```sql
-- ============================================================================
-- Exercice 6 : Artistes ayant eu plusieurs responsabilités au cours de leur carrière
-- ============================================================================
-- Cette requête compte le nombre de catégories distinctes (actor, director, etc.)
-- pour chaque artiste, et ne garde que ceux qui en ont plusieurs.
-- ============================================================================

SELECT
    tArtist.idArtist,                                -- Identifiant de l'artiste
    tArtist.primaryName,                             -- Nom de l'artiste
    COUNT(DISTINCT tJob.category) AS NombreResponsabilites  -- Nombre de rôles différents
FROM
    tArtist
INNER JOIN
    tJob ON tArtist.idArtist = tJob.idArtist        -- Jointure artiste-rôle
GROUP BY
    tArtist.idArtist, tArtist.primaryName            -- Regroupement par artiste
HAVING
    COUNT(DISTINCT tJob.category) > 1                -- Filtre : au moins 2 responsabilités
ORDER BY
    NombreResponsabilites DESC;                      -- Tri : les plus polyvalents d'abord
```

**Explication:**

Cette requête est similaire à l'exercice 5, mais compte les **catégories** distinctes au lieu des **films** distincts :

**1. INNER JOIN tJob :**
   - Relie chaque artiste à tous ses rôles dans tJob
   - Donne accès à la colonne `category` (actor, director, producer, etc.)

**2. GROUP BY idArtist, primaryName :**
   - Regroupe toutes les lignes par artiste
   - Permet de calculer des statistiques par artiste

**3. COUNT(DISTINCT category) :**
   - Compte le nombre de **catégories/responsabilités différentes** pour chaque artiste
   - DISTINCT élimine les doublons : si quelqu'un a joué dans 10 films, on compte "acted in" une seule fois
   - Exemples de catégories : "acted in", "directed", "produced", "composed"

**4. HAVING COUNT(DISTINCT category) > 1 :**
   - Filtre après agrégation
   - Ne garde que les artistes **polyvalents** qui ont eu au moins 2 types de responsabilités
   - Exclut ceux qui n'ont été qu'acteur, ou que réalisateur, etc.

**5. ORDER BY NombreResponsabilites DESC :**
   - Trie par polyvalence décroissante
   - Les artistes les plus polyvalents (ex: acteur + réalisateur + producteur) apparaissent en premier

**Concepts SQL utilisés :**
- **COUNT(DISTINCT)** sur une colonne catégorielle (category)
- **HAVING** pour filtrer sur un résultat d'agrégation
- **Agrégation sans WHERE** : on considère tous les rôles de chaque artiste

**Différence avec l'exercice 5 :**
- Question : Ex5 = Plusieurs films ? / Ex6 = Plusieurs responsabilités ?
- WHERE : Ex5 = category = 'acted in' / Ex6 = Aucun (tous les rôles)
- COUNT : Ex5 = DISTINCT idFilm / Ex6 = DISTINCT category
- Signification : Ex5 = Nombre de films / Ex6 = Nombre de types de rôles

**Exemple de résultat attendu :**
- nm0000123, Clint Eastwood : 4 responsabilités (acted in, directed, produced, composed)
- nm0000456, Ben Affleck : 3 responsabilités (acted in, directed, produced)
- nm0000789, Angelina Jolie : 2 responsabilités (acted in, directed)


---

### Exercice 7 (¾ pt): Film(s) avec le plus d'acteurs

**Requête SQL:**
```sql
-- ============================================================================
-- Exercice 7 : Trouver le(s) film(s) ayant le plus d'acteurs
-- ============================================================================
-- Cette requête utilise TOP 1 WITH TIES pour retourner tous les films
-- ex-aequo ayant le nombre maximum d'acteurs.
-- ============================================================================

SELECT TOP 1 WITH TIES
    tFilm.idFilm,                                 -- Identifiant du film
    tFilm.primaryTitle,                           -- Titre du film
    COUNT(DISTINCT tJob.idArtist) AS NombreActeurs  -- Nombre d'acteurs distincts
FROM
    tFilm
INNER JOIN
    tJob ON tFilm.idFilm = tJob.idFilm           -- Jointure film-rôle
WHERE
    tJob.category = 'acted in'                    -- Restriction : uniquement acteurs
GROUP BY
    tFilm.idFilm, tFilm.primaryTitle              -- Regroupement par film
ORDER BY
    NombreActeurs DESC;                           -- Tri décroissant : max en premier
```

**Explication:**

Cette requête trouve le(s) film(s) avec le **casting le plus large** en utilisant une technique spéciale pour gérer les ex-aequo :

**1. INNER JOIN tJob :**
   - Relie chaque film à tous ses membres d'équipe dans tJob
   - Permet d'accéder à la catégorie de chaque personne

**2. WHERE category = 'acted in' :**
   - Filtre important : on ne compte que les acteurs
   - Exclut les directors, producers, writers, etc.
   - Sans ce filtre, on compterait toute l'équipe technique

**3. GROUP BY idFilm, primaryTitle :**
   - Regroupe toutes les lignes par film
   - Permet de calculer le nombre d'acteurs par film
   - On doit inclure `primaryTitle` car on le sélectionne

**4. COUNT(DISTINCT idArtist) :**
   - Compte le nombre d'acteurs **distincts** dans chaque film
   - DISTINCT évite de compter deux fois le même acteur (cas rare mais possible)

**5. ORDER BY NombreActeurs DESC :**
   - Trie par nombre d'acteurs décroissant
   - Le(s) film(s) avec le plus d'acteurs apparaissent en premier

**6. TOP 1 WITH TIES (Technique clé) :**
   - `TOP 1` : Normalement, retourne seulement la première ligne
   - `WITH TIES` : **Retourne aussi toutes les lignes ex-aequo** ayant la même valeur dans ORDER BY
   - Exemple : Si 3 films ont 150 acteurs (le maximum), les 3 seront retournés
   - Sans WITH TIES, un seul film serait retourné arbitrairement

**Concepts SQL utilisés :**
- **TOP n WITH TIES** : Technique SQL Server pour gérer les ex-aequo
- **Jointure + Filtrage + Regroupement** : Combinaison de plusieurs opérations
- **COUNT(DISTINCT)** : Comptage sans doublons

**Alternative avec sous-requête (approche plus portable) :**
```sql
WITH FilmActorCount AS (
    SELECT
        tFilm.idFilm,
        tFilm.primaryTitle,
        COUNT(DISTINCT tJob.idArtist) AS NombreActeurs
    FROM tFilm
    INNER JOIN tJob ON tFilm.idFilm = tJob.idFilm
    WHERE tJob.category = 'acted in'
    GROUP BY tFilm.idFilm, tFilm.primaryTitle
)
SELECT idFilm, primaryTitle, NombreActeurs
FROM FilmActorCount
WHERE NombreActeurs = (SELECT MAX(NombreActeurs) FROM FilmActorCount);
```
Cette version utilise une **CTE (Common Table Expression)** et une sous-requête pour trouver le maximum.

**Exemple de résultat attendu :**
- tt0000123, The Avengers: Endgame : 127 acteurs
- tt0000456, Lord of the Rings: Return : 127 acteurs
(Si les deux films ont exactement 127 acteurs, les deux sont retournés grâce à WITH TIES)


---

### Exercice 8 (1 pt): Artistes avec plusieurs responsabilités dans un même film

**Requête SQL:**
```sql
-- ============================================================================
-- Exercice 8 : Artistes ayant plusieurs responsabilités dans un MÊME film
-- ============================================================================
-- Cette requête combine un regroupement sur deux dimensions (artiste ET film)
-- pour trouver les cas où une personne a plusieurs rôles dans un projet.
-- ============================================================================

SELECT
    tArtist.idArtist,                                -- Identifiant de l'artiste
    tArtist.primaryName,                             -- Nom de l'artiste
    tFilm.idFilm,                                    -- Identifiant du film
    tFilm.primaryTitle,                              -- Titre du film
    COUNT(DISTINCT tJob.category) AS NombreResponsabilites  -- Nombre de rôles dans ce film
FROM
    tJob
INNER JOIN
    tArtist ON tJob.idArtist = tArtist.idArtist     -- Jointure pour nom de l'artiste
INNER JOIN
    tFilm ON tJob.idFilm = tFilm.idFilm             -- Jointure pour titre du film
GROUP BY
    tArtist.idArtist, tArtist.primaryName,           -- Regroupement par artiste
    tFilm.idFilm, tFilm.primaryTitle                 -- ET par film (granularité fine)
HAVING
    COUNT(DISTINCT tJob.category) > 1                -- Filtre : au moins 2 rôles
ORDER BY
    NombreResponsabilites DESC,                      -- Tri : les plus polyvalents d'abord
    tArtist.primaryName;                             -- Puis alphabétique
```

**Explication:**

Cette requête est la **plus complexe** de la série. Elle trouve les cas où un artiste cumule plusieurs rôles **dans un même film** (ex: acteur ET réalisateur dans "The Batman") :

**1. Doubles jointures :**
   - `INNER JOIN tArtist` : Pour récupérer le nom de l'artiste
   - `INNER JOIN tFilm` : Pour récupérer le titre du film
   - Ces jointures permettent d'afficher des informations lisibles

**2. GROUP BY sur DEUX dimensions (artiste, film) :**
   - `GROUP BY idArtist, primaryName, idFilm, primaryTitle`
   - Chaque groupe représente **une combinaison unique (artiste × film)**
   - Granularité plus fine que l'exercice 6 qui groupait seulement par artiste
   - Permet de détecter les cumuls de rôles **projet par projet**

**3. COUNT(DISTINCT category) :**
   - Compte le nombre de catégories différentes pour chaque couple (artiste, film)
   - Exemples de combinaisons trouvées :
     - Clint Eastwood : acted in + directed dans "Unforgiven"
     - Ben Affleck : acted in + directed + produced dans "Argo"
     - Charlie Chaplin : acted in + directed + composed dans "Modern Times"

**4. HAVING COUNT(DISTINCT category) > 1 :**
   - Filtre les groupes (artiste × film) ayant au moins 2 responsabilités
   - Exclut les cas normaux où une personne n'a qu'un seul rôle

**5. ORDER BY :**
   - Premier critère : `NombreResponsabilites DESC` (les multi-talents d'abord)
   - Second critère : `primaryName` (ordre alphabétique pour faciliter la lecture)

**Concepts SQL utilisés :**
- **Jointures multiples** : 2 INNER JOIN pour enrichir les données
- **GROUP BY composite** : Regroupement sur plusieurs colonnes (artiste ET film)
- **Granularité du regroupement** : Niveau de détail plus fin que les exercices précédents
- **HAVING** : Filtrage après agrégation

**Différence avec l'exercice 6 :**
- Question : Ex6 = Plusieurs responsabilités dans sa carrière / Ex8 = Plusieurs responsabilités dans un même film
- GROUP BY : Ex6 = (idArtist) / Ex8 = (idArtist, idFilm)
- Résultat : Ex6 = 1 ligne par artiste polyvalent / Ex8 = 1 ligne par (artiste × film)
- Exemple : Ex6 = Ben Affleck : 3 responsabilités / Ex8 = Ben Affleck + Argo : 3 responsabilités

**Visualisation du regroupement :**
Données dans tJob : Ben Affleck a "acted in", "directed", "produced" dans Argo (3 catégories) et "acted in", "directed" dans The Town (2 catégories). Après GROUP BY (idArtist, idFilm), on obtient : Ben Affleck + Argo = 3 responsabilités (retourné) et Ben Affleck + The Town = 2 responsabilités (retourné).

**Exemple de résultat attendu :**
- nm0000123, Clint Eastwood, tt0000456, Unforgiven : 3 responsabilités (acted in, directed, produced)
- nm0000789, Ben Affleck, tt0000123, Argo : 3 responsabilités (acted in, directed, produced)
- nm0001234, Charlie Chaplin, tt0000999, City Lights : 4 responsabilités (acted in, directed, composed)

Cette requête révèle les **véritables auteurs complets** du cinéma qui maîtrisent plusieurs aspects de la création cinématographique dans leurs projets.


