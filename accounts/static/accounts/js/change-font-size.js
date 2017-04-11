/**
 * Changes font size.
 *
 * @param ratio
 */
var changeFontSize = function(ratio) {
    var fontSizes = {
        'body': 14,
        'h3': 18,
        'h1': 24,
        '.sidebar-menu .treeview-menu > li > a': 14,
        '.content-header > .breadcrumb': 12,
        '.user-panel > .info > a': 11
    };

    $.each(fontSizes, function (index, value) {
       var $el = $(index);
       $el.css("font-size", parseInt(fontSizes[index]) * ratio);
    });
};

$(function() {
    $("#increase-font").click(function (e) {
        e.preventDefault();
        $.post(
            "/accounts/settings/change-font-size/",
            {
                action: "increase"
            },
            function (data) {
                changeFontSize(data.ratio);
            }
        );
    });

    $("#decrease-font").click(function (e) {
        e.preventDefault();
        $.post(
            "/accounts/settings/change-font-size/",
            function (data) {
                changeFontSize(data.ratio);
            }
        );
    });
});
