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
    sessionmaker,
    aliased
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

# 6. Thêm dữ liệu
jack = User(
    name="jack",
    fullname="Jack Bean",
    nickname="gjffdd"
)

jack.addresses = [
    Address(email_address="jack@google.com"),
    Address(email_address="j25@yahoo.com"),
    Address(email_address="jack@hotmail.com")
]

wendy = User(
    name="wendy",
    fullname="Wendy Williams",
    nickname="windy"
)

wendy.addresses = [
    Address(email_address="wendy@gmail.com")
]

session.add_all([jack, wendy])
session.commit()

# 7. Tạo alias cho Address
adalias1 = aliased(Address)
adalias2 = aliased(Address)

# 8. Truy vấn User có cả hai địa chỉ email
print("\n--- QUERY USING TWO ALIASES ---")

query = (
    session.query(User)
    .join(adalias1, User.addresses)
    .filter(adalias1.email_address == "jack@google.com")
    .join(adalias2, User.addresses)
    .filter(adalias2.email_address == "j25@yahoo.com")
)

for user in query.all():
    print(user)

# 9. Hiển thị câu truy vấn SQL
print("\n--- GENERATED SQL ---")
print(query)

# 10. Đóng Session
session.close()