from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    addresses = relationship(
        "Address",
        back_populates="user",
        cascade="all, delete, delete-orphan"
    )

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

# Create Jack and his addresses
jack = User(
    name="jack",
    fullname="Jack Bean",
    nickname="gjffdd",
    addresses=[
        Address(email_address="jack@google.com"),
        Address(email_address="j25@yahoo.com"),
    ],
)

session.add(jack)
session.commit()

# Load Jack
jack = session.query(User).filter_by(name="jack").one()

print("\n--- INITIAL ADDRESSES ---")
print(jack.addresses)

# Remove one Address from Jack's collection
del jack.addresses[1]

print("\n--- AFTER REMOVING ONE ADDRESS ---")

remaining_count = session.query(Address).filter(
    Address.email_address.in_(
        ["jack@google.com", "j25@yahoo.com"]
    )
).count()

print("Remaining addresses:", remaining_count)

# Delete Jack
session.delete(jack)

print("\n--- AFTER DELETING JACK ---")

user_count = session.query(User).filter_by(name="jack").count()

address_count = session.query(Address).filter(
    Address.email_address.in_(
        ["jack@google.com", "j25@yahoo.com"]
    )
).count()

print("Remaining users:", user_count)
print("Remaining addresses:", address_count)

session.close()