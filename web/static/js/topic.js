function replySubmit(id){
    $.ajax({
        url:"/update_comment/",
        type:"POST",
        data:$('#replyForm_'+id).serialize(),
        dataType:"JSON",
        success:function (res) {
            if(res.status){
                if(res.owner_status){
                    var comment_html = '<div id="reply_' + res.reply_id + '"><span>' + res.username +
                                 ':回复' + res.by_owner
                }else{
                    var comment_html = '<div id="reply_' + res.reply_id + '"><span>' + res.username
                    }
                var comment_html = comment_html + '</span><span> (' + res.comment_time + 
                    '):</span><div><span>' + res.text + '</span><a >回复</a><a href="javascript:replyDel(' +
                    res.reply_id + ');"> 删除</a></div></div>';
                $(".reply_list_"+id).append(comment_html);
            }else{
                   console.log('error');
            }
        }
    })
    $('#reply_text_'+id).val('');
}
function reply(replyid, floorid){
        $('.comment_id').val(replyid);
        var name = $('#replyowner_'+replyid).text();
        name = '回复:' + name;
        $('#comment_name_'+floorid).text(name);
}
function replyShow(id){
        $("#reply_form_"+id).toggle(function(){
            if ($('#replyshow'+id).text() == '回复'){
                $('#replyshow'+id).text('收起回复');
            }
            else{
                $('#replyshow'+id).text('回复');
            }
		});
        $('.comment_id').val(0);
        var name = $('#owner_'+id).text();
        name = '回复:' + name;
        $('#comment_name_'+id).text(name);
}


function floorDel(id) {
    var flag = confirm("您真的确定要删除吗？")
    if (flag) {
        var pk = id
        var url = '/floor_del/' + pk + '/'
        $.ajax({
            url: url,
            type: "POST",
            success: function (res) {
                if(res.status){
                $('#floor_'+id).remove()
                }
            }
        })
    }
}
function replyDel(id) {
    var flag = confirm("您确定要删除您的回复吗？")
    if (flag) {
        var pk = id
        var url = '/comment_del/' + pk + '/'
        $.ajax({
            url: url,
            type: "POST",
            success: function (res) {
            if(res.status){
                $('#reply_'+id).remove()
            }
            }
        })
    }
}

function Collect(id) {
    var pk = id
    var url = '/collect/' + pk + '/'
    $.ajax({
        url: url,
        type: "POST",
        success: function (res) {
            if(res.status){
            $('#collect_'+id).text("取消收藏");
            var script = 'javascript:unCollect(' + pk + ');'
            $('#collect_'+id).attr("href",script);
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
            $('#collect_'+id).text("收藏");
            var script = 'javascript:Collect(' + pk + ');'
            $('#collect_'+id).attr("href",script);
            }
        }
    })
}
function floorGreat(id) {
    var pk = id
    var url = '/floor_great/' + pk + '/'
    $.ajax({
        url: url,
        type: "POST",
        success: function (res) {
            if(res.status){
            $('#floorGreat_'+id).text("已点赞");
            }
        }
    })
}
function unfloorGreat(id) {
    var pk = id
    var url = '/unfloor_great/' + pk + '/'
    $.ajax({
        url: url,
        type: "POST",
        success: function (res) {
            if(res.status){
            $('#unfloorGreat_'+id).remove();
            }
        }
    })
}
function commentGreat(id) {
    var pk = id
    var url = '/comment_great/' + pk + '/'
    $.ajax({
        url: url,
        type: "POST",
        success: function (res) {
            if(res.status){
            $('#commentGreat_'+id).text("点赞");
            }
        }
    })
}
function uncommentGreat(id) {
    var pk = id
    var url = '/uncomment_great/' + pk + '/'
    $.ajax({
        url: url,
        type: "POST",
        success: function (res) {
            if(res.status){
            $('#uncommentGreat_'+id).remove();
            }
        }
    })
}
function Top(id) {
    var pk = id
    $.ajax({
        url: '/top/',
        type: "POST",
        data: {id:pk},
        dataType: "JSON",
        success: function (res) {
            if(res.status){
            $('#top').text("取消置顶");
            href = "javascript:unTob(" + pk+ ");";
            $('#top').attr("href",href);
            }
        }
    })
}
function unTop(id) {
    var pk = id
    $.ajax({
        url: '/untop/',
        type: "POST",
        data: {id:pk},
        dataType: "JSON",
        success: function (res) {
            if(res.status){
            $('#top').text("置顶");
            href = "javascript:Tob(" + pk+ ");";
            $('#top').attr("href",href);
            }
        }
    })
}
function Refined(id) {
    var pk = id
    $.ajax({
        url: '/refined/',
        type: "POST",
        data: {id:pk},
        dataType: "JSON",
        success: function (res) {
            if(res.status){
            $('#refined').text("取消加精");
            href = "javascript:unRefined(" + pk+ ");";
            $('#refined').attr("href",href);
            }
        }
    })
}
function unRefined(id) {
    var pk = id
    $.ajax({
        url: '/unrefined/',
        type: "POST",
        data: {id:pk},
        dataType: "JSON",
        success: function (res) {
            if(res.status){
            $('#refined').text("加精");
            href = "javascript:Refined(" + pk+ ");";
            $('#refined').attr("href",href);
            }
        }
    })
}