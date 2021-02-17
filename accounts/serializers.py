from rest_framework import serializers
from .models import Profile

from django.utils.translation import gettext as _
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.validators import UniqueValidator
from .validators import NewASCIIUsernameValidator

class ProfileSerializer(RegisterSerializer):
    username = serializers.CharField(
        required=True,
        min_length=5,
        max_length=20,
        validators=[UniqueValidator(queryset=Profile.objects.all()), NewASCIIUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    class Meta:
        model = Profile
    
    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        # 추가적인 속성이 들어갈 경우
        # data_dict['nickname'] = self.validated_data.get('nickname', '')
        # data_dict['introduction'] = self.validated_data.get('introduction', '')
        # data_dict['profile_image'] = self.validated_data.get('profile_image', '')
        return data_dict

# 아이디를 통해서 이메일 재 전송하기 (username)
# class UsernameEmailAddress(serializers.ModelSerializer):
#     username = serializers.CharField(required=True, min_length=5, max_length=20)
#     email = serializers.EmailField(required=True)
    
#     class Meta:
#         model = Profile
#         fields = ("username", "email")