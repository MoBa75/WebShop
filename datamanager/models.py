from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


class User(Base):
    """
    Represents a user of the system, either a customer or an admin.

    Attributes:
        id (int): Primary key.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        company (str): Optional company name.
        email (str): Unique email address.
        phone_number (str): Contact phone number.
        address (str): Street and house number.
        zip_code (int): Postal code.
        city (str): City of residence.
        is_admin (bool): Admin status (default: False).
        created_at (datetime): Timestamp when the user was created.
        updated_at (datetime): Timestamp when the user was last updated.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    company = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    address = Column(String)
    zip_code = Column(Integer)
    city = Column(String)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    orders = relationship("Order", back_populates="user")


class Product(Base):
    """
    Represents a product that can be ordered by users.

    Attributes:
        id (int): Primary key.
        name (str): Product name.
        unit (str): Unit of measure (e.g., "piece", "bottle").
        price (float): Unit price.
        description (str): Product description.
        stock (int): Current inventory.
        image_path (str): Relative path to the image folder.
        created_at (datetime): Creation timestamp.
        updated_at (datetime): Last updated timestamp.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    unit = Column(String)
    price = Column(Float)
    description = Column(String)
    stock = Column(Integer)
    image_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    order_items = relationship("OrderItem", back_populates="product")


class Order(Base):
    """
    Represents a customer order.

    Attributes:
        id (int): Primary key.
        user_id (int): Foreign key to the user placing the order.
        date (date): Date the order was placed.
        status (str): Status of the order (e.g., "processing", "shipped").
        created_at (datetime): Creation timestamp.
        updated_at (datetime): Last updated timestamp.
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    invoice = relationship("Invoice", back_populates="order", uselist=False)
    shipment = relationship("Shipment", back_populates="order", uselist=False)


class OrderItem(Base):
    """
    Represents an individual item within an order.

    Attributes:
        id (int): Primary key.
        order_id (int): Foreign key to the order.
        product_id (int): Foreign key to the product.
        quantity (int): Number of units ordered.
        unit_price (float): Price per unit at the time of order.
    """
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


class Invoice(Base):
    """
    Represents an invoice for a completed order.

    Attributes:
        id (int): Primary key.
        order_id (int): Foreign key to the order.
        invoice_date (date): Date of the invoice.
        total_amount (float): Total amount to be paid.
        is_paid (bool): Payment status.
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

    Attributes:
        id (int): Primary key.
        invoice_id (int): Foreign key to the invoice.
        reminder_date (date): Date the reminder was sent.
        status (str): Status of the reminder (e.g., "open", "closed").
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

    Attributes:
        id (int): Primary key.
        order_id (int): Foreign key to the order.
        tracking_number (str): Shipment tracking number.
        shipped_date (date): Date the order was shipped.
        carrier (str): Shipping service provider.
    """
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    tracking_number = Column(String)
    shipped_date = Column(Date)
    carrier = Column(String)

    order = relationship("Order", back_populates="shipment")
