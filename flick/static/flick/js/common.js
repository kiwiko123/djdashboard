
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
    }
};