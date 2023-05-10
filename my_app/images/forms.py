from django import forms

from images.models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image_name']

    def clean_image_data(self):
        image = self.cleaned_data.get('image_data')
        if image:
            return image.read()
        return None
