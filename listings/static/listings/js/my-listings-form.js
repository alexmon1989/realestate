$(function () {
    var fillCitiesdByRegion = function () {
        var value = $("#id_region").val();
        if (value) {
            $.getJSON('/listings/get-cities-by-region/' + value + '/', function (data) {
                $('#id_city').empty().select2({
                    data: data.results
                }).trigger('change');
            });
        } else {
            $('#id_city').html('').select2({data: {id: null, text: null}});
            $('#id_suburb').html('').select2({data: {id: null, text: null}});
        }
    };

    var fillSuburbsByCity = function () {
        var value = $("#id_city").val();
        if (value) {
            $.getJSON('/listings/get-suburbs-by-city/' + value + '/', function (data) {
                $('#id_suburb').empty().select2({
                    data: data.results
                })
            });
        } else {
            $('#id_suburb').html('').select2({data: {id: null, text: null}});
        }
    };

    if (!$("#id_suburb").val()) {
        fillCitiesdByRegion();
        fillSuburbsByCity();
    }

    $("#id_region").change(function () {
        fillCitiesdByRegion();
    });

    $("#id_city").change(function () {
        fillSuburbsByCity();
    });
});