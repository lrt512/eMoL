$(document).ready(function() {
    "use strict";

    // Initialize datepicker
    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayHighlight: true,
        clearBtn: true
    });

    // Handle cancel button
    $('.btn-close').on('click', function() {
        window.history.back();
    });

    // Add postal/zip code validation
    function isValidPostalCode(code) {
        // Canadian postal code format
        const canadianFormat = /^[A-Z]\d[A-Z] ?\d[A-Z]\d$/;
        // US ZIP code format (both 5 and 9 digit formats)
        const usFormat = /^\d{5}(-\d{4})?$/;
        
        code = code.toUpperCase().trim();
        return canadianFormat.test(code) || usFormat.test(code);
    }

    // Format postal/zip code as user types
    $('[name="postal_code"]').on('input', function() {
        let value = $(this).val().toUpperCase();
        const province = $('#edit-combatant-province').val();
        
        if (province === 'MI') {
            // US ZIP code formatting
            value = value.replace(/[^0-9-]/g, '');
            if (value.length > 10) value = value.substr(0, 10);
            // Only allow one hyphen
            const parts = value.split('-');
            if (parts.length > 1) {
                value = parts[0] + '-' + parts.slice(1).join('');
            }
        } else {
            // Canadian postal code formatting
            value = value.replace(/[^A-Z0-9]/g, '');
            if (value.length > 6) value = value.substr(0, 6);
            if (value.length > 3) {
                value = value.substr(0, 3) + ' ' + value.substr(3);
            }
        }
        $(this).val(value);
    });

    // Update postal code format when province changes
    $('#edit-combatant-province').on('change', function() {
        const postalInput = $('[name="postal_code"]');
        const currentValue = postalInput.val();
        if (currentValue) {
            // Trigger the input handler to reformat
            postalInput.trigger('input');
        }
    });

    // Form validation
    function validateForm() {
        let isValid = true;
        const requiredFields = ['legal_name', 'phone', 'address1', 'city', 'postal_code'];
        
        requiredFields.forEach(field => {
            const input = $(`[name="${field}"]`);
            if (!input.val()) {
                input.addClass('is-invalid');
                isValid = false;
            } else if (field === 'postal_code' && !isValidPostalCode(input.val())) {
                input.addClass('is-invalid');
                isValid = false;
            } else {
                input.removeClass('is-invalid');
            }
        });

        // Validate member number and expiry combination
        const memberNumber = $('[name="member_number"]').val();
        const memberExpiry = $('[name="member_expiry"]').val();
        if (memberExpiry && !memberNumber) {
            $('[name="member_number"]').addClass('is-invalid');
            isValid = false;
        }

        if (!isValid) {
            $('#validation-error-notice').show();
        } else {
            $('#validation-error-notice').hide();
        }
        return isValid;
    }

    // Form submission
    $('form').on('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
        }
    });

    // Format phone number as user types
    $('[name="phone"]').on('input', function() {
        let value = $(this).val().replace(/\D/g, '');
        if (value.length > 10) value = value.substr(0, 10);
        if (value.length > 6) {
            value = value.substr(0, 3) + '-' + value.substr(3, 3) + '-' + value.substr(6);
        } else if (value.length > 3) {
            value = value.substr(0, 3) + '-' + value.substr(3);
        }
        $(this).val(value);
    });

    // Update postal code validation based on selected region
    function getPostalFormatRegex(format) {
        switch(format) {
            case 'CAN':
                return /^[A-Z]\d[A-Z] ?\d[A-Z]\d$/;
            case 'USA':
                return /^\d{5}(-\d{4})?$/;
            default:
                return /.*/;
        }
    }
});
