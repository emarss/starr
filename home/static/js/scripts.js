var dict_words= undefined;
var story_id = undefined;
var dict_quote = $("#result").html()
$.ajaxSetup({
    headers:{
        "X-CSRFToken": $("input[name=csrfmiddlewaretoken]").val()
    }
});
$("#story_form").submit(function(event) {
    $.ajax({
        url: "/journey/story/",
        type: "post",
        data: $("#story_form").serialize(),
        beforeSend: function() {
            document.getElementById("story_form").reset();
            $("form .btn").addClass("disabled");
            $("form .btn").blur();
        },
        success: function(e) {
            $("form .btn").removeClass("disabled");
            if( e['result'] == 'success'){
                $(".star-journey-sucess").html(e['html'])
                $(".journey-stories").prepend(e['new_story'])
            }else{
                $(".star-journey-messages").html(e['html'])
            }
        },
        error: function(e) {
            $("form .btn").removeClass("disabled");
            alert("An unknown error has occured. Please refresh this page and try again")
        }
    });

    return false;
});

function editStory(id) {
    story_id = id;
    story_body = $("#story_id_" + story_id + " p").html();
    $("#edit_story_form textarea").html(story_body);
    $("#edit_story").modal('show');
}

function deleteStory(id) {
    story_body = $("#story_id_" + id + " p").html().split(0, 20);
    $("#delete_story #delete_message").html(
            "Are you sure you want to delete the story: <i>\"" +
            story_body + "...</i>\" ?"
        );
    $("#delete_story #delete_btn").attr(
            "href", "/journey/story/delete/" + id
        );
    $("#delete_story").modal('show');
}


$("#edit_story_form").submit(function(event) {
    if( story_id != undefined){
        $.ajax({
            url: "/journey/story/update/"+ story_id,
            type: "post",
            data: $("#edit_story_form").serialize(),
            beforeSend: function() {
                $("form .btn").addClass("disabled");
                $("form .btn").blur();
            },
            success: function(e) {
                $("form .btn").removeClass("disabled");
                document.getElementById("edit_story_form").reset();
                if( e['result'] == 'success'){
                    $(".star-journey-sucess").html(e['html'])
                    $("#story_id_" + story_id).html(e['your_story'])
                    $("#edit_story").modal('hide');
                    story_id = undefined;
                }
                else{
                    $(".star-journey-messages").html(e['html'])
                }
            },
            error: function(e) {
                $("form .btn").removeClass("disabled");
                alert("An unknown error has occured. Please refresh this page and try again")
            }
        });
    }

    return false;
});

/******************************************************/
// Dictioany
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
                $(".star-dict-messages").html(e['html'])
            }

        },
        error: function(e) {
            $("form .btn").removeClass("disabled");
            alert("An unknown error has occured. Please refresh this page and try again")
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