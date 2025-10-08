import os
import databases
import sqlalchemy
from dotenv import load_dotenv
import asyncio

# Load environment variables from a .env file
load_dotenv()

# --- MySQL Database Configuration ---
# These variables are now loaded securely from your .env file.
# Make sure your .env file is in the root directory of your project.
MYSQL_USER = os.getenv("DB_USER")
MYSQL_PASSWORD = os.getenv("DB_PASSWORD")
MYSQL_HOST = os.getenv("DB_HOST")
MYSQL_DB = os.getenv("DB_NAME")

# Update the database URL to use pymysql
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"

# Create the core database objects
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Define the table structure for logging predictions
predictions_log = sqlalchemy.Table(
    "predictions_log",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("longitude", sqlalchemy.Float),
    sqlalchemy.Column("latitude", sqlalchemy.Float),
    sqlalchemy.Column("housing_median_age", sqlalchemy.Float),
    sqlalchemy.Column("total_rooms", sqlalchemy.Float),
    sqlalchemy.Column("total_bedrooms", sqlalchemy.Float),
    sqlalchemy.Column("population", sqlalchemy.Float),
    sqlalchemy.Column("households", sqlalchemy.Float),
    sqlalchemy.Column("median_income", sqlalchemy.Float),
    sqlalchemy.Column("ocean_proximity", sqlalchemy.String(255)),
    sqlalchemy.Column("predicted_value", sqlalchemy.Float),
)

# Update engine creation with connect_args
engine = sqlalchemy.create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={
        "connect_timeout": 10
    }
)

# Make this function async
async def create_db_and_tables():
    try:
        # Create a new connection
        async with database:
            # Create a synchronous connection for table creation
            with engine.begin() as conn:
                metadata.create_all(conn)
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise