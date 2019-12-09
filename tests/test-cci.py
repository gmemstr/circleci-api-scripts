# Tests for cci.py "shared functions" file
import cci
from tests import tests


def test_get_data():
    result = cci.get_data("http://localhost:7483")
    if "success" in result and result['success']:
        tests.success()
    else:
        tests.fail()


def test_post_data():
    result = cci.post_data("http://localhost:7483")
    if "success" in result and result['success']:
        tests.success()
    else:
        tests.fail()


def test_is_valid_slug_short():
    test_valid_s = cci.is_valid_slug("gh/testing/testing")
    if test_valid_s:
        tests.success("")
    test_invalid_s = cci.is_valid_slug("cci/testing/testing")
    if not test_invalid_s:
        tests.success("")


def test_is_valid_slug_long():
    test_valid_l = cci.is_valid_slug("github/testing/testing")
    if test_valid_l:
        tests.success()
    test_invalid_l = cci.is_valid_slug("circleci/testing/testing")
    if not test_invalid_l:
        tests.success()
