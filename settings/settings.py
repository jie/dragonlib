import os


class Settings(object):

    settings_data = {}

    def get_prefix(self):
        '''
        override prefix
        '''
        return 'dragon_'

    def __getattr__(self, name):
        if name.startswith(self.get_prefix()):

            if name in self.settings_data:
                return self.settings_data[name]

            if name in os.environ:
                value = os.environ.get(name)
                self.settings_data[name] = value
                return value
        return super(Settings, self).__getattribute__(name)


settings = Settings()
