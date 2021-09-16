--  list the titles of the five highest rated movies (in order) that Chadwick Boseman starred in
SELECT title FROM movies
JOIN stars
    ON stars.movie_id = movies.id
JOIN people 
    ON people.id = stars.person_id
JOIN ratings
    ON movies.id = ratings.movie_id
WHERE name = "Chadwick Boseman"
ORDER BY rating DESC
LIMIT 5;