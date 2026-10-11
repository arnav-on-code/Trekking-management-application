from datetime import UTC, datetime

from extensions import db


class Booking(db.Model):
    __tablename__ = "bookings"
    __table_args__ = (
    db.UniqueConstraint("user_id", "trek_id", name="unique_user_trek_booking"),
    )

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    trek_id = db.Column(db.Integer, db.ForeignKey("treks.id"), nullable=False)

    booking_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))

    status = db.Column(db.String(20), nullable=False, default="Booked")  # Booked, Cancelled, Completed

    user = db.relationship("User", back_populates="bookings")

    trek = db.relationship("Trek", back_populates="bookings")

    def __repr__(self):
        return f"<Booking(id={self.id}, user_id={self.user_id}, trek_id={self.trek_id}, status='{self.status}')>"

    def __str__(self):
        return f"Booking #{self.id}"