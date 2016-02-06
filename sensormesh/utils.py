class DataAdapter(object):
    def __init__(self):
        super().__init__()

        self._remote_to_local = {}
        self._local_to_remote = {}

    def add_field(self, local_name, remote_name):
        if not remote_name or not local_name:
            raise ValueError('Inputs must be non-empty strings')

        if remote_name in self._remote_to_local:
            if self._remote_to_local[remote_name] == local_name:
                # already have remote_name <-> local_name
                pass
            else:
                # already have remote_name but doesn't correspond to
                # local_name
                raise KeyError('Local and Remote names must be unique.')
        elif local_name in self._local_to_remote:
                # already have local_name but doesn't correspond to
                # remote_name
            raise KeyError('Local and Remote names must be unique.')
        else:
            self._remote_to_local[remote_name] = local_name
            self._local_to_remote[local_name] = remote_name

    def parse_local(self, local_data):
        return self._rename_fields(local_data, self._local_to_remote)

    def parse_remote(self, remote_data):
        return self._rename_fields(remote_data, self._remote_to_local)

    def _rename_fields(self, data, names):
        return {names[k]: data[k] for k in names if k in data}

