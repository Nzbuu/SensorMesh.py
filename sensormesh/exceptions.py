class SensorMeshError(Exception):
    pass


class ConfigurationError(SensorMeshError):
    pass


class DuplicateFieldError(SensorMeshError):
    pass
