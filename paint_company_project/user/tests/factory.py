from django.contrib.auth import get_user_model

from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    email = "test@mail.com"
    username = "test_user"

    class Meta:
        model = get_user_model()
        django_get_or_create = ["email"]
