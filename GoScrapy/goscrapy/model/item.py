# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class Item(Base):
    
    __tablename__='items'
    
    id=Column(Integer,primary_key=True)
    name=Column(String)
    description = Column(String)
    price = Column(String)
    special = Column(String)
    options = Column(String)
    main_image_link = Column(String)
    multiple_images_link = Column(String)
    category = Column(String)
    images_path = Column(String)
    download = Column(String)
    main_images = Column(String)
    sku = Column(String)
    parent_url=Column(String)
    from_url = Column(String)