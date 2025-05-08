
from django.urls import path, include

from account.urls import app_name
from .route import router

app_name = 'web_api'
urlpatterns = [
    path('api/', include(router.urls))
]
