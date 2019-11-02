document.addEventListener('DOMContentLoaded', init);
const timerID = {};

function init() {
    window.dummy_url = $('#dummy_url');
    window.dummy_url.detach();
    $('#submit_btn').click(submit_handler);
}

function submit_handler(event){
    let url = $('#search').val();
    if(url === '' || url.includes(' ')) {
        alert('You need to enter a valid url first');
        return;
    }
    if(url in timerID){
        alert("url is already submitted");
        return;
    }
    let new_url = window.dummy_url.clone();
    new_url.attr("id", url);
    new_url.html(new_url.html().replace("dummy.com", url));
    new_url.find('span').hide();
    $('#url_list').append(new_url);
    timerID[url] = setInterval(() => submit_url(url), 1000);
}


async function submit_url(url){
    try{
        let form_data = new FormData();
        form_data.append("url", url);

        let response = await fetch('/view',{
            method: "POST",
            body: form_data
        });

        let response_json = await response.json();
        if(!response_json.done){
            return;
        }
        $(`#${url}`).find('span').show();
        clearInterval(timerID[url]);
    }catch (err) {
        alert(`Encounters this message ${err.message}`);
    }
}
