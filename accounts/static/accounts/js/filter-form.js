// Select2 theme - bootstrap
$.fn.select2.defaults.set( "theme", "bootstrap" );

$(function(){
    // treeMultiselect for suburbs
    $("#id_suburbs").treeMultiselect({ enableSelectAll: true, startCollapsed: true });

    //Date picker
    $('#id_listings_date_created').datepicker({
        autoclose: true,
        format: 'yyyy-mm-dd'
    });

    $("#pricing-methods-select-all").click(function (e) {
        e.preventDefault();
        $("#id_pricing_methods > option").prop("selected", "selected");
        $("#id_pricing_methods").trigger("change");
    });

    $("#property-type-select-all").click(function (e) {
        e.preventDefault();
        $("#id_property_type > option").prop("selected", "selected");
        $("#id_property_type").trigger("change");
    });
});