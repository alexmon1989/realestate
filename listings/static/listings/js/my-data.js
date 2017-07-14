$(function () {
    /**
     * Calculates and displays asking_price_to_government_value.
     */
    var calculateAskingPriceToGovernmentValue = function () {
        var price = parseFloat($("#price").html()) || 0;
        var governmentValue = parseFloat($("#id_government_value").val()) || 0;
        if (price > 0 && governmentValue > 0) {
            var priceToGovernmentValue = price / governmentValue;
            $("#asking_price_to_government_value").html(priceToGovernmentValue.toFixed(2));
            $("#dl_asking_price_to_government_value").show();
        } else {
            $("#asking_price_to_government_value").html('');
            $("#dl_asking_price_to_government_value").hide();
        }
    };

    calculateAskingPriceToGovernmentValue();

    $("#use-offer-price").click(function (e) {
        e.preventDefault();
        $("#id_market_reg_value").val( $("#id_offer_price").val() );
    });

    $("#use-asking-price").click(function (e) {
        e.preventDefault();
        $("#id_market_reg_value").val( $("#price").html() );
    });

    $("#use-government-value").click(function (e) {
        e.preventDefault();
        $("#id_market_reg_value").val( $("#id_government_value").val() );
    });

    $("#id_rent_per_week").change(function () {
        $("#id_weekly_rent").val( $("#id_rent_per_week").val() );
    });

    $("#id_offer_price").change(function () {
        $("#id_purchase_price").val( $("#id_offer_price").val() );
    });

    $("#id_government_value").change(function () {
        calculateAskingPriceToGovernmentValue();
    });

    $(document.body).on('click', '.expense-delete' ,function(e) {
        e.preventDefault();
        var $this = $(this);

        $.get( "/listings/liked/delete-other-expenses-item/" + $this.parent().parent().data('expense_id') + '/', function (data) {
            $this.parent().parent().remove();
            $("#total_other_expenses").html(data.total_other_expenses.value__sum);
        });
    });

    /**
     * Creates other expense item.
     */
    $("#create-expense").click(function (e) {
        e.preventDefault();

        $.post( "/listings/liked/create-other-expenses-item/", {
            key: $("#id_key").val(),
            value: $("#id_value").val(),
            house_user_data: $("#house_user_data_id").val()
        }).done(function(data) {
            var $id_key = $("#id_key");
            var $id_value = $("#id_value");

            var html =
                '<tr data-expense_id="' + data.pk + '">' +
                '<td><strong>' + data.key + '</strong></td>' +
                '<td>' + data.value + '</td>' +
                '<td><a href="#" title="Delete" class="expense-delete"><i class="fa fa-trash" aria-hidden="true"></i></a></td>' +
                '</tr>';

            $(html).insertBefore($id_key.parent().parent());
            $("#total_other_expenses").html(data.total_other_expenses.value__sum);

            $id_key.val('').parent().removeClass('has-error').find(".help-block").remove();
            $id_value.val('').parent().removeClass('has-error').find(".help-block").remove();
        }).fail(function (data) {
            var errors = data.responseJSON.errors;
            for (var i in errors) {
                $item = $('#id_' + i);
                $item.parent().addClass('has-error').find(".help-block").remove();
                $item.after('<span class="help-block">' + errors[i] + '</span>');
            }
        });
    });

    $("#id_new_build").change(function () {
        var isNewBuild = $("#id_new_build").is(":checked");

        $.get('/listings/get-deposit-values/',
            {
                'is_new_build': isNewBuild ? 1 : 0
            },
            function (data) {
                var globalDeposit = data.global_deposit;
                var userDeposit = data.user_deposit;

                $("#global-deposit").html("Global value: " + globalDeposit.toFixed(1) + "%").data('value', globalDeposit);
                $("#user-deposit").html("User's value: " + userDeposit.toFixed(1) + "%").data('value', userDeposit);
            });
    });

    $("#id_flooding_10, #id_flooding_100")
        .parent()
        .attr('data-placement', 'bottom')
        .attr('data-toggle', 'tooltip')
        .attr('title', 'Tick appropriate box/es if you\'ve checked flooding map for the property and found that it is prone to flooding.');

    $("#id_body_corporate")
        .prev()
        .attr('data-placement', 'bottom')
        .attr('data-toggle', 'tooltip')
        .attr('title', 'Only for properties that have body corporate on them.');

    $("#id_renovations")
        .prev()
        .attr('data-placement', 'bottom')
        .attr('data-toggle', 'tooltip')
        .attr('title', 'Optional field. Enter estimate costs of renovations that you want to do on the property.');

    $("#id_other_annual_expenses")
        .attr('data-placement', 'bottom')
        .attr('data-toggle', 'tooltip')
        .attr('title', 'Optional field. Add any other expenses that you want to include in calculations and are not covered by above.');

    $("#id_walk_away_price")
        .prev()
        .attr('data-placement', 'bottom')
        .attr('data-toggle', 'tooltip')
        .attr('title', 'Maximum price that you are willing to pay for the property.');

    $("#id_revisit_on")
        .prev()
        .attr('data-placement', 'bottom')
        .attr('data-toggle', 'tooltip')
        .attr('title', 'Optional field to complete if you want to make another offer on this property later.');


    var initialFormData = $("#form-my-data").serialize();
    var isDataChanged = false;

    $("#form-my-data :input").change(function() {
        //$('#modal-default').modal('show');
        var $this = $("#form-my-data");
        var currentFormData = $this.serialize();
        isDataChanged = (initialFormData !== currentFormData);
    });

    $(window).on("beforeunload", function() {
        if (isDataChanged) {
            $('#modal-default').modal('show');
            return false;
        }
    });

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        if (isDataChanged) {
            $('#modal-default').modal('show');
            return false;
        }
    });

    $("#btn-dont-save").click(function () {
        isDataChanged = false;
    });

    $("#btn-save").click(function () {
        isDataChanged = false;
        $("#return_url").val("/" + window.location.pathname.substring(1));
        $("#form-my-data").submit();
    });

    $("#form-my-data button[type=submit]").click(function () {
        isDataChanged = false;
    });

    var showOrHideManagers = function () {
        var value = $('input[name=rent_type]:checked').val();
        if (value === '3') {
            $("#id_managers").parent().show();
        } else {
            $("#id_managers").parent().hide();
        }
    };

    showOrHideManagers();

    $("input[name=rent_type]").change(function () {
        showOrHideManagers();
    });

    $('body').on('click', '#add_manager', function() {
        $("#id_managers").select2('close');
    });

    $("#save-manager").click(function (e) {
        e.preventDefault();

        $.post( "/managers/create-manager-ajax/", {
            name: $("#id_name").val(),
            agency: $("#id_agency").val(),
            phone_numbers: $("#id_phone_numbers").val(),
            email: $("#id_email").val(),
            rate: $("#id_rate").val(),
            city: $("#id_city").val()
        }).done(function(data) {
            $("#id_name").val('').parent().removeClass('has-error').find(".help-block").remove();
            $("#id_agency").val('').parent().removeClass('has-error').find(".help-block").remove();
            $("#id_phone_numbers").val('').parent().removeClass('has-error').find(".help-block").remove();
            $("#id_email").val('').parent().removeClass('has-error').find(".help-block").remove();
            $("#id_rate").val('').parent().removeClass('has-error').find(".help-block").remove();
            $("#id_city").val('').parent().removeClass('has-error').find(".help-block").remove();

            $('#modal-add-manager').modal('hide');
            $("#id_managers").append("<option value='"+data.pk+"' selected>"+data.name+"</option>").trigger('change');
        }).fail(function (data) {
            var errors = data.responseJSON.errors;
            for (var i in errors) {
                $item = $('#id_' + i);
                $item.parent().addClass('has-error').find(".help-block").remove();
                $item.after('<span class="help-block">' + errors[i] + '</span>');
            }
        });
    });

});