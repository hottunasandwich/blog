from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    def handle(self, *args, **options):
        normal_perms = ['view_post', 'view_tag', 'view_comment', 'view_category', 'add_comment', 'add_commentlike', 'add_postlike', 'view_commentlike', 'view_postlike']
        writer_perms = normal_perms + ['add_post']
        editor_perms = writer_perms + ['change_comment', 'change_post']
        admins_perms = editor_perms + ['view_category', 'change_category', 'change_category', 'add_category']
        group_dict = {
            'admin': admins_perms,
            'editor': editor_perms,
            'writer': writer_perms,
            'normal': normal_perms
        }
      
        for group_name, group_perms in group_dict.items():
            obj_group, created = Group.objects.get_or_create(name=group_name.capitalize())
            if created:
                self.stdout.write(self.style.SUCCESS(f'SUCCESSFULLY added <{obj_group.name}>'))
            else:
                self.stdout.write(self.style.NOTICE(f'Group <{obj_group.name}> already existed'))
            
            for perm in group_perms:
                obj, created = Permission.objects.get_or_create(codename=perm)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'SUCCESSFULLY created <{perm}> Permission'))
                else:
                    self.stdout.write(self.style.NOTICE(f'Permission <{perm}> already existed'))
                
                obj_group.permissions.add(obj)
            