$(document).ready(function() {
   var anchor = $(".thumbsup");
   anchor.each(function anonymouse_founction(index, element) {
   		$(this).on('click', function likeDrink() {
   			var html_id = $(this).attr('id');
   			console.log(html_id.split('-').slice(-1).pop());
   		});
   });
});