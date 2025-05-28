from lib.db.connection import CURSOR, CONN

class Magazine:
    all = {}

    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f"<Magazine {self.id}: {self.name}, {self.category}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value):
            self._name = value
        else:
            raise ValueError("Name must be a non-empty string.")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value):
            self._category = value
        else:
            raise ValueError("Category must be a non-empty string.")

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL
            );
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS magazines")
        CONN.commit()

    def save(self):
        sql = "INSERT INTO magazines (name, category) VALUES (?, ?)"
        CURSOR.execute(sql, (self.name, self.category))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, category):
        magazine = cls(name, category)
        magazine.save()
        return magazine

    @classmethod
    def find_by_id(cls, id):
        row = CURSOR.execute("SELECT * FROM magazines WHERE id = ?", (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        row = CURSOR.execute("SELECT * FROM magazines WHERE name = ?", (name,)).fetchone()
        return cls.instance_from_db(row) if row else None


    

    @classmethod
    def instance_from_db(cls, row):
        return cls(row["name"], row["category"], row["id"])

    def articles(self):
        from lib.models.article import Article
        sql = "SELECT * FROM articles WHERE magazine_id = ?"
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Article.instance_from_db(row) for row in rows]

    def contributors(self):
        from lib.models.author import Author
        sql = """
            SELECT DISTINCT authors.*
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Author.instance_from_db(row) for row in rows]
   

    def article_titles(self):
        from lib.models.article import Article
        
        sql = """
            SELECT title
            FROM articles
            WHERE magazine_id = ?
        """
        
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Article.instance_from_db(row) for row in rows]
   
    

    def contributing_authors(self):
        from lib.models.author import Author
        
        sql = """
           SELECT au.*, COUNT(a.id) as article_count
            FROM authors au
            JOIN articles a ON au.id = a.author_id
            WHERE a.magazine_id = ?
            GROUP BY au.id
            HAVING article_count > 2
        """
        
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Author.instance_from_db(row) for row in rows]