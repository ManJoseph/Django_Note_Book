from django import forms
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField
from .models import User, VerificationCode


class UserAdminCreationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        strip=False,
    )
    re_password = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta:
        model = User
        fields = ('first_name','email', 'username')   # ← only fields that actually exist

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("re_password")
        if password and re_password and password != re_password:
            raise forms.ValidationError("The two password fields didn't match.")
        return re_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text="Raw passwords are not stored, so there is no way to see "
                  "this user's password, but you can change it using "
                  "<a href=\"../password/\">this form</a>."
    )

    class Meta:
        model = User
        fields = ('first_name','email', 'username', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class CreateAccountForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password",
        required=True,
    )
    re_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password",
        required=True,
    )

    class Meta:
        model = User
        fields = ('first_name','username', 'email', 'password', 're_password')   # ← re_password is extra

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        re_password = cleaned_data.get("re_password")

        if password and re_password and password != re_password:
            raise forms.ValidationError({"re_password": "Passwords do not match."})

        email = cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError({"email": "This email is already in use."})

        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            is_active=True,
        )

        # Generate verification code
        # code = random_with_N_digits(6)   # assuming this function exists
        # code_inst = VerificationCode.objects.create(
        #     user=user,
        #     code=code,
        #     label=VerificationCode.SIGNUP,
        #     email=user.email
        # )

        # context = {
        #     "activate_url": f"http://localhost:8000/activate-account/?code={code_inst.code}&email={code_inst.email}"
        # }
        # send_email_custom(user.email, "Activate your account", context)

        return user


class CustomLoginForm(AuthenticationForm):
    pass