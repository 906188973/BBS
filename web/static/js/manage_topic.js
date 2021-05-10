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
(function(){   
    var oDiv=document.getElementById("float");   
    var H=0,iE6;   
    var Y=oDiv;   
    while(Y){H+=Y.offsetTop;Y=Y.offsetParent};   
    iE6=window.ActiveXObject&&!window.XMLHttpRequest;   
    if(!iE6){   
        window.onscroll=function()   
        {   
            var s=document.body.scrollTop||document.documentElement.scrollTop;   
            if(s>H){oDiv.className="div1 div2";if(iE6){oDiv.style.top=(s-H)+"px";}}   
            else{oDiv.className="div1";}       
        };   
    }   
})(); 
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
            $('#top_'+id).text("Ture");
            href = "unTob(" + id + ");";
            $('#top_'+id).attr("onclick","").click(function(){unTop(id)});
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
            $('#top_'+ id).text("False");
            href = "Tob(" + id + ");";
            $('#top_'+id).attr("onclick","").click(function(){Top(id)});
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
            $('#refined_'+id).text("Ture");
            href = "unRefined(" + id+ ");";
            $('#refined_'+id).attr("onclick","").click(function(){unRefined(id)});
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
            $('#refined_'+id).text("False");
            href = "Refined(" + id+ ");";
            $('#refined_'+id).attr("onclick","").click(function(){Refined(id)});
            }
        }
    })
  }
}