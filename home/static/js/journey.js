var story_id  = undefined;

$("#story_form").submit(function(event) {
    event.preventDefault();
    $("#id_story").val(editor.getData())
    if($("#id_story").val() == 0){
        openMessage("You cannot sent a blank story");
        return false;
    }
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
                openMessage(e['html'])
                editor.setData("")
                $(".journey-stories").prepend(e['new_story'])
            }else{
                openMessage(e['html'])
            }
        },
        error: function(e) {
            $("form .btn").removeClass("disabled");
            openMessage("An unknown error has occured. Please refresh this page and try again")
        }
    });

    return false;
});

function editStory(id) {
    story_id = id; //updating the global
    var story_body = $("#story_id_" + story_id + " p").html();
    $("#edit_story_form textarea").html(story_body);
    $("#edit_story").modal('show');
}

function deleteStory(id) {
    var story_body = $("#story_id_" + id + " p").html().split(0, 20);
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
                    openMessage(e['html'])
                    $("#story_id_" + story_id).html(e['your_story'])
                    $("#edit_story").modal('hide');
                    story_id = undefined;
                }
                else{
                    openMessage(e['html'])
                }
            },
            error: function(e) {
                $("form .btn").removeClass("disabled");
                openMessage("An unknown error has occured. Please refresh this page and try again")
            }
        });
    }

    return false;
});