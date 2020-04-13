var story_id = undefined;

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
        },
        success: function(e) {
            $("form .btn").removeClass("disabled");
            $(".star-journey-sucess").html(e['html'])
            $(".journey-stories").prepend(e['new_story'])
        },
        error: function(e) {
            $("form .btn").removeClass("disabled");
            $(".star-journey-messages").html(e['html'])
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
            },
            success: function(e) {
                console.log(e['your_story'])
                document.getElementById("edit_story_form").reset();
                $("form .btn").removeClass("disabled");
                $(".star-journey-sucess").html(e['html'])
                $("#story_id_" + story_id).html(e['your_story'])
                $("#edit_story").modal('hide');
                story_id = undefined;
            },
            error: function(e) {
                $("form .btn").removeClass("disabled");
                $(".star-journey-messages").html(e['html'])
            }
        });
    }

    return false;
});