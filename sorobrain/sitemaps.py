from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
	priority = 1.0
	changefreq = 'monthly'

	def items(self):
		return ['index', 'contact', 'catalog', 'account_signup',
		        'account_login', 'profile', 'book']

	def location(self, item):
		return reverse(item)
