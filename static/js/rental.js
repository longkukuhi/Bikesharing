$( "#report-bike" ).click(function( event ) {
    // Stop form from submitting normally
    event.preventDefault();
    $.ajax({
        type:'POST',
        url: '/api/report_defect',
        data: JSON.stringify({
            bike_id: $('#bike-id-report').val(), def_category :$('#def-category-report').val(),
            def_details: $('#def-details-report').val()
            }),
        success: function(data){alert(data.retstatus) ;},
        contentType: "application/json",
        dataType: 'json'
    });
    
});

$( "#rent-bike" ).click(function( event ) {
    // Stop form from submitting normally
    event.preventDefault();
    $.ajax({
        type:'POST',
        url: '/api/rent_bike',
        data: JSON.stringify({
            bike_id: $('#bike-id-rent').val()
            }),
        success: function(data){alert(data.retstatus) ;
            $('#order-id-return').val(data.orderid);
            $('#bike-id-return').val($('#bike-id-rent').val());
            var form = $('<form action="' + '/Rent' + '" method="post">' +
            '<input type="text" name="orderid" value="' + $('#order-id-return').val() + '" />' +
            '<input type="text" name="bikeid" value="' + $('#bike-id-return').val() + '" />' +
            '</form>');
            $('body').append(form);
            form.submit();
        },
        contentType: "application/json",
        dataType: 'json'
    });
    
});

$( "#return-bike" ).click(function( event ) {
    // Stop form from submitting normally
    event.preventDefault();
    $.ajax({
        type:'POST',
        url: '/api/return_bike',
        data: JSON.stringify({
            order_id: $('#order-id-return').val(),bike_id:$('#bike-id-return').val(),
            station_id:$('#location-ID-return').val()
            }),
        success: function(data){alert(data.retstatus + ' paid  amount: ' + data.amount + ' for duration ' + data.duration + 'minutes') ;
            $('#order-id-return').val('');
            $('#bike-id-return').val('');
            $('#bike-id-rent').val('');
            var form = $('<form action="' + '/Rent' + '" method="post">' +
            '<input type="text" name="orderid" value="' + $('#order-id-return').val() + '" />' +
            '<input type="text" name="bikeid" value="' + $('#bike-id-return').val() + '" />' +
            '</form>');
            $('body').append(form);
            form.submit();            
        },
        contentType: "application/json",
        dataType: 'json'
    });
    
});