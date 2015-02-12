$(function(){
    $('#search').keyup(function() {
        $.ajax({
            type: "GET",
            url:"/rango/user_search/",
            data: {
                'user_search_text': $('#search').val(),
                'project_id':$('#curr_project').val()
            },
            success: searchSuccess,
            dataType:'html'
        });
    });
});
function searchSuccess(data,textStatus,jqXHR)
{
    $('#search-results').html(data);
}