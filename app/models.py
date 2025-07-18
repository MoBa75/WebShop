from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


class User(Base):
    """
    Represents a user of the system, either a customer or an admin.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    company = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    birth_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    orders = relationship("Order", back_populates="user")
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")



class Address(Base):
    """
    Represents an address used by a user for billing or shipping.
    """
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    street = Column(String, nullable=False)
    zip_code = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    is_billing = Column(Boolean, default=False)
    is_shipping = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="addresses")



class Product(Base):
    """
    Represents a product that can be ordered by users.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
    image_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    order_items = relationship("OrderItem", back_populates="product")



class Order(Base):
    """
    Represents a customer order.
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    shipping_address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
    billing_address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    invoice = relationship("Invoice", back_populates="order", uselist=False)
    shipment = relationship("Shipment", back_populates="order", uselist=False)
    shipping_address = relationship("Address", foreign_keys=[shipping_address_id])
    billing_address = relationship("Address", foreign_keys=[billing_address_id])


class OrderItem(Base):
    """
    Represents an individual item within an order.
    """
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


class Invoice(Base):
    """
    Represents an invoice for a completed order.
    """
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    invoice_date = Column(Date)
    total_amount = Column(Float)
    is_paid = Column(Boolean, default=False)

    order = relationship("Order", back_populates="invoice")
    reminders = relationship("Reminder", back_populates="invoice", cascade="all, delete-orphan")


class Reminder(Base):
    """
    Represents a reminder for an unpaid invoice.
    """
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    reminder_date = Column(Date)
    status = Column(String)

    invoice = relationship("Invoice", back_populates="reminders")


class Shipment(Base):
    """
    Represents the shipment details of an order.
    """
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    tracking_number = Column(String)
    shipped_date = Column(Date)
    carrier = Column(String)

    order = relationship("Order", back_populates="shipment")
