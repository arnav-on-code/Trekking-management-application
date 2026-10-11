from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from extensions import db
from models import Trek, Booking
from utils.decorators import user_required

user_bp = Blueprint(
    "user",
    __name__,
    url_prefix="/user"
)


@user_bp.route("/dashboard")
@login_required
@user_required
def dashboard():

    difficulty = request.args.get("difficulty", "").strip()
    location = request.args.get("location", "").strip()

    query = Trek.query.filter_by(status="Open")

    if difficulty:
        query = query.filter_by(difficulty=difficulty)

    if location:
        query = query.filter_by(location=location)

    treks = query.order_by(Trek.start_date).all()

    bookings = Booking.query.filter_by(
        user_id=current_user.id,
        status="Booked"
    ).order_by(
        Booking.booking_date.desc()
    ).all()

    booked_trek_ids = {
        booking.trek_id
        for booking in bookings
    }

    locations = [
        row[0]
        for row in db.session.query(Trek.location)
        .filter_by(status="Open")
        .distinct()
        .all()
    ]

    return render_template(
        "user/dashboard.html",
        treks=treks,
        bookings=bookings,
        booked_trek_ids=booked_trek_ids,
        locations=locations,
        selected_difficulty=difficulty,
        selected_location=location
    )

@user_bp.route("/bookings")
@login_required
@user_required
def bookings():

    bookings = Booking.query.filter(
        Booking.user_id == current_user.id,
        Booking.status.in_(["Booked", "Cancelled"])
    ).order_by(
        Booking.booking_date.desc()
    ).all()

    return render_template(
        "user/bookings.html",
        bookings=bookings
    )

@user_bp.route("/treks")
@login_required
@user_required
def treks():

    location = request.args.get("location", "").strip()
    difficulty = request.args.get("difficulty", "").strip()

    query = Trek.query.filter_by(status="Open")

    if location:
        query = query.filter(Trek.location.contains(location))

    if difficulty:
        query = query.filter_by(difficulty=difficulty)

    treks = query.order_by(Trek.start_date).all()

    booked_trek_ids={
        booking.trek_id for booking in Booking.query.filter_by(user_id=current_user.id).all()
        if booking.status=="Booked"
    }

    return render_template(
        "user/treks.html",
        treks=treks,
        booked_trek_ids=booked_trek_ids
    )

@user_bp.route("/treks/<int:trek_id>")
@login_required
@user_required
def trek_details(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    if trek.status != "Open":
        flash(
            "This trek is not currently available.",
            "warning"
        )

        return redirect(
            url_for("user.treks")
        )

    booking = Booking.query.filter_by(
        user_id=current_user.id,
        trek_id=trek.id
    ).first()

    return render_template(
        "user/trek_details.html",
        trek=trek,
        booking=booking
    )

@user_bp.route("/book/<int:trek_id>")
@login_required
@user_required
def book_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    if trek.status != "Open":

        flash("This trek is not open for booking.", "danger")
        return redirect(url_for("user.dashboard"))

    if trek.available_slots <= 0:

        flash("No slots available.", "danger")
        return redirect(url_for("user.dashboard"))

    existing_booking = Booking.query.filter_by(
        user_id=current_user.id,
        trek_id=trek.id
    ).first()

    if existing_booking:

        flash("You have already booked this trek.", "warning")
        return redirect(url_for("user.dashboard"))

    booking = Booking(
        user_id=current_user.id,
        trek_id=trek.id
    )

    trek.available_slots -= 1

    db.session.add(booking)
    db.session.commit()

    flash("Trek booked successfully.", "success")

    return redirect(url_for("user.history"))

@user_bp.route("/history")
@login_required
@user_required
def history():

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Booking.booking_date.desc()
    ).all()

    return render_template(
        "user/history.html",
        bookings=bookings
    )


@user_bp.route("/profile", methods=["GET", "POST"])
@login_required
@user_required
def profile():

    if request.method == "POST":

        current_user.full_name = request.form.get("full_name")
        current_user.phone = request.form.get("phone")

        db.session.commit()

        flash("Profile updated successfully.", "success")

        return redirect(url_for("user.profile"))

    return render_template("user/profile.html")
