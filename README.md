vk_friends
==========

Граф дружеских связей в vk.com. Больше инфы можно прочитать [здесь](http://habrahabr.ru/post/221251/) и [здесь](http://habrahabr.ru/post/N/). Если вам нужен старый релиз, то он [тут](https://github.com/stleon/vk_friends/releases/tag/v1.0.0). Перед тем, как что-то делать, рекомендую прочесть всю документацию.

##Что нужно

* Python 3.4
* [requests](https://github.com/kennethreitz/requests)
* [RabbitMQ](http://www.rabbitmq.com)
* [Celery](http://www.celeryproject.org)
* [networkx](https://github.com/networkx/networkx)

##Первые шаги

Для начала необходимо создать [Standalone-приложение](https://vk.com/dev/standalone) в VK. Делается это [там](https://vk.com/editapp?act=create). В итоге попросят ввести код-подтверждения, высланный на мобильный, после чего мы попадаем на страницу управления приложением. На вкладке **Настройки** нам пригодится **ID приложения** для получения **access_token**. 

Чтобы его получить необходимо [сформировать](https://vk.com/dev/auth_mobile) **url**:
```
https://oauth.vk.com/authorize?client_id=IDприложения&scope=friends,offline&redirect_uri=https://oauth.vk.com/blank.html&display=page&v=5.21&response_type=token
```

Если адрес сформирован правильно, переходим по нему и получаем нечто вроде:
```
https://oauth.vk.com/blank.html#access_token=ACCESS_TOKEN&expires_in=0&user_id=USER_ID
```

После этого редактируем файл **settings.py**, вставляя туда полученные **access_token** и **user_id**.

Далее переходим по ссылке **https://vk.com/editapp?id=IDприложения&section=functions** и создаем хранимую процедуру **getMutual**.
Копируем содержимое **execute_getMutual.js** в форму и сохраняем.

Для получения глубинного списка друзей (друзья-друзей и т.д.) проделываем те же самые действия с **execute_deepFriends.js**, назвав хранимую процедуру **deepFriends**.

Ура!

##RabbitMQ & Celery

После их установки необходимо создать **virtual host** для **RabbitMQ**:

```
rabbitmqctl add_vhost vk_friends
rabbitmqctl add_user user password
rabbitmqctl set_permissions -p vk_friends user ".*" ".*" ".*"
```

Далее в конфигурационном файле **RabbitMQ** (у меня это /usr/local/etc/rabbitmq/rabbitmq-env.conf) указать ip, на котором он установлен:

```
NODE_IP_ADDRESS=192.168.1.14 // example
```

В **settings.py** заполнить:

**broker/backend** - словари, содержащие информацию для доступа к брокеру и бэкенду

в соответствии с данными, введенными выше.

##Что дальше

Запускаем **RabbitMQ**:

```
rabbitmq-server
```

Затем воркера (из папки проекта):

```
celery -A tasks worker --loglevel=info
```

Воркеров может быть несколько.

Если вы все настроили правильно и нет никаких сообщений об ошибках, то:

```
python call.py
```

1 - Общие друзья, 2 - Друзья-друзей и тд, в зависимости от глубины (**deep** - в **settings.py**).

После первого запуска результат сохраняется в файлах **_dct**. Теперь можно рисовать/анализировать графы. По-умолчанию, **graph.py** работает с "глубинными друзьями". После запуска 

```
python graph.py
```

вы увидите некоторую информацию о графе, а в папке проекта появится файл **.png**. Для болиших графов рекомендую закомментировать строчку 

```
deep_friends.draw_graph()
```

##Полезности
В **settings.py** можете вбить **id** любого интересующего вас человека.

