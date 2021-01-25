$(document).ready(function () {
    $(document).on("click", "#leaveCommentForm button", function (e) {
        var post_id = document.getElementById("post_id").innerText;
        var author = $(this).parent().parent().find("#name").val();
        var content = $(this).parent().parent().find("#message").val();
        var dataString = '{ "post_id":"' + post_id + '",' +
            '"author":"' + standardize_request(author) + '",' +
            '"content":"' + standardize_request(content) + '"' +
            '}';

        $.ajax({
            type: "POST",
            url: "/en/blog/post_comment",
            contentType: 'application/json',
            data: dataString,
            success: function (dataserver) {
                var x = document.getElementById('commentList').innerHTML;
                var comment = "<li class='comment root-comment c-level-0'><p id='comment_id' hidden>" + dataserver.id + "</p><div class='vcard bio'><img src='/static/images/person_1.jpg' alt='Image placeholder'></div><div class='comment-body'><h3>" + dataserver.author_username + "</h3><div class='meta mb-3'>" + format_date(dataserver.created_at) + "</div><p>" + dataserver.content + "</p><a class='replycm'>"+gettext("Reply")+"</a></div><ul class='children'></ul></li>";
                x = comment + x;
                document.getElementById("commentList").innerHTML = x;
                $('#leaveCommentForm #message').val('');
            }
        });


        e.preventDefault();
    });
});

$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});


function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}

function getNow() {
    var d = new Date();

    var month = Intl.DateTimeFormat('en-US', { month: 'long' }).format(d).slice(0, 3);
    var date = d.getUTCDate();
    var year = d.getUTCFullYear();
    var hour = d.getUTCHours();
    var am_pm = ""
    if (hour == 12) {
        am_pm = "P.M.";
    } else if (hour > 12) {
        am_pm = "P.M.";
        hour = hour - 12;
    } else {
        am_pm = "A.M."
    }
    var min = d.getUTCMinutes();
    if (min < 9) {
        min = "0" + min;
    }

    render_date = month + ". " + date + ", " + year + ", " + hour + ":" + min + " " + am_pm;
    return render_date
}

$(document).ready(function () {
    
    $(document).on("click", "a.replycm", function () {
        if(username) {
            $("#replyCommentForm").remove();
            $(this).parent().append(
                '<form id="replyCommentForm" style="margin-top: 15px;"><div class="form-group"><div class="row" style="margin-bottom: 10px;margin-left: 0;margin-right: 0;"><div class="col" style="padding: 0;"><input type="text" class="form-control" value="' + username + '" readonly required></div></div><textarea type="text" class="form-control" id="formGroupExampleInput2" style="margin-bottom: 10px;" required></textarea><button type="button" class="btn btn-primary replycm">'+gettext("Comment")+'</button><button class="btn btn-cancel">'+gettext("Cancel")+'</button></div></form>'
            );
        } else {
            $("#loginReminder").remove()
            $(this).parent().append(
                '<p id="loginReminder"><a href="/en/accounts/login/">'+gettext("Login")+'</a> '+gettext("to leave comments")+'</p>'
            );
        }
    })

    $(document).on('click', '#replyCommentForm button.btn-cancel', function () {
        $("#replyCommentForm").remove();

    })

    $(document).on('click', 'button.replycm', function () {
        var post_id = document.getElementById("post_id").innerText;
        var parent_id = $("#replyCommentForm").parent().parent().find('#comment_id')[0].innerHTML;
        var author = $(this).parent().find('input').val()
        var content = $(this).parent().find('textarea').val();
        var dataString = '{ "post_id":"' + post_id + '",' +
            '"author":"' + standardize_request(author) + '",' +
            '"content":"' + standardize_request(content) + '",' +
            '"parent_id":"' + standardize_request(parent_id) + '"' +
            '}';

        root = $(this).closest("li.comment")
        console.log(root.hasClass("final-level"))
        $.ajax({
            type: "POST",
            url: "/en/blog/post_comment",
            contentType: 'application/json',
            data: dataString,
            success: function (dataserver) {
                if (root.hasClass("c-level-2")) {
                    console.log("2")
                    var li = "<br><li class='comment c-level-2'><p id='comment_id' hidden>" + dataserver.id + "</p><div class='vcard bio'><img src='/static/images/person_1.jpg' alt='Image placeholder'></div><div class='comment-body'><h3>" + replace_quotes(dataserver.author_username) + "</h3><div class='meta mb-3'>" + format_date(dataserver.created_at) + "</div><p>" + replace_quotes(dataserver.content) + "</p><a class='replycm'>"+ gettext("Reply")+"</a></div></li>";
                    root.append(li);
                }
                else if (root.hasClass("c-level-1")) {
                    console.log("1")
                    var li = "<li class='comment c-level-2'><p id='comment_id' hidden>" + dataserver.id + "</p><div class='vcard bio'><img src='/static/images/person_1.jpg' alt='Image placeholder'></div><div class='comment-body'><h3>" + replace_quotes(dataserver.author_username) + "</h3><div class='meta mb-3'>" + format_date(dataserver.created_at) + "</div><p>" + replace_quotes(dataserver.content) + "</p><a class='replycm'>"+ gettext("Reply")+"</a></div><ul class='children'></ul></li>";
                    root.find("ul.children").append(li);
                }
                else if (root.hasClass("c-level-0")) {
                    console.log("0")
                    var li = "<li class='comment c-level-1'><p id='comment_id' hidden>" + dataserver.id + "</p><div class='vcard bio'><img src='/static/images/person_1.jpg' alt='Image placeholder'></div><div class='comment-body'><h3>" + replace_quotes(dataserver.author_username) + "</h3><div class='meta mb-3'>" + format_date(dataserver.created_at) + "</div><p>" + replace_quotes(dataserver.content) + "</p><a class='replycm'>"+ gettext("Reply")+"</a></div><ul class='children'></ul></li>";
                    root.find("ul.children").append(li);
                }

                $("#replyCommentForm").remove();
            }
        });
    })
})

var data;

const preload_comments = (id) => {
    $.ajax("/blog/load_comments/post=" + id, {
        success: function (dataserver, status, xhr) {
            comments_count = dataserver.slice(-1)[0]
            if (comments_count > 1) {
                document.getElementById("comments_count").innerText = comments_count + " " + gettext("Comments")
            }
            else if (comments_count == 1) {
                document.getElementById("comments_count").innerText = comments_count + " " + gettext("Comment")
            }
            dataserver.pop()
            data = dataserver.reverse();
            loadComment();
        }
    })
}

// const load_recent_posts = (id) => {
//     $.ajax("/blog/load_comments/post=" + id, {
//         success: function (dataserver, status, xhr) {
//             data = dataserver.reverse();
//             loadComment();
//         }
//     })
// }

function load_recent_posts () {
    var post_id = document.getElementById("post_id").innerText;
    var random = 3;
    var dataString = '{ "random":"' + random + '",' +
        '"except":"' + post_id + '"}';

    $.ajax({
        type: "POST",
        url: "/en/blog/get_recent_posts",
        contentType: 'application/json',
        data: dataString,
        success: function (dataserver, status, xhr) {
            var div = ""
            for (post of dataserver) {
                div +=   '<div class="block-21 mb-4 d-flex">' +
                            '<a class="blog-img mr-4" style="background-image: url( /static/images/image_1.jpg );"></a>' +
                            '<div class="text" style="position: relative;">' +
                                '<h3 class="heading"><a href="/blog/post/' + post.id + '">' + post.title + '</a></h3>' +
                                '<div class="meta" style="position: absolute; bottom: 0px;">' +
                                    '<div><a href="#"><span class="icon-calendar"></span>' + format_date(post.date) + '</a></div>' +
                                    '<div><a href="#"><span class="icon-chat"></span>' + post.number_comments + '</a></div>' +
                                '</div>' +
                            '</div>' +
                        '</div>'             
            }
            document.getElementById("side_bar_recents").innerHTML += div;
            
        }
    });
};

var start = 0;
var stop = 1;

var loadComment = () => {
    // alert(data.length);
    // var max = 1;
    // var len = document.getElementById('commentList').childElementCount;
    // var viewMoreCommentsButton = document.getElementById("viewMoreComment");

    for (start; start < data.length; start++) {
        if (start <= stop) {
            parent = data[start];
            document.getElementById('commentList').innerHTML += render_group_comment(parent);
        } else {
            // start = stop;
            stop += 2;
            break;
        }
    }
    if (start == data.length) {
        // $('#viewMoreComment').remove();
        document.getElementById("viewMoreComment").style.display = "none";
    }
    else {
        document.getElementById("viewMoreComment").style.display = "block";
    }
}

function render_group_comment(parent) {
    var li = "<li class='comment root-comment c-level-0'>";
    li += "<p id='comment_id' hidden>" + parent.id + "</p><div class='vcard bio'></div><div class='comment-body'><h3>" + replace_quotes(parent.author_username) + "</h3><div class='meta mb-3'>" + format_date(parent.created_at) + add_flag(parent.flag) + "</div><p>" + replace_quotes(parent.content) + "</p><a class='replycm'>"+gettext("Reply")+"</a></div>"
    var children = parent.children;
    if (children) {
        li += "<ul class='children'>";
        for (index in children) {
            var child = children[index];
            li += "<li class='comment c-level-1'><p id='comment_id' hidden>" + child.id + "</p><div class='vcard bio'></div><div class='comment-body'><h3>" + replace_quotes(child.author_username) + "</h3><div class='meta mb-3'>" + format_date(child.created_at) + "</div><p>" + replace_quotes(child.content) + "</p><a class='replycm'>"+gettext("Reply")+"</a></div></li>";

            var children2 = child.children;
            if (children2) {
                li += "<ul class='children'>";
                for (index2 in children2) {
                    var child2 = children2[index2];
                    li += "<li class='comment c-level-2'><p id='comment_id' hidden>" + child2.id + "</p><div class='vcard bio'></div><div class='comment-body'><h3>" + replace_quotes(child2.author_username) + "</h3><div class='meta mb-3'>" + format_date(child2.created_at) + "</div><p>" + replace_quotes(child2.content) + "</p><a class='replycm'>"+gettext("Reply")+"</a></div></li>";
                }
                li += "</ul>";
            }
            else {
                li += "<ul class='children'></ul>"
            }
        }
        li += "</ul>";
    }
    else {
        li += "<ul class='children'></ul>"
    }
    li += "</li>";
    return li;
}

function format_date(date) {
    // lang = gettext("en")
    // if (lang == "vi") {
    //     console.log("yes")
    // }
    return date.month + ". " + date.day + ", " + date.year + ", " + date.hour + ":" + date.minute + " " + date["AM-PM"]
    // return Nov. 17, 2020, 2:47 p.m.
}

function add_flag(is_flagged) {
    if (is_flagged) {
        return '<i style="position: relative; left:10px; color: red;" class="fas fa-flag"></i><span style="position: relative; left:15px;">'+ gettext("WARNING")+'</span>'
    }
    else {
        return ""
    }
}

function replace_quotes(raw_string) {
    result = raw_string.replaceAll("'", '"');
    return result;
}

function standardize_request(raw_string) {
    return raw_string.replaceAll('"', "'").replaceAll("\\", "\\\\")
}

var username;
function is_logged_in() {
    $.ajax({
        type: "GET",
        url: "/en/accounts/user/",
        async: false,
        success: function (dataserver) {
            username = dataserver;
        }
    });
}

function init_comment_func() {
    if(username) {
        var html =  '<button class="btn" data-toggle="collapse" data-target="#leaveCommentForm" style="padding:0;" ><h3>'+gettext("Leave a comment")+'</h3></button>' +
                    '<form id="leaveCommentForm" class="p-5 bg-light collapse">' +
                        '<div class="form-group">' +
                            '<label for="name">'+gettext("Name")+' *</label>' +
                            '<input type="text" class="form-control" id="name" value="' + username + '" readonly required>' +
                        '</div>' +
                        '<div class="form-group">' +
                            '<label for="message">'+ gettext("Message")+' *</label>' +
                            '<textarea name="" id="message" cols="30" rows="10" class="form-control" required></textarea>' +
                        '</div>' +
                        '<div class="form-group">' +
                            '<button type="button" class="btn py-3 px-4 btn-primary">'+gettext("Post Comment")+'</button>' +
                        '</div>' +
                    '</form>'

        
    }
    else {
        var html = '<h3><a href="/en/accounts/login/">'+gettext("Login")+'</a> '+gettext("to leave comments")+'</h3>'
    };
    document.getElementById("commentContainer").innerHTML += html
}


$(document).ready(function () {
    is_logged_in();
    var post_id = document.getElementById("post_id").innerText;
    document.getElementById("viewMoreComment").style.display = "none";
    preload_comments(post_id);
    load_recent_posts();
    init_comment_func();
})

window.onload = function () {
    var ps = document.getElementsByClassName("content");
    for (p of ps) { p.innerHTML = p.textContent }
}


let content_editor
function createPost() {
    let category = document.getElementById("category").value
    let title = document.getElementById("post-title").value
    let content = content_editor.getData();
    let thumbnail = thumbnail_editor.getData();
    if (thumbnail) {
        let re = /src=(\"|\')(.*)(\"|\')/g
        thumbnail = re.exec(thumbnail)[2]
    }

    let dataString = '{ "category":"' + category + '",' +
        '"title":"' + standardize_request(title) + '",' +
        '"content":"' + standardize_request(content) + '",' +
        '"thumbnail":"' + standardize_request(thumbnail) + '"' +
        '}';

    $.ajax({
        type: "POST",
        url: "/en/blog/admin/post/create/",
        contentType: 'application/json',
        data: dataString,
        success: function (dataserver) {
            if (document.getElementById("notification")) {
                document.getElementById("notification").remove()
            }
            section = document.getElementsByClassName("ftco-section")[0].innerHTML
            section = '<div id="notification" style="border: 1px;"><p>Post "'+ dataserver.title + '" is created. Click <a href=/en/blog/admin/post/update/'+ dataserver.id +'>here</a> to edit.</p></div>' + section;
            document.getElementsByClassName("ftco-section")[0].innerHTML = section
        }
    });
};

InlineEditor
    .create(document.querySelector('#content-editor'), {
        toolbar: [ 'heading', '|', 'bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote', 'code', 'codeBlock', "imageInsert",],
    heading: {
        options: [
            { model: 'paragraph', title: 'Paragraph', class: 'ck-heading_paragraph' },
            { model: 'heading1', view: 'h1', title: 'Heading 1', class: 'ck-heading_heading1' },
            { model: 'heading2', view: 'h2', title: 'Heading 2', class: 'ck-heading_heading2' }
        ]
    }
    })
    .then(newEditor => {
        content_editor = newEditor;
    })
    .catch(error => {
        console.error(error);
    });

InlineEditor
    .create(document.querySelector('#thumbnail-editor'), {
        toolbar: ["imageInsert"],
    })
    .then(newEditor => {
        thumbnail_editor = newEditor;
    })
    .catch(error => {
        console.error(error);
    });


function updatePost() {
    let category = document.getElementById("category").value
    let title = document.getElementById("post-title").value
    let content = content_editor.getData();
    let thumbnail = thumbnail_editor.getData();
    if (thumbnail) {
        let re = /src=(\"|\')(.*)(\"|\')/g
        thumbnail = re.exec(thumbnail)[2]
    }
    let dataString = '{ "category":"' + category + '",' +
        '"title":"' + standardize_request(title) + '",' +
        '"content":"' + standardize_request(content) + '",' +
        '"thumbnail":"' + standardize_request(thumbnail) + '"' +
        '}';

    let id = document.getElementById("post-id").innerHTML;
    let url = "/en/blog/admin/post/update/" + id;

    $.ajax({
        type: "POST",
        url: url,
        contentType: 'application/json',
        data: dataString,
        success: function (dataserver) {
            if (document.getElementById("notification")) {
                document.getElementById("notification").remove()
            }
            section = document.getElementsByClassName("ftco-section")[0].innerHTML
            section = '<div id="notification" style="border: 1px;"><p>Post is updated.</p>' + section;
            document.getElementsByClassName("ftco-section")[0].innerHTML = section
        }
    });
};

$("#profile-form").submit(function(e) {
    var username = document.getElementById("uname").value;
    var first = document.getElementById("fname").value;
    var last = document.getElementById("lname").value;
    var email = document.getElementById("email").value;
    var dataString =    '{ "username":"' + standardize_request(username) + '",' +
                        '"first_name":"' + standardize_request(first) + '",' +
                        '"last_name":"' + standardize_request(last) + '",' +
                        '"email":"' + standardize_request(email) + '"}';

    $.ajax({
        type: "POST",
        url: "/en/accounts/profile/",
        contentType: 'application/json',
        data: dataString,
        success: function (dataserver, status, xhr) {
            if (document.getElementById("notification")) {
                document.getElementById("notification").remove()
            }
            if (dataserver.message) {
                form = document.getElementById("profile-form").innerHTML
                form = "<p id='notification' style='color:red;'>"+dataserver.message+"</p>" + form
                document.getElementById("profile-form").innerHTML = form
            }
            else {
                form = document.getElementById("profile-form").innerHTML
                form = "<p id='notification' style='color:green;'>Update account successfully!</p>" + form
                document.getElementById("profile-form").innerHTML = form
            }
        }
    });

    e.preventDefault();
});