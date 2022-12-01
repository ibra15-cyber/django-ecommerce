from .models import *
from django import forms



class ProfileForm(forms.ModelForm):
    """Form definition for MODELNAME."""

    class Meta:
        """Meta definition for MODELNAMEform."""
        Abstract = True
        model = Profile
        fields = (
                    )
