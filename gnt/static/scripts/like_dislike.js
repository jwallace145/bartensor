$(document).ready(function() {
    var anchor = $(".thumbsup");
    // Add click listener to each thumbs up button
    anchor.each(function likeDrink(index, element) {
        $(this).on("click", function likeDrink() {
            var user = $(this).attr("user");
            var drink_id = $(this).attr("drinkid");
            var url = APPURL + "/like_drink/";
            var payload = {
                drink_id: drink_id,
                user: user
            };
            var csrftoken = getCookie("csrftoken");
            $.ajax({
                url: url,
                method: "POST",
                headers: { "X-CSRFToken": csrftoken },
                data: payload,
                dataType: "json",
                success: function(data) {
                    if (data["status"] == 201) {
                        console.log("Drink liked");
                    } else if (data["status"] == 422) {
                        console.log("Already liked");
                    } else {
                        console.log(data["status"]);
                        console.log(data["message"]);
                    }
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    console.log(xhr);
                }
            });
        });
    });
});

$(document).ready(function() {
    var anchor = $(".thumbsdown");
    // Add click listener to each thumbs up button
    anchor.each(function likeDrink(index, element) {
        $(this).on("click", function likeDrink() {
            var user = $(this).attr("user");
            var drink_id = $(this).attr("drinkid");
            var url = APPURL + "/dislike_drink/";
            var payload = {
                drink_id: drink_id,
                user: user
            };
            var csrftoken = getCookie("csrftoken");
            $.ajax({
                url: url,
                method: "POST",
                headers: { "X-CSRFToken": csrftoken },
                data: payload,
                dataType: "json",
                success: function(data) {
                    if (data["status"] == 201) {
                        console.log("disliked")
                    } else if (data["status"] == 422) {
                        console.log("already disliked");
                    } else {
                        console.log("Error in disliking drink");
                    }
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    console.log(xhr);
                }
            });
        });
    });
});

