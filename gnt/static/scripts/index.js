function display_duck() {
    $('#index-div').html('<div class="loading_gif_wrapper"><img class="duck_loading" src="../../static/duck.gif" alt="oof where dat duck boi at"/></div>');
}

$(document).ready(function() {
    // Listen for input when mic is clicked
    $(".assistant_button").click(function listening() {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            console.log('getUserMedia supported.');
            navigator.mediaDevices.getUserMedia({audio: true})
            .then(function(stream) { // success callback
                const mediaRecorder = new MediaRecorder(stream);
                var harker = hark(stream, {});

                // start recording when harker detects speech
                harker.on('speaking', function() {
                    mediaRecorder.start();
                    console.log('recording');
                });

                // stop recording when harker de-detects speech
                harker.on('stopped_speaking', function() {
                    mediaRecorder.stop();
                    harker.stop();
                    console.log('stopped recording');
                });

                // after stopped recording, send data
                mediaRecorder.ondataavailable = function(e) {
                    var blob = e.data;

                    console.log("start sending binary data...");
                    var form = new FormData();
                    form.append('audio', blob);
                    var url = APPURL + '/results/';
                    var csrftoken = getCookie("csrftoken");
                    $.ajax({
                        url: url,
                        type: 'POST',
                        headers: {"X-CSRFToken": csrftoken},
                        data: form,
                        processData: false,
                        contentType: false,
                        success: function (data) {
                            var dom = $(data).find("body")
                            $("body").html(data);
                            color_thumbs();// replace entire page with response
                        },
                        error: function (xhr, ajaxOptions, thrownError) {
                            console.log(xhr.status);
                            console.log(thrownError);
                        }
                    });
                    display_duck();
                }
            })
            .catch(function(err) { // error callback
                console.log('The following getUserMedia error occured: ' + err);
            });
        } else {
           console.log('getUserMedia not supported on your browser!');
        }
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

    // overwrite form's builtin post request
    $('#index-search-form').on('submit', function() {
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            dataType: 'html',
            data: $(this).serialize(),
            success: function(data) {
                var dom = $(data).find("body")
                $("body").html(data);
                color_thumbs();// replace entire page with response
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        });
        display_duck();
    });
});

function color_thumbs(){
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
}
