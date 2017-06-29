*******************
Приложение Settings
*******************

Модели
======

Находятся в файле *settings/models.py*.

.. class:: Global(models.Model)

    Модель для работы с таблицей `settings_global`.

Административная часть
======================

Описание классов для модуля администрирования django-admin находятся в файле *settings/admin.py*.

.. class:: DeleteNotAllowedModelAdmin(SingleModelAdmin)

    Класс для запрета удаления записи модели.

Регистрация модели Global в django-admin:

.. code-block:: python

   admin.site.register(Global, DeleteNotAllowedModelAdmin)
