$(document).ready(function() {
   var anchor = $(".thumbsup");
   anchor.each(function likeDrink(index, element) {
   		$(this).on('click', function likeDrink() {
   			var html_id = $(this).attr('id');
   			var drink_id= html_id.split('-').slice(-1).pop();
   		});
   });
});

$(document).ready(function() {
   var anchor = $(".thumbsdown");
   anchor.each(function dislikeDrink(index, element) {
   		$(this).on('click', function likeDrink() {
   			var html_id = $(this).attr('id');
   			var drink_id= html_id.split('-').slice(-1).pop();
   		});
   });
});