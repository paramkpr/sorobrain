import hashlib
import os
from uuid import uuid4

import razorpay
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from razorpay.errors import SignatureVerificationError

from main.models.code import DiscountCode


class PaidObjectMixin(models.Model):
	"""Mixin that makes the object that inherits it payable, this
	makes the payment process stateless. """

	class Meta:
		abstract = True

	cost = models.IntegerField()
	discount = models.IntegerField(verbose_name='Discount Percentage',
	                               blank=True, null=True)

	@property
	def sub_total(self):
		if type(self.discount) == int and self.discount > 0:
			return int(self.cost * (1 - self.discount / 100))
		return self.cost

	def pay(self, request, amount, success_url, failure_url, code='', udf2=''):
		"""
		This function takes a payment object and returns the JSON response
		required by the BOLT-PayU payment protocol.
		:param self:
		:param request: The request object from the view
		:param amount: This is explicit to allow for special pricing etc
		:param success_url: absolute url of view to redirect to on payment success
		:param failure_url: absolute url of view to redirect to on payment success
		:param code: discount code for this payment
		:param udf2: anything you want to pass to the success view

		:return: json response for BOLT
		"""
		login_url = request.build_absolute_uri(reverse('account_login'))

		if not request.user.is_authenticated:
			messages.add_message(request, messages.WARNING,
			                     "You need to login before you can buy something!")
			JsonResponse({'status': 'Error', 'redirect': login_url})

		if request.user.profile_setup_progress() > 0:
			messages.add_message(request, messages.WARNING,
			                     "You need to complete your profile first!")
			JsonResponse({'status': 'Error', 'redirect': reverse('settings')})

		if code != '':
			if not code.is_used and not code.is_expired:
				if ContentType.objects.get_for_model(
						self) == code.content_type:
					if self.id == code.object_id:
						amount = amount * ((100 - code.discount) / 100)

		client = razorpay.Client(auth=(os.environ.get('RAZORPAY_KEY'), os.environ.get('RAZORPAY_SECRET_KEY')))
		client.set_app_details({"title": "Django", "version": os.environ.get('APP_VERSION')})

		amount = amount
		notes = {'udf2': udf2, 'code': code}

		response = JsonResponse(client.order.create(dict(amount=int(amount) * 100, currency='INR', notes=notes)))
		print(response)
		return response


	@staticmethod
	def is_payment_valid(request, rzp_order_id, rzp_payment_id, rzp_signature):
		"""
		This method validates the payment by checking the hash sent from
		payu against a hash that it creates itself.
		:param request: the request object from the view
		:return: Returns a redirect if invalid hash, and a true if valid
		"""

		client = razorpay.Client(auth=(os.environ.get('RAZORPAY_KEY_ID'), os.environ.get('RAZORPAY_KEY_SECRET')))
		params = {
			'razorpay_order_id'  : rzp_order_id,  # request.POST.get('razorpay_order_id'),
			'razorpay_payment_id': rzp_payment_id,  # request.POST.get('razorpay_payment_id'),
			'razorpay_signature' : rzp_signature,  # request.POST.get('razorpay_signature')
		}
		try:
			client.utility.verify_payment_signature(params)
		except SignatureVerificationError:
			return JsonResponse({'status': True, 'redirect': reverse('payment_error')})

		code = client.notes.get('code')
		if code != '':
			DiscountCode.objects.get(code=code).use()

		return True
