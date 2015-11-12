/**
 * Created by herve on 10/11/15.
 */
function ajax_exercises_by_muscles(muscle) {
    $("#loader").show();
    $("#loader-message").show();
    console.log("Loading exercises information") // sanity check
    $.ajax({
        url : "/exercises/muscles/ajax-exercises-by-muscles/", // the endpoint
        type : "POST", // http method
        data : { muscle : muscle }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            json = JSON.stringify(json);
            json = JSON.parse(json);
            $("#loader").hide();
            $("#loader-message").hide();
            $("#exercises-count").text(json.count);
            $("#exercises-count").attr('href', json.link);

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

