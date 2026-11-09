from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

# Association table
post_keywords = Table(
    "post_keywords",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("keyword_id", ForeignKey("keywords.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    posts = relationship("BlogPost", back_populates="author")

    def __repr__(self):
        return "User(%r)" % self.name

class BlogPost(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    headline = Column(String(255), nullable=False)
    body = Column(Text)

    # Many to many BlogPost <-> Keyword
    keywords = relationship(
        "Keyword",
        secondary=post_keywords,
        back_populates="posts",
    )

    # Many to one BlogPost -> User
    author = relationship("User", back_populates="posts")

    def __init__(self, headline, body, author):
        self.author = author
        self.headline = headline
        self.body = body

    def __repr__(self):
        return "BlogPost(%r, %r, %r)" % (
            self.headline,
            self.body,
            self.author,
        )

class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False, unique=True)

    posts = relationship(
        "BlogPost",
        secondary=post_keywords,
        back_populates="keywords",
    )

    def __init__(self, keyword):
        self.keyword = keyword

    def __repr__(self):
        return "Keyword(%r)" % self.keyword

# Database
engine = create_engine("sqlite:///:memory:", echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Create users
jack = User(name="jack")
ed = User(name="ed")

session.add_all([jack, ed])
session.commit()

# Create keywords
py = Keyword("Python")
sql = Keyword("SQL")
orm = Keyword("ORM")

session.add_all([py, sql, orm])
session.commit()

# Create blog posts
post1 = BlogPost(
    "Learning Python",
    "Python is a programming language.",
    jack,
)

post2 = BlogPost(
    "Learning SQLAlchemy",
    "SQLAlchemy is a Python SQL toolkit and ORM.",
    jack,
)

post3 = BlogPost(
    "Database Basics",
    "Introduction to relational databases.",
    ed,
)

# Associate keywords with posts
post1.keywords.append(py)
post1.keywords.append(sql)

post2.keywords.append(py)
post2.keywords.append(orm)
post2.keywords.append(sql)

post3.keywords.append(sql)

session.add_all([post1, post2, post3])
session.commit()

# Query all blog posts
print("\n--- ALL BLOG POSTS ---")

for post in session.query(BlogPost).all():
    print("\nPost:", post.headline)
    print("Author:", post.author.name)
    print("Keywords:", post.keywords)

# Query posts containing Python keyword
print("\n--- POSTS WITH PYTHON KEYWORD ---")

python_keyword = (
    session.query(Keyword)
    .filter_by(keyword="Python")
    .one()
)

for post in python_keyword.posts:
    print(post.headline)

# Query keywords used by Learning SQLAlchemy
print("\n--- KEYWORDS OF LEARNING SQLALCHEMY ---")

post = (
    session.query(BlogPost)
    .filter_by(headline="Learning SQLAlchemy")
    .one()
)

for keyword in post.keywords:
    print(keyword.keyword)

session.close()