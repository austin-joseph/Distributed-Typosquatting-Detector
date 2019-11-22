document.addEventListener('DOMContentLoaded', init);

function init() {
    window.dummy_url = $('#dummy_url');
    window.dummy_url.detach();
    $("#url_list").hide();
    $('#submit_btn').click(submit_handler);
}

function submit_handler(event) {
    let url = $('#search').val();
    if (url === '' || url.includes(' ')) {
        alert('You need to enter a valid url first');
        return;
    }
    let new_url = window.dummy_url.clone();
    new_url.html(new_url.html().replace("dummy.com", url));
    new_url.removeAttr("id");
    let result_urls = new_url.find(".list-group");
    result_urls.empty();
    new_url.find('span').hide();
    $('#url_list').append(new_url);
    submit_url(url);
    $("#url_list").show();
}


async function submit_url(url) {
    try {
        let form_data = new FormData();
        form_data.append("url", url);

        let response = await fetch('/view', {
            method: "POST",
            body: form_data
        });

        let response_json = await response.json();
        if(response_json.error !== 0) throw new Error(`server sent back error code ${response_json.error}`);
        for(let element of response_json.generatedUrls){
            let result_urls = $(".list-group").last();
            result_urls.append(`<li class="list-group-item"><a href="image/${element}">${element}</a></li>`);
        }
        $("#url_list span").last().show();
    } catch (err) {
        $("#url_list span").last().html("Error");
        $("#url_list span").last().show();
        alert(`Encounters this error: ${err.message}`);
    }
}