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
SELECT birthYear
FROM tArtist
WHERE primaryName = 'Jude Law';
```

**Explication:**

Simple SELECT avec WHERE pour filtrer un artiste spécifique et retourner uniquement son année de naissance.

---

### Exercice 2 (¼ pt): Nombre d'artistes dans la base

**Requête SQL:**

```sql
SELECT COUNT(*) AS NombreArtistes
FROM tArtist;
```

**Explication:**

Utilise COUNT(*) pour compter le nombre total de lignes dans la table tArtist.

---

### Exercice 3 (¼ pt): Artistes nés en 1960

**Requête SQL:**

```sql
-- Partie 1 : Liste des noms
SELECT primaryName
FROM tArtist
WHERE birthYear = 1960;

-- Partie 2 : Nombre total
SELECT COUNT(*) AS NombreArtistesNes1960
FROM tArtist
WHERE birthYear = 1960;
```

**Explication:**

Deux requêtes simples : la première liste les noms avec WHERE, la seconde compte avec COUNT(*).

---

### Exercice 4 (1 pt): Année de naissance la plus représentée

**Requête SQL:**

```sql
SELECT TOP 1
    birthYear,
    COUNT(DISTINCT tArtist.idArtist) AS NombreActeurs
FROM tArtist
INNER JOIN tJob ON tArtist.idArtist = tJob.idArtist
WHERE tJob.category = 'acted in'
    AND birthYear != 0
    AND birthYear IS NOT NULL
GROUP BY birthYear
ORDER BY NombreActeurs DESC;
```

**Explication:**

JOIN entre tArtist et tJob, filtrage des acteurs uniquement, regroupement par année de naissance, comptage des acteurs distincts par année, tri décroissant et TOP 1 pour obtenir l'année la plus représentée.

---

### Exercice 5 (½ pt): Artistes ayant joué dans plus d'un film

**Requête SQL:**

```sql
SELECT
    tArtist.idArtist,
    tArtist.primaryName,
    COUNT(DISTINCT tJob.idFilm) AS NombreFilms
FROM tArtist
INNER JOIN tJob ON tArtist.idArtist = tJob.idArtist
WHERE tJob.category = 'acted in'
GROUP BY tArtist.idArtist, tArtist.primaryName
HAVING COUNT(DISTINCT tJob.idFilm) > 1
ORDER BY NombreFilms DESC;
```

**Explication:**

JOIN entre artistes et rôles, filtrage sur category='acted in', regroupement par artiste, comptage des films distincts, clause HAVING pour ne garder que ceux avec plus d'un film.

---

### Exercice 6 (½ pt): Artistes avec plusieurs responsabilités

**Requête SQL:**

```sql
SELECT
    tArtist.idArtist,
    tArtist.primaryName,
    COUNT(DISTINCT tJob.category) AS NombreResponsabilites
FROM tArtist
INNER JOIN tJob ON tArtist.idArtist = tJob.idArtist
GROUP BY tArtist.idArtist, tArtist.primaryName
HAVING COUNT(DISTINCT tJob.category) > 1
ORDER BY NombreResponsabilites DESC;
```

**Explication:**

Similaire à l'exercice 5, mais compte les catégories distinctes (acted in, directed, produced, etc.) au lieu des films. Pas de WHERE donc considère tous les rôles. HAVING filtre les artistes ayant au moins 2 types de responsabilités.

---

### Exercice 7 (¾ pt): Film(s) avec le plus d'acteurs

**Requête SQL:**

```sql
SELECT TOP 1 WITH TIES
    tFilm.idFilm,
    tFilm.primaryTitle,
    COUNT(DISTINCT tJob.idArtist) AS NombreActeurs
FROM tFilm
INNER JOIN tJob ON tFilm.idFilm = tJob.idFilm
WHERE tJob.category = 'acted in'
GROUP BY tFilm.idFilm, tFilm.primaryTitle
ORDER BY NombreActeurs DESC;
```

**Explication:**

JOIN entre films et rôles, filtrage des acteurs uniquement (category='acted in'), regroupement par film, comptage des acteurs distincts par film. TOP 1 WITH TIES retourne le film avec le plus d'acteurs, ainsi que tous les ex-aequo si plusieurs films ont le même maximum.

---

### Exercice 8 (1 pt): Artistes avec plusieurs responsabilités dans un même film

**Requête SQL:**

```sql
SELECT
    tArtist.idArtist,
    tArtist.primaryName,
    tFilm.idFilm,
    tFilm.primaryTitle,
    COUNT(DISTINCT tJob.category) AS NombreResponsabilites
FROM tJob
INNER JOIN tArtist ON tJob.idArtist = tArtist.idArtist
INNER JOIN tFilm ON tJob.idFilm = tFilm.idFilm
GROUP BY tArtist.idArtist, tArtist.primaryName, tFilm.idFilm, tFilm.primaryTitle
HAVING COUNT(DISTINCT tJob.category) > 1
ORDER BY NombreResponsabilites DESC, tArtist.primaryName;
```

**Explication:**

Similaire à l'exercice 6 mais avec GROUP BY sur (artiste, film) au lieu de juste (artiste). Cela permet de détecter les cas où un artiste a plusieurs rôles dans UN MÊME film (ex: Ben Affleck acteur+réalisateur dans Argo). Double JOIN pour récupérer les noms lisibles.
