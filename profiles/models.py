from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from . import manager

class CustomUser(AbstractBaseUser):
    """
    A custom user class that basically mirrors Django's `AbstractUser` class
    """

    name = models.CharField(_('name'), max_length=254, blank=True, default="")
    email = models.EmailField(_('email address'), max_length=254, unique=True)

    date_of_birth = models.DateField(blank=True, null=True)

    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=False,
    help_text=_('Designates whether this user should be treated as active. Unselect it instead of deleting accounts.'))

    USERNAME_FIELD = 'email'

    objects = manager.CustomUserManager()

    def __unicode__(self):
        return str(self.email)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return self.name

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.name.strip()

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def forgot_password(self, *args, **kwargs):
        """
        send random password and link the password edit form
        """

        User.password_change(self)
        super(User, self).save(*args, **kwargs)

    def password_change(self):
        password = User.objects.make_random_password()

        #Send random generated password and link to password edit form
        # Commenting this code as SMTP server not working
        ask_for_password_change(password, self.get_full_name(), self.email)

        self.set_password(password)

    @property
    def is_superuser(self):
        return self.is_staff

    @property
    def is_admin(self):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    def get_perms(self):
        all_perms = []
        for group in self.groups.all():
            all_perms += group.permissions.all()
        return all_perms

    def get_perms_names(self):
        all_perms = []
        for group in self.groups.all():
            for perm in group.permissions.all():
                all_perms.append(str(perm.codename))
        return all_perms

    def get_all_groups_names(self):
        all_groups = []
        for group in self.groups.all():
            all_groups.append(str(group.display_name))
        return all_groups

    def get_allowed_categories_as_writer(self):
        categories = []
        for i in self.groups.filter(name__contains="writer"):
            categories.append(i.name[0:-len('-writer')])
        return categories

    def get_allowed_categories_as_editor(self):
        categories = []
        for i in self.groups.filter(name__contains="writer"):
            categories.append(i.name[0:-len('-writer')])
        return categories

admin.site.register(CustomUser)