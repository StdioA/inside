from django.contrib.auth.models import User, Group, Permission
User.objects.create_superuser('admin', 'myemail@example.com', 'password')

add_post = Permission.objects.get(name="Can add post")
change_post = Permission.objects.get(name="Can change post")

writer_group = Group(name="Writer")
writer_group.save()
writer_group.permissions.add(add_post, change_post)
writer_group.save()

manager = User.objects.create_user('manager', 'guest@guest.com', 'managerpassword')
manager.groups.add(writer_group)
manager.save()
