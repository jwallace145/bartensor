function display_duck() {
    $('#index-div').html('<div class="loading_gif_wrapper"><img class="duck_loading" src="../../static/duck.gif" alt="oof where dat duck boi at"/></div>');
}

$(document).ready(function () {
    // Listen for input when mic is clicked
    $(".assistant_button").click(function listening() {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            console.log('getUserMedia supported.');
            navigator.mediaDevices.getUserMedia({
                    audio: true
                })
                .then(function (stream) { // success callback
                    const mediaRecorder = new MediaRecorder(stream);
                    var harker = hark(stream, {});

                    // start recording when harker detects speech
                    harker.on('speaking', function () {
                        mediaRecorder.start();
                        console.log('recording');
                    });

                    // stop recording when harker de-detects speech
                    harker.on('stopped_speaking', function () {
                        mediaRecorder.stop();
                        harker.stop();
                        console.log('stopped recording');
                    });

                    // after stopped recording, send data
                    mediaRecorder.ondataavailable = function (e) {
                        var blob = e.data;

                        console.log("start sending binary data...");
                        var form = new FormData();
                        form.append('audio', blob);
                        var url = APPURL + '/results/';
                        var csrftoken = getCookie("csrftoken");
                        $.ajax({
                            url: url,
                            type: 'POST',
                            headers: {
                                "X-CSRFToken": csrftoken
                            },
                            data: form,
                            processData: false,
                            contentType: false,
                            success: function (data) {
                                $("#index-div").hide();
                                $("#content_here").append(data);
                                hide_disliked_drinks();
                                color_thumbs();
                                thumbs_up();
                                thumbs_down();

                            },
                            error: function (xhr, ajaxOptions, thrownError) {
                                console.log(xhr.status);
                                console.log(thrownError);
                                $("#index-div").hide();
                                $("#content_here").append('<h6 class="backend-error">Error searching drinks</h6>');
                            }
                        });
                        display_duck();
                    }
                })
                .catch(function (err) { // error callback
                    console.log('The following getUserMedia error occured: ' + err);
                });
        } else {
            console.log('getUserMedia not supported on your browser!');
        }
    });

    // When search bar is selected, make underline of button match
    $(".search-bar").on({
        focus: function () {
            //also maybe 7abcf5 or 9bc7ed, I don't know how to find the exact color
            $(".search-button").css("border-bottom", "2px solid #7ac0f5");
        },
        focusout: function () {
            $(".search-button").css("border-bottom", "2px solid black");
        }
    });

    $(".search-nav-link").click(function () {
        $(".search-nav-link").removeClass("active"); // make all tabs inactive
        $(this).addClass("active"); // make clicked tab active
        $(this).prev().prop("checked", true); // check corresponding radiobutton
    });

    // overwrite form's builtin post request
    $('#index-search-form').on('submit', function search(e) {
        // This prevents the ajax call from navigating to the /results endpoint
        // Makes it stay on index which is what we want
        e.preventDefault();
        e.stopPropagation();
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            dataType: 'html',
            data: $(this).serialize(),
            success: function (data) {
                $("#index-div").hide();
                $("#content_here").append(data);
                color_thumbs();
                thumbs_up();
                thumbs_down();
                hide_disliked_drinks();
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.statusCode);
                console.log(xhr.statusText);
                console.log(thrownError);
                $("#index-div").hide();
                $("#content_here").append('<h6 class="backend-error">Error searching drinks</h6>');
            }
        });
        display_duck();
    });
});

function color_thumbs() {
    var url = APPURL + "/get_liked_disliked_drinks/";
    var csrftoken = getCookie("csrftoken");
    $.ajax({
        url: url,
        method: "GET",
        headers: {
            "X-CSRFToken": csrftoken
        },
        dataType: "json",
        success: function (data) {
            if (data["status"] == 201) {
                liked_drinks = data["message"][0];
                disliked_drinks = data["message"][1];
                $(".thumbsup").each(function () {
                    var drink_id = $(this).attr("drinkid");
                    if (liked_drinks.includes(drink_id)) {
                        $(this).children("#blank_thumbsup").hide();
                        $(this).children("#filled_thumbsup").show();
                    } else {
                        $(this).children("#blank_thumbsup").show();
                        $(this).children("#filled_thumbsup").hide();
                    }
                });
                $(".thumbsdown").each(function () {
                    var drink_id = $(this).attr("drinkid");
                    if (disliked_drinks.includes(drink_id)) {
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

function hide_disliked_drinks() {
    const checkbox = $("#hide-disliked-drinks-checkbox");
    var url = APPURL + "/get_liked_disliked_drinks/";
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
                $(".thumbsdown").each(function () {
                    var drink_id = $(this).attr("drinkid");
                    var checked = checkbox.prop("checked");
                    if (disliked_drinks.includes(drink_id)) {
                        if (checked) {
                            $("#drink_id_" + drink_id).hide();
                        } else {
                            $("#drink_id_" + drink_id).show();
                        }
                    }
                });
            } else {
                console.log(data["status"]);
                console.log("Error in hide disliked drinks checkbox");
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log("ERROR")
        }
    });
}

function thumbs_up() {
    var anchor = $(".thumbsup");
    // Remove listeners if there were any
    anchor.each(function removeListner() {
        $(this).unbind();
    })
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

function thumbs_down() {
    var anchor = $(".thumbsdown");
    // Remove listeners if there were any
    anchor.each(function removeListner() {
        $(this).unbind();
    })
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
                        dislikeDrinkAnimation(thumbsup, thumbsdown);
                    } else if (data["status"] == 422) {
                        console.log(
                            "This is already in your disliked drinks"
                        );
                    } else {
                        console.log("Error in disliking drink");
                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr);
                }
            });
        });
    });
}

var offset = 0;

function load_more_drinks() {
    offset += 1;
    var url = APPURL + '/more_results/';
    var csrftoken = getCookie("csrftoken");
    query = $(".query-header").text();
    query = query.split("Query: ").slice(1).pop();
    question = $("#question-span").text();
    $.ajax({
        url: url,
        type: 'POST',
        headers: {
            "X-CSRFToken": csrftoken
        },
        data: {
            text: query,
            offset: offset * 10,
            question: question
        },
        dataType: "html",
        success: function (data) {
            // There are no more drinks to load
            if (data.length == 1) {
                console.log("done");
                $(".load-more").html("<h5>All drinks loaded</h5>");
            } else {
                $(".load-more").before(data);
                color_thumbs();
                thumbs_up();
                thumbs_down();
                hide_disliked_drinks();
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
            $(".load-more-error").html('');
            $("#content_here").append('<div class="load-more-error">Cannot load more drinks</div>');
        }
    });
}