from django.urls import path
from .views import (
    RegisterView,
    MyTokenObtainPairView,
    LoginView,
    RefreshTokenView,
    CheckTokenView,
    LogoutView,
)


urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view(), name="login_view"),
    path("logout/", LogoutView.as_view(), name="logout_view"),
    path("token/refresh/", RefreshTokenView.as_view(), name="refresh_token"),
    path("token/", CheckTokenView.as_view(), name="check_token"),
]
