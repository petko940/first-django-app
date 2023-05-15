from django import forms

from images.models import Image


class ImageForm(forms.ModelForm):
    image_name = forms.CharField(max_length=30,widget=forms.TextInput(
        attrs={'placeholder': 'Enter image name',
               'class': 'upload-name-image'}),
        label=''
    )

    class Meta:
        model = Image
        fields = ['image_name']

    def clean_image_data(self):
        image = self.cleaned_data.get('image_data')
        if image:
            return image.read()
        return None
