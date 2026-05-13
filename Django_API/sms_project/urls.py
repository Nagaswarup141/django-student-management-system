from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('api/auth/login/',   TokenObtainPairView.as_view(),  name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(),     name='token_refresh'),
    path('api/auth/verify/',  TokenVerifyView.as_view(),      name='token_verify'),
    path('api/auth/logout/',  TokenBlacklistView.as_view(),   name='token_blacklist'),
    path('api/students/',     include('students.urls')),
    path('api/attendance/',   include('attendance.urls')),
    path('api/grades/',       include('grades.urls')),
    path('api/fees/',         include('fees.urls')),
    path('api/courses/',      include('courses.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)