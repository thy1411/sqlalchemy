from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# Create Engine
engine = create_engine("sqlite:///:memory:", echo=True)

# Create Base
Base = declarative_base()

# Declare Mapping
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name,
            self.fullname,
            self.nickname,
        )

# Create all tables
Base.metadata.create_all(engine)

# Create an instance of User
ed_user = User(
    name="ed",
    fullname="Ed Jones",
    nickname="edsnickname"
)

# Display the instance
print(ed_user)

# Display the id
print(ed_user.id)