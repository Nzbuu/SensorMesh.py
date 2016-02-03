from unittest.mock import Mock

import pytest

from sensormesh.base import DataSourceWrapper


class TestDataSourceWrapper:
    def test_can_create_without_callable(self):
        s = DataSourceWrapper(name='test_source')
        assert s.name == 'test_source'

    def test_throws_on_extra_positional_args(self):
        with pytest.raises(ValueError):
            s = DataSourceWrapper('test_source', 'x')  # 'test_source' is name

    def test_can_wrap_one_callable(self):
        m = Mock(return_value=10)
        s = DataSourceWrapper(value=m)

        d = s.read()
        assert d == {'value': 10}

    def test_can_wrap_two_callables(self):
        m1 = Mock(return_value=10)
        m2 = Mock(return_value=20)
        s = DataSourceWrapper(field1=m1, field2=m2)

        d = s.read()
        assert d == {'field1': 10, 'field2': 20}
