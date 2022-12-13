from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div,Submit


COL_TO_NUM = (
    ("0","A"), ("1","B"), ("2","C"), ("3","D"),
    ("4","E"), ("5","F"), ("6","G"), ("7","H"),
    ("8","I"), ("9","J"), ("10","K"), ("11","L"),
    ("12","M"), ("13","N"), ("14","O"), ("15","P"),
    ("16","Q"), ("17","R"), ("18","S"), ("19","T"),
    ("20","Y"), ("21","V"), ("22","W"), ("23","X"),
    ("24","Y"), ("25","Z")
    #TODO case !?
)

class ComparisonForm(forms.Form):

    first_med_col = forms.ChoiceField(label='First medicine column', choices=COL_TO_NUM)
    first_co_col = forms.ChoiceField(label='First manufacture column', choices=COL_TO_NUM)
    first_file = forms.FileField()

    second_med_col = forms.ChoiceField(label="Second medicine column", choices=COL_TO_NUM)
    second_co_col = forms.ChoiceField(label='Second manufacture column', choices=COL_TO_NUM)
    second_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div('first_med_col', "first_co_col", "first_file", css_class='col-sm-6 col-12 border p-5'),
                Div('second_med_col', "second_co_col", "second_file", css_class='col-sm-6 col-12 border p-5'),      
            css_class='row p-2 position-relative'), 

            Div(
                Submit('submit', 'COMPARE', css_class="btn btn-success btn-lg "),
                css_class="d-flex justify-content-center")
        )
 