import pytest

from sensormesh.base import DataAdapter


class TestDataAdapter:
    def test_can_create_object(self):
        o = DataAdapter()
        assert not o._remote_names
        assert not o._local_names

    # Configuration tests
    def test_can_configure_with_feeds(self):
        o = DataAdapter(feeds={'r1': 'l1', 'r2': 'l2'})
        assert o._local_names == {'r1': 'l1', 'r2': 'l2'}
        assert o._remote_names == {'l1': 'r1', 'l2': 'r2'}

    def test_can_add_fields(self):
        o = DataAdapter(feeds={'r2': 'l2'})
        o.add_field(r1='l1')
        assert o._local_names == {'r1': 'l1', 'r2': 'l2'}
        assert o._remote_names == {'l1': 'r1', 'l2': 'r2'}

    def test_cannot_add_empty_local_name(self):
        with pytest.raises(ValueError):
            o = DataAdapter(feeds={'a': ''})

    def test_cannot_add_empty_remote_name(self):
        with pytest.raises(ValueError):
            o = DataAdapter(feeds={'': 'a'})

    def test_cannot_duplicate_remote_name(self):
        o = DataAdapter(feeds={'r': 'l2'})
        with pytest.raises(KeyError):
            o.add_field(r='l1')

    def test_cannot_duplicate_local_name(self):
        o = DataAdapter(feeds={'r2': 'l'})
        with pytest.raises(KeyError):
            o.add_field(r1='l')

    def test_can_duplicate_whole_entry(self):
        o = DataAdapter(feeds={'r': 'l'})
        o.add_field(r='l')
        assert o._local_names == {'r': 'l'}
        assert o._remote_names == {'l': 'r'}

    # Parsing tests
    def test_can_convert_local_data(self):
        o = DataAdapter(feeds={'r1': 'l1', 'r2': 'l2'})
        remote = o.parse_local({'l1': 5, 'l2': 3})
        assert remote == {'r1': 5, 'r2': 3}

    def test_ignore_missing_local_data(self):
        o = DataAdapter(feeds={'r1': 'l1', 'r2': 'l2'})
        remote = o.parse_local({'l1': 5})
        assert remote == {'r1': 5}

    def test_ignore_missing_local_field(self):
        o = DataAdapter(feeds={'r2': 'l2'})
        remote = o.parse_local({'l1': 5, 'l2': 3})
        assert remote == {'r2': 3}

    def test_can_convert_remote_data(self):
        o = DataAdapter(feeds={'r1': 'l1', 'r2': 'l2'})
        local = o.parse_remote({'r1': -3, 'r2': 4})
        assert local == {'l1': -3, 'l2': 4}

    def test_ignore_missing_remote_data(self):
        o = DataAdapter(feeds={'r1': 'l1', 'r2': 'l2'})
        local = o.parse_remote({'r1': -3})
        assert local == {'l1': -3}

    def test_ignore_missing_remote_field(self):
        o = DataAdapter(feeds={'r2': 'l2'})
        local = o.parse_remote({'r1': -3, 'r2': 4})
        assert local == {'l2': 4}
