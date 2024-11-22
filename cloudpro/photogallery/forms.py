from django import forms
from .models import Photo, PhotoFolder


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image', 'folder', 'title', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, kwargs)
        if user:
            self.fields['folder'].queryset = PhotoFolder.objects.filter(user=user)


class FolderCreateForm(forms.ModelForm):
    class Meta:
        model = PhotoFolder
        fields = ('name',)


class PhotoEditForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'description']