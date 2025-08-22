from django.urls import path
from .views import RegisterView, LoginView, ForgotPassView, EmailVerificationView, ResetPasswordView, DeleteUserAccount, CartView,CheckoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgotPass/', ForgotPassView.as_view(), name='forgotPass'),
    path('emailverification/', EmailVerificationView.as_view(), name='emailverification'),
    path('resetpassword/', ResetPasswordView.as_view(), name='resetpassword'),
    path('DeleteUser/', DeleteUserAccount.as_view(), name='DeleteUser'),
    path('Cart/', CartView.as_view(), name='Cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout')
]
