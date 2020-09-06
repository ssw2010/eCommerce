from django.apps import AppConfig


class StoreConfig(AppConfig):
    name = 'store'

    def ready(self):
    	import store.signals

class PagesConfig(AppConfig):
    name = 'pages'

class PollsConfig(AppConfig):
    name = 'polls'