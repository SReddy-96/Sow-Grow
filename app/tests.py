from django.test import TestCase
from .forms import SowForm, YearReviewForm, UserYearForm
import uuid

import pdb;

# Create your tests here.
from .models import User, Plant, UserYear

class BaseFormTestCase(TestCase):
    # creating a all round class for plant and user to use on all tests.
    @classmethod
    def setUpTestData(cls):
        # Create instances of related models that are commonly used in form tests
        cls.username = f"testuser_{uuid.uuid4().hex[:6]}" # generating a unique ID for each user
        cls.user = User.objects.create(username=cls.username)
        cls.plant = Plant.objects.create(user=cls.user, name='Test Plant')
        cls.userYear = UserYear.objects.create(user=cls.user, year=3000)

    # Add more common setup methods as needed

    def setUp(self):
        # Call the superclass's setUp method to ensure common setup is executed
        super().setUp()

class SowFormTest(BaseFormTestCase):

    # mock data for testing
    mock_data = {}
    def setUp(self):
        super().setUpTestData()
        self.mock_data = {
            'user': self.user.pk,
            'plant': self.plant.pk,
            'method': "IS",
            'start_month': 2,
            'end_month': 4,
            'depth_cm': 1.1,
            'spacing_cm': 10.1,
            'row_spacing_cm': 10.1,
            }
        
    # testing depth_cm
    def test_clean_depth_cm_invalid(self):
        self.mock_data['depth_cm'] = -1.1
        form = SowForm(data=self.mock_data)
        self.assertFalse(form.is_valid())
        
    def test_clean_depth_cm(self):
        self.mock_data['depth_cm'] = 1.1
        form = SowForm(data=self.mock_data)
        self.assertTrue(form.is_valid())

    # testing spacing_cm
    def test_clean_spacing_cm_invalid(self):
        self.mock_data['spacing_cm'] = -10.1
        form = SowForm(data=self.mock_data)
        self.assertFalse(form.is_valid())
        
    def test_clean_spacing_cm(self):
        self.mock_data['spacing_cm'] = 10.1
        form = SowForm(data=self.mock_data)
        self.assertTrue(form.is_valid())

    # testing row spacing cm
    def test_clean_row_spacing_cm_invalid(self):
        self.mock_data['row_spacing_cm'] = -10.1
        form = SowForm(data=self.mock_data)
        self.assertFalse(form.is_valid())
        
    def test_clean_row_spacing_cm(self):
        self.mock_data['row_spacing_cm'] = 10.1
        form = SowForm(data=self.mock_data)
        self.assertTrue(form.is_valid())
        
class UserYearFormTest(BaseFormTestCase):
    
    # creating mock data to create valid form
    mock_data = {}
    def setUp(self):
        super().setUpTestData()
        self.mock_data = {
            'user': self.user.pk,
            'year': 2020
            }
        
    # testing planting year form year 
    def test_clean_year_invalid(self):
        self.mock_data['year'] = 2020
        form = UserYearForm(data=self.mock_data)
        self.assertFalse(form.is_valid())
        
    def test_clean_year(self):
        self.mock_data['year'] = 2025
        form = UserYearForm(data=self.mock_data)
        self.assertTrue(form.is_valid())
        
        
class YearReviewFormTest(BaseFormTestCase):
    
    mock_data = {}
    def setUp(self):
        super().setUpTestData()
        self.mock_data = {
            'user': self.user.pk,
            'plant': self.plant.pk,
            'year': self.userYear.pk
            }

    # testing yield 
    def test_clean_yield_amount_invalid(self):
        self.mock_data['yield_amount'] = -100
        form = YearReviewForm(data=self.mock_data)
        self.assertFalse(form.is_valid())
        
    def test_clean_yield_amount(self):
        self.mock_data['yield_amount'] = 100
        form = YearReviewForm(data=self.mock_data)
        self.assertTrue(form.is_valid())