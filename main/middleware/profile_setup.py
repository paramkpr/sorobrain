from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from main.views.utils import user_profile_setup_progress


class ProfileNotFilledMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response
		# One-time configuration and initialization.

	def __call__(self, request):
		print(request.path)
		print(request.path == '/accounts/save_profile/')
		if not request.path == '/accounts/save_profile/':
			if not request.path == '/accounts/settings/':
				if request.user.is_authenticated:
					empty_fields = user_profile_setup_progress(request.user)
					if empty_fields > 0:
						messages.add_message(request, messages.INFO,
						                     f"Finish setting up your profile <a href={reverse('settings')}> here</a>. You have {empty_fields} fields to fill.")
						return redirect(reverse('settings'))

		response = self.get_response(request)

		# Code to be executed for each request/response after
		# the view is called.

		return response
