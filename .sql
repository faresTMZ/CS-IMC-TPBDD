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
