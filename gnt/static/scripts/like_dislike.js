$(document).ready(function() {
    var anchor = $(".thumbsup");
    // Add click listener to each thumbs up button
    anchor.each(function likeDrink(index, element) {
        $(this).on("click", function likeDrink() {
            var html_id = $(this).attr("id");
            var user = $(this).attr("user");
            var drink_id = html_id
                .split("-")
                .slice(-1)
                .pop();
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
                    if (data['status'] == 200){
                        likeDrinkFeedback('Drink liked!');
                    } else if (data['status'] == 422){
                        likeDrinkFeedback('This is already in your liked drinks');
                    } else {
                        likeDrinkError('Error in liking drink');
                        console.log("Error in liking drink");
                    }
                 },
                 error: function (xhr, ajaxOptions, thrownError) {
                    likeDrinkError('Error in liking drink');
                  }
            });
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

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == name + "=") {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

function likeDrinkFeedback(message){
    document.getElementById("like-drink").innerHTML = message;
    $("#like-drink").show("slow");
    setTimeout(hideLikeDrinkFeedback, 5000);
}

function likeDrinkError(message){
    document.getElementById("like-drink").innerHTML = message;
    $("#like-drink").show("slow");
    setTimeout(hideLikeDrinkError, 5000);
}

function hideLikeDrinkFeedback(){
    $("#like-drink").hide("slow");
}

function hideLikeDrinkError(){
    $("#dislike-drink").hide("slow");
}
