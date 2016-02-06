import pytest

from sensormesh.utils import DataAdapter


class TestDataAdapter:
    def test_can_create_object(self):
        o = DataAdapter()
        assert not o._local_to_remote
        assert not o._remote_to_local

    # Configuration tests
    def test_can_add_fields(self):
        o = DataAdapter()
        o.add_field('l1', 'r1')
        o.add_field('l2', 'r2')
        assert o._remote_to_local == {'r1': 'l1', 'r2': 'l2'}
        assert o._local_to_remote == {'l1': 'r1', 'l2': 'r2'}

    def test_names_are_ordered(self):
        o = DataAdapter()
        o.add_field('l5', 'r1')
        o.add_field('l2', 'r2')
        o.add_field('l6', 'r4')
        o.add_field('l4', 'r3')
        assert list(o.local_names) == ['l5', 'l2', 'l6', 'l4']
        assert list(o.remote_names) == ['r1', 'r2', 'r4', 'r3']

    def test_cannot_add_empty_local_name(self):
        o = DataAdapter()
        with pytest.raises(ValueError):
            o.add_field('', 'r')

    def test_cannot_add_empty_remote_name(self):
        o = DataAdapter()
        with pytest.raises(ValueError):
            o.add_field('', 'a')

    def test_cannot_duplicate_remote_name(self):
        o = DataAdapter()
        o.add_field('l2', 'r')
        with pytest.raises(KeyError):
            o.add_field('l1', 'r')

    def test_cannot_duplicate_local_name(self):
        o = DataAdapter()
        o.add_field('l', 'r1')
        with pytest.raises(KeyError):
            o.add_field('l', 'r2')

    def test_can_duplicate_whole_entry(self):
        o = DataAdapter()
        o.add_field('l', 'r')
        o.add_field('l', 'r')
        assert o._remote_to_local == {'r': 'l'}
        assert o._local_to_remote == {'l': 'r'}

    # Parsing tests
    def test_can_convert_local_data(self):
        o = DataAdapter()
        o.add_field('l1', 'r1')
        o.add_field('l2', 'r2')

        remote = o.create_remote_struct({'l1': 5, 'l2': 3})
        assert remote == {'r1': 5, 'r2': 3}

    def test_ignore_missing_local_data(self):
        o = DataAdapter()
        o.add_field('l1', 'r1')
        o.add_field('l2', 'r2')

        remote = o.create_remote_struct({'l1': 5})
        assert remote == {'r1': 5}

    def test_create_missing_local_data_as_option(self):
        o = DataAdapter()
        o.create_missing = True
        o.add_field('l1', 'r1')
        o.add_field('l2', 'r2')

        remote = o.create_remote_struct({'l1': 5})
        assert remote == {'r1': 5, 'r2': None}

    def test_ignore_extra_local_field(self):
        o = DataAdapter()
        o.add_field('l2', 'r2')

        remote = o.create_remote_struct({'l1': 5, 'l2': 3})
        assert remote == {'r2': 3}

    def test_can_convert_remote_data(self):
        o = DataAdapter()
        o.add_field('l1', 'r1')
        o.add_field('l2', 'r2')

        local = o.create_local_struct({'r1': -3, 'r2': 4})
        assert local == {'l1': -3, 'l2': 4}

    def test_ignore_missing_remote_data(self):
        o = DataAdapter()
        o.add_field('l1', 'r1')
        o.add_field('l2', 'r2')

        local = o.create_local_struct({'r1': -3})
        assert local == {'l1': -3}

    def test_create_missing_remote_data_as_option(self):
        o = DataAdapter()
        o.create_missing = True
        o.add_field('l1', 'r1')
        o.add_field('l2', 'r2')

        local = o.create_local_struct({'r1': -3})
        assert local == {'l1': -3, 'l2': None}

    def test_ignore_extra_remote_field(self):
        o = DataAdapter()
        o.add_field('l2', 'r2')

        local = o.create_local_struct({'r1': -3, 'r2': 4})
        assert local == {'l2': 4}
