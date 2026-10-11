from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models import Trek, Booking, TrekAssignment
from utils.decorators import staff_required


staff_bp = Blueprint(
    "staff",
    __name__,
    url_prefix="/staff"
)


@staff_bp.route("/dashboard")
@login_required
@staff_required
def dashboard():

    assignments = TrekAssignment.query.filter_by(
        staff_id=current_user.id
    ).all()

    trek_ids = [
        assignment.trek_id
        for assignment in assignments
    ]

    if trek_ids:

        total_participants = Booking.query.filter(
            Booking.trek_id.in_(trek_ids),
            Booking.status == "Booked"
        ).count()

    else:

        total_participants = 0

    open_treks = sum(
        1
        for assignment in assignments
        if assignment.trek.status == "Open"
    )

    participant_counts = {}

    for assignment in assignments:

        participant_counts[assignment.trek_id] = Booking.query.filter_by(
            trek_id=assignment.trek_id,
            status="Booked"
        ).count()

    return render_template(
        "staff/dashboard.html",
        assignments=assignments,
        total_treks=len(assignments),
        total_participants=total_participants,
        open_treks=open_treks,
        participant_counts=participant_counts
    )

@staff_bp.route("/treks")
@login_required
@staff_required
def assigned_treks():

    assignments = TrekAssignment.query.filter_by(
        staff_id=current_user.id
    ).all()

    return render_template(
        "staff/treks.html",
        assignments=assignments
    )


@staff_bp.route("/treks/<int:trek_id>/manage", methods=["GET", "POST"])
@login_required
@staff_required
def manage_trek(trek_id):

    assignment = TrekAssignment.query.filter_by(
        trek_id=trek_id,
        staff_id=current_user.id
    ).first()

    if not assignment:

        flash("You are not assigned to this trek.", "danger")

        return redirect(
            url_for("staff.assigned_treks")
        )

    trek = Trek.query.get_or_404(trek_id)

    if request.method == "POST":

        available_slots = int(
            request.form.get("available_slots")
        )

        status = request.form.get("status")

        if available_slots < 0:

            flash(
                "Available slots cannot be negative.",
                "danger"
            )

            return render_template(
                "staff/manage_trek.html",
                trek=trek
            )

        if available_slots > trek.total_slots:

            flash(
                "Available slots cannot exceed total slots.",
                "danger"
            )

            return render_template(
                "staff/manage_trek.html",
                trek=trek
            )

        if status not in {
            "Open",
            "Closed",
            "Completed"
        }:

            flash(
                "Invalid trek status.",
                "danger"
            )

            return render_template(
                "staff/manage_trek.html",
                trek=trek
            )

        trek.available_slots = available_slots

        trek.status = status

        db.session.commit()

        flash(
            "Trek updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "staff.manage_trek",
                trek_id=trek.id
            )
        )

    return render_template(
        "staff/manage_trek.html",
        trek=trek
    )


@staff_bp.route("/participants")
@login_required
@staff_required
def all_participants():

    assignments = TrekAssignment.query.filter_by(
        staff_id=current_user.id
    ).all()

    trek_ids = [
        assignment.trek_id
        for assignment in assignments
    ]

    if trek_ids:

        bookings = Booking.query.filter(
            Booking.trek_id.in_(trek_ids),
            Booking.status == "Booked"
        ).order_by(
            Booking.booking_date.desc()
        ).all()

    else:

        bookings = []

    return render_template(
        "staff/all_participants.html",
        bookings=bookings
    )


@staff_bp.route("/treks/<int:trek_id>/participants")
@login_required
@staff_required
def participants(trek_id):

    assignment = TrekAssignment.query.filter_by(
        trek_id=trek_id,
        staff_id=current_user.id
    ).first()

    if not assignment:

        flash(
            "You are not assigned to this trek.",
            "danger"
        )

        return redirect(
            url_for("staff.assigned_treks")
        )

    trek = Trek.query.get_or_404(trek_id)

    bookings = Booking.query.filter_by(
        trek_id=trek.id
    ).all()

    return render_template(
        "staff/participants.html",
        trek=trek,
        bookings=bookings
    )

@staff_bp.route("/profile", methods=["GET", "POST"])
@login_required
@staff_required
def profile():

    if request.method == "POST":

        current_user.full_name = request.form.get(
            "full_name"
        )

        current_user.phone = request.form.get(
            "phone"
        )

        db.session.commit()

        flash(
            "Profile updated successfully.",
            "success"
        )

        return redirect(
            url_for("staff.profile")
        )

    return render_template(
        "staff/profile.html"
    )