from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import User
from countries.admin import PlaceAdmin
from tags.models import TaggedPlace
from countries.models import Place


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username',
                           'password1',
                           'password2',
                           'email',
                           'first_name',
                           'last_name'),
            },
        ),
    )


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedPlace
    extra = 0
    min_num = 1


class CustomPlaceAdmin(PlaceAdmin):
    inlines = [TagInline]


admin.site.unregister(Place)
admin.site.register(Place, CustomPlaceAdmin)
