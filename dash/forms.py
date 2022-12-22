from django import forms
from django.core.exceptions import ValidationError


class AddProjectForm(forms.Form):

    project_name = forms.CharField(required=True)
    project_image = forms.FileField()
    estimated_budget = forms.DecimalField(max_digits=12, decimal_places=2)


'''


client
project_category
start_date
end_date
project_link
project_description
timestamp
project_slug
'''
