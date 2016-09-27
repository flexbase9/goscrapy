from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class CommonItem(Base):
    
    __tablename__ = 'common_items'
    
    id = Column(Integer, primary_key=True)
    site_name=Column(String)
    from_url=Column(String)
    parent_url=Column(String)
    items = relationship("CommonItemLine")
    
    
    
    
    
    
    
    
    
class CommonItemLine(Base):
    
    __tablename__ = 'common_item_line'
    
    id = Column(Integer, primary_key=True)
    item_id=Column(Integer,ForeignKey("common_items.id"))
    field=Column(String)
    value=Column(String)
    
    owner=relationship("CommonItem",back_populates="items")