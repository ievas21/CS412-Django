from django.contrib import admin
from .models import *

# Registers the profile model, so we can manually add profiles on /admin
# Ieva sagaitis, ievas@bu.edu

admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(Friend)