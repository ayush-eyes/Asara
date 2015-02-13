function refresh() {
    $.ajax({
            type: "POST",
        url: '/rango/chatrefresh/',
        data: {
            'project_id': $('#project_id').val(),
            'user_username': $('#user_username').val(),
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function(data) {
            $('#discussions').html(data);
            $('#discussions').scrollTop($('#discussions')[0].scrollHeight);
        }
    });
}

$(function(){
    refresh();
    setInterval("refresh()", 2000);
});
