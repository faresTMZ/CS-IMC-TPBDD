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

### Exercice 1 (¼ pt): Année de naissance de Brad Pitt

**Requête SQL:**
```sql
-- A COMPLETER
```

**Explication:**


---

### Exercice 2 (¼ pt): Nombre d'artistes dans la base

**Requête SQL:**
```sql
-- A COMPLETER
```

**Explication:**


---

### Exercice 3 (¼ pt): Artistes nés en 1960

**Requête SQL:**
```sql
-- A COMPLETER
```

**Explication:**


---

### Exercice 4 (1 pt): Année de naissance la plus représentée

**Requête SQL:**
```sql
-- A COMPLETER
```

**Explication:**


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


