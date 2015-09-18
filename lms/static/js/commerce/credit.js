/**
 * Credit-related utilities
 */
var edx = edx || {};

(function ($) {
    'use strict';

    edx.commerce = edx.commerce || {};
    edx.commerce.credit = edx.commerce.credit || {};

    edx.commerce.credit.createCreditRequest = function (providerId, courseKey, username, error) {
        $.ajax({
            url: '/api/credit/v1/providers/' + providerId + '/request/',
            type: 'POST',
            headers: {
                'X-CSRFToken': $.cookie('csrftoken')
            },
            data: JSON.stringify({
                'course_key': courseKey,
                'username': username
            }),
            context: this,
            success: function (requestData) {
                var $form = $('<form>', {
                    'action': requestData.url,
                    'method': 'POST',
                    'accept-method': 'UTF-8'
                });

                _.each(requestData.parameters, function (value, key) {
                    $('<textarea>').attr({
                        name: key,
                        value: value
                    }).appendTo($form);
                });

                $form.submit();
            },
            error: error
        });
    };
})(jQuery);
