from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ('title', 'content',)

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['title'].widget.attrs.update({ 
            'class': 'document_title', 
            'required':'', 
            'name':'title', 
            'id':'title', 
            'type':'text', 
            'placeholder':'إضافة عنوان للوثيقة...', 
            }) 