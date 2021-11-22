;
var member_reg_ops = {
    init:function () {
        this.eventBind()
    },
    eventBind:function () {
        $(".reg-wrap .do-reg").click(function () {
            // 增加不能重复点击
            var btn_target = $(this);
            if(btn_target.hasClass("disabled")){
                common_ops.alert("正在处理，请稍后。。。");
                return;
            }

            var login_name = $(".reg-wrap input[name=login_name]").val()
            var login_pwd = $(".reg-wrap input[name=login_pwd]").val()
            var login_pwd2 = $(".reg-wrap input[name=login_pwd2]").val()
            var nickname = $(".reg-wrap input[name=nickname]").val()
            // alert(login_name + login_pwd + login_pwd2)
            if (login_name == undefined || login_name.length < 1){
                common_ops.alert("用户名不能为空");
                return;
            };
            if (login_pwd == undefined || login_pwd.length < 6){
                common_ops.alert("密码不能为空并且不能小于6个字符");
                return;
            };
            if (login_pwd2 == undefined || login_pwd2 != login_pwd){
                common_ops.alert("确认密码不正确");
                return;
            };
            btn_target.addClass("disabled");
            $.ajax({
                url:common_ops.buildUrl("/member/reg"),
                type:"POST",
                data:{
                    login_name:login_name,
                    login_pwd:login_pwd,
                    login_pwd2:login_pwd2,
                    nickname:nickname
                },
                dataType:"json",
                success:function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200){
                        callback = function(){
                            window.location.href = common_ops.buildUrl("/");
                        }
                    };
                    common_ops.alert(res.msg, callback);
                },
                error:function (res) {
                    btn_target.removeClass("disabled");
                }
            });
        });
    }
};

$(document).ready(function () {
    member_reg_ops.init();
});


