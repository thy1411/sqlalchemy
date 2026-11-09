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

# 4. Khai báo quan hệ One-to-Many
User.addresses = relationship(
    "Address",
    order_by=Address.id,
    back_populates="user"
)

# 5. Tạo bảng
Base.metadata.create_all(engine)

# 6. Tạo Session
Session = sessionmaker(bind=engine)
session = Session()

# 7. Tạo User
jack = User(
    name="jack",
    fullname="Jack Bean",
    nickname="gjffdd"
)

# Kiểm tra danh sách địa chỉ ban đầu
print("\nDanh sach addresses ban dau:")
print(jack.addresses)

# 8. Thêm Address vào User
jack.addresses = [
    Address(email_address="jack@google.com"),
    Address(email_address="j25@yahoo.com")
]

print("\nDanh sach addresses sau khi them:")
print(jack.addresses)

# 9. Truy cập Address từ User
print("\nDia chi email thu hai:")
print(jack.addresses[1])

# 10. Truy cập ngược từ Address về User
print("\nUser cua dia chi email thu hai:")
print(jack.addresses[1].user)

# 11. Thêm User vào Session
session.add(jack)

# Kiểm tra các đối tượng trong Session
print("\nKiem tra Session:")
print("jack in session:", jack in session)
print("address 1 in session:", jack.addresses[0] in session)
print("address 2 in session:", jack.addresses[1] in session)

# 12. Lưu dữ liệu vào database
session.commit()

# 13. Truy vấn User bằng Query
jack = session.query(User).filter_by(name="jack").one()

print("\nUser sau khi truy van:")
print(jack)

# 14. Truy cập danh sách Address từ database
print("\nDanh sach addresses tu database:")
print(jack.addresses)

# 15. Đóng Session
session.close()