from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from datetime import datetime

from models import User, Trek, Booking, TrekAssignment
from utils.decorators import admin_required

from extensions import db

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():

    total_users = User.query.filter_by(role="user").count()

    total_staff = User.query.filter_by(role="staff").count()

    total_treks = Trek.query.count()

    total_bookings = Booking.query.count()

    recent_bookings = (
        Booking.query
        .order_by(Booking.booking_date.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_staff=total_staff,
        total_treks=total_treks,
        total_bookings=total_bookings,
        recent_bookings=recent_bookings
    )

@admin_bp.route("/treks")
@login_required
@admin_required
def treks():

    all_treks = Trek.query.order_by(Trek.start_date).all()

    return render_template(
        "admin/treks.html",
        treks=all_treks
    )
@admin_bp.route("/treks/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_trek():

    if request.method == "POST":

        total_slots = int(request.form.get("total_slots"))

        start_date = datetime.strptime(
            request.form.get("start_date"),
            "%Y-%m-%d"
        ).date()

        end_date = datetime.strptime(
            request.form.get("end_date"),
            "%Y-%m-%d"
        ).date()


        if total_slots <= 0:
            flash("Total slots must be greater than zero.", "danger")
            return render_template("admin/add_trek.html")

        if end_date < start_date:
            flash("End date cannot be before the start date.", "danger")
            return render_template("admin/add_trek.html")

        trek = Trek(
            name=request.form.get("name"),
            location=request.form.get("location"),
            difficulty=request.form.get("difficulty"),
            duration=int(request.form.get("duration")),
            total_slots=total_slots,
            available_slots=total_slots,
            description=request.form.get("description"),
            start_date=start_date,
            end_date=end_date,
            status=request.form.get("status")
        )

        db.session.add(trek)
        db.session.commit()

        flash("Trek created successfully.", "success")

        return redirect(url_for("admin.treks"))

    return render_template("admin/add_trek.html")

@admin_bp.route("/treks/<int:trek_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_trek(trek_id):
    
    trek = Trek.query.get_or_404(trek_id)
    if request.method == "POST":
        total_slots= int(request.form.get("total_slots"))

        start_date = datetime.strptime(request.form.get("start_date"), "%Y-%m-%d").date()

        end_date= datetime.strptime(request.form.get("end_date"), "%Y-%m-%d").date()

        if total_slots <=0:
            flash("Total slots must be greater than zero.", "danger")
            return render_template("admin/edit_trek.html", trek = trek)
        if end_date < start_date:
            flash("End date cannot be before the start date.", "danger")
            return render_template("admin/edit_trek.html", trek = trek)
        
        if request.form.get("difficulty") not in{ "Easy", "Moderate", "Hard"}:
            flash("Invalid difficulty value.", "danger")
            return render_template("admin/edit_trek.html", trek = trek)
        
        if request.form.get("status") not in {
            "pending", "approved", "Open", "closed", "completed"
        }:
            flash("Invalid status", "danger")
            return render_template("admin/edit_trek.html", trek=trek)
        
        trek.name = request.form.get("name")
        trek.location = request.form.get("location")
        trek.difficulty = request.form.get("difficulty")
        trek.duration= int(request.form.get("duration"))
        trek.total_slots = total_slots
        trek.description = request.form.get("description")
        trek.start_date = start_date
        trek.end_date = end_date
        trek.status = request.form.get("status")

        if trek.available_slots > trek.total_slots:
            trek.available_slots = trek.total_slots
        
        db.session.commit()

        flash("Trek updated successfully.", "success")
        
        return redirect(url_for("admin.treks"))

    return render_template(
        "admin/edit_trek.html",
        trek=trek
    )

@admin_bp.route("/treks/<int:trek_id>/delete", methods = ["POST"])
@login_required
@admin_required

def delete_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)

    db.session.delete(trek)
    db.session.commit()

    flash("Trek deleted successfully.", "success")
    return redirect(url_for("admin.treks"))


@admin_bp.route("/staffs")
@login_required
@admin_required
def staffs():

    staffs = User.query.filter_by(role="staff").order_by(User.full_name).all()

    return render_template(
        "admin/staffs.html",
        staffs=staffs
    )


@admin_bp.route("/staffs/<int:staff_id>/approve", methods=["POST"])
@login_required
@admin_required
def approve_staff(staff_id):

    staff = User.query.get_or_404(staff_id)

    if staff.role != "staff":
        flash("Invalid staff account.", "danger")
        return redirect(url_for("admin.staffs"))

    staff.status = "approved"

    db.session.commit()

    flash(f"{staff.full_name} has been approved.", "success")

    return redirect(url_for("admin.staffs"))


@admin_bp.route("/staffs/<int:staff_id>/blacklist", methods=["POST"])
@login_required
@admin_required
def blacklist_staff(staff_id):

    staff = User.query.get_or_404(staff_id)

    if staff.role != "staff":
        flash("Invalid staff account.", "danger")
        return redirect(url_for("admin.staffs"))

    staff.status = "blacklisted"

    db.session.commit()

    flash(f"{staff.full_name} has been blacklisted.", "warning")

    return redirect(url_for("admin.staffs"))
        

@admin_bp.route("/assign-staff", methods=["GET", "POST"])
@login_required
@admin_required
def assign_staff():

    treks = Trek.query.order_by(Trek.name).all()

    staffs = User.query.filter_by(
        role="staff",
        status="approved"
    ).order_by(User.full_name).all()

    if request.method == "POST":

        trek_id = int(request.form.get("trek_id"))
        staff_id = int(request.form.get("staff_id"))

        existing_assignment = TrekAssignment.query.filter_by(
            trek_id=trek_id,
            staff_id=staff_id
        ).first()

        if existing_assignment:
            flash("Staff is already assigned to this trek.", "warning")
            return redirect(url_for("admin.assign_staff"))

        assignment = TrekAssignment(
            trek_id=trek_id,
            staff_id=staff_id
        )

        db.session.add(assignment)
        db.session.commit()

        flash("Staff assigned successfully.", "success")

        return redirect(url_for("admin.assign_staff"))

    return render_template(
        "admin/assign_staff.html",
        treks=treks,
        staffs=staffs
    )

@admin_bp.route("/users")
@login_required
@admin_required
def users():

    users = User.query.filter_by(role="user").order_by(User.full_name).all()

    return render_template(
        "admin/users.html",
        users=users
    )

@admin_bp.route("/users/<int:user_id>/blacklist", methods=["POST"])
@login_required
@admin_required
def blacklist_user(user_id):

    user = User.query.get_or_404(user_id)

    if user.role != "user":
        flash("Invalid user account.", "danger")
        return redirect(url_for("admin.users"))

    user.status = "blacklisted"

    db.session.commit()

    flash(f"{user.full_name} has been blacklisted.", "warning")

    return redirect(url_for("admin.users"))

@admin_bp.route("/users/<int:user_id>/approve", methods=["POST"])
@login_required
@admin_required
def approve_user(user_id):

    user = User.query.get_or_404(user_id)

    if user.role != "user":
        flash("Invalid user account.", "danger")
        return redirect(url_for("admin.users"))

    user.status = "approved"

    db.session.commit()

    flash(f"{user.full_name} has been approved.", "success")

    return redirect(url_for("admin.users"))


@admin_bp.route("/bookings")
@login_required
@admin_required
def bookings():

    bookings = Booking.query.order_by(
        Booking.booking_date.desc()
    ).all()

    return render_template(
        "admin/bookings.html",
        bookings=bookings
    )

@admin_bp.route("/search", methods=["GET", "POST"])
@login_required
@admin_required
def search():

    users = []
    staffs = []
    treks = []

    if request.method == "POST":

        search_type = request.form.get("search_type")
        keyword = request.form.get("keyword")

        if search_type == "user":

            users = User.query.filter(
                User.role == "user",
                User.full_name.ilike(f"%{keyword}%")
            ).all()

        elif search_type == "staff":

            staffs = User.query.filter(
                User.role == "staff",
                User.full_name.ilike(f"%{keyword}%")
            ).all()

        elif search_type == "trek":

            treks = Trek.query.filter(
                Trek.name.ilike(f"%{keyword}%")
            ).all()

    return render_template(
        "admin/search.html",
        users=users,
        staffs=staffs,
        treks=treks
    )