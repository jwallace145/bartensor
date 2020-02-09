$(document).ready(function() {
    var anchor = $(".thumbsup");
    // Add click listener to each thumbs up button
    anchor.each(function likeDrink(index, element) {
        $(this).on("click", function likeDrink() {
            var html_id = $(this).attr("id");
            var drink_id = html_id
                .split("-")
                .slice(-1)
                .pop();
            console.log(drink_id);
            console.log(APPURL);
            //TODO: Add call to /likedrink endpoint
        });
    });
});

$(document).ready(function() {
    var anchor = $(".thumbsdown");
    // Add click listener to each thumbs down button
    anchor.each(function dislikeDrink(index, element) {
        $(this).on("click", function likeDrink() {
            var html_id = $(this).attr("id");
            var drink_id = html_id
                .split("-")
                .slice(-1)
                .pop();
            //TODO: Add call to /dislikedrink endpoint
        });
    });
});
