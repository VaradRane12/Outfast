import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///store.db', echo=True)

Base = declarative_base()

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
    image_link = Column(String(100))

Base.metadata.create_all(engine)

df = pd.read_csv("Fashion Data/final_styles.csv")
df_images = pd.read_csv("Fashion Data/images_final.csv")
Session = sessionmaker(bind=engine)
session = Session()

image_map = dict(zip(df_images["filename"], df_images["link"])) 

for _, row in df.iterrows():
    product_id = row["id"]
    image_link = image_map.get(product_id, None)

    product = Product(
        id=product_id,
        gender=row["gender"],
        masterCategory=row.get("masterCategory", None),
        subCategory=row.get("subCategory", None),
        articleType=row.get("articleType", None),
        baseColour=row.get("baseColour", None),
        season=row.get("season", None),
        year=row.get("year", None),
        usage=row.get("usage", "0"),
        productDisplayName=row.get("productDisplayName", None),
        image_link=image_link
    )
    session.add(product)
session.commit()

session.close()

print("Data inserted successfully.") 