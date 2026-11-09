from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy import and_, or_
from sqlalchemy.orm import declarative_base, sessionmaker

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

# 7. Toán tử bằng ==
print("\n1. NAME BẰNG ed")

for user in session.query(User).filter(User.name == "ed"):
    print(user)

# 8. Toán tử khác !=
print("\n2. NAME KHÁC ed")

for user in session.query(User).filter(User.name != "ed"):
    print(user)

# 9. Tìm kiếm like()
print("\n3. TÌM KIẾM LIKE")

for user in session.query(User).filter(User.name.like("%e%")):
    print(user)

# 10. Tìm kiếm ilike()
print("\n4. TÌM KIẾM ILIKE")

for user in session.query(User).filter(User.name.ilike("%ED%")):
    print(user)

# 11. Lọc bằng in_()
print("\n5. LỌC BẰNG IN_")

for user in session.query(User).filter(
    User.name.in_(["ed", "wendy", "jack"])
):
    print(user)

# 12. Lọc phủ định bằng ~
print("\n6. LỌC KHÔNG NẰM TRONG DANH SÁCH")

for user in session.query(User).filter(
    ~User.name.in_(["ed", "wendy"])
):
    print(user)

# 13. Kiểm tra NULL
print("\n7. KIỂM TRA NAME IS NULL")

for user in session.query(User).filter(User.name.is_(None)):
    print(user)

# 14. Kiểm tra NOT NULL
print("\n8. KIỂM TRA NAME IS NOT NULL")

for user in session.query(User).filter(User.name.is_not(None)):
    print(user)

# 15. Kết hợp AND bằng and_()
print("\n9. KẾT HỢP AND")

for user in session.query(User).filter(
    and_(
        User.name == "ed",
        User.fullname == "Ed Jones"
    )
):
    print(user)

# 16. Kết hợp AND bằng nhiều điều kiện
print("\n10. FILTER VỚI NHIỀU ĐIỀU KIỆN")

for user in session.query(User).filter(
    User.name == "ed",
    User.fullname == "Ed Jones"
):
    print(user)

# 17. Kết hợp AND bằng nhiều lần filter()
print("\n11. GỌI FILTER LIÊN TIẾP")

for user in session.query(User).filter(
    User.name == "ed"
).filter(
    User.fullname == "Ed Jones"
):
    print(user)

# 18. Kết hợp OR
print("\n12. KẾT HỢP OR")

for user in session.query(User).filter(
    or_(
        User.name == "ed",
        User.name == "wendy"
    )
):
    print(user)