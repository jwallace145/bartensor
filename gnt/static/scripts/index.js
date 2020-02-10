$(document).ready(function() {
    // From demo
    $(".listen").hide();
    $(".assistant_button").click(function waiting() {
        $(".listen").show();
        setTimeout(function redirect_to_loading() {
            var url = window.location;
            window.location.replace(url + "loading");
        }, 10000);
    });
    $(".single_drink_rec").click(function redirect_to_loading() {
        var url = window.location;
        window.location.replace(url + "loading");
    });

    // When search bar is selected, make underline of button match
    $(".search-bar").on({
        focus: function() {
            //also maybe 7abcf5 or 9bc7ed, I don't know how to find the exact color
            $(".search-button").css("border-bottom", "2px solid #7ac0f5");
        },
        focusout: function() {
            $(".search-button").css("border-bottom", "2px solid black");
        }
    });

    $(".search-nav-link").click(function() {
        $(".search-nav-link").removeClass("active"); // make all tabs inactive
        $(this).addClass("active"); // make clicked tab active
        $(this).prev().prop("checked", true); // check corresponding radiobutton
    });
});