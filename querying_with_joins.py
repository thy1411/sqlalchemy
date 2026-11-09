from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

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

# 6. Thêm dữ liệu mẫu
jack = User(
    name="jack",
    fullname="Jack Bean",
    nickname="gjffdd"
)

jack.addresses = [
    Address(email_address="jack@google.com"),
    Address(email_address="j25@yahoo.com")
]

session.add(jack)
session.commit()

# 7. Implicit Join bằng filter()
print("\n--- IMPLICIT JOIN ---")

for user, address in (
    session.query(User, Address)
    .filter(User.id == Address.user_id)
    .filter(Address.email_address == "jack@google.com")
    .all()
):
    print(user)
    print(address)

# 8. Sử dụng Query.join()
print("\n--- QUERY JOIN ---")

users = (
    session.query(User)
    .join(Address)
    .filter(Address.email_address == "jack@google.com")
    .all()
)

for user in users:
    print(user)

# 9. Join với điều kiện ON tường minh
print("\n--- JOIN WITH EXPLICIT CONDITION ---")

users = (
    session.query(User)
    .join(Address, User.id == Address.user_id)
    .filter(Address.email_address == "j25@yahoo.com")
    .all()
)

for user in users:
    print(user)

# 10. Join thông qua relationship
print("\n--- JOIN THROUGH RELATIONSHIP ---")

users = (
    session.query(User)
    .join(User.addresses)
    .filter(Address.email_address == "jack@google.com")
    .all()
)

for user in users:
    print(user)

# 11. Join với target và relationship
print("\n--- JOIN WITH TARGET AND RELATIONSHIP ---")

users = (
    session.query(User)
    .join(Address, User.addresses)
    .filter(Address.email_address == "j25@yahoo.com")
    .all()
)

for user in users:
    print(user)

# 12. Outer Join
print("\n--- OUTER JOIN ---")

results = (
    session.query(User, Address)
    .outerjoin(User.addresses)
    .all()
)

for user, address in results:
    print(user, address)

# 13. select_from()
print("\n--- SELECT FROM ADDRESS ---")

results = (
    session.query(User, Address)
    .select_from(Address)
    .join(User)
    .all()
)

for user, address in results:
    print(user, address)

# 14. Đóng Session
session.close()