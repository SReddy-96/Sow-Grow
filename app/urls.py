from django.urls import path

from . import views

# url paths
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addPlant", views.addPlant, name="addPlant"),
    path("addPlantData/<int:plant_id>", views.addPlantData, name="addPlantData"),
    path("profile", views.profile, name="profile"),
    path("plantProfile/<int:plant_id>", views.plantProfile, name="plantProfile"),
    path("addAYear", views.AddAYear, name="addAYear"),
    path("year/<int:year_id>", views.Year, name="year"),
    path("year/<int:year_id>/delete/<int:plant_id>", views.deletePlantYear, name="delete_plant_from_year" ),
    path("year/<int:year_id>/review/<int:plant_id>", views.reviewPlantYear, name="reviewPlantYear"),
    path("year/<int:year_id>/addActions/<int:plant_id>", views.addActions, name="addActions"),
    path("year/<int:year_id>/deleteEntireYear", views.deleteEntireYear, name="deleteEntireYear"),
    path("termsAndConditions", views.termsAndConditions, name="termsAndConditions"),
]