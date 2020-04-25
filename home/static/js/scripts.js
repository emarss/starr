$.ajaxSetup({
    headers:{
        "X-CSRFToken": $("input[name=csrfmiddlewaretoken]").val()
    }
});

$(document).ready(function($) {
    $(".message-box").hide();
    $(".message-box").removeClass("d-none");
});
function openMessage(message) {
    $(".message-box span").html(message)
    $(".message-box").slideDown();
    setTimeout(function () {
        closeMessage()
    }, 5000);
}
function closeMessage() {
    $(".message-box").slideUp();
}