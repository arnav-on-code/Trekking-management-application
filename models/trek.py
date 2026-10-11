from datetime import datetime, UTC

from extensions import db


class Trek(db.Model):
    __tablename__ = "treks"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    location = db.Column(db.String(100), nullable=False)

    difficulty = db.Column(db.String(20),nullable=False) 

    duration = db.Column(db.Integer,nullable=False)  

    total_slots = db.Column(db.Integer,nullable=False)

    available_slots = db.Column(db.Integer,nullable=False)

    description = db.Column(db.Text)

    start_date = db.Column(db.Date,nullable=False)

    end_date = db.Column(db.Date,nullable=False)

    status = db.Column(db.String(20),nullable=False,default="Pending")  # Pending, Approved, Open, Closed, Completed

    created_at = db.Column(db.DateTime,nullable=False,default=lambda: datetime.now(UTC))

    updated_at = db.Column(db.DateTime,nullable=False,default=lambda: datetime.now(UTC),onupdate=lambda: datetime.now(UTC))


    bookings = db.relationship("Booking",back_populates="trek",cascade="all, delete-orphan")

    staff_assignments = db.relationship("TrekAssignment",back_populates="trek",cascade="all, delete-orphan")

    def __repr__(self):
        return (
            f"<Trek(id={self.id}, "
            f"name='{self.name}', "
            f"status='{self.status}')>"
        )

    def __str__(self):
        return self.name