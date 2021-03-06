from datetime import date

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField, IntegerField
from wtforms import RadioField, DateField
from wtforms.validators import DataRequired


class AddTransactionForm(FlaskForm):
    description = StringField("Description", validators=[DataRequired()])
    date = DateField("Registry Date", default=date.today(), validators=[DataRequired()])
    value = StringField("Value", validators=[DataRequired()])
    transaction = RadioField("Type of Transaction",
                             choices=[
                                 ('earnings', "Receita"),
                                 ('brokerage_transfers', "Investimento"),
                                 ('expenses', "Gasto")
                             ])

    pay_method = RadioField("Payment Method",
                            choices=[
                                ("Dinheiro", "Dinheiro"),
                                ("Crédito", "Crédito"),
                                ("Terceiros", "Terceiros")
                            ])
    installments = IntegerField("Installments", default=1, validators=[DataRequired()])
    new_cat = StringField("New Category")
    cat_expense = SelectField("Category")
    cat_earning = SelectField("Category")

    submit = SubmitField("Add it")
