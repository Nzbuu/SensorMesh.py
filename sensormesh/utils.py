class DataAdapter(object):
    def __init__(self, feeds=None):
        super().__init__()

        self._local_names = {}
        self._remote_names = {}
        if feeds:
            self.add_field(**feeds)

    def add_field(self, **kwargs):
        for remote_name, local_name in kwargs.items():
            if not remote_name or not local_name:
                raise ValueError('Inputs must be non-empty strings')

            if remote_name in self._local_names:
                if self._local_names[remote_name] == local_name:
                    # already have remote_name <-> local_name
                    pass
                else:
                    # already have remote_name but doesn't correspond to
                    # local_name
                    raise KeyError('Local and Remote names must be unique.')
            elif local_name in self._remote_names:
                    # already have local_name but doesn't correspond to
                    # remote_name
                raise KeyError('Local and Remote names must be unique.')
            else:
                self._local_names[remote_name] = local_name
                self._remote_names[local_name] = remote_name

    def parse_local(self, local_data):
        return self._rename_fields(local_data, self._remote_names)

    def parse_remote(self, remote_data):
        return self._rename_fields(remote_data, self._local_names)

    def _rename_fields(self, data, names):
        return {names[k]: data[k] for k in names if k in data}

