
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template import loader
from django.http import Http404
from collections import defaultdict

from .forms import *
from .models import *

# Create your views here.

# to handle the error page.
def render_error(request, error_message):
    return render(request, "app/error.html", {
        "code": 400,
        "message": error_message,
        **base_context(request),
    })

# to display the users years in navbar
def base_context(request):
    if request.user.is_authenticated:
        userYears = UserYear.objects.filter(user=request.user)
    else:
        userYears = None
    return {'userYears': userYears}


def index(request):
    return render(request, "app/index.html", {
        **base_context(request),
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "app/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "app/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "app/register.html")

@login_required
def addPlant(request):
    current_user = request.user

    if request.method == "POST":
        form = PlantForm(request.POST)
        
        # validate form 
        if form.is_valid():
            name = form.cleaned_data['name']
            variety = form.cleaned_data['variety']
            category = form.cleaned_data['category']
            
            # using try catch to add the input as a new row in plant
            try: 
                new_plant = Plant(name=name, variety=variety, category=category, user=current_user)
                new_plant.save()
            
            except Exception as e:
                return render_error(request, e)
            
            return redirect('addPlantData', plant_id=new_plant.id)

        # invalid form
        else:
                return render_error(request, 'Invalid Form')
        
    # GET request        
    return render(request, 'app/addPlant.html',{
        "plantForm": PlantForm(),
        **base_context(request),        
    })

@login_required
def addPlantData(request, plant_id):
    plant = Plant.objects.get(pk=plant_id)
    # POST request
    if request.method == "POST":
        sowForm = SowForm(request.POST)
        tendingForm = TendingForm(request.POST)
        harvestForm = HarvestForm(request.POST)
        
        # validate sow form 
        if sowForm.is_valid():
            method = sowForm.cleaned_data['method']
            sowing_comments = sowForm.cleaned_data['sowing_comments']
            start_sowing_month = sowForm.cleaned_data['start_sowing_month']
            end_sowing_month = sowForm.cleaned_data['end_sowing_month']
            depth_cm = sowForm.cleaned_data['depth_cm']
            spacing_cm = sowForm.cleaned_data['spacing_cm']
            row_spacing_cm = sowForm.cleaned_data['row_spacing_cm']

            # using try catch to add the input as a new row in plant
            try: 
                new_plant_sowing = Sowing(method=method, sowing_comments=sowing_comments, start_sowing_month=start_sowing_month, end_sowing_month=end_sowing_month, depth_cm=depth_cm, spacing_cm=spacing_cm, row_spacing_cm=row_spacing_cm, plant=plant)
                new_plant_sowing.save()
            
            except Exception as e:
                return render_error(request, e)
            
        # invalid form
        else:
            return render_error(request, e) 
        
        # validate tending form 
        if tendingForm.is_valid():
            light_requirements = tendingForm.cleaned_data['light_requirements']
            water_requirements = tendingForm.cleaned_data['water_requirements']
            fertilizer_needs = tendingForm.cleaned_data['fertilizer_needs']
            pest_control = tendingForm.cleaned_data['pest_control']
            disease_control = tendingForm.cleaned_data['disease_control']
            thinning = tendingForm.cleaned_data['thinning']
            start_transfer_month = tendingForm.cleaned_data['start_transfer_month']
            end_transfer_month = tendingForm.cleaned_data['end_transfer_month']
            
            # using try catch to add the input as a new row in plant
            try: 
                new_plant_tending = Tending(light_requirements=light_requirements, water_requirements=water_requirements, fertilizer_needs=fertilizer_needs, pest_control=pest_control, disease_control=disease_control, thinning=thinning, start_transfer_month=start_transfer_month, end_transfer_month=end_transfer_month, plant=plant)
                new_plant_tending.save()
            
            except Exception as e:
                return render_error(request, e)
            
        # invalid form
        else:
            return render_error(request, tendingForm.errors)
        
        # validate harvest form 
        if harvestForm.is_valid():
            start_harvest_month = harvestForm.cleaned_data['start_harvest_month']
            end_harvest_month = harvestForm.cleaned_data['end_harvest_month']
            cut_and_grow = harvestForm.cleaned_data['cut_and_grow']
            harvest_comments = harvestForm.cleaned_data['harvest_comments']            

            # using try catch to add the input as a new row in plant
            try: 
                new_plant_harvest = Harvest(plant=plant, start_harvest_month=start_harvest_month, end_harvest_month=end_harvest_month, cut_and_grow=cut_and_grow, harvest_comments=harvest_comments)
                new_plant_harvest.save()
            
            except Exception as e:
                return render_error(request, e)

        # invalid form
        else:
            return render_error(request, harvestForm.errors)
        
        return HttpResponseRedirect(reverse('profile'))
            

    return render(request, 'app/addPlantData.html', {
        'sowingForm': SowForm(),
        "tendingForm": TendingForm(),
        "harvestForm": HarvestForm(),
        "plant": plant,
        **base_context(request),
    })

@login_required
def profile(request):

    # Get the current user
    current_user = get_object_or_404(User, pk=request.user.id)

    # filter years users has
    try:
        get_user_years = UserYear.objects.filter(user=current_user)
        user_years = get_user_years.order_by('year')
    except Exception as e:
        return render_error(request, e)
    
    print(user_years)
    # filter planting review user has
    try:
        plant_reviews = YearReview.objects.filter(user=current_user)
    except Exception as e:
        return render_error(request, e)
    
    # get all the users plants to display on profile
    try:
        users_plants = Plant.objects.filter(user=current_user)
    except Exception as e:
        return render_error(request, e)

    # get all the users plants sowed, transferred and harvested to display on each year
    try:
        user_plants_actions = PlantingYear.objects.filter(user=current_user)
    except Exception as e:
        return render_error(request, e)

    # Group plant_reviews by year
    reviews_by_year = defaultdict(list)
    for review in plant_reviews:
        reviews_by_year[review.year.id].append(review)

    return render(request, 'app/profile.html', {
        "plants": users_plants,
        "current_user": current_user,
        **base_context(request),
        "user_years": user_years,
        "reviews_by_year": reviews_by_year,
        "user_plants_actions": user_plants_actions,
    })


# the update and delete for a page
@login_required
def plantProfile(request, plant_id):
    current_plant = get_object_or_404(Plant, pk=plant_id)
    current_sowing = get_object_or_404(Sowing, plant=current_plant)
    current_harvest = get_object_or_404(Harvest, plant=current_plant)
    current_tending = get_object_or_404(Tending, plant=current_plant)

    if request.method == 'POST':
        if 'updateForm' in request.POST:
            plantForm = PlantForm(request.POST, instance=current_plant)
            sowingForm = SowForm(request.POST, instance=current_sowing)
            harvestForm = HarvestForm(request.POST, instance=current_harvest)
            tendingForm = TendingForm(request.POST, instance=current_tending)

            # using an array to iterate over the forms to see if they are valid and then save the updated data to the model
            forms = [plantForm, sowingForm, harvestForm, tendingForm]
            if all(form.is_valid() for form in forms):
                try:
                    for form in forms:
                        form.save()
                    return HttpResponseRedirect(reverse('profile'))
                except Exception as e:
                    return render_error(request, e)
            else:
                return render_error(request, "One or more forms are invalid.")

        elif 'deletePlant' in request.POST:
            try:
                current_plant.delete()
                return HttpResponseRedirect(reverse('profile'))
            except Exception as e:
                return render_error(request, e)

        else:
            return render_error(request, 'Invalid POST request.')

    else:  # GET request
        plantForm = PlantForm(instance=current_plant)
        sowingForm = SowForm(instance=current_sowing)
        harvestForm = HarvestForm(instance=current_harvest)
        tendingForm = TendingForm(instance=current_tending)

        return render(request, 'app/plantProfile.html', {
            "plantForm": plantForm,
            "sowingForm": sowingForm,
            "harvestForm": harvestForm,
            "tendingForm": tendingForm,
            "plant": current_plant,
            **base_context(request),
        })

@login_required
def AddAYear(request):
    current_user = request.user
    

    if request.method == 'POST':
        yearForm = UserYearForm(request.POST) 

        if yearForm.is_valid():
            year = yearForm.cleaned_data['year']

            # making user not to have the same year
            if UserYear.objects.filter(user=current_user, year=year).exists():
                return render_error(request, "This year already exists")
            
            try:
                new_year = UserYear(user=current_user, year=year)
                new_year.save()
            except Exception as e:
                return render_error(request, e)
            return HttpResponseRedirect(reverse('year', args=[new_year.id]))
        else:
            return render_error(request, yearForm.errors)

    else: # GET request    
        return render(request, "app/addAYear.html", {
            "yearForm": UserYearForm(),
            **base_context(request),
            
        })

@login_required
def Year(request, year_id):
    current_year = get_object_or_404(UserYear, pk=year_id)

    # handling selection of plant for year
    if request.method == 'POST':
        plant_id = request.POST.get('plantSelector')
        if plant_id:
            try:
                selected_plant = Plant.objects.get(pk=plant_id, user=request.user)
                user_plant = PlantingYear(plant=selected_plant, user=request.user, year=current_year)
                user_plant.save()
            except Exception as e:
                return render_error(request, e)  

            return HttpResponseRedirect(reverse('year', args=[year_id]))
        
    else: # GET request    

        # get users plants to add to selection input
        try:
            users_plants = Plant.objects.filter(user=request.user)
        except Exception as e:
            return render_error(request, e) 
        
        # getting all plants from that year then putting them in alphabetical order by plant name
        try:
            gathering_plants = PlantingYear.objects.filter(year=current_year, user=request.user)
            current_planting_years = gathering_plants.order_by('plant__name')
        except PlantingYear.doesNotExist:
            return render(request, 'app/year.html', {
                **base_context(request),
                'current_year': current_year,
                'plants': users_plants,
                "plants_data": None,
            })  

        plants_data = []
            
        # creating a dict for each plant with all the data
        for planting_year in current_planting_years:
            plant = planting_year.plant
            sowing = Sowing.objects.filter(plant=plant).first()
            harvest = Harvest.objects.filter(plant=plant).first()
            tending = Tending.objects.filter(plant=plant).first()


            # Calculate colspan for each activity
            sowing_colspan = sowing.end_sowing_month - sowing.start_sowing_month + 1 if sowing else 0
            harvest_colspan = harvest.end_harvest_month - harvest.start_harvest_month + 1 if harvest else 0
            tending_colspan = tending.end_transfer_month - tending.start_transfer_month + 1 if tending else 0

            # calculate month numbers
            sowing_month_numbers = range(sowing.start_sowing_month, sowing.end_sowing_month + 1)
            harvest_month_numbers = range(harvest.start_harvest_month, harvest.end_harvest_month + 1)
            tending_month_numbers = range(tending.start_transfer_month, tending.end_transfer_month + 1)

            # filling in review form if there is already a review
            try:
                current_review = get_object_or_404(YearReview, user=request.user, plant=plant, year=current_year)  
            except Http404:
                current_review = None # saving as none for empty form
                
            plants_data.append({
                'plant': plant,
                'sowing': sowing,
                'harvest': harvest,
                'tending': tending,
                "sowing_colspan": sowing_colspan,
                "harvest_colspan": harvest_colspan,
                "tending_colspan": tending_colspan,
                "sowing_month_numbers": sowing_month_numbers,
                "harvest_month_numbers":harvest_month_numbers,
                "tending_month_numbers": tending_month_numbers,
                "planting_year": planting_year,
                "year_review_form": YearReviewForm(instance=current_review),
                })


        return render(request, 'app/year.html', {
            **base_context(request),
            'current_year': current_year,
            'plants': users_plants,
            "plants_data": plants_data,
            "months": MONTH_CHOICES,
            "planting_year_form": PlantingYearForm(),

        })

# handle deleting the plant from the year
@login_required 
def deletePlantYear(request, year_id, plant_id):

    if request.method == 'POST':
        plant = get_object_or_404(Plant, pk=plant_id)
        planting_year = get_object_or_404(UserYear, pk=year_id)

        try:
            deleted_plant = PlantingYear.objects.get(user=request.user, year=planting_year, plant=plant)
            deleted_plant.delete()
        except Exception as e:
            return render_error(request, e) 

        return HttpResponseRedirect(reverse('year', args=[year_id]))
    else:
        return render_error(request, 'Has to be a POST Request')

# handle the review of a plant for a certain year
@login_required
def reviewPlantYear(request, year_id, plant_id):

    if request.method == 'POST':
        plant = get_object_or_404(Plant, pk=plant_id)
        planting_year = get_object_or_404(UserYear, pk=year_id)
        plant_review = YearReviewForm(request.POST) 

        if plant_review.is_valid():
            yield_amount = plant_review.cleaned_data['yield_amount']
            review_comments = plant_review.cleaned_data['review_comments']
            
            # if there are any other reviews then it deletes them
            try:
                current_review = get_object_or_404(YearReview, user=request.user, plant=plant, year=planting_year)
                current_review.delete()
            except Http404:
                pass

            # create the review
            try:
                add_review = YearReview(user=request.user, year=planting_year, plant=plant, yield_amount=yield_amount, review_comments=review_comments)
                add_review.save()
            except Exception as e:
                return render_error(request, e)

            return HttpResponseRedirect(reverse('year', args=[year_id]))
        
        else:
            return render_error(request, plant_review.errors)
    else:
        return render_error(request, 'Has to be a POST Request')

# add actions to planting year model 
@login_required
def addActions(request, year_id, plant_id):

    if request.method == 'POST':
        plant = get_object_or_404(Plant, pk=plant_id)
        planting_year = get_object_or_404(UserYear, pk=year_id)
        planting_actions = PlantingYearForm(request.POST) 

        if planting_actions.is_valid():
            sowed = planting_actions.cleaned_data['sowed']
            transferred = planting_actions.cleaned_data['transferred']
            harvested = planting_actions.cleaned_data['harvested']

            # update the actions in planting year, checking data to see if it has changed, then it'll update 
            try:
                planting_year_object = PlantingYear.objects.get(plant=plant, year=planting_year)
                if 'sowed' in planting_actions.changed_data:
                    planting_year_object.sowed = sowed
                if 'transferred' in planting_actions.changed_data:
                    planting_year_object.transferred = transferred
                if 'harvested' in planting_actions.changed_data:
                    planting_year_object.harvested = harvested
                planting_year_object.save()
            except Exception as e:
                return render_error(request, e)

            return HttpResponseRedirect(reverse('year', args=[year_id]))
        
        else:
            return render_error(request, planting_actions.errors)
        
    else:
        return render_error(request, 'Has to be a POST Request')

# handle deleting the entire year
@login_required
def deleteEntireYear(request, year_id):

    if request.method == 'POST':
        try:
            deleted_plant = UserYear.objects.get(user=request.user, pk=year_id)
            deleted_plant.delete()
        except Exception as e:
            return render_error(request, e) 

        return HttpResponseRedirect(reverse('index'))
    else:
        return render_error(request, 'Has to be a POST Request')

def termsAndConditions(request):
    return render(request, 'app/termsAndConditions.html', {
        **base_context(request),
    })