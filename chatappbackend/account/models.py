from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group, Permission

class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, mobilenumber, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, mobilenumber=mobilenumber, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, mobilenumber, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)

        return self.create_user(email, name, mobilenumber, password, **extra_fields)

class UserAccount(AbstractBaseUser, PermissionsMixin):
    username  = models.CharField(max_length=50,null= True,unique=True)
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(unique=True, max_length=255)
    mobilenumber = models.CharField(max_length=20, null=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name="useraccount_set",  
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="useraccount_set",  
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobilenumber']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin or super().has_perm(perm, obj)
    
    def has_module_perms(self, app_label):
        return self.is_admin or super().has_module_perms(app_label)
