*******************
Приложение Accounts
*******************

Представления (Views)
=====================

Находятся в файле *accounts/views.py*.

.. function:: profile(request)

    Показывает страницу с формой редактирования, содержащей данные профиля пользователя, а также сохраняет данные формы.

    Представление вызывается при запросе url */accounts/settings/*.

    :param request: объект запроса
    :type request: HttpRequest
    :rtype: HttpResponse

**Алгоритм работы**

    #. Проверить тип запроса (GET или POST).
    #. Тип запроса - POST:
        #. Произвести валидацию данных.
        #. Если валидация успешна, то сохранить данные пользователя.
        #. Переадресовать на страницу профиля.
    #. Получить данные теущего пользователя с помощью модели *User* (используя свойство *user* параметра *request*).
    #. Отобразить страницу профиля (шаблон `accounts/profile.html`).

.. function:: house_filters(request)

    Показывает страницу со списком фильтров пользователя.

    Представление вызывается при запросе url */accounts/settings/house-filters/*.

    :param request: объект запроса
    :type request: HttpRequest
    :rtype: HttpResponse

**Алгоритм работы**

    #. Получить из БД списка фильтров с помощью модели HousesFilter.
    #. Отобразить страницу со списком фильтров (шаблон `accounts/house_filters.html`).

.. function:: region_and_cities_constants(request)

    Показывает страницу с формой редактирования, содержащей константы регионов и городов, а также сохраняет данные формы.

    Представление вызывается при запросе url */accounts/settings/region-and-cities-constants/*.

    :param request: объект запроса
    :type request: HttpRequest
    :rtype: HttpResponse

**Алгоритм работы**

    #. Проверить тип запроса (GET или POST).
    #. Тип запроса - POST:
        #. Произвести валидацию данных.
        #. Если валидация успешна, то сохранить данные.
        #. Переадресовать на страницу констант городов и регионов.
    #. Получить данные констант городов и регионов текущего пользователя с помощью модели *CitiesConstants*.
    #. Отобразить страницу констант городов и регионов (шаблон `accounts/region_and_cities_constants.html`).

.. function:: create_filter(request)

    Показывает страницу с формой создания фильтра, также сохраняет данные формы (создаёт фильтр).

    Представление вызывается при запросе url */accounts/settings/filters/create/*.

    :param request: объект запроса
    :type request: HttpRequest
    :rtype: HttpResponse

**Алгоритм работы**

    #. Проверяется тип запроса (GET или POST).
    #. Тип запроса - POST:
        #. Произвести валидацию данных.
        #. Если валидация успешна, то сохранить данные (создать фильтр).
        #. Переадресовать на страницу списка фильтров.
    #. Отобразить страницу с формой создания фильтра (шаблон `accounts/create_filter.html`).

.. function:: edit_filter(request, pk)

    Показывает страницу с формой для редактирования фильтра, также сохраняет данные формы (редактирует данные фильтра).

    Представление вызывается при запросе url */accounts/settings/filters/edit/:pk/*, где *:pk* - идентификатор фильтра.

    :param request: объект запроса
    :type request: HttpRequest
    :param pk: id фильтра
    :type pk: integer
    :rtype: HttpResponse

**Алгоритм работы**

    #. Получение данных фильтра из БД по его id и id текущего пользователя с помощью модели *HousesFilter*.
    #. Если фильтр не существует, то отобразить 404 ошмбку.
    #. Проверяется тип запроса (GET или POST).
    #. Тип запроса - POST:
        #. Произвести валидацию данных.
        #. Если валидация успешна, то сохранить данные (редактирование данных фильтра).
        #. Переадресовать на страницу списка фильтров.
    #. Отобразить страницу с формой редактирования фильтра (шаблон `accounts/edit_filter.html`).

.. class:: FilterDeleteView(SuccessMessageMixin, DeleteView)

    Class-Based представление для удаления фильтра пользователя.

    Представление вызывается при запросе url */accounts/settings/filters/delete/:pk*, где *:pk* - идентификатор фильтра.

    .. function:: get_success_url(self)

        Возвращает URL, на который происходит переадресация при успешном удалении.

    .. function:: get_queryset(self)

        Возвращает только фильтры текущего пользователя для того чтоб не было возможности удалять "чужие", использует модель *HousesFilter*.

    .. function:: delete(self, request, *args, **kwargs):

        Удаляет фильтр.

    .. function:: dispatch(self, *args, **kwargs):

        Метод специально "обёрнут" декораторами login_required, group_required('Users'), чтоб убедится, что пользователь залогинен и принадлежит к группе Users. Если какой-либо из декораторов вернёт False, то фильтр удалён не будет.

.. function:: users_constants(request)

    Показывает страницу с формой для редактирования констант пользователя, также сохраняет данные формы.

    Представление вызывается при запросе url */accounts/settings/users-constants/*, где *:pk* - идентификатор фильтра.

    :param request: объект запроса
    :type request: HttpRequest
    :rtype: HttpResponse

**Алгоритм работы**

    #. Проверяется тип запроса (GET или POST).
    #. Тип запроса - POST:
        #. Произвести валидацию данных.
        #. Если валидация успешна, то сохранить данные.
        #. Переадресовать на страницу констант пользователя.
    #. Получить данные констант городов и регионов текущего пользователя с помощью модели *Constants*.
    #. Отобразить страницу с формой констант пользователя (шаблон `accounts/users_constants.html`).

.. function:: change_password(request)

    Показывает страницу с формой для смены пароля пользователя, также сохраняет данные формы.

    Представление вызывается при запросе url */accounts/settings/change-password/*.

    :param request: объект запроса
    :type request: HttpRequest
    :rtype: HttpResponse

**Алгоритм работы**

    #. Проверяется тип запроса (GET или POST).
    #. Тип запроса - POST:
        #. Произвести валидацию данных.
        #. Если валидация успешна, то сохранить данные (изменить пароль).
        #. Переадресовать на страницу смены пароля пользователя.
    #. Отобразить страницу с формой смены пароля пользователя (шаблон `accounts/change_password.html`).

.. function:: change_show_title_photo(request)

    Меняет значение пользовательской настройки "показывать или нет фото дома в списке домов". Обработчик Ajax-запроса.

    Представление вызывается при запросе url */accounts/settings/change-show-title-photo/*.

    :param request: объект запроса
    :type request: HttpRequest
    :rtype: JsonResponse

**Алгоритм работы**

    #. Получение значения GET-параметра value.
    #. Сохранение этого значения в поле show_photos_filters модели Profile.
    #. Возврат JSON {'success': True}.

.. function:: change_font_size(request)

    Меняет значение пользовательской настройки "размер шрифта". Обработчик Ajax-запроса.

    Представление вызывается при запросе url */accounts/settings/change-font-size/*.

    :param request: объект запроса
    :type request: HttpRequest
    :rtype: JsonResponse

**Алгоритм работы**

    #. Получение значения GET-параметра action.
    #. Получение текущего значения коефициента размера шрифта.
    #. Если action == increase, то увеличить коефициента размера шрифта на 0.1. Иначе - уменьшить на 0.1.
    #. Сохранение этого значения в поле font_ratio модели Profile.
    #. Возврат JSON {'success': True, 'ratio': %значение коефициента размера шрифта%}.

.. function:: toggle_disabled(request, pk):

    Делает фильтр активным или неактивным. Обработчик Ajax-запроса.

    Представление вызывается при запросе url */accounts/settings/filters/toggle-disabled/:pk/*, где *:pk* - идентификатор фильтра.

    :param request: объект запроса
    :type request: HttpRequest
    :param pk: id фильтра
    :type pk: integer
    :rtype: JsonResponse

**Алгоритм работы**

    #. Получение данных фильтра из БД по его id и id текущего пользователя с помощью модели *HousesFilter*.
    #. Если фильтр не существует, то отобразить 404 ошмбку.
    #. Изменить значение атрибута disabled на противоположное.
    #. Сохранить данные фильтра.
    #. Возврат JSON {'success': True, 'disabled': %0 или 1 в зависимости от того активен ли фильтр сейчас%}.


.. function:: get_capital_growth(request, city_id):

    Возвращает JSON с величиной capital_growth определённого города.

    Представление вызывается при запросе url */accounts/settings/users-constants/get-capital-growth/:city_id/*, где *:city_id* - идентификатор фильтра.

    :param request: объект запроса
    :type request: HttpRequest
    :param city_id: id города
    :type city_id: integer
    :rtype: JsonResponse

**Алгоритм работы**

    #. Получение данных города из БД по его id и id текущего пользователя c помощью модели City.
    #. Если город не существует, то отобразить 404 ошмбку.
    #. Получить данные констант города текущего пользователя, используя модель CitiesConstants.
    #. Если константы города текущего пользователя существуют, то брать capital_growth из них. Иначе брать как city.capital_growth.
    #. Сохранить данные фильтра.
    #. Возврат JSON {'success': True, 'capital_growth': capital_growth, 'global_capital_growth': city.capital_growth}

Модели
======

Находятся в файле *accounts/models.py*.

.. class:: HousesFilter(models.Model)

    Модель для работы с таблицей `accounts_housefilter`.

.. class:: Profile(models.Model)

    Модель для работы с таблицей `accounts_profile`. Является моделью, расширяющей базовую модель Auth.Users, связь - 1 к 1.

.. class:: Constants(models.Model)

    Модель для работы с таблицей `accounts_constants`.

.. class:: CitiesConstants(models.Model)

    Модель для работы с таблицей `accounts_citiesconstants`.

Шаблоны
=======

Находятся в каталоге *accounts/templates*.

JavaScript
==========

Скрипты приложения находятся в каталоге *accounts/static/accounts/js*.

change-font-size.js
    Отвечает за обработку события изменения шрифта интерфейса.

filter-form.js
    Отвечает за вид и поведение отдельных элементов формы создания/редактирования фильтров.
