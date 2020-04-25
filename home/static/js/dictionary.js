var dict_words = undefined;
var dict_quote = $("#result").html()

$("#dict_form").submit(function(event) {
    event.preventDefault();
    $.ajax({
        url: "/dictionary/search/",
        type: "post",
        data: $("#dict_form").serialize(),
        beforeSend: function() {
            $("form .btn").addClass("disabled");
            $("#id_word").focus();
        },
        success: function(e) {
            $("form .btn").removeClass("disabled");
            if( e['result'] == 'success'){
                $("#result").html(e['search_results'])
                $(".star-dict-history ul").html(e['history'])
            }else{
                openMessage(e['html'])
            }

        },
        error: function(e) {
            $("form .btn").removeClass("disabled");
            openMessage("An unknown error has occured. Please refresh this page and try again")
        }
    });

    // return false;
});

function resetDict() {
    document.getElementById("dict_form").reset()
    $("#id_word").focus();
    $("#result").html(dict_quote)
}

function findSuggested(word) {
    $("#id_word").val(word);
    $("#dict_form").submit()
}
