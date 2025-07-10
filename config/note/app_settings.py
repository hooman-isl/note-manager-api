from django.conf import settings


class AppSettings:
    def __init__(self, prefix):
        self.prefix = prefix

    def _settings(self, varname, default):
        return getattr(settings, self.prefix + varname, default)

    @property
    def DATETIME_FORMAT(self):
        return self._settings("DATETIME_FORMAT", "%Y-%m-%d %H:%M:%S")


_app_settings = AppSettings("NOTE_API_")


def __getattr__(name):
    # See https://peps.python.org/pep-0562/
    return getattr(_app_settings, name)
