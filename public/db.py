from config import settings
from sqlalchemy import insert, select
from sqlalchemy import create_engine, text
from models.good import User, Base
from models.users import Categor, Staff

# определяем параметры для подключения
# settings.DATABASE_URL = 'sqlite:///./test02.db
#ur_p = "postgresql://postgres:artem@localhost:5432/dbtest04"
ur_s = settings.POSTGRES_DATABASE_URLS
ur_a = settings.POSTGRES_DATABASE_URLA

print(ur_s)
engine_s = create_engine(ur_s, echo=True)

# engine_a = create_async_engine(ur_a, echo=True)
def create_tables():
    #pass
    Base.metadata.drop_all(bind=engine_s)
    Base.metadata.create_all(bind=engine_s)
    # Base.metadata.drop_all(bind=engine_s)
    # Base.metadata.create_all(bind=engine_s)
    # metadata.create_all(bind=engine_s)


def f():
    with engine_s.connect() as conn:
        answer = conn.execute(text('select * from users;'))
        print(f"answer = {answer.all()}")

def f_bilder():
    with engine_s.connect() as conn:
        query = insert(Categor).values([
            {"title": "SSSuiu", "description": "123545"},
            {"title": "SSSuiu22", "description": "12354445"}
        ])
        conn.execute(query)
        conn.execute(text('commit;'))
        query = select(User)
        answer = conn.execute(query)
        print(f"answer = {answer.all()}")