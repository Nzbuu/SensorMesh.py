# -*- coding: utf-8 -*-

import unittest.mock as mock

import pytest

from sensormesh.sources import DataSourceWrapper


class TestDataSourceWrapper:
    def test_cannot_create_without_callable(self):
        with pytest.raises(ValueError):
            _ = DataSourceWrapper(name='test_source')

    def test_default_field_is_value(self):
        m = mock.Mock(return_value=10)
        s = DataSourceWrapper(source=m, name='test_source')
        assert s.name == 'test_source'
        assert s.fields == ['value']

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

    def test_can_wrap_object_properties(self):
        class O:
            def __init__(self):
                self._count = 0

            @property
            def value(self):
                self._count += 1
                return self._count

        obj = O()
        s = DataSourceWrapper(source=obj, fields=[('result', 'value')])

        with s:
            d = s.read()
            assert d == {'result': 1}

            d = s.read()
            assert d == {'result': 2}
