from django import forms
from .models import CustomUser
from django.utils import timezone
from django.forms.widgets import DateInput, PasswordInput
import os
from organizer.models import Organizer
from ckeditor.widgets import CKEditorWidget


class UserRegistrationForm(forms.ModelForm):
    organization = forms.ChoiceField(choices=[('user', 'User'), ('organizer', 'Organizer')])

    # Organizer fields
    organization_name = forms.CharField(max_length=100, required=False)
    organization_description = forms.CharField(widget=CKEditorWidget(), required=False)
    organization_logo = forms.ImageField(required=False)
    organization_address = forms.CharField(widget=forms.Textarea, required=False)
    organization_type = forms.CharField(max_length=20, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'phone_number', 'address', 'photo', 'date_of_birth', 'gender',
                  'country', 'city', 'state']
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),  # Set the widget for date_of_birth field to DateInput
            'password': PasswordInput(),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']

        if phone_number and len(phone_number) < 10:
            raise forms.ValidationError('Phone number must be at least 10 digits long.')

        return phone_number

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']

        if date_of_birth and date_of_birth >= timezone.now().date():
            raise forms.ValidationError('Date of birth cannot be in the future.')

        return date_of_birth

    def clean_photo(self):
        photo = self.cleaned_data['photo']

        if photo:
            if photo.size > 2 * 1024 * 1024:
                raise forms.ValidationError('The photo size should not exceed 2MB.')

            allowed_extensions = ['jpeg', 'jpg', 'png']
            ext = os.path.splitext(photo.name)[1].lower()
            if not ext or ext[1:] not in allowed_extensions:
                raise forms.ValidationError('Please upload a valid photo in JPEG, JPG, or PNG format.')

        return photo

    def save(self, *args, **kwargs):
        organization = self.cleaned_data.get('organization')
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if organization == 'organizer':
            user.save()
            organizer = Organizer(user=user)
            organizer.organization_name = self.cleaned_data['organization_name']
            organizer.organization_description = self.cleaned_data['organization_description']
            organizer.organization_logo = self.cleaned_data['organization_logo']
            organizer.organization_address = self.cleaned_data['organization_address']
            organizer.organization_type = self.cleaned_data['organization_type']
            organizer.save()
        else:
            user.save()

        return user
