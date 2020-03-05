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

function likeDrinkAnimation(thumbsup, thumbsdown){
    thumbsup.children("#blank_thumbsup").hide();
    thumbsup.children("#filled_thumbsup").show();
    thumbsdown.children("#blank_thumbsdown").show();
    thumbsdown.children("#filled_thumbsdown").hide();
}

function dislikeDrinkAnimation(thumbsup, thumbsdown){
    thumbsup.children("#blank_thumbsup").show();
    thumbsup.children("#filled_thumbsup").hide();
    thumbsdown.children("#blank_thumbsdown").hide();
    thumbsdown.children("#filled_thumbsdown").show();
}
