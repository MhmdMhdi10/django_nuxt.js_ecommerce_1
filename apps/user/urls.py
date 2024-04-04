from django.urls import path
from apps.user.views import RegisterUser, RegisterUserVerifyCode, LoginUser, RefreshTokenView, LogoutUser, \
    GetCurrentUser, ChangePassword, RecoverRequest, RecoverLinkVerify, RecoverChangePassword, CheckAuthentication, \
    LoginADMIN

app_name = 'product'
urlpatterns = [
    path('register/', RegisterUser.as_view()),
    path('verify/', RegisterUserVerifyCode.as_view()),
    path('login/', LoginUser.as_view()),
    path('refresh/', RefreshTokenView.as_view()),
    path('logout/', LogoutUser.as_view()),
    path('change_password/', ChangePassword.as_view()),
    path('me/', GetCurrentUser.as_view()),
    path('recover_link/', RecoverRequest.as_view()),
    path('recover_link_verify/', RecoverLinkVerify.as_view()),
    path('recover_change_password/', RecoverChangePassword.as_view()),
    path('check_authentication/', CheckAuthentication.as_view()),

    # ADMIN
    path('admin/login/', LoginADMIN.as_view()),
]
