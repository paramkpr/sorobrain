import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View

from competition.forms import SendCertificatesForm
from competition.models.competition import Competition, CompetitionCertificate
from competition.views.utils import send_certificate
from main.models import User


class Compete(LoginRequiredMixin, View):
	@staticmethod
	def get(request, slug):
		competition = get_object_or_404(Competition, slug=slug)
		if competition.is_over: 
			if competition.result is not None:
				return redirect(reverse('competition:result', args=[competition.slug]))
			else:
				competition.populate_result()
				return redirect(reverse('competition:result', args=[competition.slug]))
		if not competition.has_user_finished(request.user) and competition.is_started:
			progress = competition.user_progress(request.user)
			active_quiz = list(competition.quizzes.all())[progress.index(0)]
		else:
			active_quiz = -1
		return render(request, 'competition/compete/compete.html', {
			'competition': competition,
			'active_quiz': active_quiz
		})


class Result(View):
	@staticmethod
	def get(request, slug):
		competition = get_object_or_404(Competition, slug=slug)
		result = json.loads(competition.result)
		if result == {}:
			competition.populate_result()
		result = dict(list(result.items())[:competition.leaderboard_rank_limit])
		# TODO: remove this
		return render(request, 'competition/compete/result.html', {
			'competition': competition,
			'result': result
		})


class Certificate(View):
	"""
	The url for this view is 'certificate/<certificate_id>/<user_name>/'
	"""
	@staticmethod
	def get(request, slug, username):
		c = get_object_or_404(Competition, slug=slug)
		user = get_object_or_404(User, username=username)
		certificate = get_object_or_404(CompetitionCertificate, slug=slug)
		return render(request, 'competition/compete/certificate.html', {
			'certificate': certificate,
			'competition': c,
			'user': user
		})


class SendCertificates(View, LoginRequiredMixin):
	@staticmethod
	def get(request, competition_slug):
		if not request.user.is_staff:
			messages.add_message(request, messages.WARNING, 'Access not allowed')
			return redirect(reverse('index'))
		c = get_object_or_404(Competition, slug=competition_slug)
		form = SendCertificatesForm(competition=c)
		return render(request, 'competition/send_certificate.html', {
			'form': form,
			'c': c
		})

	@staticmethod
	def post(request, competition_slug):
		if not request.user.is_staff:
			messages.add_message(request, messages.WARNING, 'Access not allowed')
			return redirect(reverse('index'))

		c = get_object_or_404(Competition, slug=competition_slug)
		form = SendCertificatesForm(request.POST, competition=c)
		if form.is_valid():
			data = form.cleaned_data
			users = data['users']
			for u in users:
				send_certificate(c, u)
			messages.add_message(request, messages.SUCCESS, 'Certificates Sent!')
		else:
			messages.add_message(request, messages.WARNING, 'Invalid form data!')
		return redirect(reverse('competition:send_certificate', args=[c.slug]))
