from django import forms
from django.contrib.auth.forms import UserCreationForm
from . models import UserProfile, Task
from django.contrib.auth import authenticate

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=60, help_text='Required. Add a valid email address')

    class Meta:
        model = UserProfile
        fields = ('email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """
          specifying styles to fields 
        """
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in (self.fields['email'], self.fields['username'], self.fields['password1'], self.fields['password2']):
            field.widget.attrs.update({'class': 'form-control '})


class UserAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('email', 'password')
    
    def __init__(self, *args, **kwargs):
        """
          specifying styles to fields 
        """
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        for field in (self.fields['email'], self.fields['password']):
            field.widget.attrs.update({'class': 'form-control '})

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login')


class TaskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Add new task...'}))
    description = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Add description...'}))
    due_date = forms.DateField(widget=forms.SelectDateWidget())

    class Meta:
        model = Task
        fields = ('title', 'description', 'category', 'due_date')
