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
var goto_top_type = -1;  
var goto_top_itv = 0;  
  
function goto_top_timer() {  
    var y = goto_top_type == 1 ? document.documentElement.scrollTop  
            : document.body.scrollTop;  
    var moveby = 15;  
    y -= Math.ceil(y * moveby / 100);  
    if (y < 0) {  
        y = 0;  
    }  
    if (goto_top_type == 1) {  
        document.documentElement.scrollTop = y;  
    } else {  
        document.body.scrollTop = y;  
    }  
    if (y == 0) {  
        clearInterval(goto_top_itv);  
        goto_top_itv = 0;  
    }  
}  
  
function goto_top() {  
    if (goto_top_itv == 0) {  
        if (document.documentElement && document.documentElement.scrollTop) {  
            goto_top_type = 1;  
        } else if (document.body && document.body.scrollTop) {  
            goto_top_type = 2;  
        } else {  
            goto_top_type = 0;  
        }  
        if (goto_top_type > 0) {  
            goto_top_itv = setInterval('goto_top_timer()', 50);  
        }  
    }  
} 
function switchtag(a){
    $(".divforums").hide();
    $("#"+a).slideDown("slow");
}