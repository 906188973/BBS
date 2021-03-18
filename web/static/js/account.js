
function topicDel(id) {
    var flag = confirm("您确定要删除您的回复吗？")
    if (flag) {
        var pk = id
        var url = '/topic_del/' + pk + '/'
        $.ajax({
            url: url,
            type: "POST",
            success: function (res) {
                if(res.status){
                $('#topic_'+id).remove();
                }
            }
        })
    }
}
 function unConcerned(id) {
    var pk = id
    var url = '/unconcerned/' + pk + '/'
    $.ajax({
        url: url,
        type: "POST",
        success: function (res) {
            if(res.status){
            $('#concerned_'+id).remove();
            }
        }
    })
}
function unCollect(id) {
    var pk = id
    var url = '/uncollect/' + pk + '/'
    $.ajax({
        url: url,
        type: "POST",
        success: function (res) {
            if(res.status){
            $('#collect_'+id).remove();
            }
        }
    })
}