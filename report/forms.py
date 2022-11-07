from django import forms

class ReportForm(forms.Form):
    dirty_report = forms.CharField(widget=forms.Textarea(attrs={'class':"form-control", "name":"report", "rows":"12"}), label='')
