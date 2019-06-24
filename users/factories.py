import factory
from django.contrib.auth import get_user_model


User = get_user_model()


class UserFactory(factory.Factory):

    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')
