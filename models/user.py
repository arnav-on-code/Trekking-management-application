from datetime import datetime, UTC

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

    password_hash = db.Column(db.String(255), nullable=False)

    phone = db.Column(db.String(15), nullable= False)

    role = db.Column(db.String(10), nullable=False, default="user")

    status = db.Column(db.String(20),nullable=False,default="approved")

    created_at = db.Column(db.DateTime,default= lambda: datetime.now(UTC),nullable=False)

    updated_at = db.Column(db.DateTime, default= lambda:datetime.now(UTC), onupdate= lambda:datetime.now(UTC), nullable=False)

    bookings = db.relationship("Booking",back_populates="user",cascade="all, delete-orphan")

    staff_assignments = db.relationship("TrekAssignment", back_populates="staff", cascade="all, delete-orphan")


    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
       return (
        f"<User(id={self.id}, "
        f"name='{self.full_name}', "
        f"role='{self.role}')>"
    )

    def __str__(self):
        return self.full_name
        
    @property
    def is_admin(self):
        return self.role == "admin"


    @property
    def is_staff(self):
        return self.role == "staff"


    @property
    def is_user(self):
        return self.role == "user"
    