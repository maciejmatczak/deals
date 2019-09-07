import pytest
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.mark.django_db
def test_standard_scenario(user_factory):
    user1 = user_factory.create()
    assert User.objects.count() == 1

    user2 = user_factory.create()
    assert User.objects.count() == 2
