import unittest.mock as mock

import pytest

from sensormesh.endpoints import DataSourceWrapper, ConfigurationError


class TestDataSourceWrapper:
    def test_cannot_create_without_callable(self):
        with pytest.raises(ConfigurationError):
            s = DataSourceWrapper(name='test_source')

    def test_default_field_is_value(self):
        m = mock.Mock(return_value=10)
        s = DataSourceWrapper(source=m, name='test_source')
        assert s.name == 'test_source'
        assert s.fields == ['value']

    def test_can_wrap_one_callable(self):
        m = mock.Mock(return_value=10)
        s = DataSourceWrapper(fields=['count'], source=[m])

        assert s.fields == ['count']

        with s:
            d = s.read()
        assert d == {'count': 10}

    def test_can_wrap_two_callables(self):
        m1 = mock.Mock(return_value=10)
        m2 = mock.Mock(return_value=20)
        s = DataSourceWrapper(fields=['field1', 'field2'], source=[m1, m2])

        assert s.fields == ['field1', 'field2']

        with s:
            d = s.read()
        assert d == {'field1': 10, 'field2': 20}

    def test_can_wrap_single_output(self):
        m = mock.Mock(return_value=(110, 120))
        s = DataSourceWrapper(fields=['field3'], source=m)

        assert s.fields == ['field3']

        with s:
            d = s.read()
        assert d == {'field3': (110, 120)}

    def test_can_wrap_multiple_outputs(self):
        m = mock.Mock(return_value=(210, 220))
        s = DataSourceWrapper(fields=['field3', 'field1'], source=m)

        assert s.fields == ['field3', 'field1']

        with s:
            d = s.read()
        assert d == {'field3': 210, 'field1': 220}

    def test_can_wrap_two_callables_with_mapping(self):
        m1 = mock.Mock(return_value=10)
        m2 = mock.Mock(return_value=20)
        s = DataSourceWrapper(fields=['field1', ('field2', 'remote2')], source=[m1, m2])

        assert s.fields == ['field1', 'field2']

        with s:
            d = s.read()
        assert d == {'field1': 10, 'field2': 20}

    def test_can_wrap_single_output_with_mapping(self):
        m = mock.Mock(return_value=(110, 120))
        s = DataSourceWrapper(fields=[('field3', 'remote3')], source=m)

        assert s.fields == ['field3']

        with s:
            d = s.read()
        assert d == {'field3': (110, 120)}

    def test_can_wrap_multiple_outputs_with_mapping(self):
        m = mock.Mock(return_value=(210, 220))
        s = DataSourceWrapper(fields=[('field3', 'remote3'), 'field1'], source=m)

        assert s.fields == ['field3', 'field1']

        with s:
            d = s.read()
        assert d == {'field3': 210, 'field1': 220}
