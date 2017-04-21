// Select2 theme - bootstrap
$.fn.select2.defaults.set( "theme", "bootstrap" );

$(function(){
    // treeMultiselect for suburbs
    $("#id_suburbs").treeMultiselect({ enableSelectAll: true, startCollapsed: true });

    $("#pricing-methods-select-all").click(function (e) {
        e.preventDefault();
        $("#id_pricing_methods > option").prop("selected", "selected");
        $("#id_pricing_methods").trigger("change");
    });

    $("#property-type-select-all").click(function (e) {
        e.preventDefault();
        $("#id_property_type option").prop("selected", "selected");
        $("#id_property_type").trigger("change");
    });

    $("#property-type-select-residential").click(function (e) {
        e.preventDefault();
        $("#id_property_type > optgroup").first().find("option").prop("selected", "selected");
        $("#id_property_type").trigger("change");
    });

    $("#property-type-select-other").click(function (e) {
        e.preventDefault();
        $("#id_property_type > optgroup").last().find("option").prop("selected", "selected");
        $("#id_property_type").trigger("change");
    });

    $(".set-custom-value").click(function (e) {
        e.preventDefault();
        var $this = $(this);
        var $select = $this.parent().siblings("select").first();
        var $input = $('<input class="form-control" placeholder="Custom value" title="" type="number" name="' + $select.attr('name')
            + '" id="' + $select.attr('id') + '">');

        $select.remove();
        $input.insertAfter($this.parent().siblings("label"));
        $input.focus();
    });
});