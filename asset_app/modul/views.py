from datetime import date

from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from asset_app import app, db
from asset_app.modul.models import Violation, Fine, Driver, Violations


@app.route('/')
@app.route('/index')
def hello():
    return render_template('index.html')


@app.route('/list_fines')
def list():
    current_fine = finesUser()
    return render_template('list_fines.html', current_fine=current_fine)


@app.route('/fines', methods=['GET', 'POST'])
@login_required
def fine_forms():
    form = Violation()
    if form.validate_on_submit():
        with app.app_context():
            db.create_all()
            nam = form.name.data
            number_plate = form.number_plate.data
            fines = form.violations.data
            date_violation = form.date_violations.data

            fine = Fine.query.filter_by(fine=fines).first()
            violation = Violations(fine, date_violation)

            driver = Driver.query.filter_by(name=nam).first()

            if driver is None:
                driver = Driver(nam, number_plate, violation)

            else:
                driver = Driver.query.filter_by(name=nam).update(violation=violation).first()

            db.session.add(driver)













        driver = Intruder(name, number_plate)
        addViolation(driver, violations, date_violation)
        return redirect(url_for('list'))
    return render_template('fine.html', form=form)


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    form = PaymentForm()
    current_datetime = date.today()
    if form.validate_on_submit():

        id_fine = form.id_fine.data
        payment_fine(current_datetime, id_fine)
        flash('Штраф оплачен!', 'success')
        return render_template('payment.html', form=form)
    return render_template('payment.html', form=form)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search_forms():
    form = SearchForm()
    current_fine = False
    if form.validate_on_submit():
        number_plate = form.number_plate.data
        if searchFines(number_plate):
            current_fine = searchFines(number_plate)
        else:
            current_fine = None

        return render_template('searchViolation.html', form=form, current_fine=current_fine)
    return render_template('searchViolation.html', form=form, current_fine=current_fine)

@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title='Страница не найдена'), 404