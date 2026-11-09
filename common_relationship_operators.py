from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    sessionmaker
)

# 1. Kết nối database
engine = create_engine("sqlite:///:memory:", echo=True)

Base = declarative_base()

# 2. Khai báo bảng users
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
            self.nickname
        )

# 3. Khai báo bảng addresses
class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address

User.addresses = relationship(
    "Address",
    order_by=Address.id,
    back_populates="user"
)

# 4. Tạo bảng
Base.metadata.create_all(engine)

# 5. Tạo Session
Session = sessionmaker(bind=engine)
session = Session()

# 6. Tạo dữ liệu mẫu
jack = User(
    name="jack",
    fullname="Jack Bean",
    nickname="gjffdd"
)

ed = User(
    name="ed",
    fullname="Ed Jones",
    nickname="eddie"
)

wendy = User(
    name="wendy",
    fullname="Wendy Williams",
    nickname="windy"
)

jack_address1 = Address(
    email_address="jack@google.com"
)

jack_address2 = Address(
    email_address="j25@yahoo.com"
)

ed_address = Address(
    email_address="ed@gmail.com"
)

# Gán địa chỉ cho User
jack.addresses = [
    jack_address1,
    jack_address2
]

ed.addresses = [
    ed_address
]

# Tạo Address chưa thuộc User nào
orphan_address = Address(
    email_address="orphan@example.com"
)

session.add_all([
    jack,
    ed,
    wendy,
    orphan_address
])

session.commit()

# 7. Comparator.__eq__()
print("\n--- RELATIONSHIP EQUALS ---")

results = session.query(Address).filter(
    Address.user == jack
).all()

for address in results:
    print(address)

# 8. Comparator.__ne__()
print("\n--- RELATIONSHIP NOT EQUALS ---")

results = session.query(Address).filter(
    Address.user != jack
).all()

for address in results:
    print(address)

# 9. IS NULL
print("\n--- RELATIONSHIP IS NULL ---")

results = session.query(Address).filter(
    Address.user == None
).all()

for address in results:
    print(address)

# 10. Comparator.contains()
print("\n--- CONTAINS ---")

results = session.query(User).filter(
    User.addresses.contains(jack_address1)
).all()

for user in results:
    print(user)

# 11. Comparator.any() với điều kiện
print("\n--- ANY WITH CRITERION ---")

results = session.query(User).filter(
    User.addresses.any(
        Address.email_address == "jack@google.com"
    )
).all()

for user in results:
    print(user)

# 12. Comparator.any() với keyword argument
print("\n--- ANY WITH KEYWORD ARGUMENT ---")

results = session.query(User).filter(
    User.addresses.any(email_address="jack@google.com")
).all()

for user in results:
    print(user)

# 13. Comparator.has()
print("\n--- HAS ---")

results = session.query(Address).filter(
    Address.user.has(name="ed")
).all()

for address in results:
    print(address)

# 14. Query.with_parent()
print("\n--- WITH_PARENT ---")

results = session.query(Address).with_parent(
    jack,
    User.addresses
).all()

for address in results:
    print(address)

# 15. Đóng Session
session.close()