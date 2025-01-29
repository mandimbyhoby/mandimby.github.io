from django import forms
from .models import ClientRegistration, Schedule

# Form for client registration
class ClientRegistrationForm(forms.ModelForm):
    class Meta:
        model = ClientRegistration
        fields = ['first_name', 'last_name', 'email', 'contact', 'payment_on_day']  # Exclude schedule and registration_date fields

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['name', 'day', 'start_time', 'end_time', 'instructor', 'max_participants']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_max_participants(self):
        max_participants = self.cleaned_data.get('max_participants')
        if max_participants <= 0:
            raise forms.ValidationError("Le nombre maximum de participants doit être supérieur à zéro.")
        return max_participants