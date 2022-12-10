from models import CustomUser
import pytest


@pytest.mark.django_db
def test_user_create():
  CustomUser.objects.create_user('admin@admib.com', 'admin123password')
  assert CustomUser.objects.count() == 1


