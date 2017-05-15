$(function () {
    // Initial values for weekly_rent and purchase_price
    $("#id_weekly_rent").val( $("#id_rent_per_week").val() );
    $("#id_purchase_price").val( $("#id_offer_price").val() );

    $(".change-value").click(function (e) {
        e.preventDefault();
        var $this = $(this);
        var value = $this.data('value');
        var $input = $this.parent().siblings("input").first();
        if ($input.val() !== value) {
            $input.val(value);
            $input.trigger('change');
        }
    });

    /**
     * Saves user's calculator data for house.
     */
    var saveCalculatorData = function () {
        $.post(
            "/listings/save-calculator-data/" + houseId + "/",
            {
                managed: $("#id_managed").prop('checked') ? 1 : 0,
                property_managers_commission: $("#id_property_managers_commission").val(),
                int_rate: $("#id_int_rate").val(),
                deposit: $("#id_deposit").val(),
                vacancy: $("#id_vacancy").val(),
                capital_growth: $("#id_capital_growth").val(),
                gross_yield: $("#id_gross_yield").val(),
                net_yield: $("#id_net_yield").val(),
                min_cashflow: $("#id_min_cashflow").val()
            }
        );
    };

    /**
     * Clacilates values in Fixed, Buying sections
     */
    var calculateFixedBuying = function () {
        var managed = $("#id_managed").is(':checked');
        var propertyMarketValue = parseFloat($("#id_market_reg_value").val()) || 0;
        var amountOfLoan = parseFloat($("#id_purchase_price").val()) || 0;
        var intRate = parseFloat($("#id_int_rate").val()) || 0;
        var IOPayments = amountOfLoan * intRate / 100;
        var purchasePrice = parseFloat($("#id_purchase_price").val()) || 0;
        var depositForm = parseFloat($("#id_deposit").val()) || 0;
        var deposit = purchasePrice * depositForm / 100;
        var rates = parseFloat($("#id_rates").val()) || 0;
        var insurance = parseFloat($("#id_insurance").val()) || 0;
        var repairsMaintenance = parseFloat($("#id_repairs_maintenance").val()) || 0;
        var bodyCorporate = parseFloat($("#id_body_corporate").val()) || 0;
        var weeklyRent = parseInt($("#id_weekly_rent").val()) || 0;
        var vacancy = parseInt($("#id_vacancy").val()) || 0;
        var rate = parseFloat($("#id_property_managers_commission").val()) || 0;
        var propertyExpenses;
        if (managed) {
            propertyExpenses = rates + insurance + repairsMaintenance
                + bodyCorporate + otherExpences
                + (weeklyRent * (52 - vacancy) * (rate / 100) * (1 + gst / 100))
                + (weeklyRent * vacancy);
        } else {
            propertyExpenses = rates + insurance + repairsMaintenance
                + bodyCorporate + otherExpences
                + (weeklyRent * vacancy);
        }
        var discount = propertyMarketValue - purchasePrice;
        var percent = discount / propertyMarketValue * 100;
        var capitalGrowthRate = parseFloat($("#id_capital_growth").val()) || 0;
        var equity = propertyMarketValue - amountOfLoan;
        var cashFlow = weeklyRent * 52 - IOPayments - propertyExpenses;
        var oneYearReturn = capitalGrowthRate * propertyMarketValue / 100 + equity + cashFlow;
        var returnOnDeposit = oneYearReturn / deposit * 100;
        var resultingGrossYield = weeklyRent * 52 / purchasePrice * 100;
        var resultingNetYield = (weeklyRent * 52 - propertyExpenses) / amountOfLoan * 100;
        var grossYield = parseFloat($("#id_gross_yield").val()) || 0;
        var netYield = parseFloat($("#id_net_yield").val()) || 0;
        var minCashflow = parseFloat($("#id_min_cashflow").val()) || 0;
        var governmentValue = parseFloat($("#id_government_value").val()) || 0;
        var purchasePriceToGovernmentValue = 0;
        if (purchasePrice > 0 && governmentValue > 0) {
            purchasePriceToGovernmentValue = purchasePrice / governmentValue;
        }

        $("#io-payments").html('$ ' + IOPayments.toFixed(2));
        $("#amount-of-loan").html('$ ' + amountOfLoan.toFixed(2));
        $("#deposit").html('$ ' + deposit.toFixed(2));
        $("#property-expences").html('$ ' + propertyExpenses.toFixed(2));

        $("#discount").html('$ ' + discount.toFixed(2));
        $("#percent").html(percent.toFixed(2) + ' %');
        $("#one-year-return").html('$ ' + oneYearReturn.toFixed(2));
        $("#return-on-deposit").html(returnOnDeposit.toFixed(2) + ' %');
        $("#equity").html('$ ' + equity.toFixed(2));
        if (purchasePrice > 0 && governmentValue > 0) {
            $("#purchase_price_to_government_value").html(purchasePriceToGovernmentValue.toFixed(2));
        } else {
             $("#purchase_price_to_government_value").html('');
        }
        $("#resulting-gross-yield").html(resultingGrossYield.toFixed(2) + ' %');
        $("#resulting-net-yield").html(resultingNetYield.toFixed(2) + ' %');
        $("#cashflow").html('$ ' + cashFlow.toFixed(2));

        if (resultingGrossYield >= grossYield) {
            $( "#resulting-gross-yield" ).removeClass('text-red').addClass('text-green');
        } else {
            $( "#resulting-gross-yield" ).removeClass('text-green').addClass('text-red');
        }

        if (resultingNetYield >= netYield) {
            $( "#resulting-net-yield" ).removeClass('text-red').addClass('text-green');
        } else {
            $( "#resulting-net-yield" ).removeClass('text-green').addClass('text-red');
        }

        if (cashFlow >= minCashflow) {
            $( "#cashflow" ).removeClass('text-red').addClass('text-green');
        } else {
            $( "#cashflow" ).removeClass('text-green').addClass('text-red');
        }
    };

    $("#id_managed, " +
        "#id_property_managers_commission, " +
        "#id_int_rate, " +
        "#id_deposit, " +
        "#id_vacancy, " +
        "#id_capital_growth, " +
        "#id_gross_yield, " +
        "#id_net_yield, " +
        "#id_min_cashflow").on('change', function() {
            saveCalculatorData();
            calculateFixedBuying();
    });

    $("#id_weekly_rent, #id_purchase_price").on('change', function() {
            calculateFixedBuying();
    });

    /**
     * "Find Rent" button click handler.
     */
    $("#findRent").click(function () {
        var purchasePrice = parseFloat($("#id_purchase_price").val()) || 0;
        var grossYield = parseFloat($("#id_gross_yield").val()) || 0;

        var weeklyRent = parseInt(purchasePrice * grossYield / 100 / 52);

        var $id_weekly_rent = $("#id_weekly_rent");
        $id_weekly_rent.val(weeklyRent);
        $id_weekly_rent.trigger('change');
    });

    /**
     * "Find Price" button click handler.
     */
    $("#findPrice").click(function () {
        var weeklyRent = parseFloat($("#id_weekly_rent").val()) || 0;
        var grossYield = parseFloat($("#id_gross_yield").val()) || 0;

        var purchasePrice = weeklyRent * 52 * 100 / grossYield;

        var $id_purchase_price = $("#id_purchase_price");
        $id_purchase_price.val(purchasePrice);
        $id_purchase_price.trigger('change');
    });

    /**
     * "Reset" button click handler. Resets rent_per_week, offer_price values to default.
     */
    $("#reset").click(function () {
        $("#id_weekly_rent").val( $("#id_rent_per_week").val() );
        $("#id_purchase_price").val( $("#id_offer_price").val() ).trigger('change');
    });

    calculateFixedBuying();
});
