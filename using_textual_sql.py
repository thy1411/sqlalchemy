from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy import text
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

# 7. Sử dụng text() trong filter() và order_by()
print("\n1. TEXT() TRONG FILTER() VÀ ORDER_BY()")

for user in (
    session.query(User)
    .filter(text("id<224"))
    .order_by(text("id"))
    .all()
):
    print(user.name)

# 8. Sử dụng params()
print("\n2. SỬ DỤNG PARAMS()")

user = (
    session.query(User)
    .filter(text("id<:value and name=:name"))
    .params(
        value=224,
        name="fred"
    )
    .order_by(User.id)
    .one()
)

print(user)

# 9. Sử dụng from_statement()
print("\n3. SỬ DỤNG FROM_STATEMENT()")

users = (
    session.query(User)
    .from_statement(
        text("SELECT * FROM users where name=:name")
    )
    .params(name="ed")
    .all()
)

print(users)

# 10. Sử dụng columns() để ánh xạ cột
print("\n4. SỬ DỤNG COLUMNS()")

stmt = text(
    "SELECT name, id, fullname, nickname "
    "FROM users where name=:name"
)

stmt = stmt.columns(
    User.name,
    User.id,
    User.fullname,
    User.nickname
)

users = (
    session.query(User)
    .from_statement(stmt)
    .params(name="ed")
    .all()
)

print(users)

# 11. Truy vấn các cột riêng lẻ từ câu SQL
print("\n5. TRUY VẤN CÁC CỘT RIÊNG LẺ")

stmt = text(
    "SELECT name, id FROM users where name=:name"
)

stmt = stmt.columns(
    User.name,
    User.id
)

results = (
    session.query(User.id, User.name)
    .from_statement(stmt)
    .params(name="ed")
    .all()
)

print(results)

# 12. Đóng Session
session.close()