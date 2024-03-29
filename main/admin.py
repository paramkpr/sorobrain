import json

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericInlineModelAdmin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.urls import reverse, NoReverseMatch
from django.utils.safestring import mark_safe

from quiz.models import Quiz
from .forms import AddUserForm, UpdateUserForm
from .models import User, BookAccess, OneOnOneClass, ReferralCode, Ledger
from .models.code import DiscountCode
from .models.invoices import Invoice


def get_user_emails(modeladmin, request, queryset):
	emails = [user.email for user in queryset]
	string_emails = "".join([e + ", " for e in emails])
	request.session['_user_emails'] = string_emails
	return redirect(reverse('selected_emails'))


def get_user_phone(modeladmin, request, queryset):
	names_and_phones = [(user.name, str(user.phone)) for user in queryset if user.phone is not None]
	request.session['_user_phones'] = json.dumps(names_and_phones)
	return redirect(reverse('selected_phones'))


def give_users_competition_access(modeladmin, request, queryset):
	usernames = [user.username for user in queryset]
	string_usernames = "".join([u + ", " for u in usernames])
	request.session['_usernames'] = string_usernames
	return redirect(reverse('grant_competition_access'))


def give_users_quiz_access(modeladmin, request, queryset):
	usernames = [user.username for user in queryset]
	string_usernames = "".join([u + ", " for u in usernames])
	request.session['_usernames'] = string_usernames
	return redirect(reverse('grant_quiz_access'))


def give_users_workshop_access(modeladmin, request, queryset):
	usernames = [user.username for user in queryset]
	string_usernames = "".join([u + ", " for u in usernames])
	request.session['_usernames'] = string_usernames
	return redirect(reverse('grant_workshop_access'))


def manage_soromoney(modeladmin, request, queryset):
	usernames = [user.username for user in queryset]
	string_usernames = "".join([u + ", " for u in usernames])
	request.session['_usernames'] = string_usernames
	return redirect(reverse('give_soromoney'))


def export_to_excel(modeladmin, request, queryset):
	usernames = [user.username for user in queryset]
	string_usernames = "".join([u + ", " for u in usernames])
	request.session['_usernames'] = string_usernames
	return redirect(reverse('export_users'))


class UserAdmin(BaseUserAdmin):
	form = UpdateUserForm
	add_form = AddUserForm

	list_display = ('username', 'email', 'points', 'name', 'date_joined', 'is_staff')
	list_filter = ('is_staff', 'is_active', 'level', 'education', 'gender', 'notification_level', 'school', 'country')
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Personal info', {'fields': ('name', 'avatar', 'school_id', 'points', 'date_of_birth',
		                              'phone', 'gender', 'level', 'education', 'school', 'city', 'country')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'notification_level', 'groups', 'user_permissions')}),
	)
	add_fieldsets = (
		(
			None,
			{
				'classes': ('wide',),
				'fields' : (
					'email', 'name', 'phone', 'gender', 'level', 'education', 'notification_level'
				)
			}
		),
	)
	search_fields = ('username', 'email', 'name', 'phone')
	ordering = ('username',)
	filter_horizontal = ('user_permissions', 'groups')
	readonly_fields = ('points',)
	actions = [get_user_emails, get_user_phone, give_users_competition_access, give_users_quiz_access,
	           give_users_workshop_access, manage_soromoney, export_to_excel]


admin.site.register(User, UserAdmin)


class BookAccessAdmin(admin.ModelAdmin):
	list_display = ('user', 'active', 'created_on')
	list_filter = ('active',)
	search_fields = ('user',)
	readonly_fields = ('created_on',)


admin.site.register(BookAccess, BookAccessAdmin)


class DiscountCodeAdmin(admin.ModelAdmin):
	list_display = ('code', 'uses', 'discount', 'content_type', 'content_object', 'expiry_date')
	list_filter = ('content_type',)
	search_fields = ('content_object',)
	readonly_fields = ('code', 'created_on')


admin.site.register(DiscountCode, DiscountCodeAdmin)


class OneOnOneClassAdmin(admin.ModelAdmin):
	list_display = ('title', 'cost', 'duo_cost', 'level', 'created_on')
	list_filter = ('level', 'active')
	search_fields = ('title',)
	list_editable = ('cost', 'duo_cost')
	readonly_fields = ('created_on', 'slug')


admin.site.register(OneOnOneClass, OneOnOneClassAdmin)


def update_incentive(modeladmin, request, queryset):
	codes = [code.id for code in queryset]
	string_codes = "".join([str(c) + ", " for c in codes])
	request.session['_codes'] = string_codes
	return redirect(reverse('update_incentive'))


class ReferralCodeAdmin(admin.ModelAdmin):
	list_display = ('referrer', 'code', 'uses', 'referrer_incentive', 'referee_incentive')
	list_filter = ('referrer__is_staff', 'referrer__is_active', 'referrer__level',
	               'referrer__education', 'referrer__school', 'referrer__country', 'referrer__city',
	               'referrer_incentive', 'referee_incentive')
	list_editable = ('referrer_incentive', 'referee_incentive')
	filter_horizontal = ('used_by',)
	actions = [update_incentive]
# readonly_fields = ("used_by", "code", "referrer", "created")


admin.site.register(ReferralCode, ReferralCodeAdmin)


class LedgerAdmin(admin.ModelAdmin):
	list_display = ('user', 'credit', 'debit', 'balance', 'description', 'time')
	readonly_fields = ('user', 'credit', 'debit', 'description', 'time', 'balance')
	list_filter = ('user',)


admin.site.register(Ledger, LedgerAdmin)


class InvoiceAdmin(admin.ModelAdmin):
	def link(self, obj):
		try:
			url = reverse('view_invoice', args=[obj.id])
		except NoReverseMatch:
			url = '/'
		return mark_safe(f"<a href='{url}'>Open Invoice</a>")

	link.allow_tags = True

	fieldsets = (
		(None, {
			'fields': ('user', 'description', 'amount', 'date', 'paid', 'link')
		}),
	)

	list_filter = ('user',)
	list_display = ('id', 'user', 'description', 'amount', 'date', 'paid', 'link')
	readonly_fields = ('link', 'invoice_html')


admin.site.register(Invoice, InvoiceAdmin)
