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
        $this.hide();
        $input.insertAfter($this.parent().siblings("label"));
        $input.focus();
    });

    $("#reset-filter-form").click(function (e) {
        e.preventDefault();
        $('#filter-form').trigger('reset');
        $('#filter-form select').trigger('change');
        $('.tree-multiselect').remove();
        $('#id_suburbs').treeMultiselect({
          enableSelectAll: true,
          startCollapsed: true
        });
    });

    $("#id_price_from, #id_price_to")
            .prev()
            .attr('data-placement', 'bottom')
            .attr('data-toggle', 'tooltip')
            .attr('title', 'Choose from the list or click on Custom value to enter your own value.');

    $("#id_pricing_methods")
        .prev()
        .attr('data-placement', 'bottom')
        .attr('data-toggle', 'tooltip')
        .attr('title', 'Click on the field to see the list of pricing methods to choose from. To add the method click on it. To add more methods, continue clicking on the field and adding as many methods as you like.');

    $("#id_government_value_from, #id_government_value_to")
        .prev()
        .attr('data-placement', 'bottom')
        .attr('data-toggle', 'tooltip')
        .attr('title', 'Choose from the list or click on Custom value to enter your own value.');

    $("#id_property_type")
        .prev()
        .attr('data-placement', 'bottom')
        .attr('data-toggle', 'tooltip')
        .attr('title', 'Click on the field to see the list of property types to choose from. To add the type click on it. To add more property types, continue clicking on the field and adding as many as you like or use one of the \'Select\' options.');

    $("#id_ensuite")
        .parent()
        .attr('data-placement', 'bottom')
        .attr('data-toggle', 'tooltip')
        .attr('title', 'Tick this box if you want to filter only properties that have ensuite bathroom.');

    $("#id_disabled")
        .parent()
        .attr('data-placement', 'bottom')
        .attr('data-toggle', 'tooltip')
        .attr('title', 'Tick this box if you don\'t want this filter to be in use straight away. Un-tick this box once you\'ve decided to start using it.');

    var showOrHidePrices = function () {
        var values = $("#id_pricing_methods").val();
        if (!values || values.indexOf('1') !== -1) {
            $("#id_price_from").parent().show();
            $("#id_price_to").parent().show();
        } else {
            $("#id_price_from").parent().hide();
            $("#id_price_to").parent().hide();
        }
    };

    $("#id_pricing_methods").change(function () {
        showOrHidePrices();
    });

    showOrHidePrices();
});