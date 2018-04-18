
var common = {
    fieldEmpty: function(element) {
        return $(element).val().length === 0;
    },

    all: function(arr) {
        for (var i = 0; i < arr.length; ++i) {
            if (!arr[i]) {
                return false;
            }
        }
        return true;
    },

    any: function(arr) {
        for (var i = 0; i < arr.length; ++i) {
            if (arr[i]) {
                return true;
            }
        }
        return false;
    },

    /**
     * Adds a red, bolded border around element's textbox if the field is empty.
     *
     * @param element
     */
    redBorderEmptyField: function(element) {
        if (common.fieldEmpty(element)) {
            $(element).addClass("text-box-invalid");
        }
        else {
            $(element).removeClass("text-box-invalid");
        }
    },

    /**
     * Applies a red border around inputTextElement if it is empty on key-up.
     *
     * @param inputTextElement
     */
    requireFieldNonEmpty: function(inputTextElement) {
        $(inputTextElement).keyup(function(){ common.redBorderEmptyField($(inputTextElement)); });
    },

    /**
     * Examines all fields from selector -
     * if any of them are empty, it will disable buttonElement (aesthetically and functionally).
     *
     * TODO: currently bound to mousemove - buggy, but works
     *
     * @param buttonElement
     * @param selector - e.g., "form#FORM-ID :input"
     */
    disableButtonUnlessAllFieldsFilled: function(buttonElement, selector) {
        $(selector).not(":button, :hidden").each(function(index, input) {
            $(input).mousemove(function() {
                if (!($(this).val())) {
                    $(buttonElement).prop('disabled', true);
                    $(buttonElement).addClass('disabled');
                    return;
                }
                $(buttonElement).removeClass('disabled');
                $(buttonElement).prop('disabled', false);
            })
        });
    },
};