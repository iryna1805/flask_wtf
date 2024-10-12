from flask import Flask, flash, redirect, render_template, request, url_for
from wtforms import Form, StringField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange
from decimal import Decimal

app = Flask(__name__)
app.secret_key = b'-26_0gt'

class BookingForm(Form):
    last_name: str = StringField('Прізвище', validators=[DataRequired(), Length(min=2)])
    first_name: str = StringField("Ім'я", validators=[DataRequired(), Length(min=2)])
    passport_number: str = StringField('Номер паспорта', validators=[DataRequired(), Length(min=8, max=12)])
    luggage_weight: Decimal = DecimalField('Вага багажу (кг)', validators=[DataRequired(), NumberRange(min=0, max=40)])

    def save(self):
        print(f"Прізвище: {self.last_name.data}, Ім'я: {self.first_name.data}, Номер паспорта: {self.passport_number.data}, Вага багажу: {self.luggage_weight.data} кг")

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/book")
def get_booking():
    form = BookingForm()
    return render_template("form.html", form=form)

@app.post("/book")
def post_booking():
    form = BookingForm(request.form)
    if form.validate():
        form.save()
        flash("Бронювання успішно створене!", "success")
        return redirect(url_for("index"))
    else:
        for _, error in form.errors.items():
            flash(error, "danger")
        return render_template("form.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
