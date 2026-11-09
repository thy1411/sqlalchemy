from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy import func
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

# 7. Đếm bằng Query.count()
print("\n1. QUERY.COUNT()")

count = (
    session.query(User)
    .filter(User.name.like("%e%"))
    .count()
)

print("Số người dùng có tên chứa chữ e:", count)

# 8. Đếm số lượng theo từng tên
print("\n2. FUNC.COUNT() VÀ GROUP_BY()")

results = (
    session.query(func.count(User.name), User.name)
    .group_by(User.name)
    .all()
)

print(results)

# 9. Đếm toàn bộ bằng COUNT(*)
print("\n3. FUNC.COUNT('*')")

total = (
    session.query(func.count("*"))
    .select_from(User)
    .scalar()
)

print("Tổng số người dùng:", total)

# 10. Đếm bằng khóa chính
print("\n4. FUNC.COUNT(User.id)")

total = session.query(func.count(User.id)).scalar()

print("Tổng số người dùng:", total)

# 11. Đóng Session
session.close()