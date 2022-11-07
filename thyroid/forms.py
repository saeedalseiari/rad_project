from django import forms


COMPOSITION = [
    ('Completely or almost completely cystic (0)', 'Cystic 0'),
    ('Mixed cystic/solid (1)', 'Mixed cystic solid 1'),
    ('Spongiform, no points for other features (0)', 'Spongiform 0'),
    ('Possibly, but not definitely spongiform (0)', 'Possibly Spongiform 0'),
    ('Solid (2)', 'Solid 2')
]

ECHOGENICITY = [
    ('Hyperechoic (1)', 'Hyperechoic 1'),
    ('Isoechoic (1)', 'Isoechoic 1'),
    ('Hypoechoic (2)', 'Hypoechoic 2'),
    ('Very hypoechoic (3)', 'Very hypoechoic 3'),
    ('Anechoic (0)', 'Anechoic 0'),
    ("Can't be determined (1)", "Can't be determined 1")
]

SHAPE = [
    ('Wider than tall (0)', 'Wider than tall 0'),
    ('Taller than wide (3)', 'Taller than wide 3')
]

MARGINS = [
    ('Smooth (0)', 'Smooth 0'),
    ('Lobulated (2)', 'Lobulated 2'),
    ('Irregular (2)', 'Irregular 2'),
    ('Extrathyroid extension (3)', 'Extrathyroid extension 3'),
    ('Indistinct margins (0)', 'Indistinct margins 0')
]

FOCI =[
    ('No echogenic foci (0)', 'No echogenic foci 0'),
    ('Large comet-tail artifacts (0)', 'Large comet-tail artifacts 0'),
    ('Peripheral calcification (2)', 'Peripheral calcification 2'),
    ('Macrocalcification (1)', 'Macrocalcification 1'),
    ('Multiple punctate echogenic foci (3)', 'Multiple punctate echogenic foci 3')
]

LOBE = [
    ('right', 'Right'),
    ('left', 'Left'),
    ('isthmus', 'Isthmus')
]

ASPECT = [
    ('upper', 'Upper'),
    ('mid', 'Mid'),
    ('lower', 'Lower'),
]

POSITION = [
    ('anteriorly', 'Anteriorly'),
    ('posteriorly', 'Posteriorly'),
]

PARENCHYMA = [
    ('normal', 'Normal'),
    ('mildly heterogenous', 'Mildly heterogenous'),
    ('heterogenous', 'Heterogenous'),
    ('insignificant lesions', 'Insignificant lesions')
]


class NoduleForm(forms.Form):

    parenchyma = forms.ChoiceField(choices=PARENCHYMA, widget=forms.RadioSelect, label="Parenchyma")

    lobe = forms.ChoiceField(choices=LOBE, widget=forms.RadioSelect, label="Lobe")
    aspect = forms.ChoiceField(choices=ASPECT, widget=forms.RadioSelect, label="Aspect")
    position = forms.ChoiceField(choices=POSITION, widget=forms.RadioSelect, label="Position")

    composition = forms.ChoiceField(choices=COMPOSITION, widget=forms.RadioSelect, label="Composition")
    echogenicity = forms.ChoiceField(choices=ECHOGENICITY, widget=forms.RadioSelect, label="Echogenicity")
    shape = forms.ChoiceField(choices=SHAPE, widget=forms.RadioSelect, label="Shape")
    margins = forms.ChoiceField(choices=MARGINS, widget=forms.RadioSelect, label="Margins")
    foci = forms.ChoiceField(choices=FOCI, widget=forms.RadioSelect, label="Echogenic Foci")


    isthmus = forms.FloatField(label="Isthmus AP (cm)", widget=forms.NumberInput(attrs={'step': '0.1', 'min': '0.0'}))
    length = forms.FloatField(label="Length (cm)", widget=forms.NumberInput(attrs={'step': '0.1', 'min': '0.0'}))
    width = forms.FloatField(label="Width (cm)", widget=forms.NumberInput(attrs={'step': '0.1', 'min': '0.0'}))
    height = forms.FloatField(label="Height (cm)", widget=forms.NumberInput(attrs={'step': '0.1', 'min': '0.0'}))
    rt_vol = forms.FloatField(label="Right lobe volume (cc)", widget=forms.NumberInput(attrs={'step':'0.1', 'min': '0.0'}))
    lt_vol = forms.FloatField(label="Left lobe volume (cc)", widget=forms.NumberInput(attrs={'step': '0.1', 'min': '0.0'}))

    nodule_num = forms.IntegerField(label="Nodule to be modified:", required=False, widget=forms.NumberInput(attrs={'step': '1', 'min': '0'}))



