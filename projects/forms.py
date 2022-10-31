from django.forms import ModelForm
from .models import project
from django import forms

class ProjectForm(ModelForm):
    class Meta:
        model=project
        fields=['title','featured_image','description','source_link','demo_link','tags']
        widgets={
            'tags':forms.CheckboxSelectMultiple(),
        }
    def __init__(self,*args,**kwargs):
        super(ProjectForm,self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})