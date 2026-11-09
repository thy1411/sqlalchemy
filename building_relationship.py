from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship

# 1. Kết nối database SQLite trong bộ nhớ
engine = create_engine("sqlite:///:memory:", echo=True)

# 2. Khai báo Base
Base = declarative_base()

# 3. Khai báo bảng users
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

# 4. Khai báo bảng addresses
class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)

    # Khóa ngoại liên kết với bảng users
    user_id = Column(Integer, ForeignKey("users.id"))

    # Quan hệ từ Address đến User
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address

# 5. Khai báo quan hệ từ User đến Address
User.addresses = relationship(
    "Address",
    order_by=Address.id,
    back_populates="user"
)

# 6. Tạo các bảng trong database
Base.metadata.create_all(engine)