from django.test import TestCase
from django.urls import reverse  # Import reverse function
from django.contrib.auth.models import User
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import views as auth_views
from .forms import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Create your tests here.


#Create testing for views.users:
class UserRegisterViewsTest(TestCase):
    
    def test_register_view_GET(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'users/register.html')

    def test_register_view_POST_valid_data(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(reverse('register'), data)  # Use the correct URL name for registration
        self.assertEqual(response.status_code, 302)  # 302 is the status code for a redirect
        self.assertRedirects(response, reverse('login'))
        
class UserProfileViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='Testing321'
        )
        self.client.login(username='testuser', password='testpassword123')

    def test_register_view_GET(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response,'users/profile.html')

#Create testing for models.users:

class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up a user for testing
        test_user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_profile(self):
        user = User.objects.get(id=1)
        profile = Profile.objects.create(user=user, image='test.jpg')
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.image, 'profile_pics/test.jpg')    


#Create testing for forms.users:
class UserRegisterFormTest(TestCase):
    def test_valid_user_registration_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_registration_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'invalid_email',
            'password1': 'testpassword123',
            'password2': 'mismatched_password',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

class UserUpdateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')

    def test_valid_user_update_form(self):
        form_data = {
            'username': 'updatedusername',
            'email': 'updatedemail@example.com',
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_user_update_form(self):
        form_data = {
            'username': '',
            'email': 'invalid_email',
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())

class ProfileUpdateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        cls.profile = Profile.objects.create(user=cls.user, image='test.jpg')

    def test_valid_profile_update_form(self):
        form_data = {}
        form = ProfileUpdateForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_invalid_profile_update_form(self):
        form_data = {'image': 'invalid_image.txt'}
        form = ProfileUpdateForm(data=form_data, instance=self.profile)
        self.assertFalse(form.is_valid())