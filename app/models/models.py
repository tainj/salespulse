from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True)
    phone = Column(String(20))
    country = Column(String(50))

    def __repr__(self):
        return f"<Client {self.firstname} {self.lastname}>"

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(50))

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, default=1)             # Сколько купили
    total_price = Column(Float, nullable=False)       # price * quantity
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связи
    client = relationship("Client")
    product = relationship("Product")

    def __repr__(self):
        return f"<Order {self.id}: {self.client.firstname} {self.client.lastname} bought {self.quantity}x {self.product.name}>"