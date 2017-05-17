
`wget https://gist.github.com/alexopryshko/6ed67f6f9df30a678dc955d23801881a -O rating.sql`

`./mysql2sqlite.sh rating.sql | sqlite3 rating.db`

`sqlite3 rating.db`

`sqlite> .read homework.sql`
