from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
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

# 6. Thêm dữ liệu ban đầu
session.add_all(
    [
        User(
            name="ed",
            fullname="Ed Jones",
            nickname="eddie"
        ),
        User(
            name="wendy",
            fullname="Wendy Williams",
            nickname="windy"
        ),
        User(
            name="mary",
            fullname="Mary Contrary",
            nickname="mary"
        ),
        User(
            name="fred",
            fullname="Fred Flintstone",
            nickname="freddy"
        ),
    ]
)

session.commit()

# 7. Truy vấn toàn bộ đối tượng User
print("\n1. TRUY VẤN TOÀN BỘ USER")

for instance in session.query(User).order_by(User.id):
    print(instance.name, instance.fullname)

# 8. Chỉ truy vấn name và fullname
print("\n2. CHỈ TRUY VẤN NAME VÀ FULLNAME")

for name, fullname in session.query(User.name, User.fullname):
    print(name, fullname)

# 9. Truy vấn User kết hợp với cột name
print("\n3. TRUY VẤN USER VÀ NAME")

for row in session.query(User, User.name).all():
    print(row.User, row.name)

# 10. Đặt tên khác cho cột bằng label()
print("\n4. TRUY VẤN VỚI LABEL")

for row in session.query(User.name.label("name_label")).all():
    print(row.name_label)