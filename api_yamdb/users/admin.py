from users.models import User

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'role',
                  'first_name',
                  'last_name',
                  'bio',
                  'confirm_code'
                  )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    class Meta:
        model = User
        fields = ('username', 'email')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username',
                    'email',
                    'is_active',
                    'is_admin',
                    'role',
                    'first_name',
                    'last_name',
                    'bio',
                    'confirm_code')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'email')}),
        ('Personal info', {'fields': ('first_name',
                                      'last_name',
                                      'bio')}),
        ('Permissions', {'fields': ('role',
                                    'confirm_code',
                                    'is_admin',
                                    'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username',
                       'email',
                       'is_active',
                       'is_admin',
                       'role',
                       'first_name',
                       'last_name',
                       'bio',
                       'confirm_code'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
