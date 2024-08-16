from app.DB import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
class Author(db.Model):
    """
    Author model.

    Attributes:
        id (int): The primary key for the author.
        name (str): The name of the author.
        bio (str): A brief biography of the author.
        books (relationship): A relationship to the books authored by this author.
    """

    __tablename__ = "Author"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    books = db.relationship('Book', backref='author', lazy=True)

    def __init__(self, name, bio):
        """
        Initializes an Author instance.

        Args:
            name (str): The name of the author.
            bio (str): A brief biography of the author.
        """
        self.name = name
        self.bio = bio

    def to_dict(self):
        """
        Converts the Author instance to a dictionary.

        Returns:
            dict: A dictionary representation of the Author instance.
        """
        return {
            'ID': self.id,
            'Name': self.name,
            'Bio': self.bio
        }


class Book(db.Model):
    """
    Book Model.

    Attributes:
        id (int): The primary key for the book.
        title (str): The title of the book.
        published_date (date): The date the book was published.
        isbn (str): The ISBN of the book.
        borrow_records (relationship): A relationship to the borrow records of this book.
        author_id (int): The ID of the author who wrote the book.
    """

    __tablename__ = "Book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    published_date = db.Column(db.Date)
    isbn = db.Column(db.String(255), unique=True, nullable=False)
    borrow_records = db.relationship('BorrowRecord', backref='book', lazy=True)
    author_id = db.Column(db.Integer, db.ForeignKey('Author.id'), nullable=False)

    def __init__(self, title, published_date, isbn, author_id):
        """
        Initializes a Book instance.

        Args:
            title (str): The title of the book.
            published_date (date): The date the book was published.
            isbn (str): The ISBN of the book.
            author_id (int): The ID of the author who wrote the book.
        """
        self.title = title
        self.published_date = published_date
        self.isbn = isbn
        self.author_id = author_id

    def to_dict(self):
        """
        Converts the Book instance to a dictionary.

        Returns:
            dict: A dictionary representation of the Book instance.
        """
        return {
            'ID': self.id,
            'Title': self.title,
            'Published Date': self.published_date.isoformat() if self.published_date else None,
            'ISBN': self.isbn,
            'Author ID': self.author_id
        }


class BorrowRecord(db.Model):
    """
    Borrow_Record Model.

    Attributes:
        id (int): The primary key for the borrow record.
        borrow_date (date): The date the book was borrowed.
        return_date (date): The date the book was returned.
        book_id (int): The ID of the borrowed book.
        user_id (int): The ID of the user who borrowed the book.
    """

    __tablename__ = "BorrowRecord"
    id = db.Column(db.Integer, primary_key=True)
    borrow_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.Date)
    book_id = db.Column(db.Integer, db.ForeignKey('Book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __init__(self, borrow_date, book_id, user_id, return_date=None):
        """
        Initializes a BorrowRecord instance.

        Args:
            borrow_date (datetime): The date when the book was borrowed.
            book_id (int): The ID of the book being borrowed.
            user_id (int): The ID of the user borrowing the book.
            return_date (datetime, optional): The date when the book was returned. Defaults to None.
        """
        self.borrow_date = borrow_date
        self.book_id = book_id
        self.user_id = user_id
        self.return_date = return_date

    def to_dict(self):
        """
        Converts the BorrowRecord instance to a dictionary.

        Returns:
            dict: A dictionary representation of the BorrowRecord instance.
        """
        return {
            'ID': self.id,
            'Borrow Date': self.borrow_date.isoformat() if self.borrow_date else None,
            'Return Date': self.return_date.isoformat() if self.return_date else None,
            'Book ID': self.book_id,
            'User ID': self.user_id
        }



class User(db.Model):
    """
    User Model.

    Attributes:
        id (int): The primary key for the user.
        username (str): The username of the user.
        password (str): The hashed password of the user.
        role (str): The role of the user (e.g., admin, user).
        token (str): An authentication token for the user.
        request_count (int): The number of requests made by the user.
        last_request_time (datetime): The time of the last request made by the user.
        borrow_records (relationship): A relationship to the borrow records of this user.
    """

    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    token = db.Column(db.String(200), unique=True, nullable=True)
    request_count = db.Column(db.Integer, default=0)
    last_request_time = db.Column(db.DateTime, default=datetime.utcnow)
    borrow_records = db.relationship('BorrowRecord', backref='user', lazy='dynamic')

    def __init__(self, username, password, role='user', token=None, request_count=0, last_request_time=None):
        """
        Initializes a User instance.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            role (str): The role of the user (e.g., admin, user). Defaults to 'user'.
            token (str, optional): An authentication token for the user. Defaults to None.
            request_count (int, optional): The number of requests made by the user. Defaults to 0.
            last_request_time (datetime, optional): The time of the last request made by the user. Defaults to None.
        """
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role
        self.token = token
        self.request_count = request_count
        self.last_request_time = last_request_time

    def set_password(self, password):
        """
        Sets the user's password after hashing it.

        Args:
            password (str): The plain-text password.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks if the provided password matches the stored hashed password.

        Args:
            password (str): The plain-text password.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password, password)

    @staticmethod
    def generate_token():
        """
        Generates a UUID token.

        Returns:
            str: The generated UUID token.
        """
        return str(uuid.uuid4())

    def to_dict(self):
        """
        Converts the User instance to a dictionary.

        Returns:
            dict: A dictionary representation of the User instance.
        """
        return {
            'ID': self.id,
            'Username': self.username,
            'Role': self.role,
            'Token': self.token,
            'Request Count': self.request_count,
            'Last Request Time': self.last_request_time.isoformat() if self.last_request_time else None
        }
