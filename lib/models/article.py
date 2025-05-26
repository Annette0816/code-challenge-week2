from lib.db.connection import CURSOR, CONN

class Article:
    all = {}

    def __init__(self, title, author, magazine, id=None):
        self.id = id
        self.title = title
        self.author = author
        self.magazine = magazine

    def __repr__(self):
        return f"<Article {self.id}: {self.title}>"

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if isinstance(value, str) and len(value):
            self._title = value
        else:
            raise ValueError("Title must be a non-empty string.")

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author_id INTEGER,
                magazine_id INTEGER,
                FOREIGN KEY (author_id) REFERENCES authors(id),
                FOREIGN KEY (magazine_id) REFERENCES magazines(id)
            );
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS articles")
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO articles (title, author_id, magazine_id)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.title, self.author.id, self.magazine.id))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, title, author, magazine):
        article = cls(title, author, magazine)
        article.save()
        return article

    @classmethod
    def find_by_id(cls, id):
        row = CURSOR.execute("SELECT * FROM articles WHERE id = ?", (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_title(cls, title):
        row = CURSOR.execute("SELECT * FROM articles WHERE title = ?", (title,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def instance_from_db(cls, row):
        from lib.models.author import Author
        from lib.models.magazine import Magazine
        author = Author.find_by_id(row["author_id"])
        magazine = Magazine.find_by_id(row["magazine_id"])
        return cls(row["title"], author, magazine, row["id"])
