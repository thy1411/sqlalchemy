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

# 6. Tạo đối tượng ed_user
ed_user = User(
    name="ed",
    fullname="Ed Jones",
    nickname="edsnickname"
)

# 7. Thêm ed_user vào Session
session.add(ed_user)

# 8. Truy vấn đối tượng vừa thêm
our_user = (
    session.query(User)
    .filter_by(name="ed")
    .first()
)

print("Đối tượng truy vấn:", our_user)

# 9. Kiểm tra Identity Map
print("Có phải cùng một đối tượng:", ed_user is our_user)

# 10. Thêm nhiều User cùng lúc
session.add_all(
    [
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

# 11. Cập nhật nickname của ed_user
ed_user.nickname = "eddie"

# 12. Kiểm tra các đối tượng đã thay đổi
print("Các đối tượng đã thay đổi:")
print(session.dirty)

# 13. Kiểm tra các đối tượng mới
print("Các đối tượng đang chờ lưu:")
print(session.new)

# 14. Lưu thay đổi vào database
session.commit()

# 15. Kiểm tra ID sau khi lưu
print("ID của ed_user:", ed_user.id)