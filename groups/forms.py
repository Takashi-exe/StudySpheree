from django import forms
from .models import StudyGroup

class GroupForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ['name', 'description', 'cover_image', 'is_private']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
