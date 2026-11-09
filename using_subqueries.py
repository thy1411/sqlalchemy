from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

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

# 6. Thêm dữ liệu User
ed_user = User(
    name="ed",
    fullname="Ed Jones",
    nickname="eddie"
)

wendy = User(
    name="wendy",
    fullname="Wendy Williams",
    nickname="windy"
)

mary = User(
    name="mary",
    fullname="Mary Contrary",
    nickname="mary"
)

fred = User(
    name="fred",
    fullname="Fred Flintstone",
    nickname="freddy"
)

jack = User(
    name="jack",
    fullname="Jack Bean",
    nickname="gjffdd"
)

# Thêm hai địa chỉ cho Jack
jack.addresses = [
    Address(email_address="jack@google.com"),
    Address(email_address="j25@yahoo.com")
]

session.add_all([
    ed_user,
    wendy,
    mary,
    fred,
    jack
])

session.commit()

# 7. Tạo Subquery đếm số Address của từng User
stmt = (
    session.query(
        Address.user_id,
        func.count("*").label("address_count")
    )
    .group_by(Address.user_id)
    .subquery()
)

# 8. Truy vấn User và số lượng Address
print("\n--- USERS AND ADDRESS COUNTS ---")

for user, count in (
    session.query(User, stmt.c.address_count)
    .outerjoin(stmt, User.id == stmt.c.user_id)
    .order_by(User.id)
):
    print(user, count)

# 9. Hiển thị câu truy vấn SQL
print("\n--- GENERATED SQL ---")

query = (
    session.query(User, stmt.c.address_count)
    .outerjoin(stmt, User.id == stmt.c.user_id)
    .order_by(User.id)
)

print(query)

# 10. Đóng Session
session.close()