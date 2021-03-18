function Concerned(id) {
    var pk = id
    var url = '/concerned/' + pk + '/'
    $.ajax({
        url: url,
        type: "POST",
        success: function (res) {
            if(res.status){
            $('#concerned_'+id).text("取消关注");
            var script = 'javascript:unConcerned(' + pk + ');'
            }
        }
    })
}
function unConcerned(id) {
    var pk = id
    var url = '/unconcerned/' + pk + '/'
    $.ajax({
        url: url,
        type: "POST",
        success: function (res) {
            if(res.status){
            $('#concerned_'+id).text("关注");
            var script = 'javascript:Concerned(' + pk + ');'
            $('#concerned_'+id).attr("href",script);
            $('#user_concerned_'+id).remove();
            }
        }
    })
}