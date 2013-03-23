from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from accounts.models import UserProfile, Customer, Domains

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'user profile'

# Same for the customer profile
class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    verbose_name_plural = 'customer profile'

# Same for the domain
class DomainInline(admin.StackedInline):
    model = Domains
    can_delete = False
    verbose_name_plural = 'custom domain'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, CustomerInline, DomainInline)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
