from django import forms
from .models import StudyGroup, GroupResource

class GroupForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ['name', 'description', 'cover_image', 'is_private']

class GroupResourceForm(forms.ModelForm):
    class Meta:
        model = GroupResource
        fields = ['file']