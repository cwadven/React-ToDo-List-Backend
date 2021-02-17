from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

class CustomAccountAdapter(DefaultAccountAdapter):
    # 인증 메일 시 url front로 변경
    # def send_mail(self, template_prefix, email, context):
    #     context['activate_url'] = settings.URL_FRONT + 'accounts/account-confirm/' + context['key']
    #     msg = self.render_mail(template_prefix, email, context)
    #     msg.send()

    # 추가적인 내용 넣기
    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        # user.nickname = data.get('nickname')
        # user.introduction = data.get('introduction')
        # user.profile_image = data.get('profile_image')
        user.save()
        return user