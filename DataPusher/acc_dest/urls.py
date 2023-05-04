from django.urls import path, re_path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('account/create/', create_account),
                  path('account/login/', login_account),
                  path('account/edit/', edit_account),
                  path('account/delete/', delete_account),
                  path('account/all/', all_accounts),
                  path('destination/add/', add_destination),
                  path('destination/view/', get_destination),
                  path('destination/edit/', edit_destination),
                  path('destination/delete/', delete_destination),
                  path('server/incoming_data/', server_data)
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
