# # from django.contrib.auth import get_user_model
# from .models import User
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.contrib.sites.shortcuts import get_current_site
# from .tokens import account_activation_token
# from django.core.mail import send_mail
# from django.utils.encoding import force_bytes
# from django.template.loader import render_to_string


# # def activate(request, uidb64, token):
# #     User = get_user_model()
# #     try:
# #         uid = force_text(urlsafe_base64_decode(uidb64))
# #         user = User.objects.get(pk=uid)
# #     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
# #         user = None
# #     if user is not None and account_activation_token.check_token(user, token):
# #         user.is_active = True
# #         user.save()
# #         return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
# #     else:
# #         return HttpResponse('Activation link is invalid!')