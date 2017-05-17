SELECT "1) Вывести все года, где были фильмы, оцененные на 4, 5";

SELECT DISTINCT
	year
FROM Movie
INNER JOIN Rating
	ON (Movie.mID = Rating.mID)
WHERE
	stars=4 or stars=5;


SELECT "2) Вывести всех обзорщиков, которые не поставили даты";

SELECT DISTINCT
	name
FROM Reviewer
INNER JOIN Rating
	ON (Reviewer.rID = Rating.rID)
WHERE
	ratingDate is NULL;


SELECT "3) Вывести максимальный рейтинг фильма";

SELECT
	Movie.title,
	MAX(score) as max
FROM(
	SELECT
		mID as id,
		AVG(stars) as score
	FROM Rating
	GROUP BY
		mID
)
INNER JOIN Movie
	ON (mID=Movie.mID);

SELECT "Или же максимальная оценка для каждого?";


SELECT
	Movie.title as title,
	MAX(Rating.stars) as max
FROM Movie
INNER JOIN Rating
	ON (Movie.mID = Rating.mID)
GROUP BY Movie.mID;


SELECT "4) Вывести неоцененные фильмы";

SELECT
	Movie.title
FROM
	Movie
WHERE
	mID NOT IN (SELECT DISTINCT mID FROM Rating);


SELECT "5) Вывести обзорщиков на фильм GONE WITH THE WIND";

SELECT DISTINCT
	Reviewer.name
FROM Movie
INNER JOIN Rating
	ON (Movie.mID = Rating.mID)
INNER JOIN Reviewer
	ON (Rating.rID = Reviewer.rID)
WHERE
    UPPER(Movie.title) LIKE UPPER('GONE WITH THE WIND');


SELECT "6) Вывести разницу между мин. и макс. рейтингом фильма";

SELECT
	Movie.title as title,
	MAX(Rating.stars) - MIN(Rating.stars)  as diff
FROM Movie
INNER JOIN Rating
	ON (Movie.mID = Rating.mID)
GROUP BY Movie.mID;
