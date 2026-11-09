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

# Display Table object
print(User.__table__)

# Create all tables
Base.metadata.create_all(engine)