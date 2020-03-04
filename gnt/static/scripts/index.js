$(document).ready(function() {
    // Listen for input when mic is clicked
    $(".assistant_button").click(function listening() {
        // https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
        // https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_Recording_API/Using_the_MediaStream_Recording_API
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

                // collect audio data when recording
                let chunks = [];
                mediaRecorder.ondataavailable = function(e) {
                  chunks.push(e.data);
                }

                // stop recording when harker de-detects speech
                harker.on('stopped_speaking', function() {
                    mediaRecorder.stop();
                    harker.stop()
                    console.log('stopped recording')

                    const blob = new Blob(chunks, {'type': 'audio/mpeg'});
                    chunks = []; // reset chunks

                    // https://stackoverflow.com/questions/51130675/how-to-upload-large-audio-file-to-a-django-server-given-a-blob-url
                    console.log("start sending binary data...");
                    var form = new FormData();
                    form.append('audio', blob);
                    var formElement = document.querySelector("form");

                    var csrftoken = getCookie("csrftoken");
                    var util = {};
                    util.post = function(url, fields) {
                        var $form = $('<form>', {
                            action: url,
                            method: 'post'
                        });
                        $.each(fields, function(key, val) {
                             $('<input>').attr({
                                 type: "hidden",
                                 name: key,
                                 value: val
                             }).appendTo($form);
                        });
                        $form.appendTo('body').submit();
                    }
                    $.ajax({
                        url: url,
                        type: 'POST',
                        headers: {"X-CSRFToken": csrftoken},
                        data: form,
                        processData: false,
                        contentType: false,
                        success: function (data) {
                            console.log('response' + JSON.stringify(data));
                            console.log(data.redirect)
                            window.location.href = data.redirect
                        },
                        error: function (xhr, ajaxOptions, thrownError) {
                            console.log(xhr.status);
                            console.log(thrownError);
                        }
                    });
                });
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