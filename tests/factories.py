import factory
from faker import Faker
from app.models import User
import uuid

fake = Faker()

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "flush"

    id = factory.LazyFunction(uuid.uuid4)
    email = factory.LazyAttribute(lambda _: fake.email())
    encrypted_password = factory.LazyAttribute(lambda _: fake.password(length=10))
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    status = "active"
