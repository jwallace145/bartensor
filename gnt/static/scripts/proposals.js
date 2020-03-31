function up_vote() {
    var anchor = $(".upvote");
    // Remove listeners if there were any
    anchor.each(function removeListner() {
        $(this).unbind();
    })
    // Add click listener to each thumbs up button
    anchor.each(function likeDrink(index, element) {
        $(this).on("click", function likeDrink() {
            var user = $(this).attr("user");
            var drink_id = $(this).attr("drinkid");
            var url = APPURL + "/like_user_drink/";
            var payload = {
                drink_id: drink_id,
                user: user
            };
            var csrftoken = getCookie("csrftoken");
            var thumbsup = $("a[drinkid='" + drink_id + "']:first");
            var thumbsdown = $("a[drinkid='" + drink_id + "']:last");
            $.ajax({
                url: url,
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken
                },
                data: payload,
                dataType: "json",
                success: function (data) {
                    if (data["status"] == 201) {
                        console.log("Drink liked!");
                        var votes = $("#drink" + drink_id + "_votes").text();
                        if (thumbsdown.children('#filled_thumbsdown').is(":visible")) {
                            $("#drink" + drink_id + "_votes").html(Number(votes) + 2);
                        } else {
                            $("#drink" + drink_id + "_votes").html(Number(votes) + 1);
                        }
                        likeDrinkAnimation(thumbsup, thumbsdown);
                    } else if (data["status"] == 422) {
                        console.log("Already liked");
                    } else {
                        console.log(data["status"]);
                        console.log(data["message"]);
                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr);
                }
            });
        });
    });
}

function down_vote() {
    var anchor = $(".downvote");
    // Remove listeners if there were any
    anchor.each(function removeListner() {
        $(this).unbind();
    })
    // Add click listener to each thumbs up button
    anchor.each(function dislikeDrink(index, element) {
        $(this).on("click", function dislikeDrink() {
            var user = $(this).attr("user");
            var drink_id = $(this).attr("drinkid");
            var url = APPURL + "/dislike_user_drink/";
            var payload = {
                drink_id: drink_id,
                user: user
            };
            var csrftoken = getCookie("csrftoken");
            var thumbsup = $("a[drinkid='" + drink_id + "']:first");
            var thumbsdown = $("a[drinkid='" + drink_id + "']:last");
            $.ajax({
                url: url,
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken
                },
                data: payload,
                dataType: "json",
                success: function (data) {
                    if (data["status"] == 201) {
                        console.log("Drink disliked!");
                        var votes = $("#drink" + drink_id + "_votes").text();
                        if (thumbsup.children('#filled_thumbsup').is(":visible")) {
                            $("#drink" + drink_id + "_votes").html(Number(votes) - 2);
                        } else {
                            $("#drink" + drink_id + "_votes").html(Number(votes) - 1);
                        }
                        dislikeDrinkAnimation(thumbsup, thumbsdown);
                    } else if (data["status"] == 422) {
                        console.log("Already disliked");
                    } else {
                        console.log(data["status"]);
                        console.log(data["message"]);
                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr);
                }
            });
        });
    });
}


function color_thumbs_proposals() {
    var url = APPURL + "/get_liked_disliked_user_drinks/";
    var csrftoken = getCookie("csrftoken");
    $.ajax({
        url: url,
        method: "GET",
        headers: {
            "X-CSRFToken": csrftoken
        },
        data: {
            csrfmiddlewaretoken: '{{ csrf_token}}'
        },
        dataType: "json",
        success: function (data) {
            if (data["status"] == 201) {
                liked_drinks = data["message"][0];
                disliked_drinks = data["message"][1];
                $(".upvote").each(function () {
                    var drink_id = $(this).attr("drinkid");
                    if (liked_drinks.includes(Number(drink_id))) {
                        $(this).children("#blank_thumbsup").hide();
                        $(this).children("#filled_thumbsup").show();
                    } else {
                        $(this).children("#blank_thumbsup").show();
                        $(this).children("#filled_thumbsup").hide();
                    }
                });
                $(".downvote").each(function () {
                    var drink_id = $(this).attr("drinkid");
                    if (disliked_drinks.includes(Number(drink_id))) {
                        $(this).children("#blank_thumbsdown").hide();
                        $(this).children("#filled_thumbsdown").show();
                    } else {
                        $(this).children("#blank_thumbsdown").show();
                        $(this).children("#filled_thumbsdown").hide();
                    }
                });
            } else {
                console.log(data["status"]);
                console.log("Error in finding liked and disliked drinks");

            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log("ERROR")
        }
    });
}

$(document).ready(function () {
    color_thumbs_proposals();
    up_vote();
    down_vote();
})