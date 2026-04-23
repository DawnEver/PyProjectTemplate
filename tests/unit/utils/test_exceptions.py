from unittest.mock import patch

import pytest

from app.utils.exceptions import (
    ParameterException,
    deprecated,
    not_implemented,
)


@patch('app.utils.exceptions.log')
def test_parameter_exception(mock_log):
    """Test ParameterException."""
    exception = ParameterException('Invalid parameter')
    assert str(exception) == 'ParameterException: Invalid parameter'
    mock_log.assert_called_once_with('ParameterException: Invalid parameter', level='ERROR')



def test_not_implemented():
    """Test not_implemented decorator."""

    @not_implemented
    def dummy_function():
        pass

    with pytest.raises(NotImplementedError, match='dummy_function is not implemented yet.'):
        dummy_function()


def test_deprecated():
    """Test deprecated decorator."""

    @deprecated
    def dummy_function():
        pass

    with pytest.raises(DeprecationWarning, match='dummy_function has been deprecated.'):
        dummy_function()
