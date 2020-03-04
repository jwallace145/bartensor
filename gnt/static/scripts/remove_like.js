$(document).ready(function () {
    var anchor = $(".remove");
    // Add click listener to each remove button
    anchor.each(function removeLike(index, element) {
        var user = $(this).attr("user");
        var drink_id = $(this).attr("drinkid");
        var url = APPURL + "/remove_liked_drink/";
        var payload = {
            drink_id: drink_id,
            user: user
        };
        $(this).on("click", function removeLike() {
            var csrftoken = getCookie("csrftoken");
            $.ajax({
                url: url,
                method: "POST",
                headers: { "X-CSRFToken": csrftoken },
                data: payload,
                dataType: "json",
                success: function(data) {
                    if (data["status"] == 200) {
                        removeLikedDrink(drink_id);
                    } else if (data["status"] == 404) {
                        console.log("Not in liked drinks") //TODO: Replace with expressive response
                    } else {
                        console.log("Error in removing liked drink");
                    }
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    console.log("Error");
                    console.log(xhr);
                }
            });
        });
    });
});




function removeLikedDrink(drinkid) {
    html_id = "#drink_id_" + drinkid;
    $(html_id).hide("slow");
}