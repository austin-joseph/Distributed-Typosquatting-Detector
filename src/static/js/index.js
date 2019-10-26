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
                $("#url_table").html("We've submitted your url for processing, we'll inform you once its done");
                setTimeout(loadUrlData(url), 1000);
                count = count + 1;
                return;
            } else {
                $("#url_table").html(count);
                urlList[url] = data;
            }
        });
}

$(document).ready(function() {
    $("#submit_button").click(function() {
        var newUrl = $("#textbox_url").val();
        if (urlList[newUrl] == null && newUrl != "") {
            loadUrlData(newUrl);
            // console.log(result);
        }
    });
});