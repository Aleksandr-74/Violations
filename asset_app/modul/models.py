from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SearchField
from wtforms.validators import DataRequired, Length

from asset_app import db, app

intruder_violations = db.Table('driver_violations',
                               db.Column('driver_id', db.Integer, db.ForeignKey('driver.id')),
                               db.Column('violations_id', db.Integer, db.ForeignKey('violations.id')))


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),  unique=True, nullable=False)
    number_plate = db.Column(db.String(10), nullable=False)
    driver_violations = db.relationship('Violations', secondary=intruder_violations, lazy=True, backref='drivers')

    def __init__(self, name, number_plate, violations):
        self.name = name
        self.number_plate = number_plate
        self.violations = violations

    # def addDrivers(self, name, number_plate):
    #     with app.app_context():
    #         db.create_all()
    #         def chekDrivers(nams, number_plates):
    #             name = Fine.query.filter_by(name=nams).first()
    #             number_plate = Fine.query.filter_by(number_plate=number_plates).first()
    #             if not name and not number_plate:
    #                 driver = Driver(name, number_plate)
    #                 db.session.add(driver)
    #                 return
    #             else
    #
    #     def chek


class Fine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fine = db.Column(db.String(255),  unique=True, nullable=False)
    sum_fine = db.Column(db.Float(10), nullable=False)
    violations = db.relationship('Violations', lazy='fine', backref='intruder')

    def __init__(self, fine, sum_fine):
        self.fine = fine
        self.sum_fine = sum_fine


class Violations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fine_id = db.Column(db.Integer, db.ForeignKey('fine.id'))
    date_violation = db.Column(db.DATE, nullable=False)
    date_Payment = db.Column(db.DATE)

    def __init__(self, date_violation, fine):
        self.fine = fine
        self.date_violation = date_violation
        self.date_payment = None

    # @addViolations
    # def addViolation(self, *args):
    #     with app.app_context():
    #         db.create_all()
    #
    #         def checks(args):
    #
    #
    #         fine_id = Fine.query.filter_by(fine=args).first()




class Violation(FlaskForm):
    name = StringField("Имя", validators=[DataRequired(), Length(min=1, max=30, message=None)])
    number_plate = StringField("Гос номер", validators=[DataRequired(), Length(min=1, max=6, message=None)])
    violations = StringField('Нарушение', validators=[DataRequired()])
    date_violations = DateField("Дата нарушения", format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Отправить')

#Поиск
class SearchForm(FlaskForm):
    number_plate = SearchField("Гос номер", validators=[DataRequired(), Length(min=1, max=6, message=None)])
    submit = SubmitField('Отправить')









# class PaymentForm(FlaskForm):
#     id_fine = TelField("№ Штрафа", validators=[DataRequired()])
#     submit = SubmitField('Оплатить')



# def searchFines(number):
#     try:
#         connection = sqlite3.connect(DB_PATH)
#         cursor = connection.cursor()
#         cursor.execute(f'''
#                 SELECT offense_id, name, number_plate, violation, sum_fine, date_violation, date_payment
#                 FROM offense
#                 WHERE number_plate = '{number}';
#             ''')
#         current_fine = cursor.fetchall()
#     except sqlite3.Error as error:
#         print(f'Не удалось подключиться searchFines к бд : {error}')
#
#     finally:
#         if connection:
#             connection.close()
#
#     return current_fine
#
#
# def addViolation(driver, violation, date_violation):
#     print('подключится к базе')
#     try:
#         connection = sqlite3.connect(DB_PATH)
#         cursor = connection.cursor()
#         cursor.execute(f'''
#             INSERT INTO offense(name, number_plate, violation, sum_fine, date_violation, date_payment)
#             VALUES('{driver.name}', '{driver.number_plate}', '{violation}',
#             Null, '{date_violation}', Null);
#          ''')
#         connection.commit()
#
#         cursor = connection.cursor()
#         cursor.execute('''
#                     UPDATE offense
#                     SET sum_fine = (SELECT sum_fine FROM violation)
#                     WHERE violation = (SELECT violation FROM violation)
#                 ''')
#         connection.commit()
#         cursor.close()
#         print('подключится к базе')
#     except sqlite3.Error as error:
#         print(f'Не удалось подключится addViolation к базе: {error}')
#     finally:
#         if connection:
#             connection.close()
#
#
# def finesUser():
#     try:
#         connection = sqlite3.connect(DB_PATH)
#         cursor = connection.cursor()
#         cursor.execute(
#             '''
#                 SELECT offense_id, name, number_plate, violation, sum_fine, date_violation, date_payment
#                 FROM offense;
#
#             ''')
#         current_fine = cursor.fetchall()
#         cursor.close()
#
#     except sqlite3.Error as error:
#         print(f'Не удалось подключиться finesUser к бд: {error}')
#
#     finally:
#         if connection:
#             connection.close()
#
#     return current_fine
#
#
# def payment_fine(current_datetime, id_fine):
#     try:
#         connection = sqlite3.connect(DB_PATH)
#         cursor = connection.cursor()
#         cursor.execute(f'''
#                 UPDATE offense
#                 SET date_payment = '{current_datetime}'
#                 WHERE {id_fine} = offense_id
#             ''')
#         connection.commit()
#         cursor.close()
#     except sqlite3.Error as error:
#         print(f'Не удалось подключится offense к базе: {error}')
#     finally:
#         if connection:
#             connection.close()
