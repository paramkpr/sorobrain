import hashlib
import os
from uuid import uuid4

from django.contrib import messages
from django.db import models
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse


class PaidObjectMixin(models.Model):
	"""Mixin that makes the object that inherits it payable, this
	makes the payment process stateless. """
	class Meta:
		abstract = True

	cost = models.IntegerField()
	discount = models.IntegerField(verbose_name='Discount Percentage',
	                               blank=True, null=True)

	def pay(self, request, amount, success_url, failure_url):
		"""
		This function takes a payment object and returns the JSON response
		required by the BOLT-PayU payment protocol.
		:param self:
		:param request: The request object from the view
		:param amount: This is explicit to allow for special pricing etc
		:param success_url: url of view to redirect to on payment success
		:param failure_url: url of view to redirect to on payment success
		:return: json response for BOLT
		"""
		login_url = reverse('account_login')

		if not request.user.is_authenticated:
			messages.add_message(request, messages.WARNING, "You need to login before you can buy something!")
			return redirect(login_url)

		product_info = self.title if not self.title == '' else 'no-product-info'

		data = {
			'merchant_key': os.environ.get('PAYU_MERCHANT_KEY'),
			'txn_id'      : str(uuid4().hex),
			'amount'      : int(amount),
			'product_info': product_info,
			'first_name'  : request.user.name.split(' ', 1)[0],
			'email_id'    : request.user.email,
			'phone_number': str(request.user.phone),
			'surl'        : success_url,
			'furl'        : failure_url
		}

		data['hash'] = str(hashlib.sha512(
				('%s|%s|%s|%s|%s|%s|||||||||||%s' % (
					data['merchant_key'],
					data['txn_id'],
					data['amount'],
					data['product_info'],
					data['first_name'],
					data['email_id'],
					os.environ.get('PAYU_MERCHANT_SALT')
				)).encode('utf-8')
		).hexdigest())

		# REVIEW: add some kind of logging here.
		# TODO: Add send customer and admin mail here

		return JsonResponse(data)
