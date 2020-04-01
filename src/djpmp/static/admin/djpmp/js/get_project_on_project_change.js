// 根据输入动态展示内容的示例代码

$(document).ready(function () {
    on_project_selected();
});

function on_project_selected() {
    django.jQuery('#id_project').on('change', function (e) {
        var project_id_selected = e.target.value;
        if (project_id_selected) {
            $.get(`/api/v1/pm/project/${project_id_selected}`).done(function (e) {
                $('.field-_project_code > div').html(e.code)
            })
        } else {
            // clear project info
            $('.field-_project_code > div').html('-')
        }
    })
}
