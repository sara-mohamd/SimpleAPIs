from app.DB import db

class Author(db.Model):
    """
    Author model
    """

    __tablename__ = "Author"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    books = db.relationship('Book', backref='author', lazy=True)

    def __init__(self, name, bio):
        self.name = name
        self.bio = bio

    def to_dict(self):
        return {
            'ID':self.id,
            'Name':self.name,
            "Bio":self.bio
        }


class Book(db.Model):
    """
    Book Model
    """

    __tablename__ = "Book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    published_date = db.Column(db.Date)
    isbn = db.Column(db.String(255), unique=True, nullable=False)
    borrow_records = db.relationship('BorrowRecord', backref='book', lazy=True)
    author_id = db.Column(db.Integer, db.ForeignKey('Author.id'), nullable=True)

    def __init__(self, title, published_date, isbn, author_id):
        self.title = title
        self.published_date = published_date
        self.isbn = isbn
        self.author_id = author_id

    def to_dict(self):
        return {
            'ID': self.id,
            'Title': self.title,
            'Published Date': self.published_date,
            'ISBN': self.isbn,
            'Author ID': self.author_id
        }


class BorrowRecord(db.Model):
    """
    Borrow_Record Model
    """

    __tablename__ = "BorrowRecord"
    id = db.Column(db.Integer, primary_key=True)
    borrow_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    book_id = db.Column(db.Integer, db.ForeignKey('Book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

class User(db.Model):
    """
    user model
    """

    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    token = db.Column(db.String(255))
    request_count = db.Column(db.Integer, default=0)
    last_request_time = db.Column(db.DateTime)
    borrow_records = db.relationship('BorrowRecord', backref='user')