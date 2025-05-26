from lib.db.connection import CURSOR, CONN

class Author:
    all = {}

    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Author {self.id}: {self.name}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value):
            self._name = value
        else:
            raise ValueError("Name must be a non-empty string.")

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS authors")
        CONN.commit()

    def save(self):
        sql = "INSERT INTO authors (name) VALUES (?)"
        CURSOR.execute(sql, (self.name,))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name):
        author = cls(name)
        author.save()
        return author

    @classmethod
    def find_by_id(cls, id):
        row = CURSOR.execute("SELECT * FROM authors WHERE id = ?", (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        row = CURSOR.execute("SELECT * FROM authors WHERE name = ?", (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def instance_from_db(cls, row):
        return cls(row["name"], row["id"])

    def articles(self):
        from lib.models.article import Article
        rows = CURSOR.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,)).fetchall()
        return [Article.instance_from_db(row) for row in rows]

    def magazines(self):
        from lib.models.magazine import Magazine
        sql = """
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            WHERE a.author_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Magazine.instance_from_db(row) for row in rows]

    def add_article(self, magazine, title):
        from lib.models.article import Article
        return Article.create(title, self, magazine)

    def topic_areas(self):
        sql = """
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [row["category"] for row in rows]
