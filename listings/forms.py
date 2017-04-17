from django.forms import ModelForm
from .models import HouseUserData, Calculator


class HouseUserDataForm(ModelForm):
    class Meta:
        model = HouseUserData
        exclude = ('user', 'house')


class CalculatorForm(ModelForm):
    @staticmethod
    def get_fields_addons(users_constants, global_constants, global_capital_growth, user_capital_growth):
        return {
            'property_managers_commission': '<a href="#" data-value="{0}" class="btn btn-primary change-value">User\'s value: {0}%</a>'
                                            '<a href="#" data-value="{1}" class="btn btn-warning change-value">Global value: {1}%</a>'.format(
                users_constants.property_management_commission,
                global_constants.property_management_commission,
            ),
            'int_rate': '<a href="#" data-value="{0}" class="btn btn-primary change-value">User\'s value: {0}%</a>'.format(
                users_constants.loan_interest_rate
            ),
            'deposit': '<a href="#" data-value="{0}" class="btn btn-primary change-value">User\'s value: {0}%</a>'
                       '<a href="#" data-value="{1}" class="btn btn-warning change-value">Global value: {1}%</a>'.format(
                users_constants.loan_deposit,
                global_constants.loan_deposit,
            ),
            'vacancy': '<a href="#" data-value="{0}" class="btn btn-primary change-value">User\'s value: {0}</a>'
                       '<a href="#" data-value="{1}" class="btn btn-warning change-value">Global value: {1}</a>'.format(
                users_constants.vacancy_rate,
                global_constants.vacancy_rate,
            ),
            'capital_growth': '<a href="#" data-value="{0}" class="btn btn-primary change-value">User\'s value: {0}%</a>'
                              '<a href="#" data-value="{1}" class="btn btn-warning change-value">Global value: {1}%</a>'.format(
                user_capital_growth,
                global_capital_growth or 0,
            ),
            'gross_yield': '<a href="#" data-value="{0}" class="btn btn-primary change-value">User\'s value: {0}%</a>'.format(
                users_constants.gross_yield,
            ),
            'net_yield': '<a href="#" data-value="{0}" class="btn btn-primary change-value">User\'s value: {0}%</a>'.format(
                users_constants.net_yield,
            ),
            'min_cashflow': '<a href="#" data-value="{0}" class="btn btn-primary change-value">User\'s value: {0}$</a>'.format(
                users_constants.min_cashflow,
            ),
        }

    class Meta:
        model = Calculator
        exclude = ('user', 'house')
