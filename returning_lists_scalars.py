from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# 1. Tạo Engine
engine = create_engine("sqlite:///:memory:", echo=True)

# 2. Khai báo Base
Base = declarative_base()

# 3. Khai báo class User
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

# 4. Tạo bảng
Base.metadata.create_all(engine)

# 5. Tạo Session
Session = sessionmaker(bind=engine)
session = Session()

# 6. Thêm dữ liệu
session.add_all(
    [
        User(name="ed", fullname="Ed Jones", nickname="eddie"),
        User(name="wendy", fullname="Wendy Williams", nickname="windy"),
        User(name="mary", fullname="Mary Contrary", nickname="mary"),
        User(name="fred", fullname="Fred Flintstone", nickname="freddy"),
    ]
)

session.commit()

# 7. Sử dụng all()
print("\n1. ALL()")

users = session.query(User).order_by(User.id).all()

print(users)

print("Kiểu dữ liệu:", type(users))

# 8. Sử dụng first()
print("\n2. FIRST()")

user = (
    session.query(User)
    .filter(User.name == "ed")
    .first()
)

print(user)

# 9. first() khi không tìm thấy
print("\n3. FIRST() KHÔNG CÓ KẾT QUẢ")

user = (
    session.query(User)
    .filter(User.name == "unknown")
    .first()
)

print(user)

# 10. Sử dụng one()
print("\n4. ONE()")

user = (
    session.query(User)
    .filter(User.name == "ed")
    .one()
)

print(user)

# 11. one() khi không có kết quả
print("\n5. ONE() KHÔNG CÓ KẾT QUẢ")

try:
    user = (
        session.query(User)
        .filter(User.name == "unknown")
        .one()
    )
except NoResultFound as error:
    print(type(error).__name__)
    print(error)

# 12. one() khi có nhiều kết quả
print("\n6. ONE() CÓ NHIỀU KẾT QUẢ")

try:
    user = (
        session.query(User)
        .filter(User.name.like("%e%"))
        .one()
    )
except MultipleResultsFound as error:
    print(type(error).__name__)
    print(error)

# 13. Sử dụng one_or_none()
print("\n7. ONE_OR_NONE()")

user = (
    session.query(User)
    .filter(User.name == "ed")
    .one_or_none()
)

print(user)

# 14. one_or_none() khi không có kết quả
print("\n8. ONE_OR_NONE() KHÔNG CÓ KẾT QUẢ")

user = (
    session.query(User)
    .filter(User.name == "unknown")
    .one_or_none()
)

print(user)

# 15. one_or_none() khi có nhiều kết quả
print("\n9. ONE_OR_NONE() CÓ NHIỀU KẾT QUẢ")

try:
    user = (
        session.query(User)
        .filter(User.name.like("%e%"))
        .one_or_none()
    )
except MultipleResultsFound as error:
    print(type(error).__name__)
    print(error)

# 16. Sử dụng scalar()
print("\n10. SCALAR()")

user_id = (
    session.query(User.id)
    .filter(User.name == "ed")
    .order_by(User.id)
    .scalar()
)

print("User ID:", user_id)

# 17. Đóng Session
session.close()