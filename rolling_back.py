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

# 7. Thêm Ed vào Session
session.add(ed_user)

# 8. Thêm các User khác
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

# 9. Cập nhật nickname của Ed
ed_user.nickname = "eddie"

# 10. Lưu dữ liệu ban đầu
session.commit()

# 11. Thay đổi tên Ed
ed_user.name = "Edwardo"

# 12. Tạo đối tượng fake_user
fake_user = User(
    name="fakeuser",
    fullname="Invalid",
    nickname="12345"
)

# 13. Thêm fake_user vào Session
session.add(fake_user)

# 14. Truy vấn các đối tượng vừa thay đổi
users_before_rollback = (
    session.query(User)
    .filter(User.name.in_(["Edwardo", "fakeuser"]))
    .all()
)

print("\nDữ liệu trước khi rollback:")
print(users_before_rollback)

# 15. Hoàn tác transaction
session.rollback()

# 16. Kiểm tra tên Ed sau rollback
print("\nTên Ed sau khi rollback:")
print(ed_user.name)

# 17. Kiểm tra fake_user có còn trong Session không
print("\nfake_user còn trong Session:")
print(fake_user in session)

# 18. Truy vấn lại database
users_after_rollback = (
    session.query(User)
    .filter(User.name.in_(["ed", "fakeuser"]))
    .all()
)

print("\nDữ liệu sau khi rollback:")
print(users_after_rollback)