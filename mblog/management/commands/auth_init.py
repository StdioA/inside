from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission


class Command(BaseCommand):

    def handle(*args, **kwargs):
        sus = User.objects.filter(is_superuser=True).first()
        if not sus:
            User.objects.create_superuser('admin', 'myemail@example.com',
                                          'password')
        else:
            print("There's already a super user")

        try:
            writer_group = Group.objects.get(name="Writer")
        except Group.DoesNotExist:
            writer_group = Group(name="Writer")
            writer_group.save()
            add_post = Permission.objects.get(name="Can add post")
            change_post = Permission.objects.get(name="Can change post")
            writer_group.permissions.add(add_post, change_post)
            writer_group.save()
        else:
            print("The group Writer already exists")

        try:
            manager = User.objects.get(username="manager")
        except User.DoesNotExist:
            manager = User.objects.create_user('manager', 'guest@guest.com',
                                               'managerpassword')
            manager.groups.add(writer_group)
            manager.save()
        else:
            print("The user 'manager' already exists")

        print("Auth Done")
