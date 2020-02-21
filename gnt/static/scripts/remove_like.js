$(document).ready(function() {
    var anchor = $(".remove");
    // Add click listener to each thumbs up button
    anchor.each(function likeDrink(index, element) {
        $(this).on("click", function removeDrink(){
            console.log("remove drink");
        }