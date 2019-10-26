var urlList = {};
var count = 0;

function loadUrlData(url) {
    $.post("/view", {
            url: url
        },
        function(data) {
            var data = JSON.parse(data);
            // console.log(data);
            if (data == null || !data.done) {
                setTimeout(loadUrlData(url), 1000);
                count = count + 1;
                return;
            } else {
                urlList[url] = data;
                updateDisplay(url)
            }
        });
}

function updateDisplay(newUrl) {
    if (urlList[newUrl] == null) {
        $("#url_table").html("Sent the url to the server but the servers still processing");
    } else {
        $("#url_table").html("The url data has been loaded");
    }
}

$(document).ready(function() {
    $("#submit_button").click(function() {
        var newUrl = $("#textbox_url").val();
        if (newUrl != "") {
            if (urlList[newUrl] == null) {
                loadUrlData(newUrl);
            }
            updateDisplay(newUrl)
        }
    });
});