# Importing the forms module from Django for creating HTML forms.
from django import forms 
# Importing the UserCreationForm provided by Django for user registration.
from django.contrib.auth.forms import UserCreationForm
# Importing the authenticate function from Django for user authentication.
from django.contrib.auth import authenticate
# Importing the Account model from the 'account' app.
from account.models import Account

# Form for user registration.
class RegistrationForm(UserCreationForm):
# Adding an email field to the form.
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

    class Meta:
        # Specifying the model to use for the form.
        model = Account 
        # Defining the fields to include in the form.
        fields = ("email", "username", "password1", "password2")

# Form for user authentication.
class AccountAuthenticationForm(forms.ModelForm):
    # Adding a password field to the form.
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta:
         # Specifying the model to use for the form. 
        model = Account
        # Defining the fields to include in the form.
        fields = ('email', 'password')
    # Custom clean method to authenticate user.
    def clean(self):
        # Checking if the form is valid.
        if self.is_valid():
         # Retrieving the cleaned email data from the form.
         email = self.cleaned_data['email']
         # Retrieving the cleaned password data from the form.
         password = self.cleaned_data['password']
        # Authenticating the user using the provided email and password.
        if not authenticate(email=email, password=password):
            # Raising a validation error if authentication fails.
            raise forms.ValidationError("Invalid login")

# Form for updating user account details.
class AccountUpdateForm(forms.ModelForm):

    class Meta:
        # Specifying the model to use for the form
        model = Account 
        # Defining the fields to include in the form.
        fields = ('email', 'username')
    # Custom clean method to check if email is unique.
    def clean_email(self):
        # Checking if the form is valid.
        if self.is_valid():
            # Retrieving the cleaned email data from the form.
            email = self.cleaned_data['email']
            # Querying the database to check if the email is already in use.
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                # Returning the email if it is unique.
                return email
            # Raising a validation error if the email is not unique.
            raise forms.ValidationError('Email "%s" is already in use.' % email)
    # Custom clean method to check if username is unique.
    def clean_username(self):
        # Checking if the form is valid.
        if self.is_valid():
            # Retrieving the cleaned username data from the form.
            username = self.cleaned_data['username']
            # Querying the database to check if the username is already in use.
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                # Returning the username if it is unique.
                return username
            # Raising a validation error if the username is not unique.
            raise forms.ValidationError('Username "%s" is already in use.' % username)
