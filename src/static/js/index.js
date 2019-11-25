document.addEventListener('DOMContentLoaded', init);

function error_code_enum(){
    this.ERR_ZERO = 0;
    this.ERR_ONE = 1;
    this.ERR_TWO = 2;
    this.ERROR_MSG = {
        [this.ERR_ZERO]: "Loading....",
        [this.ERR_ONE]: "waiting",
        [this.ERR_TWO]: "processing"
    }
}

const error_codes = new error_code_enum();

const timer_control = {
    timer: {},
    current_url: ""
};

function init() {
    $('#submit_btn').click(submit_handler);
    $("#spinner").hide();
}

function submit_handler(event) {
    let url = $('#search').val();
    if (url === '' || url.includes(' ')) {
        alert('You need to enter a valid url first');
        return;
    }
    if(timer_control.current_url === url){
        alert('Url is already under processing');
        return;
    }
    $("#url_list").empty();
    $("#spinner").show();
    timer_control.current_url = url;
    timer_control.timer[url] = setInterval(() => submit_url(url), 1000);
}


async function submit_url(url) {
    try {
        if(timer_control.current_url !== url) { // if the user made a new search before the current url finishes
            clearInterval(timer_control.timer[url]);
            return;
        }

        let form_data = new FormData();
        form_data.append("url", url);
        let response = await fetch('/view', {
            method: "POST",
            body: form_data
        });
        let response_json = await response.json();
        let message = error_codes.ERROR_MSG[response_json.error];
        $("#spinner_text").html(message);
        if(response_json.error !== error_codes.ERR_ZERO){
            return;
        }
        $("#spinner").hide();

        await Promise.all(response_json.generatedUrls.map(async (element)=>{
            let result = await fetch( `//${element}`, {mode: 'no-cors'}).catch( e => {});
             $("#url_list").append(`<li class="list-group-item"><a ${(result) ? "": "class=\"red_link_text\""}  href=${(result) ? "/image/" + element: "#"}>${element}</a></li>`);
        }));

        if(response_json.generatedUrls.length === 0){
             $("#url_list").append(`<li class="list-group-item">Found no squatting urls</li>`);
        }
        timer_control.current_url = "";
        clearInterval(timer_control.timer[url]);
    } catch (err) {
	clearInterval(timer_control.timer[url]);
        alert(`Encounters this error: ${err.message}`);
    }
}
