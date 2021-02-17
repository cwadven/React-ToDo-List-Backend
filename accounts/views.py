from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import AllowAny

# 이메일 관련
# from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC

# from django.http import HttpResponseRedirect

# from allauth.account.utils import send_email_confirmation
# from allauth.account.models import EmailAddress

# 메일 인증 처리
# class ConfirmEmailView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, *args, **kwargs):
#         self.object = confirmation = self.get_object()
#         try:
#             confirmation.confirm(self.request)
#         except:
#             #인증 실패했습니다!
#             return Response(data={"detail":"something get wrong"} , status=status.HTTP_400_BAD_REQUEST)
#         # A React Router Route will handle the failure scenario
#         # 인증 성공했습니다!
#         # 인증 성공 시, 사용자 닉네임 보여주기
#         query = EmailAddress.objects.get(email=self.object.email_address)
#         return Response(data={"detail":"Email verified", } , status=status.HTTP_202_ACCEPTED)

#     def get_object(self, queryset=None):
#         key = self.kwargs['key']
#         email_confirmation = EmailConfirmationHMAC.from_key(key)
#         if not email_confirmation:
#             if queryset is None:
#                 queryset = self.get_queryset()
#             try:
#                 email_confirmation = queryset.get(key=key.lower())
#             except EmailConfirmation.DoesNotExist:
#                 # A React Router Route will handle the failure scenario
#                 return HttpResponseRedirect('/login/failure/')
#         return email_confirmation

#     def get_queryset(self):
#         qs = EmailConfirmation.objects.all_valid()
#         qs = qs.select_related("email_address__user")
#         return qs

# 이메일 재 전송 인증 보내기
# class ReEmailConfirmation(generics.CreateAPIView):
#     queryset = EmailAddress.objects.all()
#     serializer_class = UsernameEmailAddress
#     permission_classes = [AllowAny]

#     def post(self, request):
#         # 해당 이메일에서 회원가입한 닉네임으로 인증 보내버리기!!
#         serializer = self.get_serializer(data=request.data, context={"request": request})
#         if serializer.is_valid():
#             username = serializer.validated_data["username"]
#             qs = self.get_queryset().filter(user__username=username, verified=True).exists()
#             if qs:
#                 return Response({'detail': 'Email already verified'}, status=status.HTTP_406_NOT_ACCEPTABLE)
#             # 그런 후 해당 아이디를 같은 Profile을 찾고 있을 경우 이메일 전송하기
#             try:
#                 # 재인증하는 이메일이 기존에 존재하는 이메일이면
#                 if self.get_queryset().filter(user__username=username, email=serializer.validated_data["email"]).exists():
#                     pass
#                 else:
#                     # 다른 사람 이메일과 중복한 이메일이 있는 지 확인
#                     if self.get_queryset().filter(email=serializer.validated_data["email"]).exists():
#                         return Response({'detail': 'Email already used'}, status=status.HTTP_406_NOT_ACCEPTABLE)

#                 # 전 이메일과 동일하지 않고 새로운 이메일이면 이메일 수정
#                 if self.get_queryset().get(user__username=username).email != serializer.validated_data["email"]:
#                     new_email = self.get_queryset().get(user__username=username)
#                     # 이메일 변경 함수
#                     new_email.change(request, serializer.validated_data["email"], confirm=False)

#                 user = Profile.objects.get(username=username)
#                 # 이메일 전송
#                 send_email_confirmation(request, user)
#                 # 재인증 시 이메일 주소 넣기
#                 email_add = self.get_queryset().get(user__username=username)
#                 return Response({'detail': 'Email confirmation sent', 'email':email_add.email}, status=status.HTTP_200_OK)
#             except:
#                 return Response({'detail': 'User not exists'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)