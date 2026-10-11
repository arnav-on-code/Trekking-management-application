# Trekking Management Application

A Flask-based web application for managing trekking trips, staff assignments, approvals, and user bookings. The system supports three roles: Admin, Trek Staff, and Trekker (User), each with a dedicated dashboard and permissions.

## Overview

This project allows:

- Admins to manage treks, approve staff, blacklist users or staff, assign staff to treks, view bookings, and search records.
- Trek staff to manage their assigned treks, update status and available slots, and see participants.
- Users to browse open treks, filter by difficulty and location, book trips, and track their booking history.

The application uses Flask, SQLAlchemy, Flask-Login, and SQLite for storage.

## Features

### Admin Features

- Dashboard with summary metrics
- Add, edit, and delete treks
- Approve or blacklist staff accounts
- Blacklist users
- Assign staff to treks
- View all bookings
- Search users, staff, or treks

### Staff Features

- Login after admin approval
- View assigned treks dashboard
- Manage assigned trek status and available slots
- View trek participants
- Update profile details

### User Features

- Register as a trekker or staff member
- Login/logout system
- Browse open treks with filters
- View trek details
- Book treks if slots are available
- View bookings and trip history
- Manage profile information

## Tech Stack

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Login
- SQLite
- Jinja2 Templates
- Bootstrap styling

## Project Structure

```text
Trekking-management-application/
├── app.py
├── config.py
├── extensions.py
├── requirements.txt
├── api.yaml
├── .env
├── README.md
├── instance/
│   └── trekking.db
├── models/
│   ├── __init__.py
│   ├── booking.py
│   ├── trek.py
│   ├── trek_assignment.py
│   └── user.py
├── routes/
│   ├── __init__.py
│   ├── admin.py
│   ├── auth.py
│   ├── staff.py
│   └── user.py
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── admin/
│   ├── auth/
│   ├── staff/
│   ├── user/
│   ├── base.html
│   └── ...
└── utils/
    └── decorators.py
```

## Database Design

The application uses SQLite with the following core models:

- User
  - id
  - full_name
  - email
  - password_hash
  - phone
  - role
  - status
  - created_at
  - updated_at

- Trek
  - id
  - name
  - location
  - difficulty
  - duration
  - total_slots
  - available_slots
  - description
  - start_date
  - end_date
  - status

- Booking
  - id
  - user_id
  - trek_id
  - booking_date
  - status

- TrekAssignment
  - id
  - trek_id
  - staff_id
  - assigned_at

Relationships:

- A user can have many bookings.
- A trek can have many bookings.
- A staff member can be assigned to multiple treks.
- A trek can have multiple assigned staff members.

## Roles and Access Control

### Admin

The admin account is created automatically on first launch if no admin account exists.

### Staff

Staff accounts are created by self-registration but remain pending until approved by an admin.

### User

Regular trekkers can register and book treks after login.

## Default Admin Credentials

The project includes default admin values in the `.env` file:

```env
SECRET_KEY=your_secret_key_here
ADMIN_NAME=Administrator
ADMIN_EMAIL=admin@trek.com
ADMIN_PASSWORD=admin123
ADMIN_PHONE=9999999999
```

Important:

- Change the default values before deploying to a real environment.
- The application raises an error if the required admin configuration is missing.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/arnav-on-code/Trekking-management-application.git
cd Trekking-management-application
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the environment:

- Windows:

```bash
venv\Scripts\activate
```

- macOS/Linux:

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Ensure the `.env` file contains valid configuration values.

## Running the App

Start the application with:

```bash
python app.py
```

Then open the browser at:

```text
http://127.0.0.1:5000
```

The root URL redirects to the login page.

## Authentication Flow

- Users register with full name, email, phone, password, and role.
- If the role is staff, the account starts in a pending state.
- Login checks:
  - existing user
  - password validity
  - blacklisted account restrictions
  - pending staff approval
- Successful login redirects the user to their role-specific dashboard.

## API Documentation

The project includes an OpenAPI document at:

```text
api.yaml
```

This file documents major authentication, admin, user, and staff routes.

## Route Overview

### Authentication

- `/auth/register`
- `/auth/login`
- `/auth/logout`

### Admin

- `/admin/dashboard`
- `/admin/treks`
- `/admin/treks/add`
- `/admin/treks/<trek_id>/edit`
- `/admin/treks/<trek_id>/delete`
- `/admin/staffs`
- `/admin/staffs/<staff_id>/approve`
- `/admin/staffs/<staff_id>/blacklist`
- `/admin/assign-staff`
- `/admin/users`
- `/admin/users/<user_id>/blacklist`
- `/admin/users/<user_id>/approve`
- `/admin/bookings`
- `/admin/search`

### Staff

- `/staff/dashboard`
- `/staff/treks`
- `/staff/treks/<trek_id>/manage`
- `/staff/participants`
- `/staff/treks/<trek_id>/participants`
- `/staff/profile`

### User

- `/user/dashboard`
- `/user/treks`
- `/user/treks/<trek_id>`
- `/user/book/<trek_id>`
- `/user/bookings`
- `/user/history`
- `/user/profile`

## Notes

- The database is automatically created in `instance/trekking.db` when the app runs.
- The application uses `debug=True` during local development.
- Role-based decorators restrict access to particular routes.
- The app is designed for small-to-medium trekking operations and is not built as a full production-scale system.

## License

This project does not currently include a license file. If you plan to share or distribute it publicly, consider adding an open-source license such as MIT or Apache 2.0.

## Future Enhancements

Potential improvements include:

- Payment integration
- Email notifications
- Admin audit logs
- Trek cancellation policies
- Better validation and error handling
- Responsive mobile-first UI improvements
- REST API authentication and JWT support

## Contributing

Contributions are welcome. To improve the project:

1. Fork the repository.
2. Create a feature branch.
3. Make a focused change.
4. Test the application flow.
5. Open a pull request with a clear description.

## Contact

Project repository:

- GitHub: https://github.com/arnav-on-code/Trekking-management-application

