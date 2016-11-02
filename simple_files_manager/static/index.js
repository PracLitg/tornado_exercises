$(document).ready(function() {
    $("#upload_button").click(function() {
        $.ajax({
            url: "/catalog",
            type: "post",
            cache: false,
            data: new FormData($('#upload_form')[0]),
            processData: false,
            contentType: false,
        }).done(function() {
            alert("Success");
        });
    });

    $("#download").click(function() {
        checked_file = $("input[name='checked_file']")
        displayed_links = $("a[name='file_link']")
        len = checked_file.length
        for (i=0; i<len; i++) {
            if (checked_file[i].checked) {
                var link = $(displayed_links[i]).text()
                //alert(link.length)
                var url_link = $(displayed_links[i]).attr("href").slice(8)
                //var url_link1 = url_link.slice[8]
                if (link.charAt(link.length-1)!='/') {
                    var form = $("<form>")
                    form.attr("style", "display:none")
                    form.attr("target", "")
                    form.attr("method", "post")
                    form.attr("action", "file_download" + url_link)
                    $("body").append(form)
                    form.submit()
                    form.remove()
                } else {
                    alert("A File Should Be Chosen")
                }
            }
        }
    });
});
