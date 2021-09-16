-- list the names of all people who starred in a movie in which Kevin Bacon also starred
WITH kevin_bacon_movies AS
(
    SELECT movie_id from stars
    JOIN people 
        ON people.id = stars.person_id
    WHERE name = "Kevin Bacon" AND birth = '1958'
)

SELECT (name) FROM people
WHERE id IN (SELECT person_id FROM stars WHERE movie_id IN kevin_bacon_movies) 
AND name <> "Kevin Bacon";