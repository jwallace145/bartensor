$(document).ready(function () {
    var anchor = $(".remove");
    // Add click listener to each remove button
    anchor.each(function removeLike(index, element) {
        var user = $(this).attr("user");
        var drink_id = $(this).attr("drinkid");
        $(this).on("click", function removeLike() {
            console.log("remove drink " + drink_id);
            var csrftoken = getCookie("csrftoken");

            removeLikedDrink(drink_id);
        });
    });
});




function removeLikedDrink(drinkid) {
    html_id = "#drink_id_" + drinkid;
    $(html_id).hide("slow");
}