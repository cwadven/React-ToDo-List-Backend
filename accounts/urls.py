from django.urls import path, include

from rest_auth.registration.views import VerifyEmailView, RegisterView
# from accounts.views import ConfirmEmailView

from rest_auth.views import (
    LoginView, LogoutView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)

urlpatterns = [
    # 회원가입
    path("registration", RegisterView.as_view(), name='rest_register'),
    # 로그인, 로그아웃
    path('login', LoginView.as_view(), name='rest_login'),
    path('logout', LogoutView.as_view(), name='rest_logout'),
    # 비밀번호 수정
    path('password-change', PasswordChangeView.as_view(), name='rest_password_change'),

    # 비밀번호 찾기
    # # 이메일 전송 가능하게 해야함
    # path('password-reset', PasswordResetView.as_view(), name='rest_password_reset'),
    # # url에 uidb64 위치와 token 위치에 있는 것을 POST에 같이 넘기면 됨
    # path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # 이메일 인증하기
    path('allauth/', include('allauth.urls')),
    # 이메일 인증
    # re_path(r'^account-confirm/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # re_path(r'^account-confirm/(?P<key>[-:\w]+)$', ConfirmEmailView.as_view(), name='account_confirm_email'),
]