function Submit(id){
    var url = '/change_power/' + id + '/';
    var a = $('#lcomuli option:selected').val();
    console.log(a) ;
    $.ajax({
        url: url,
        type: "POST",
        data: {value: a},
        dataType: "JSON",
        success:function (res) {
         if(res.status){
             location.href = location.href;
            }
        }
    })
}
function moderator(id){
    var url = '/moderator/' + id + '/';
    var a = $('#lcomuli option:selected').val();
    console.log(a) ;
    $.ajax({
        url: url,
        type: "POST",
        data: {value: a},
        dataType: "JSON",
        success:function (res) {
         if(res.status){
             location.href = location.href;
            }
        }
    })
}