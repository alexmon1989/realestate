$(function () {
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
});