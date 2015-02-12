$(function(){
    $('#search1').keyup(function() {
        $.ajax({
            type: "POST",
            url:"/rango/search/",
            data: {
                'search_text': $('#search1').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                
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