$(document).ready(function(){   
	
	$('.send').click(function(event) {
		stocks = createJSON();

	 $.ajax({
            url: '/stocks',
            data: JSON.stringify(createJSON()),
            beforeSend: function() {
                  $('.send').attr('disabled','disabled')        
                  console.log('sending...')
            },
            complete: function() {
							console.log('done...')                        },
            success: function(result) {
              console.log('success...')    
              $('.send').attr('disabled',false) 
            },
            error: function (request, error) {
                    $('.send').attr('disabled',false) 
                    alert('error');
            },
            type: 'put',
            contentType: "application/json; charset=utf-8",
            dataType: "json"
    	});                    
	})
	event.preventDefault()

});

function createJSON() {
    jsonObj = [];
    $("tr[class=stock]").each(function() {

        var symbol = $(this).find('.symbol').val();
        var price = $(this).find('.price').val();

        item = {};
        item ["symbol"] = symbol;
        item ["price"] = price;

        jsonObj.push(item);
    });

    console.log(jsonObj);
    return jsonObj;
   
}
