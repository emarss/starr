var story_id, delete_comment_id = undefined;
var store_history;
var notebook_changed, initial_bible_request = false;
var search_results_def = $("#star_bible_search").html()
var markVerses = undefined;

jQuery(document).ready(function($) {
    // Srolling to current book
    scrollToBook($(".star-bible-books .active a").html());
    
    //get the current chapter
    $("#bible_form").submit()

    //go to book
    $("#id_bible_book").change(function(){
        $("#id_bible_chapter").val(1)
        $("#id_bible_verse").val(1)
        $("#bible_form").submit()
    });

    //goto chapter
    $("#id_bible_chapter").change(function(){
        $("#bible_form").submit()
    });

    //going to the current verse
    $("#id_bible_verse").change(function(){
        gotoVerse()
    });

    //viewing verse comments
    viewComment()

    //save notebook on change
    $(".bible-notebook-form .ck-content").keyup(function (event) {
        notebook_changed = true;
        notebook_changed_timer.clearTimeout();
        notebook_changed_timer = setTimeout(function(){
            $("#bible_notebook_form").submit();
            notebook_changed = false;
        }, 10000);
    });
});

$("#bible_form").submit(function(event) {
    if(validateDateBibleChpater()){
        $.ajax({
            url: "/bible/chapter/",
            type: "post",
            data: $("#bible_form").serialize(),
            beforeSend: function() {
            },
            success: function(e) {
                if( e['result'] == 'success'){
                    $(".star-bible-contents").html(e['chapter']);
                    $("#id_bible_chapter").attr('max',e["chapters_count"]);
                    $("#id_bible_verse").attr('max',e["verses_count"]);
                    $(".star-bible-contents").children("p").first().addClass("active");
                    $("#marked_verses").html(e["marked_verses"]);
                    markVerses = e["marked_verses"];
                    highlightBookmarks();
                    gotoVerse();
                    if(initial_bible_request){ //the inital request should not be record in history
                        if(store_history != undefined){
                            clearTimeout(store_history);
                        }
                        store_history = setTimeout(function() {
                            temp_chapter = $("#id_bible_chapter").val();
                            temp_book = $("#id_bible_verse").val();                        
                            storeHistory(temp_book, temp_chapter)
                        }, 30000);
                    }
                    initial_bible_request = true;
                }else{
                    openMessage(e['html'])
                }
            },
            error: function(e) {
                openMessage("An unknown error has occured. Please refresh this page and try again")
            }
        });
    }

    return false;
});


$("#bible_search_form").submit(function(event) {
    if(validateDateBibleChpater()){
        $.ajax({
            url: "/bible/search/",
            type: "post",
            data: $("#bible_search_form").serialize(),
            beforeSend: function() {
                $("#view_search").removeClass('d-none');
                $("input").blur()
                $("#star_bible_search").html(search_results_def);
                utilTab('search');
            },
            success: function(e) {
                if( e['result'] == 'success'){
                    $("#star_bible_search").html(e["search_results"]);
                    openMessage('Search complete.');
                    hightSearch(e['search_key']);
                }else{
                    openMessage(e['errors'])
                }
            },
            error: function(e) {
                openMessage("An unknown error has occured. Please refresh this page and try again")
            }
        });
    }

    return false;
});

function storeHistory(temp_book, temp_chapter) {
    if(
        $("#id_bible_chapter").val() == temp_chapter
        &&
        $("#id_bible_verse").val() == temp_book
        ){    
        $.ajax({
            url: "/bible/history/store/",
            type: "post",
            data: $("#bible_form").serialize(),
            success: function(e) {
                console.info("History Saved");
            }
        });
    }
}

function viewChapter(book, chapter) {
    $("#id_bible_book").val(book);
    $("#id_bible_chapter").val(chapter);
    $("#id_bible_verse").val(1);
    $("#bible_form").submit()
    scrollToBook(book);
}

function viewHistory() {
    $.ajax({
        url: "/bible/history/",
        type: "post",
        beforeSend: function() {
        },
        success: function(e) {
            $("#star_bible_history").html(e['html']);
        },
        error: function(e) {
            openMessage("An unknown error has occured. Please refresh this page and try again")
        }
    });
    utilTab("history");
    return false;
}

function validateDateBibleChpater(){
    var value = parseInt($("#id_bible_chapter").val())
    var max_value = parseInt($("#id_bible_chapter").attr("max").valueOf())
    if (value >max_value){
        $("#id_bible_chapter").val(max_value);
        return true;
    }
    return true;
}

function validateDateBibleVerse(){
    if ($("#id_bible_verse").val() > $("#id_bible_verse").attr("max")){
        $("#id_bible_verse").val($("#id_bible_verse").attr("max"));
        return false;
    }
    return true;
}
function viewBibleBook(book) {
    $("#id_bible_book").val(book);
    $("#id_bible_chapter").val(1);
    $("#id_bible_verse").val(1);
    $("#bible_form").submit();
    scrollToBook(book);
}
function getPrevSiblingsHeight(verse) {
    sib = verse.prev("p")
    height_sum = 0;
    while (true) {
        height_sum += (sib.innerHeight() + 10);
        sib = sib.prev("p");
        if (sib.innerHeight() == undefined){
            break;
        }
    }

    return height_sum;
}

function scrollToBook(book) {
    book = book.replace(/\s/g, "");
    var scrollHeight = $("#"+book).prevAll("li").length * ($("#"+book).height() + 5);
    $(".star-bible-panel-body").scrollTop(scrollHeight);

    // setting the current book to active
    $(".star-bible-books ul li").removeClass('active');
    $(".star-bible-books ul #" + book).addClass('active');    
}

function gotoVerse(withScroll=true) {
    var verse = $("#id_bible_verse").val();
    var chapter = $("#id_bible_chapter").val();
    var book = $("#id_bible_book").val();
    

    id = "#verse-"+ book.replace(/\s/g, "-").toLowerCase()+"-"+chapter+verse;
    $(".star-bible-contents p").removeClass("active");
    verseObj = $(id)
    verseObj.addClass('active');
    if(withScroll){
        $(".star-bible-contents").scrollTop(getPrevSiblingsHeight(verseObj));
    }

    //viewing comment
    viewComment()    
}
function viewVerse(key) {
    id = key.slice(key.indexOf(":")+1)
    $("#id_bible_verse").val(id)

    slugified_id = "verse-"+ key.replace(/\s/g, "-").replace(":", "").toLowerCase();
    gotoVerse(false)
}
function utilTab(tab) {
    $(".bible-util-btn").removeClass('active');
    $("#view_"+tab).addClass('active');
    $("#view_"+tab).blur();
    $(".bible-util-tab").addClass('d-none');
    $("#star_bible_"+tab).removeClass('d-none');
}
function viewResult(verse) {
    book = verse.slice(0, verse.lastIndexOf(" "));
    chapter = verse.slice(verse.lastIndexOf(" ")+1, verse.indexOf(":"));
    verse_num = verse.slice(verse.lastIndexOf(":")+1,);

    $("#id_bible_book").val(book);
    $("#id_bible_chapter").val(chapter);
    $("#id_bible_verse").val(verse_num);
    $("#bible_form").submit();
    scrollToBook(book);

    gotoVerse()
}

$("#bible_comment_form").submit(function(event){
    $.ajax({
        url: "/bible/comment/store/",
        type: "post",
        data: $("#bible_comment_form").serialize(),
        beforeSend: function() {
            document.getElementById("bible_comment_form").reset()
        },
        success: function(e) {
            if( e['result'] == 'success'){
                    $("#star_bible_comments ul").html(e['html']);
                    openMessage('Comment saved.')
                }else{
                    openMessage(e['errors'])
                }
        },
        error: function(e) {
            openMessage("An unknown error has occured. Please refresh this page and try again")
        }
    });

    return false;
});


function viewComment() {
    verse_ref = $("#id_bible_book").val() + " " 
                        + $("#id_bible_chapter").val() +
                        ":" + $("#id_bible_verse").val();

    //setting current verse key
    $("#id_current_verse_key").val(verse_ref)

    $.ajax({
        url: "/bible/comment/",
        type: "post",
        data: {
            verse: verse_ref
        },
        beforeSend: function() {
        },
        success: function(e) {
            $("#star_bible_comments ul").html(e['html']);
        },
        error: function(e) {
            openMessage("An unknown error has occured. Please refresh this page and try again")
        }
    });
    return false;
}

function deleteComment(id) {
    comment = $("#comment_" + id).html().slice(0,100);
    $("#delete_message").html(comment);
    delete_comment_id = id;
    $("#delete_comment").modal("show");
}

function editComment(id) {
    comment = $("#comment_" + id).html();
    $("#id_comment_edit").html(comment);
    $("#id_comment_edit_id").val(id);

    verse_ref = $("#id_bible_book").val() + " " 
                        + $("#id_bible_chapter").val() +
                        ":" + $("#id_bible_verse").val();
    $("#id_current_verse_edit_key").val(verse_ref);
    $("#edit_comment").modal("show");
}


function confirmDeleteComment() {
    $("#delete_comment").modal("hide");

    if(delete_comment_id != undefined){
        verse_ref = $("#id_bible_book").val() + " " 
                        + $("#id_bible_chapter").val() +
                        ":" + $("#id_bible_verse").val();

        $.ajax({
            url: "/bible/comment/delete/",
            type: "post",
            data: {
                comment_id: delete_comment_id,
                verse: verse_ref
            },
            beforeSend: function() {
            },
            success: function(e) {
                if( e['result'] == 'success'){
                    $("#star_bible_comments ul").html(e['html']);
                    openMessage('Comment deleted.')
                }else{
                    openMessage(e['errors'])
                }
            },
            error: function(e) {
                openMessage("An unknown error has occured. Please refresh this page and try again")
            }
        });
    }
}

$("#comment_edit_form").submit(function(event) {
    $.ajax({
        url: "/bible/comment/update/",
        type: "post",
        data: $("#comment_edit_form").serialize(),
        beforeSend: function() {
            document.getElementById("comment_edit_form").reset()
            $("#edit_comment").modal("hide");
        },
        success: function(e) {
            if( e['result'] == 'success'){
                    $("#star_bible_comments ul").html(e['html']);
                    openMessage('Comment updated.')
                }else{
                    openMessage(e['errors'])
                }
        },
        error: function(e) {
            openMessage("An unknown error has occured. Please refresh this page and try again")
        }
    });

    return false; 
});


$("#bible_notebook_form").submit(function(event){
    // event.preventDefault()
    $("#notebook").val(editor.getData())
    $.ajax({
        url: "/bible/notes/store/",
        type: "post",
        data: $("#bible_notebook_form").serialize(),
        beforeSend: function() {
        },
        success: function(e) {
            if( e['result'] == 'success'){
                editor.setData(e['html']);
                openMessage("Notebook Saved.")
            }else{
                openMessage(e['errors'])
            }
        },
        error: function(e) {
            openMessage("An unknown error has occured. Please refresh this page and try again.")
        }
    });

    return false;
});

function  viewNotes() {
    if(editor.getData().length == 0){
        $.ajax({
            url: "/bible/notes/",
            type: "post",
            beforeSend: function() {
            },
            success: function(e) {
                editor.setData(e['html']);
            },
            error: function(e) {
                openMessage("An unknown error has occured. Please refresh this page and try again")
            }
        });
    }
    utilTab('notebook');
    return true;
}
function hightSearch(key) {
    var words = key.split(" ");
    var results = $("#star_bible_search").find("span");
    for(i = 0; i< results.length; i++){
        for(j = 0; j < words.length; j++){
            regex = new RegExp(words[j], "gi")
            results[i].innerHTML = results[i].innerHTML.replace(regex, `<b class='highlight'>${words[j]}</b>`);
        }
    }

}
function markVerse(key) {
        $.ajax({
            url: "/bible/mark/verse/",
            type: "post",
            data: {
                key
            },
            beforeSend: function() {
            },
            success: function(e) {
                if(e['result'] == "success"){
                        slugified_id = "verse-"+ key.replace(/\s/g, "-").replace(":", "").toLowerCase();
                        if(e['action'] == "added"){
                            $("#" + slugified_id).addClass('bookmarked');
                        }else{
                            $("#" + slugified_id).removeClass('bookmarked');
                        }
                }else{
                    openMessage(e['error']);
                }
            },
            error: function(e) {
                openMessage("An unknown error has occured. Please refresh this page and try again");
            }
        });
 }
 function highlightBookmarks() { 
     for (i = 0; i < markVerses.length; i++){
        var key = markVerses[i].key;
        slugified_id = "verse-"+ key.replace(/\s/g, "-").replace(":", "").toLowerCase();
        $("#" + slugified_id).addClass('bookmarked');
     }
 }

