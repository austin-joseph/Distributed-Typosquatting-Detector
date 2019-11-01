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
                setTimeout(loadUrlData(url), 5000);
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
        $("#url_table").html("We are loading your data please give us a moment");
    } else {
        $("#url_table").html("We have loaded you data");
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