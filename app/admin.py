from django.contrib import admin

from app.models import User, Plant, Sowing, Harvest, Tending, YearReview, PlantingYear, UserYear
# Register your models here.
admin.site.register(User)
admin.site.register(Plant)
admin.site.register(Sowing)
admin.site.register(Harvest)
admin.site.register(Tending)
admin.site.register(YearReview)
admin.site.register(PlantingYear)
admin.site.register(UserYear)