import csv

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from main.models import User


def export_users_csv(request):
    if not request.user.is_staff:
        return HttpResponse(403)
    usernames_string = request.session.get('_usernames')
    users = [get_object_or_404(User, username=u.strip()) for u in usernames_string.split(',')[:-1]]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'First name', 'Phone', 'Email address', 'School', 'City', 'Country', 'Gender', 'Points'])

    users = User.objects.all().values_list('username', 'name', 'phone', 'email', 'school', 'city', 'country', 'gender', 'points')
    for user in users:
        writer.writerow(user)

    return response
