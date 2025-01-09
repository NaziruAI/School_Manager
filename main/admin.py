from django.contrib import admin
from .models import GalleryImage

admin.site.register(GalleryImage)



# Customize the title of the browser tab for the admin
admin.site.site_title = "Light CES Admin"

# Customize the header (index title) shown on the admin dashboard
admin.site.site_header = "Light Counselling Center Admin"

# Customize the index page's welcome message
admin.site.index_title = "Welcome to Light CES Administration"
