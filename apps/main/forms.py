from django import forms
from apps.users.models import Alert

class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['min_temp_c', 'max_temp_c', 'rain_probability', 'message']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom styling and widgets
        self.fields['min_temp_c'].widget = forms.NumberInput(
            attrs={
                'class': 'block w-full pr-12 border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500',
                'step': '0.1',
                'min': -50,  # Reasonable minimum temperature
                'max': 50,   # Reasonable maximum temperature
                'placeholder': '20'
            }
        )
        
        self.fields['max_temp_c'].widget = forms.NumberInput(
            attrs={
                'class': 'block w-full pr-12 border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500',
                'step': '0.1',
                'min': -50,
                'max': 50,
                'placeholder': '40'
            }
        )
        
        self.fields['rain_probability'].widget = forms.NumberInput(
            attrs={
                'class': 'block w-full pr-12 border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500',
                'step': '1',
                'min': '0',
                'max': '100',
                'placeholder': '70'
            }
        )
        
        self.fields['message'].widget = forms.TextInput(
            attrs={
                'class': 'block w-full border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Enter alert message'
            }
        )

    def clean(self):
        cleaned_data = super().clean()
        min_temp = cleaned_data.get('min_temp_c')
        max_temp = cleaned_data.get('max_temp_c')
        rain_prob = cleaned_data.get('rain_probability')

        # Validate temperature range
        if min_temp is not None and max_temp is not None:
            if min_temp >= max_temp:
                raise forms.ValidationError(
                    "Minimum temperature must be less than maximum temperature."
                )

        # Validate rain probability range
        if rain_prob is not None:
            if rain_prob < 0 or rain_prob > 100:
                raise forms.ValidationError(
                    "Rain probability must be between 0 and 100."
                )

        return cleaned_data
