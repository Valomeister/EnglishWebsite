from django.urls import path
from .views import SignUpView, AccountDetailView, AccountEditView, CustomPasswordResetView, CustomLoginView

urlpatterns = [
    path('<int:pk>/edit/', AccountEditView.as_view(), name='account_edit'),
    path('<int:pk>/', AccountDetailView.as_view(), name='account'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('login/', CustomLoginView.as_view(), name='login'),
]