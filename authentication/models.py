from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None):
        if not email:
            raise ValueError('O email é obrigatório')

        if not username:
            username = self.generate_unique_username()

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, email=None, password=None):
        if not email:
            raise ValueError('The email is required')

        if not username:
            username = email.split('@')[0]

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            is_staff=True,
            is_superuser=True,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def generate_unique_username(self):
        # Generate a unique username using a logic specific to your application
        # For example, you can use a combination of the user's email and a random string
        # Modify this method according to your needs
        pass

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    # Define the permissions
    class Meta:
        permissions = [
            ("can_view_files", "can view files"),
            ("candownloadfiles", "Can download files"),
            ("can_view_files_scripts", "can view files and scripts"),
            ("can_view_database", "can view database"),
            ("can_execute_scripts", "can execute scripts"),
            ("can_view_files_sftp", "can view files and sftp"),
            ("kubernetes", "can view kubernetes"),
            ("docker", "can view docker"),
            ("jenkins", "can view jenkins"),
            ("git", "can view git"),
            ("gitlab", "can view gitlab"),
            ("ansible", "can view ansible"),
            ("terraform", "can view terraform"),
            ("grafana", "can view grafana"),
            ("prometheus", "can view prometheus"),
            ("kibana", "can view kibana"),
            ("postgresql", "can view postgresql"),
            ("rabbitmq", "can view rabbitmq"),
            ("mongodb", "can view mongodb"),
            ("elasticsearch", "can view elasticsearch"),
            ("redis", "can view redis"),
            ("nginx", "can view nginx"),
            
        ]

    def __str__(self):
        return self.email
