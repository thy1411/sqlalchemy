from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    exists
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

jack = User(
    name="jack",
    fullname="Jack Bean",
    nickname="gjffdd"
)

jack.addresses = [
    Address(email_address="jack@google.com"),
    Address(email_address="j25@yahoo.com")
]

session.add_all([ed_user, wendy, jack])
session.commit()

# 7. Tạo biểu thức EXISTS
print("\n--- USERS HAVING ADDRESSES ---")

stmt = exists().where(Address.user_id == User.id)

for user in session.query(User).filter(stmt).all():
    print(user)

# 8. Tìm User không có Address
print("\n--- USERS WITHOUT ADDRESSES ---")

for user in session.query(User).filter(~stmt).all():
    print(user)

# 9. Kiểm tra User có địa chỉ email cụ thể
print("\n--- USERS WITH SPECIFIC EMAIL ---")

stmt_email = exists().where(
    (Address.user_id == User.id)
    & (Address.email_address == "jack@google.com")
)

for user in session.query(User).filter(stmt_email).all():
    print(user)

# 10. Sử dụng Query.exists()
print("\n--- QUERY EXISTS ---")

subquery = (
    session.query(Address)
    .filter(Address.user_id == User.id)
)

for user in session.query(User).filter(subquery.exists()).all():
    print(user)

# 11. Đóng Session
session.close()