$(function(){
    $('#add_people').keyup(function() {
        $.ajax({
            type: "GET",
            url:"/rango/task_add_people/",
            data: {
                'task_add_people': $('#add_people').val(),
                'task_id':$('#curr_task').val(),
                'project_id':$('#curr_proj').val()
                
            },
            success: searchSuccess2,
            dataType:'html'
        });
    });
});
function searchSuccess2(data,textStatus,jqXHR)
{
    $('#task_members').html(data);
}