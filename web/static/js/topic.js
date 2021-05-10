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
        $("#reply_list_"+id).toggle(function(){
            if ($('#replyshow'+id).text() == '收起回复'){
                $('#replyshow'+id).text('回复');
            }
            else{
                $('#replyshow'+id).text('收起回复');
            }
		});
        $('.comment_id').val(0);
        var name = $('#owner_'+id).text();
        name = '回复:' + name;
        $('#comment_name_'+id).text(name);
}

function replyShowmore(id){
    $(".reply_form_"+id).toggle();
    $(".replyShowmore_"+id).toggle();  
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
            var obj = $('#floorGreat_'+id);
            obj.children().attr("style","color: rgb(52,92,161)");
            obj.attr("onclick","unfloorGreat(" +id + ")");
            var nb = $('#nb_'+id).text();
            nb = parseInt(nb) + 1;
            $('#nb_'+id).text(nb);
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
                var obj = $('#floorGreat_'+id);
                obj.children().attr("style","color: rgb(136,136,136);");
                obj.attr("onclick","floorGreat(" +id + ")");
                var nb = $('#nb_'+id).text();
                nb = parseInt(nb) - 1;
                $('#nb_'+id).text(nb);
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
    var flag = confirm("您真的确定要置顶吗？")
    if(flag){
      $.ajax({
          url: '/top/',
          type: "POST",
          data: {id:id},
          dataType: "JSON",
          success: function (res) {
              if(res.status){
              $('#top').text("取消置顶");
              href = "unTob(" + id + ");";
              $('#top').attr("onclick","").click(function(){unTop(id)});
              }
          }
      })
    }
  }
  function unTop(id) {
    var flag = confirm("您真的确定要取消置顶吗？")
    if(flag){
      $.ajax({
          url: '/untop/',
          type: "POST",
          data: {id:id},
          dataType: "JSON",
          success: function (res) {
              if(res.status){
              $('#top').text("置顶");
              href = "Tob(" + id + ");";
              $('#top').attr("onclick","").click(function(){Top(id)});
              }
          }
      })
    }
  }
  function Refined(id) {
    var flag = confirm("您真的确定要加精吗？")
    if(flag){
      $.ajax({
          url: '/refined/',
          type: "POST",
          data: {id:id},
          dataType: "JSON",
          success: function (res) {
              if(res.status){
              $('#refined').text("取消加精");
              href = "unRefined(" + id+ ");";
              $('#refined').attr("onclick","").click(function(){unRefined(id)});
              }
          }
      })
    }
  }
  function unRefined(id) {
    var flag = confirm("您真的确定要取消加精吗？")
    if(flag){
      $.ajax({
          url: '/unrefined/',
          type: "POST",
          data: {id:id},
          dataType: "JSON",
          success: function (res) {
              if(res.status){
              $('#refined').text("加精");
              href = "Refined(" + id+ ");";
              $('#refined').attr("onclick","").click(function(){Refined(id)});
              }
          }
      })
    }
  }