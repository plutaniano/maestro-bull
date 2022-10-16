from bull.apps.user.models import User
from django.contrib import admin, auth
from django.contrib.auth.models import ContentType, Permission


class UserCreateForm(auth.forms.UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
        )


@admin.register(User)
class UserAdmin(auth.admin.UserAdmin):
    list_display = (
        "id",
        "nome",
        "advisor_id",
        "email",
        "branch",
        "slack",
        "is_active",
        "birth_date",
    )
    fieldsets = [
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                    "slack",
                    "advisor_id",
                    "branch",
                    "hubspot_id",
                    "cpf",
                )
            },
        ),
        (
            "Informações pessoais",
            {"fields": ("first_name", "last_name", "email", "birth_date")},
        ),
        (
            "Permissões",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    ]

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "slack",
                    "advisor_id",
                    "password",
                )
            },
        ),
    )

    def nome(self, obj):
        return obj.get_full_name()


# Django default models
admin.site.register(Permission)
admin.site.register(ContentType)
