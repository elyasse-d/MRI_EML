import datetime
import numpy as np
import cv2  
import tensorflow as tf
import os

from django.contrib import messages
from django.contrib.auth import login as auth_login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages import error 
from django.db import utils as db_utils
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView

from .forms import CustomUserCreationForm, LoginForm, ProfileEditForm
from .models import CustomUser, Profile, ScanHistory

# Machine Learning
from django.conf import settings
from django.core.files.storage import default_storage
from django.apps import apps
from django.forms.models import model_to_dict
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input  
from tensorflow.keras.models import load_model  
from tensorflow.keras.applications.resnet50 import preprocess_input  
import logging 
from django.utils.text import slugify

print(tf.__version__)

app_name = 'brainy'
def load_model(path):
    mpath= os.path.join(settings.MEDIA_ROOT, path)
    model = tf.keras.models.load_model(mpath)
    return model

logger = logging.getLogger(__name__)

def custom_logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('/login/')

def Home(request):
    return render(request,'brainy/index.html')

def Login(request):
    return render(request, 'brainy/login.html')

def profil(request):
    if request.user.is_authenticated:
        user = request.user
        profile = user.profile  
        return render(request, 'brainy/profile.html', {
            'profile': profile,
        })
    else:
        return redirect('login')



def edit_profile(request):
    if request.user.is_authenticated:
        user = request.user
        profile = user.profile

        if request.method == 'POST':
            form = ProfileEditForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile was successfully updated.')
                # Render the same page with a success message
                return render(request, 'brainy/edit_profile.html', {'form': form, 'profile': profile})
            else:
                # If the form is not valid, render the page with error messages
                messages.error(request, 'Please correct the error below.')
                # Pass the form along with the profile object
                return render(request, 'brainy/edit_profile.html', {'form': form, 'profile': profile})
        else:
            form = ProfileEditForm(instance=profile)
        
        return render(request, 'brainy/edit_profile.html', {'form': form, 'profile': profile})
    else:
        return redirect('login')
def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                Profile.objects.create(
                    user=user,
                    profile_picture='/profile_pictures/avatar.jpeg',  # Provide the path to your default profile picture  
                    birthdate=timezone.now(),  
                    name=user.username  
                )
                return redirect('profile')  # Redirect to the profile page after successful signup
        else:
            form = CustomUserCreationForm()
        return render(request, 'brainy/signup.html', {'form': form})
    else:
        return redirect('home')

class CustomLoginView(LoginView):
    template_name = 'brainy/Login.html'
    authentication_form = LoginForm
    success_url = reverse_lazy('profile')  # Updated to point to 'profile'

    @method_decorator(user_passes_test(lambda u: not u.is_authenticated, login_url='login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_success_url(self):
        return self.success_url

class HistoryScan(View):
    def get(self, request):
        if request.user.is_authenticated:
            current_user = request.user
            user_Hscans = ScanHistory.getUser(user=current_user)  # Pass the user argument
            for scan in user_Hscans:
                scan.Model1 = scan.get_prediction_category(scan.Model1)
                scan.Model2 = scan.get_prediction_category(scan.Model2)
                scan.Model3 = scan.get_prediction_category(scan.Model3)
                scan.Model4 = scan.get_prediction_category(scan.Model4)
                scan.Model5 = scan.get_prediction_category(scan.Model5)
            return render(request, 'brainy/HistoryScan.html', {'Hscans': user_Hscans})
        else:
            return redirect('login')


model1 = load_model('Efficientb1.h5')
model2 = load_model('Efficientb1LSTM.h5')
model3 = load_model('inception.h5')
model4 = load_model('Resnet.h5')
model5 = load_model('vggtrained.h5')

class Majority(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'brainy/models.html')

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            image_file = request.FILES.get('image')
            if not image_file:
                return JsonResponse({'error': 'Missing required fields: image'}, status=400)
            
            filename = slugify(image_file.name)
            temp_img_path = os.path.join(settings.MEDIA_ROOT, 'temp', filename)
            
            try:
                with default_storage.open(temp_img_path, 'wb+') as destination:
                    for chunk in image_file.chunks():
                        destination.write(chunk)
            except Exception as e:
                logger.exception(f"Error saving uploaded image: {e}")
                return JsonResponse({'error': 'An error occurred while saving the image'}, status=500)
            
            # Handle the prediction
            
            profile = request.user.profile
            IMG_SIZE = 280
            CATEGORIES = ["glioma", "meningioma", "notumor", "pituitary"]

            img_array = cv2.imread(temp_img_path, cv2.IMREAD_COLOR)  # Convert to array
            new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # Resize to normalize data size
            X_test = np.array([new_array]).reshape(-1, IMG_SIZE, IMG_SIZE, 3)
            
            # Make predictions
            model_predictions = {
                "EfficientNETB1": model1.predict(X_test)[0].tolist(),  # Get first element (prediction array)
                "EfficientNETB1 LSTM": model2.predict(X_test)[0].tolist(),
                "INCEPTIONV3": model3.predict(X_test)[0].tolist(),
                "Resnet": model4.predict(X_test)[0].tolist(),
                "VGG16": model5.predict(X_test)[0].tolist(),
            }

            # Get votes for each class
            votes = np.zeros(len(CATEGORIES))
            for pred in model_predictions.values():
                votes[np.argmax(pred)] += 1  # Vote based on predicted class index

            # Find ensemble prediction (majority voting class)
            ensemble_pred = np.argmax(votes)
            ensemble_result = CATEGORIES[ensemble_pred]

            # Save the scan history
            ScanHistory.objects.create(
                mri=image_file,
                profile=profile,
                date=timezone.now(),
                Model1=",".join(map(str, model_predictions["EfficientNETB1"])),  
                Model2=",".join(map(str, model_predictions["EfficientNETB1 LSTM"])),
                Model3=",".join(map(str, model_predictions["INCEPTIONV3"])),
                Model4=",".join(map(str, model_predictions["Resnet"])),
                Model5=",".join(map(str, model_predictions["VGG16"])),
                Result=ensemble_result
            )
            

            # Return results as a dictionary
            return JsonResponse({
                "ensemble_prediction": ensemble_result,
                "individual_predictions": model_predictions,
                "votes": votes.tolist(),
            })

        except Exception as e:
            logger.exception("An error occurred during prediction")
            return JsonResponse({'error': str(e)}, status=500)







def achivmenet(request):
    return render(request,'brainy/completed.html')