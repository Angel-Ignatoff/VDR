(function($) {
    "use strict";

    // Cache jQuery selectors
    const $validateForm = $('.validate-form');
    const $input = $('.validate-input .input100');

    $validateForm.on('submit', function() {
        let check = true;

        $input.each(function() {
            if (!validate(this)) {
                showValidate(this);
                check = false;
            }
        });

        return check;
    });

    $input.focus(function() {
        hideValidate(this);
    });

    function validate(input) {
        if ($(input).attr('type') === 'email' || $(input).attr('name') === 'email') {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test($(input).val().trim())) {
                return false;
            }
        } else {
            if ($(input).val().trim() === '') {
                return false;
            }
        }
        return true;
    }

    function showValidate(input) {
        const $thisAlert = $(input).parent();
        $thisAlert.addClass('alert-validate');
    }

    function hideValidate(input) {
        const $thisAlert = $(input).parent();
        $thisAlert.removeClass('alert-validate');
    }
})(jQuery);
