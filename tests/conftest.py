from unittest.mock import Mock

import pytest


@pytest.fixture
def notifier():
    return Mock()
