from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Sowing (Choices)
Sowing_Choices = (
    ("IS", "Indirect Sowing"),
    ("DS", "Direct Sowing"),
    ("O", "Other") 
)

# Light Requirements (choices)
LIGHT_REQUIREMENTS_CHOICES = (
    ("FS", "Full Sun"), # (6+ hours of direct sunlight)
    ("PS", "Partial Shade"), # (3-6 hours of direct sunlight)
    ("DS", "Deep Shade"), # (Less than 3 hours of direct sunlight)
)

 # Fertilizer Needs (choices)
FERTILIZER_NEEDS_CHOICES = (
    ("HF", "Heavy Feeder"), #(Needs regular fertilization)
    ("LF", "Light Feeder"), #(Needs occasional fertilization)
    ("NF", "No Fertilizer"), # (Doesn't require additional fertilizer)
)

 # Water Requirements (choices)
WATER_REQUIREMENTS_CHOICES = (
    ("DT", "Drought Tolerant"), #(Needs infrequent watering)
    ("MW", "Moderate Watering"), #(Needs watering when soil dries slightly)
    ("FW", "Frequent Watering"), #(Needs consistent moisture)
)

# month connected with a number for calendar display
MONTH_CHOICES = [
    (1, "January"),
    (2, "February"),
    (3, "March"),
    (4, "April"),
    (5, "May"),
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September"),
    (10, "October"),
    (11, "November"),
    (12, "December")
]

# User Model
class User(AbstractUser):
	pass

# plant model
class Plant(models.Model):
    name = models.CharField(max_length=50)
    variety = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=50, blank=True)  # Optional
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="plants")
    
    def __str__(self):
        return f"{self.name} by {self.user.username}"

# Sowing model
class Sowing(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="sowing")
    method = models.CharField(max_length=3, choices=Sowing_Choices, blank=True)
    sowing_comments = models.CharField(max_length=200, blank=True)
    start_sowing_month = models.IntegerField(choices=MONTH_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(12)])
    end_sowing_month = models.IntegerField(choices=MONTH_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(12)])
    depth_cm = models.DecimalField(max_digits=3, decimal_places=1) # measured in cm
    spacing_cm = models.DecimalField(max_digits=4, decimal_places=1)
    row_spacing_cm = models.DecimalField(max_digits=4, decimal_places=1)
    
    def __str__(self):
        return f"Sowing for {self.plant.name}"

# harvest model
class Harvest(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="harvest")
    start_harvest_month = models.IntegerField(choices=MONTH_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(12)])
    end_harvest_month = models.IntegerField(choices=MONTH_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(12)])
    cut_and_grow = models.BooleanField(default=False)
    harvest_comments = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Harvesting for {self.plant.name}"
    
# tending model
class Tending(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="tending")
    light_requirements = models.CharField(max_length=2, choices=LIGHT_REQUIREMENTS_CHOICES)
    water_requirements = models.CharField(max_length=2, choices=WATER_REQUIREMENTS_CHOICES)
    fertilizer_needs = models.CharField(max_length=2, choices=FERTILIZER_NEEDS_CHOICES)
    pest_control = models.TextField(blank=True) # Notes on common pests and control methods
    disease_control = models.TextField(blank=True)# Notes on common diseases and control methods
    thinning = models.BooleanField(default=False)
    start_transfer_month = models.IntegerField(choices=MONTH_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(12)])
    end_transfer_month = models.IntegerField(choices=MONTH_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(12)]) # if the sowing is indirect then its which months the seed can be transferred outside.
    
    def __str__(self):
        return f"Tending for {self.plant.name}"

# create the year
class UserYear(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_year")
    year = models.IntegerField()  # Year for which the review is done
    
    def __str__(self):
        return f"{self.user.username} is planting in {self.year}"
    

# each plant to each year
class PlantingYear(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="planting_year")
    year = models.ForeignKey(UserYear, on_delete=models.CASCADE, related_name="planting_year")
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="planting_year")
    sowed = models.DateField(blank=True, null=True)
    harvested = models.DateField(blank=True, null=True)
    transferred = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.plant.name} was planted in {self.year}"
    
# review of each plant and year and yield 
class YearReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="year_reviews")
    year = models.ForeignKey(UserYear, on_delete=models.CASCADE, related_name="year_reviews")
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="year_reviews")
    yield_amount = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    review_comments = models.CharField(blank=True, max_length=200)
    
    def __str__(self):
        return f"{self.user.username} reviewed {self.plant.name} for {self.year}"