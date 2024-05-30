from django.forms import ModelForm
from django import forms
import datetime

from .models import User, Plant, Sowing, Harvest, Tending, YearReview, PlantingYear, UserYear, MONTH_CHOICES


class PlantForm(ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'variety', 'category']

        
class SowForm(ModelForm):
    start_sowing_month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        label="Start Sowing Month",
        required=False,  # Make selection optional (checkbox)
    )
    end_sowing_month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        label="End Sowing Month",
        required=False,  # Make selection optional (checkbox)
    )
    
   # checking to see if the number is positive       
    def clean_depth_cm(self):
        depth_cm = self.cleaned_data['depth_cm']  # Retrieve the value, or None if not provided
        if depth_cm is not None:
            if depth_cm <= 0.0:  # Check if depth_cm is not None before comparison
                raise forms.ValidationError("Depth must be a positive value.")
        return depth_cm

    def clean_spacing_cm(self):
        spacing_cm = self.cleaned_data['spacing_cm']
        if spacing_cm is not None:
            if spacing_cm <= 0.0:
                raise forms.ValidationError("Spacing must be a positive value.")
        return spacing_cm

    def clean_row_spacing_cm(self):
        row_spacing_cm = self.cleaned_data['row_spacing_cm']
        if row_spacing_cm is not None:
            if row_spacing_cm <= 0.0:
                raise forms.ValidationError("Row Spacing must be a positive value.")
        return row_spacing_cm
    
    class Meta:
        model = Sowing
        fields = ['method', 'sowing_comments', 'start_sowing_month', 'end_sowing_month', 'depth_cm', 'spacing_cm', 'row_spacing_cm']


class HarvestForm(ModelForm):
    start_harvest_month = forms.ChoiceField(
        choices=MONTH_CHOICES,  
        label="Start Harvest Month",
        required=False,  # Make selection optional (checkbox)
    )
    end_harvest_month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        label="End Harvest Month",
        required=False,  # Make selection optional (checkbox)
    )
    class Meta:
        model = Harvest
        fields = ['start_harvest_month', 'end_harvest_month', 'cut_and_grow', 'harvest_comments']
				
class TendingForm(ModelForm):
    start_transfer_month = forms.ChoiceField(
        choices=MONTH_CHOICES,  
        label="Start Transfer Month",
        required=False,  # Make selection optional (checkbox)
    )
    end_transfer_month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        label="End Transfer Month",
        required=False,  # Make selection optional (checkbox)
    )
    class Meta:
        model = Tending
        fields = ['light_requirements', 'water_requirements', 'fertilizer_needs', 'pest_control','disease_control', 'thinning', 'start_transfer_month', 'end_transfer_month']
        widgets = {
          'pest_control': forms.Textarea(attrs={'rows':2, 'cols':20}),
          'disease_control': forms.Textarea(attrs={'rows':2, 'cols':20}),	
        }	

class UserYearForm(ModelForm):
    # making sure the year is more than the current year
    def clean_year(self):
        year = self.cleaned_data['year']
        today = datetime.date.today()
        current_year = today.year
        if year < current_year:  # You can adjust the minimum year as needed
            raise forms.ValidationError(f"Year must be greater than or equal to {current_year}")
        return year

    class Meta:
        model = UserYear
        fields = ['year']

class PlantingYearForm(ModelForm):
    sowed = forms.DateField(required=False, widget=forms.SelectDateWidget)
    harvested = forms.DateField(required=False, widget=forms.SelectDateWidget)
    transferred = forms.DateField(required=False, widget=forms.SelectDateWidget)
    
    class Meta:
        model = PlantingYear
        fields = ['sowed', 'harvested', 'transferred']

				
class YearReviewForm(ModelForm):

    # checking to see if the amount is either 0 or above 
    def clean_yield_amount(self):
        yield_amount  = self.cleaned_data['yield_amount']
        if yield_amount < 0.0:
            raise forms.ValidationError("yield_amount must be a positive value or 0.")
        return yield_amount
    
    class Meta:
        model = YearReview
        fields = ['yield_amount', 'review_comments']
        

				