
$(document).ready(function(){
    $('#ddns-sync').click(function(){
        var buttonName = $(this).attr('name');
        $.ajax({
            type: 'POST',
            url: '/ajax/update_service_status',
            data: { buttonName: buttonName },
            success: function(response) {
                if (response.enabled) {
                    $('#ddns-sync').removeClass('btn-success').addClass('btn-secondary').text('Disabled');
                    // You can also disable the button if you want:
                    // $('#status-btn-ddns').prop('disabled', true);
                } else {
                    $('#ddns-sync').removeClass('btn-secondary').addClass('btn-success').text('Enabled');
                }
            }
        });
    });
});
