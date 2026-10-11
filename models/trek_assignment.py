from datetime import datetime, UTC
from extensions import db

class TrekAssignment(db.Model):
    __tablename__="trek_assignments"
    __table_args__ = (
        db.UniqueConstraint("staff_id","trek_id", name="unique_user_trek_assignment"),
    )

    id = db.Column(db.Integer, primary_key = True)

    trek_id = db.Column(db.Integer, db.ForeignKey("treks.id"), nullable=False)

    staff_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    assigned_at = db.Column(db.DateTime, nullable= False, default=lambda: datetime.now(UTC))

    trek = db.relationship("Trek", back_populates = "staff_assignments")

    staff = db.relationship("User", back_populates = "staff_assignments")

    def __repr__(self):
        return (
            f"<TrekAssignment(id={self.id}, "
            f"trek_id={self.trek_id}, "
            f"staff_id={self.staff_id})>"
        )

    def __str__(self):
        return f"Trek {self.trek_id} → Staff {self.staff_id}"