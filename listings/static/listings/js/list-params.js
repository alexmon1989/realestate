/**
 * Returns URL with new or edited param.
 */
var getUrlWithNewParam = function (param, value) {
    var params = $.parseParams(location.href);
    params[param] = value;
    var queryStr = $.param( params );
    var url = window.location.href.split('?')[0];
    return url + '?' + queryStr;
};

$(function () {
    $(".view-mode").click(function (e) {
        e.preventDefault();
        var viewMode = $(this).data('view-mode');
        location.href = getUrlWithNewParam('view_mode', viewMode);
    });

    $(".per-page").click(function (e) {
        e.preventDefault();
        var perPage = $(this).data('per-page');
        location.href = getUrlWithNewParam('per_page', perPage);
    });
});