from django.contrib import admin
from .models import CustomUser, Profile , ScanHistory
from django.utils.html import format_html
# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    # Other fields you want to display in the admin panel
    list_display = ('username', 'email', 'phone_number', 'is_staff', 'is_active')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_profile_picture', 'name','get_phone_number','birthdate', 'gender')
    readonly_fields = ('get_profile_picture',)

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="width: 100px; height: auto;">'.format(obj.profile_picture.url))
        else:
            return "No profile picture uploaded"
    def get_phone_number(self, obj):
        if obj.user:
            return obj.user.phone_number
        else:
            return "No user associated"  
    get_phone_number.short_description = 'Phone Number'  

@admin.register(ScanHistory)
class ScanModel(admin.ModelAdmin):
    list_display = ['id', 'date', 'display_mri', 'get_predicted_result_label','Model1','Model2','Model3','Model4','Model5', 'profile']
    list_filter = ['Result']
    list_per_page = 10
    def display_mri(self, obj):
        if obj.mri:
            return format_html('<img src="{}" style="width="100" height="100" />'.format(obj.mri.url))
        else:
            return '-'
    def get_result_display(self, obj):
        predicted_class = obj.Result

        # Access the CATEGORY dictionary from your models.py
        category_dict = dict(CATEGORY)  # Convert CATEGORY tuple to dictionary

        # Return the human-readable label for the predicted class
        return category_dict.get(predicted_class)

     
    display_mri.short_description = 'MRI Image'