from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, selectinload

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return (
            f"<User(name={self.name!r}, "
            f"fullname={self.fullname!r}, "
            f"nickname={self.nickname!r})>"
        )

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"<Address(email_address={self.email_address!r})>"

engine = create_engine("sqlite:///:memory:", echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Create sample data
jack = User(
    name="jack",
    fullname="Jack Bean",
    nickname="gjffdd",
    addresses=[
        Address(email_address="jack@google.com"),
        Address(email_address="j25@yahoo.com"),
    ],
)

ed = User(
    name="ed",
    fullname="Ed Jones",
    nickname="eddie",
    addresses=[
        Address(email_address="ed@gmail.com"),
    ],
)

wendy = User(
    name="wendy",
    fullname="Wendy Williams",
    nickname="windy",
)

session.add_all([jack, ed, wendy])
session.commit()

# Selectin Load
jack = (
    session.query(User)
    .options(selectinload(User.addresses))
    .filter_by(name="jack")
    .one()
)

print("\n--- USER ---")
print(jack)

print("\n--- JACK ADDRESSES ---")
print(jack.addresses)

session.close()