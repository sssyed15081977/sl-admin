import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flasksl.db import get_db

bp = Blueprint('supplier', __name__, url_prefix='/supplier')

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        contact_number = request.form['contact_number']
        place = request.form['place']
        db = get_db()
        error = None

        if not name:
            error = 'Supplier Name is required.'
        elif not contact_number:
            error = 'Contact Number is required.'
        elif not place:
            error = 'Place is required.'

        if error is None:
            discount = 0.0
            
            try:
                discount = float(request.form['discount'])
            except ValueError:
                pass

            try:
                db.execute(
                    "INSERT INTO supplier (name, contact_number, discount, place) VALUES (?, ?, ?, ?)",
                    (name, contact_number, discount, place),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Supplier {name} is already registered."
            else:
                error = f"Supplier {name} is created successfully."
                # return redirect(url_for("supplier.create"))

        flash(error)

    return render_template('supplier/create.html')