from django import forms
from django.forms import ModelForm
from .models import HouseUserData, Calculator, OtherExpense


class HouseUserDataForm(ModelForm):
    rent_type = forms.ChoiceField(label='Appraisal type', choices=HouseUserData.RENT_TYPE_CHOICES, widget=forms.RadioSelect(), required=False)
    market_reg_value = forms.CharField(
        label='Market/registered value',
    )

    def __init__(self, *args, **kwargs):
        house = kwargs.pop('house', None)
        super(HouseUserDataForm, self).__init__(*args, **kwargs)
        if house and house.price_type.pk == 1:
            help_text = '<a href="#" id="use-offer-price" class="btn btn-default btn-sm">Use Offer Price</a>&nbsp;' \
                        '<a href="#" id="use-asking-price" class="btn btn-default btn-sm">Use Asking price</a>&nbsp;' \
                        '<a href="#" id="use-government-value" class="btn btn-default btn-sm">Use Government Valuation</a>'
        else:
            help_text = '<a href="#" id="use-offer-price" class="btn btn-default btn-sm">Use Offer Price</a>&nbsp;' \
                        '<a href="#" id="use-government-value" class="btn btn-default btn-sm">Use Government Valuation</a>'

        self.fields['market_reg_value'].help_text = help_text

    class Meta:
        model = HouseUserData
        exclude = ('user', 'house')


class CalculatorForm(ModelForm):
    @staticmethod
    def get_fields_addons(users_constants, global_constants, global_capital_growth, user_capital_growth, new_build):
        if new_build:
            user_deposit = users_constants.new_built_loan_deposit
            global_deposit = global_constants.new_built_loan_deposit
        else:
            user_deposit = users_constants.loan_deposit
            global_deposit = global_constants.loan_deposit

        return {
            'property_managers_commission': '<a href="#" data-value="{0}" class="btn btn-primary change-value">User\'s value: {0}%</a>'
                                            '<a href="#" data-value="{1}" class="btn btn-warning change-value">Global value: {1}%</a>'.format(
                users_constants.property_management_commission,
                global_constants.property_management_commission,
            ),
            'int_rate': '<a href="#" data-value="{0}" class="btn btn-primary change-value">User\'s value: {0}%</a>'.format(
                users_constants.loan_interest_rate
            ),
            'deposit': '<a href="#" id="user-deposit" data-value="{0}" class="btn btn-primary change-value">User\'s value: {0}%</a>'
                       '<a href="#" id="global-deposit" data-value="{1}" class="btn btn-warning change-value">Global value: {1}%</a>'.format(
                user_deposit,
                global_deposit,
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
            'min_cashflow': '<a href="#" data-value="{0}" class="btn btn-primary change-value">User\'s value: $ {0}</a>'.format(
                users_constants.min_cashflow,
            ),
        }

    class Meta:
        model = Calculator
        exclude = ('user', 'house')


class OtherExpenseForm(ModelForm):
    """Form for creating OtherExpenses objects"""
    class Meta:
        model = OtherExpense
        exclude = ('user', 'house')
