from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, Profile
from django.utils import timezone

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = CustomUser
        fields = ["email"]

        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white",
                "placeholder": "Email"
            }),
            "password1": forms.PasswordInput(attrs={
                "class": "block w-full rounded-md border bg-white px-3 py-2 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 focus:outline-2 focus:-outline-offset-2 focus:outline-primary-600 sm:text-sm/6",
                "placeholder": "Enter password",
            }),
            "password2": forms.PasswordInput(attrs={
                "class": "block w-full rounded-md border bg-white px-3 py-2 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 focus:outline-2 focus:-outline-offset-2 focus:outline-primary-600 sm:text-sm/6",
                "placeholder": "Confirm password",
            }),
        }
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].help_text = None

    def save(self, request):
        user = super().save(request)
        user.save()
        return user

        
class UserProfileUpdateForm(forms.ModelForm):
    nickname = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)
    address = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    profile_picture = forms.ImageField(required=False)
    bio = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ['email']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Ensure Profile fields are saved too
            profile, created = Profile.objects.get_or_create(user=user)
            profile.nickname = self.cleaned_data.get('nickname', profile.nickname)
            profile.first_name = self.cleaned_data.get('first_name', profile.first_name)
            profile.last_name = self.cleaned_data.get('last_name', profile.last_name)
            profile.phone_number = self.cleaned_data.get('phone_number', profile.phone_number)
            profile.address = self.cleaned_data.get('address', profile.address)
            profile.date_of_birth = self.cleaned_data.get('date_of_birth', profile.date_of_birth)
            profile.profile_picture = self.cleaned_data.get('profile_picture', profile.profile_picture)
            profile.bio = self.cleaned_data.get('bio', profile.bio)
            profile.save()  # Ensure saving the profile instance
        return user
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("Email already in use.")
        return email
    
    def clean_nickname(self):
        nickname = self.cleaned_data.get("nickname")
        if nickname and Profile.objects.exclude(user=self.instance).filter(nickname=nickname).exists():
            raise forms.ValidationError("Nickname already in use.")
        return nickname

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number:
            return None  # So the DB stores it as NULL
        if Profile.objects.exclude(user=self.instance).filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Phone number already in use.")
        return phone_number

    
    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get("profile_picture")
        if profile_picture and not profile_picture.name.endswith(('.png', '.jpg', '.jpeg')):
            raise forms.ValidationError("Profile picture must be a PNG or JPG image.")
        return profile_picture
    
    def clean_bio(self):
        bio = self.cleaned_data.get("bio")
        if bio and len(bio) > 1000:
            raise forms.ValidationError("Bio cannot exceed 1000 characters.")
        return bio

    
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if len(first_name) < 2:
            raise forms.ValidationError("First name must be at least 2 characters long.")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if len(last_name) < 2:
            raise forms.ValidationError("Last name must be at least 2 characters long.")
        return last_name
    
    def clean_address(self):
        address = self.cleaned_data.get("address")
        if len(address) < 5:
            raise forms.ValidationError("Address must be at least 5 characters long.")
        return address
    
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get("date_of_birth")
        if date_of_birth and date_of_birth > timezone.now().date():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        return date_of_birth


class UserInfoForm(forms.ModelForm):
    nickname = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = Profile
        fields = ['nickname', 'first_name', 'last_name']


class AccountInfoForm(forms.ModelForm):
    phone_number = forms.CharField(required=True)
    address = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'date_of_birth']


class SocialAccountsForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = []


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={
            "class": "block w-full rounded-md border bg-white px-3 py-2 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 focus:outline-2 focus:-outline-offset-2 focus:outline-primary-600 sm:text-sm/6",
            "placeholder": "Enter old password",
        }),
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            "class": "block w-full rounded-md border bg-white px-3 py-2 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 focus:outline-2 focus:-outline-offset-2 focus:outline-primary-600 sm:text-sm/6",
            "placeholder": "Enter new password",
        }),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            "class": "block w-full rounded-md border bg-white px-3 py-2 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 focus:outline-2 focus:-outline-offset-2 focus:outline-primary-600 sm:text-sm/6",
            "placeholder": "Confirm new password",
        }),
    )