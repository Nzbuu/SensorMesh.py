# -*- coding: utf-8 -*-

from collections import OrderedDict


class DataAdapter(object):
    def __init__(self):
        super().__init__()

        self._remote_to_local = OrderedDict()
        self._local_to_remote = OrderedDict()
        self.create_missing = False

    @property
    def count(self):
        return len(self._remote_to_local)

    @property
    def local_names(self):
        return self._local_to_remote.keys()

    @property
    def remote_names(self):
        return self._remote_to_local.keys()

    def add_field(self, local_name, remote_name):
        if not remote_name or not local_name:
            raise ValueError('Inputs must be non-empty strings')

        if (remote_name in self._remote_to_local or
                    local_name in self._local_to_remote):
            # already have local_name or remote_name
            raise KeyError('Local and Remote names must be unique.')
        else:
            self._remote_to_local[remote_name] = local_name
            self._local_to_remote[local_name] = remote_name

    def create_remote_struct(self, local_data):
        return self._rename_fields(local_data, self._local_to_remote)

    def create_local_struct(self, remote_data):
        return self._rename_fields(remote_data, self._remote_to_local)

    def _rename_fields(self, data_in, names):
        data_out = {}
        for name_in, name_out in names.items():
            if name_in in data_in:
                data_out[name_out] = data_in[name_in]
            elif self.create_missing:
                data_out[name_out] = None
        return data_out
