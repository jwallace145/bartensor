$(document).ready(function() {
//$(window).bind('load', function(){
    console.log("Running mark_liked_disliked_drinks");
    var url = APPURL + "/get_liked_disliked_drinks/";
    var csrftoken = getCookie("csrftoken");
    $.ajax({
        url: url,
        method: "GET",
        headers: { "X-CSRFToken": csrftoken },
        data: {csrfmiddlewaretoken: '{{ csrf_token}}' },
        dataType: "json",
        success: function(data) {
            if (data["status"] == 201) {
                liked_drinks = data["message"][0];
                disliked_drinks = data["message"][1];
                $(".thumbsup").each(function(){
                    var drink_id = $(this).attr("drinkid");
                    if(liked_drinks.includes(drink_id)){
                        $(this).children("#blank_thumbsup").hide();
                        $(this).children("#filled_thumbsup").show();
                    } else {
                        $(this).children("#blank_thumbsup").show();
                        $(this).children("#filled_thumbsup").hide();
                    }
                });
                $(".thumbsdown").each(function(){
                    var drink_id = $(this).attr("drinkid");
                    if(disliked_drinks.includes(drink_id)){
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
        error: function(xhr, ajaxOptions, thrownError) {
            console.log("ERROR")
        }
    });
});