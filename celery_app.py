from celery import Celery
from settings import broker, backend


def connection(dct):
	return 'amqp://{user}:{password}@{ip}/{vhost}'.format(user=dct['user'], password=dct['password'], ip=dct['ip'], vhost=dct['vhost'])

app = Celery('vk_friends',
		broker=connection(broker),
		backend=connection(backend),
		include=['tasks'],
		)

app.conf.update(
	CELERY_TIMEZONE = 'Europe/Moscow',
	CELERY_ENABLE_UTC = True,
	CELERY_ACCEPT_CONTENT = ['pickle'],
)

if __name__ == '__main__':
    app.start()