import json
from datetime import timedelta

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from django.utils import timezone

from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from taggit.managers import TaggableManager

from main.models import User
from sorobrain.settings import RECENT_TIME_LIMIT
from .store import CompetitionAccess
from quiz.models import Quiz, QuizSubmission
from sorobrain.mixins.payment import PaidObjectMixin


class Competition(PaidObjectMixin, models.Model):
	"""
	Model to manage competitions

	result field looks like = {
		<user>: <score>
	}, ordered from highest score to lowest in ascending order
	if the compete is expired redirect to the result page, if the
	result is null then calculate else display result
	"""

	LEVEL_CHOICES = [
		(None, ''),
		('fluent', 'Fluent/Native Speaker'),
		('advanced', 'Advanced'),
		('intermediate', 'Intermediate'),
		('beginner', 'Beginner'),
		('any', 'French Learner of any level')
	]

	group_cost = models.IntegerField()
	title = models.CharField(max_length=256)
	leaderboard_rank_limit = models.IntegerField(default=25)
	certificate_rank_limit = models.IntegerField(default=25)
	slug = models.SlugField(max_length=256, verbose_name='Slug', blank=True)
	description = RichTextUploadingField(config_name='minimal')
	level = models.CharField(max_length=128, verbose_name='French Level',
	                         choices=LEVEL_CHOICES)
	thumbnail = models.ImageField(upload_to='compete/thumbnails/',
	                              default='compete/thumbnails/default.jpg',
	                              null=True, blank=True)
	tags = TaggableManager()
	quizzes = models.ManyToManyField(Quiz, through='CompetitionQuiz')
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	result = JSONField(null=True, blank=True)
	active = models.BooleanField(verbose_name='Active', default=True)
	hide_leaderboard = models.BooleanField(verbose_name='Hide Leader-board', default=False)
	include_book = models.BooleanField(verbose_name='Include Book', default=False)
	not_for_sale = models.BooleanField('Not For Sale', default=False)
	created_on = models.DateTimeField(default=timezone.now,
	                                  verbose_name='Created On')

	@property
	def is_free(self):
		return self.sub_total < 1

	@property
	def is_over(self):
		return timezone.now() > self.end_date

	@property
	def is_started(self):
		return timezone.now() >= self.start_date

	@property
	def is_in_progress(self):
		return self.start_date < timezone.now() < self.end_date

	@classmethod
	def get_recent(cls):
		return cls.objects.filter(created_on__gte=(timezone.now() - RECENT_TIME_LIMIT))

	def user_progress(self, user):
		state = []
		quizzes = self.quizzes.all()
		for quiz in quizzes:
			try:
				QuizSubmission.objects.get(user=user, quiz=quiz, competition=self, score__isnull=False)
				state.append(1)
			except QuizSubmission.DoesNotExist:
				state.append(0)
		return state

	def can_user_attempt_quiz(self, user, quiz):
		q = list(self.quizzes.all()).index(quiz)
		return all(self.user_progress(user)[:q]) and (self.user_progress(user)[q] == 0)

	def has_user_finished(self, user):
		return all(self.user_progress(user))

	def calculate_total_score_for_user(self, user):
		if self.has_user_finished(user):
			submissions = [
				QuizSubmission.objects.get(user=user, competition=self, quiz=q)
				for q in self.quizzes.all()]
			return sum([qs.score for qs in submissions])
		else:
			return 0

	def populate_result(self):
		# get users from compete access and get score for each
		r = {}
		users = [ca.user for ca in CompetitionAccess.objects.filter(competition=self)]
		for user in users:
			r[user.username] = self.calculate_total_score_for_user(user)
		self.result = json.dumps(dict(sorted(r.items(), key=lambda x: x[1],
		                                     reverse=True)))
		self.save()

	def get_absolute_url(self):
		return reverse('competition:buy', args=[self.slug])

	def get_compete_url(self):
		return reverse('competition:compete', args=[self.slug])

	def save(self, *args, **kwargs):
		if self.slug is None or self.slug == '':
			self.slug = slugify(self.title)
		super(Competition, self).save(*args, **kwargs)

	def __str__(self):
		return f"{self.title} | id: {self.id}"

	class Meta:
		verbose_name = 'Competition'
		verbose_name_plural = 'Competitions'


class CompetitionQuiz(models.Model):
	competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	created_on = models.DateTimeField(default=timezone.now)

	class Meta:
		verbose_name = 'Competition Quiz'
		verbose_name_plural = 'Competition Quizzes'
		ordering = ('-created_on',)


class CompetitionCertificate(models.Model):
	competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	certificate = models.ImageField(upload_to='competition/certificates/')
	disabled = models.BooleanField(default=False)

	class Meta:
		unique_together = ('user', 'competition')
