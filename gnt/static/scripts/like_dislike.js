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
            var currentNode = $(this);
            console.log(currentNode);
            $.ajax({
                url: url,
                method: "POST",
                headers: { "X-CSRFToken": csrftoken },
                data: payload,
                dataType: "json",
                success: function(data) {
                    if (data["status"] == 201) {
                        likeDrinkFeedback("Drink liked!");
                        s = "a[drinkid='" + drink_id + "']";
                        var thumbsup = $(s);
                        // console.log(thumbsup);
                        // console.log(thumbsup[0]);
                        // console.log(thumbsup[0].children("#blank_thumbsup"));
                        // thumbsup[0].children("#blank_thumbsup").hide();
                        // thumbsup[0].children("#filled_thumbsup").show();
                        // thumbsup[1].children("#blank_thumbsdown").show();
                        // thumbsup[1].children("#filled_thumbsdown").hide();
                    } else if (data["status"] == 422) {
                        likeDrinkFeedback(
                            "This is already in your liked drinks"
                        );
                    } else {
                        likeDrinkError("Error in liking drink");
                        console.log("Error in liking drink");
                    }
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    likeDrinkError("Error in liking drink");
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
                        likeDrinkFeedback("Drink disliked!");
                        var thumbsdown = $(drinkid = drink_id, ".thumbsdown");
                        thumbsdown.children("#blank_thumbsup").hide();
                        thumbsdown.children("#filled_thumbsup").show();
                    } else if (data["status"] == 422) {
                        likeDrinkFeedback(
                            "This is already in your disliked drinks"
                        );
                        var thumbsdown = $(drinkid = drink_id, ".thumbsdown");
                        thumbsdown.children("#blank_thumbsup").hide();
                        thumbsdown.children("#filled_thumbsup").show();
                    } else {
                        likeDrinkError("Error in disliking drink");
                        console.log("Error in disliking drink");
                    }
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    likeDrinkError("Error in disliking drink");
                }
            });
        });
    });
});

function likeDrinkFeedback(message) {
    document.getElementById("like-drink").innerHTML = message;
    $("#like-drink").show("slow");
    setTimeout(hideLikeDrinkFeedback, 5000);
}

function likeDrinkError(message) {
    document.getElementById("like-drink").innerHTML = message;
    $("#like-drink").show("slow");
    setTimeout(hideLikeDrinkError, 5000);
}

function hideLikeDrinkFeedback() {
    $("#like-drink").hide("slow");
}

function hideLikeDrinkError() {
    $("#dislike-drink").hide("slow");
}
