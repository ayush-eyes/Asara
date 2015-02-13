$(function(){
    $('#chat_msg').keyup(function(e) {
            var code=e.which || e.keyCode;
            if(code == 13)        {
            var msg=$('#chat_msg').val();
            $('#chat_msg').val("");
        $.ajax({
            type: "POST",
            url:"/rango/chat/",
            data: {
                'chat_message': msg,
                'project_id': $('#project_id').val(),
                'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()

            },
            success: searchSuccess1,
            dataType:'html'
        });
        }
    });
});

function searchSuccess1(data,textStatus,jqXHR)
{
        //$('#chat_msg').val("");
}
