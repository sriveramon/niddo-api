from app.db import Base, engine
from app.models import user  # Import your models here

# Create all tables in the database
Base.metadata.create_all(bind=engine)
