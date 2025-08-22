from sqlmodel import create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5433/twitter_mini"
)

engine = create_engine(DATABASE_URL, echo=True)
