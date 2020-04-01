# coding: utf-8
import pytest

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


@pytest.fixture(scope='session')
def django_db_setup():
    pass


@pytest.fixture('function')
def client(db):
    from rest_framework.test import APIClient
    from django.contrib.auth.models import User
    user = User.objects.get(username='tjhb')
    client = APIClient()
    client.force_authenticate(user=user)
    return client
