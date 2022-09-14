"""Client object test"""

from async_reolink.rest import Client


def test_object():
    """Test can client be created"""

    assert Client()
