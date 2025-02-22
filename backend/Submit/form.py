from django import forms

class SubmitIDForm(forms.Form):
    submit_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class CrossAnalysisForm(forms.Form):
    question_id_1 = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    question_id_2 = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
