*******************
Приложение Listings
*******************

Представления (Views)
=====================

Находятся в файле *accounts/views.py*.

.. function:: new_listings(request)

    Показывает страницу с новыми листингами. Список листингов формируется на основании фильтров пользователя.

    Представление вызывается при запросе url */listings/new/*.

    :param request: объект запроса
    :type request: HttpRequest
    :rtype: HttpResponse

    **Алгоритм работы**

        #. Получить список фильтров текущего пользователя используя модель HousesFilter.
        #. Получить список листингов на основании фильтров, используя модель VHousesForTables.
        #. Отобразить страницу (шаблон `listings/new.html`).

.. function:: liked_listings(request)

    Показывает страницу с лайкнутыми листингами.

    Представление вызывается при запросе url */listings/liked/*.

    :param request: объект запроса
    :type request: HttpRequest
    :rtype: HttpResponse

    **Алгоритм работы**

        #. Получить список лайкнутых листингов текущего пользователя, используя модель MarkedHouse.
        #. Отобразить страницу (шаблон `listings/liked.html`).

.. function:: disliked_listings(request)

    Показывает страницу с дизлайкнутыми листингами.

    Представление вызывается при запросе url */listings/disliked/*.

    :param request: объект запроса
    :type request: HttpRequest
    :rtype: HttpResponse

    **Алгоритм работы**

        #. Получить список дизлайкнутых листингов текущего пользователя, используя модель MarkedHouse.
        #. Отобразить страницу (шаблон `listings/disliked.html`).

.. function:: still_thinking_listings(request)

    Показывает страницу с листингами, помеченными отметкой "Still thinking".

    Представление вызывается при запросе url */listings/still-thinking/*.

    :param request: объект запроса
    :type request: HttpRequest
    :rtype: HttpResponse

**Алгоритм работы**

    #. Получить список листингов текущего пользователя, помеченных отметкой "Still thinking". Используется модель MarkedHouse.
    #. Отобразить страницу (шаблон `listings/still_thinking.html`).

.. function:: show_new_listing(request, pk)

    Показывает страницу с новым листингом.

    Представление вызывается при запросе url */listings/new/show/:pk*, где *:pk* - идентификатор дома.

    :param request: объект запроса
    :type request: HttpRequest
    :param pk: идентификатор листинга
    :type pk: integer
    :rtype: HttpResponse

    **Алгоритм работы**

        #. Получить листинг из БД, используя модель House.
        #. Если листинг не найден, то отобразить 404 страницу.
        #. Распарсить фотографии листинга в список.
        #. Отобразить страницу (шаблон `listings/show.html`).

.. function:: show_liked_listing(request, pk)

    Показывает страницу с лайкнутым листингом.

    Представление вызывается при запросе url */listings/liked/show/:pk*, где *:pk* - идентификатор дома.

    :param request: объект запроса
    :type request: HttpRequest
    :param pk: идентификатор листинга
    :type pk: integer
    :rtype: HttpResponse

    **Алгоритм работы**

        #. Получить листинг из БД, используя модель MarkedHouse.
        #. Если листинг не найден, то отобразить 404 страницу.
        #. Распарсить фотографии листинга в список.
        #. Получить пользовательские данные этого дома, используя модель HouseUserData.
        #. Отобразить страницу (шаблон `listings/show.html`).

.. function:: delete_other_expenses_item(request, pk)

    Удаляет объект модели OtherExpense.

    Представление вызывается при запросе url */listings/liked/delete-other-expenses-item/:pk*, где *:pk* - идентификатор объекта OtherExpense.

    :param request: объект запроса
    :type request: HttpRequest
    :param pk: идентификатор OtherExpense
    :type pk: integer
    :rtype: HttpResponse

    **Алгоритм работы**

        #. Получить объект из БД, используя модель OtherExpense.
        #. Если объект не найден, то вернуть JSON с ошибкой.
        #. Проверить принадлежит ли этот объект текущему пользователю. Если нет, то вернуть JSON с ошибкой.
        #. Удалить объект.
        #. Вернуть JSON с результатами операции.


.. function:: create_other_expenses_item(request)

    Создаёт объект модели OtherExpense.

    Представление вызывается при запросе url */listings/liked/create-other-expenses-item/*.

    :param request: объект запроса
    :type request: HttpRequest
    :rtype: HttpResponse

    **Алгоритм работы**

        #. Проверить проходят ли валидацию данные, переданные в POST. Если нет, то вернуть JSON с ошибками.
        #. Создать объект OtherExpense и сохранить его.
        #. Вернуть JSON с результатами операции.

.. function:: save_calculator_data(request, house_id)

    Сохраняет данные калькулятора для определённого дома.

    Представление вызывается при запросе url */listings/save-calculator-data/house_id*, где *:house_id* - идентификатор дома.

    :param request: объект запроса
    :type request: HttpRequest
    :param house_id: идентификатор дома
    :type house_id: integer
    :rtype: HttpResponse

    **Алгоритм работы**

        #. Проверить проходят ли валидацию данные, переданные в POST. Если нет, то вернуть JSON с ошибками.
        #. Сохранить данные калькулятора с помощью модели Calculator.
        #. Вернуть JSON с результатами операции.

.. function:: reset_calculator_data(request, house_id)

    Сбрасывает данные калькулятора на данные по умолчанию.

    Представление вызывается при запросе url */listings/reset-calculator-data/:house_id*, где *:house_id* - идентификатор дома.

    :param request: объект запроса
    :type request: HttpRequest
    :param house_id: идентификатор дома
    :type house_id: integer
    :rtype: HttpResponse

    **Алгоритм работы**

        #. Получить данные калькулятора дома house_id текущего пользователя с помощью модели Calculator. Если даннвых нет, то вернуть JSON с ошибками.
        #. Удалить данные калькулятора.
        #. Создать новые калькулятор с даыынми по умолчанию с помощью модели Calculator.
        #. Вернуть JSON с результатами операции.

.. function:: show_disliked_listing(request, pk)

    Показывает страницу с новым листингом.

    Представление вызывается при запросе url */listings/disliked/show/:pk*, где *:pk* - идентификатор дома.

    :param request: объект запроса
    :type request: HttpRequest
    :param pk: идентификатор листинга
    :type pk: integer
    :rtype: HttpResponse

    **Алгоритм работы**

        #. Получить листинг из БД, используя модель House.
        #. Если листинг не найден, то отобразить 404 страницу.
        #. Распаристь фотографии листинга в список.
        #. Отобразить страницу (шаблон `listings/show.html`).

.. function:: show_still_thinking_listing(request, pk)

    Показывает страницу с листингом, помеченным меткой "Still thinking".

    Представление вызывается при запросе url */listings/still-thinking/show/:pk*, где *:pk* - идентификатор дома.

    :param request: объект запроса
    :type request: HttpRequest
    :param pk: идентификатор листинга
    :type pk: integer
    :rtype: HttpResponse

    **Алгоритм работы**

        #. Получить листинг из БД, используя модель House.
        #. Если листинг не найден, то отобразить 404 страницу.
        #. Распаристь фотографии листинга в список.
        #. Отобразить страницу (шаблон `listings/show.html`).

.. function:: mark_as_liked(request, pk)

    Делает пометку "Like" дому.

    Представление вызывается при запросе url */listings/mark-as-liked/:pk*, где *:pk* - идентификатор дома.

    :param request: объект запроса
    :type request: HttpRequest
    :param pk: идентификатор листинга
    :type pk: integer
    :rtype: HttpResponse

    **Алгоритм работы**

        #. Получить листинг из БД, используя модель House.
        #. Если листинг не найден, то отобразить 404 страницу.
        #. Создать запись в таблице `listings_markedhouse` со значением mark_id = 1.
        #. Переадресовать пользователя на страницу лайкнутого дома.

.. function:: mark_as_disliked(request, pk)

    Делает пометку "Dislike" дому.

    Представление вызывается при запросе url */listings/mark-as-disliked/:pk*, где *:pk* - идентификатор дома.

    :param request: объект запроса
    :type request: HttpRequest
    :param pk: идентификатор листинга
    :type pk: integer
    :rtype: HttpResponse

    **Алгоритм работы**

        #. Получить листинг из БД, используя модель House.
        #. Если листинг не найден, то отобразить 404 страницу.
        #. Создать запись в таблице `listings_markedhouse` со значением mark_id = 2.
        #. Переадресовать пользователя на страницу списка новых домов или, при наличии GET-параметра *return_url*, на него.

.. function:: mark_as_still_thinking(request, pk)

    Делает пометку "Still thinking" дому.

    Представление вызывается при запросе url */listings/mark-as-still-thinking/:pk*, где *:pk* - идентификатор дома.

    :param request: объект запроса
    :type request: HttpRequest
    :param pk: идентификатор листинга
    :type pk: integer
    :rtype: HttpResponse

    **Алгоритм работы**

        #. Получить листинг из БД, используя модель House.
        #. Если листинг не найден, то отобразить 404 страницу.
        #. Создать запись в таблице `listings_markedhouse` со значением mark_id = 3.
        #. Переадресовать пользователя на страницу списка новых домов или, при наличии GET-параметра *return_url*, на него.


.. function:: get_deposit_values(request)

    Возвращает JSON со значением built_loan_deposit для глобальных и пользовательских констант.

    Представление вызывается при запросе url */listings/get-deposit-values/*.

    :param request: объект запроса
    :type request: HttpRequest
    :param pk: идентификатор листинга
    :type pk: integer
    :rtype: JsonResponse

    **Алгоритм работы**

        #. Получить из БД списки глобальных и пользовательских констант с помощью моделей GlobalConstants, Constants.
        #. Если параметр GET is_new_build равен 1, то вернуть JSON с константами new_built_loan_deposit, иначе - с loan_deposit.

Модели
======

Находятся в файле *listings/models.py*.

.. class:: Mark(models.Model)

    Модель для работы с таблицей `listings_mark`.

.. class:: MarkedHouse(models.Model)

    Модель для работы с таблицей `listings_markedhouse`.

.. class:: HouseUserData(models.Model)

    Модель для работы с таблицей `listings_houseuserdata`.

.. class:: OtherExpense(models.Model)

    Модель для работы с таблицей `listings_otherexpense`.

.. class:: Calculator(models.Model)

    Модель для работы с таблицей `listings_calculator`.

    .. function:: get_or_create(user, house):

        Получает данные калькулятора по параметрам, если он существует или создаёт новый с параметрами по умолчанию.

        :param user: объект текущего пользователя
        :param house: объект дома


Шаблоны
=======

Находятся в каталоге *listings/templates*.

Административная часть
======================

Описание классов для модуля администрирования django-admin аходятся в файле *listings/admin.py*.

.. class:: HouseUserDataAdmin(admin.ModelAdmin)

    Класс для описания администрирования модели HouseUserData.

JavaScript
==========

Скрипты приложения находятся в каталоге *listings/static/listings/js*.

calculator.js
    Отвечает за вид и работу калькулятора.

my-data.js
    Отвечает за вид и работу формы My Data.
