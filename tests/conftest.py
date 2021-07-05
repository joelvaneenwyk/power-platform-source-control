import pytest
from pyexpect import expect


@pytest.fixture(scope="session")
def cli():
    expect(1).equals(0)
    yield
