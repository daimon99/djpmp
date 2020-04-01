// 根据选项动态显示内容的示例代码

$(document).ready(function () {
    on_project_status();
});


function on_project_status() {
    var close_on = $('#id_project_status').val()
    if (close_on !== '已结项') {
        $('.field-close_memo').hide();
    }

    $("#id_project_status").change(function (e) {
        var selected = e.target.value;
        if (selected === '已结项') {
            $('.field-close_memo').show();
        } else {
            $('.field-close_memo').hide();
        }
    })
}
