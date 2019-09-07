import factory
from django.contrib.auth import get_user_model

from django.contrib.auth.hashers import make_password


User = get_user_model()


class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = make_password(factory.Faker('password'))
