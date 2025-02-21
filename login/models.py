from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django_tenants.models import TenantMixin, DomainMixin
from simple_history.models import HistoricalRecords

# 🚀 Multi-Tenant User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email required")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)

# 🚀 Multi-Tenant User Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email



# 🚀 Domain Model (for Subdomains)
class Domain(DomainMixin):
    pass

# 🚀 Multi-Tenant Company Model
class Company(TenantMixin):
    name = models.CharField(max_length=255, unique=True)
    schema_name = models.CharField(max_length=100, unique=True, default="public")
    created_at = models.DateTimeField(auto_now_add=True)
    
    auto_create_schema = True  # Automatically creates a separate schema

    def __str__(self):
        return self.name
    

# 🚀 Multi-Tenant Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True) 


    def __str__(self):
        return self.full_name


# 🚀 Role Model (Per Tenant)
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.JSONField(default=dict)

    def __str__(self):
        return self.name
