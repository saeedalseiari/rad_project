from django import forms


SEX = [('Male', 'Male'), ('Female', 'Female')]

class CardiacForm(forms.Form):
    first_name = forms.CharField(label="First Name: ", max_length=25)
    last_name = forms.CharField(label="Last Name: ", max_length=25)
    gender = forms.ChoiceField(label= "Gender: ", 
        widget=forms.RadioSelect(  
            attrs={'class': 'form-check form-check-inline', 
                    'style':'margin-left:15px; margin-right:1px'}) , 
        choices=SEX)

    mrn = forms.IntegerField(label="MRN (numbers): ", widget=forms.NumberInput(attrs={'step': '1', 'min': '0'}))
    age = forms.IntegerField(label="Age (years): ", widget=forms.NumberInput(attrs={'step': '1', 'min': '0'}))
    height = forms.IntegerField(label="Height (cm): ", widget=forms.NumberInput(attrs={'step': '1', 'min': '1'}))
    weight = forms.FloatField(label="Weight (kg): ", widget=forms.NumberInput(attrs={'step': '0.5', 'min': '1'}))
    
    ledv = forms.FloatField(label="LV-EDV (ml)", widget=forms.NumberInput(attrs={'class': 'inline-block','step': '0.5', 'min': '1'}))
    lesv = forms.FloatField(label="LV-ESV (ml)", widget=forms.NumberInput(attrs={'step': '0.5', 'min': '1'}))
    lmm = forms.FloatField(label="Myocardial Mass (g)", widget=forms.NumberInput(attrs={'step': '0.5', 'min': '1'}))
    redv = forms.FloatField(label="RV-EDV (ml)", widget=forms.NumberInput(attrs={'step': '0.5', 'min': '1'}))
    resv = forms.FloatField(label="RV-ESV (ml)", widget=forms.NumberInput(attrs={'step': '0.5', 'min': '1'}))

