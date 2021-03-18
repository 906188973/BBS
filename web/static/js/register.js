$(function (){
    bindClickBtnSms();
    bindClickSubmit();
});
function bindClickBtnSms() {
    $('#btnSms').click(function() {
        $('.error-msg').empty();
        var mobilePhone = $('#id_mobile_phone').val();
        $.ajax({
            url:"{% url 'web:send_sms' %}",
            type:'GET',
            data:{mobile_phone: mobilePhone, tpl: "register"},
            dataType: "JSON",
            success:function(res) {
                if (res.status){
                    sendSmsRemind();
                }else{
                    $.each(res.error, function (key,value){
                        $("#id_" + key).next().text(value[0]);
                    })
                }
            }
        })
    })
}
function sendSmsRemind() {
    var $smsBtn = $('#btnSms');
    $smsBtn.prop('disabled', true);

    var time = 60;
    var remind = setInterval(function () {
        $smsBtn.val(time + '秒重新发送');
        time = time - 1;
        if (time < 1) {
            clearInterval(remind);
            $smsBtn.val('点击获取验证码').prop('disabled', false);
        }
    }, 1000)
}
function bindClickSubmit() {
    $('#btnSubmit').click(function (){
        $('.error-msg').empty();
        $.ajax({
            url:"{% url 'web:register' %}",
            type:"POST",
            data:$('#regForm').serialize(),
            dataType:"JSON",
            success:function (res) {
                if(res.status){
                    location.href =res.data;
                }else{
                    $.each(res.error, function(key, value){
                        $("#id_" +key).next().text(value[0]);
                    })
                }
            }
        })
    })
}