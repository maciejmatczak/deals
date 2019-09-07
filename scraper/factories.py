import factory

from .models import ScrapingTask, ScrapingJob
from users.factories import UserFactory


class ScrapingTaskFactory(factory.DjangoModelFactory):

    class Meta:
        model = ScrapingTask

    title = factory.Faker('sentence')
    task = factory.Faker('text')
    favourite = factory.Faker('boolean')
    user = factory.SubFactory(UserFactory)


class ScrapingJobFactory(factory.DjangoModelFactory):

    class Meta:
        model = ScrapingJob

    url = factory.Faker('url')
    active = factory.Faker('boolean')
    multiple = factory.Faker('boolean')
    description = factory.Faker('text')
    running_time = factory.Faker('time')

    scraping_task = factory.SubFactory(ScrapingTaskFactory)
    user = factory.SubFactory(UserFactory)
