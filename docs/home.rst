***************
Приложение Home
***************

Представления (Views)
=====================
Находятся в файле *home/views.py*.

.. function:: dashboard(request)

    Показывает стартовую страницу сервиса. Отображает шаблон *home/dashboard.html*.

    Представление вызывается при запросе url */*.

    :param request: объект запроса
    :type request: HttpRequest
    :rtype: HttpResponse

Модели
======

Находятся в файле *home/models.py*.

.. class:: Region(models.Model)

    Модель для работы с таблицей `region`.

.. class:: City(models.Model)

    Модель для работы с таблицей `city`.

.. class:: Suburb(models.Model)

    Модель для работы с таблицей `suburb`.

.. class:: PricingMethod(models.Model)

    Модель для работы с таблицей `pricing_method`.

.. class:: PropertyType(models.Model)

    Модель для работы с таблицей `property_type`.

.. class:: House(models.Model)

    Модель для работы с таблицей `house`.

    *Методы класса:*

    .. function:: get_address(self)

        Возвращает адрес дома в удобном формате.

    .. function:: get_city(self)

        Возвращает город дома.

    .. function:: get_property_type(self)

        Возвращает значение поля *Property Type* дома.

    .. function:: get_price(self)

        Возвращает значение стоимости дома.

.. class:: OpenHomes(models.Model)

    Модель для работы с таблицей `open_homes`.

.. class:: VHousesForTables(models.Model)

    Модель для работы с БД-представлением (view) `v_houses_for_tables`.

    .. function:: get_new_houses(filter_data, excluded_pks)

        Статичный метод, который возвращает новые дома согласно фильтрам пользователя.

        :param filter_data: список фильтров и их данных
        :type filter_data: list
        :param excluded_pks: список идентификаторов домов, которые не нужно включать в результаты работы метода
        :type excluded_pks: list
        :rtype: QuerySet

        **Алгоритм работы**

        #. Объявить общий пустой QuerySet.
        #. Для каждого фильтра из filter_data сформировать QuerySet, который объединяется с общим QuerySet.
        #. Вернуть общий QuerySet.

    .. function:: search(filter)

        Статичный метод, который возвращает дома согласно фильтру.

        :param filter: словарь фильтра
        :type filter: dict
        :rtype: QuerySet

        **Алгоритм работы**

        #. Сделать выборку в БД с помощью v_houses_for_tables домов, применив фильтр.
        #. Вернуть QuerySet.


.. class:: Agency(models.Model)

    Модель для работы с таблицей `agency`.

.. class:: Agent(models.Model)

    Модель для работы с БД-представлением (view) `agent`.

Шаблоны
=======

Находятся в каталоге *home/templates*.

Административная часть
======================

Описание классов для модуля администрирования django-admin аходятся в файле *home/admin.py*.

.. class:: HouseAdmin(admin.ModelAdmin)

    Класс для описания администрирования модели House.

.. class:: AgencyAdmin(admin.ModelAdmin)

    Класс для описания администрирования модели Agency.

.. class:: AgencyAdmin(admin.ModelAdmin)

    Класс для описания администрирования модели Agency.

.. class:: AgencyAdmin(admin.ModelAdmin)

    Класс для описания администрирования модели Agency.

.. class:: AgentAdmin(admin.ModelAdmin)

    Класс для описания администрирования модели Agent.

JavaScript
==========

Скрипты приложения находятся в каталоге *home/static/home/js*.

sidebar-size.js
    Скрипт для запоминания состояния sidebar (свёрнуто/развёрнуто).
