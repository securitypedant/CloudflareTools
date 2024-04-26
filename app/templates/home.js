
$(document).ready(function(){
    {% for key, service in config.items() %}
    $('#{{ service.name }}').click(function(){
        var buttonName = $(this).attr('name');
        $.ajax({
            type: 'POST',
            url: '/ajax/update_service_status',
            data: { buttonName: buttonName },
            success: function(response) {
                if (response.enabled) {
                    $('#{{ service.name }}').removeClass('btn-secondary').addClass('btn-success').text('Enabled');
                    // You can also disable the button if you want:
                    // $('#status-btn-ddns').prop('disabled', true);
                } else {
                    $('#{{ service.name }}').removeClass('btn-success').addClass('btn-secondary').text('Disabled');
                }
            }
        });
    });
    {% endfor %}
});
