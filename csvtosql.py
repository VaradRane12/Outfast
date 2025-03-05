# import pandas as pd
# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask
# app = Flask(__name__,template_folder="templates")
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
# app.config['SECRET_KEY'] = 'secretkey'
# db = SQLAlchemy(app)

# df = pd.read_csv("Fashion Data/final_styles.csv")

# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     gender = db.Column(db.String(10), nullable=False)
#     masterCategory = db.Column(db.Text)
#     subCategory = db.Column(db.Text)
#     articleType = db.Column(db.String(100))
#     baseColour = db.Column(db.String(20))
#     season = db.Column(db.String(50))
#     year = db.Column(db.Integer)
#     usage = db.Column(db.String, default=0)
#     productDisplayName = db.Column(db.Text)
# db.session.add({id = })
# db.session.commit()

# print(df.head())


import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database engine (SQLite in this case)
engine = create_engine('sqlite:///store.db', echo=True)

# Define the base class for models
Base = declarative_base()

# Define the Product model
class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    gender = Column(String(10), nullable=False)
    masterCategory = Column(Text)
    subCategory = Column(Text)
    articleType = Column(String(100))
    baseColour = Column(String(20))
    season = Column(String(50))
    year = Column(Integer)
    usage = Column(String, default="0")
    productDisplayName = Column(Text)

# Create the table
Base.metadata.create_all(engine)

# Read the CSV file
df = pd.read_csv("Fashion Data/final_styles.csv")

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Insert each row into the database
for _, row in df.iterrows():
    product = Product(
        id=row["id"],
        gender=row["gender"],
        masterCategory=row.get("masterCategory", None),
        subCategory=row.get("subCategory", None),
        articleType=row.get("articleType", None),
        baseColour=row.get("baseColour", None),
        season=row.get("season", None),
        year=row.get("year", None),
        usage=row.get("usage", "0"),
        productDisplayName=row.get("productDisplayName", None)
    )
    session.add(product)

# Commit the changes and close the session
session.commit()
session.close()

print("Data inserted successfully.")
