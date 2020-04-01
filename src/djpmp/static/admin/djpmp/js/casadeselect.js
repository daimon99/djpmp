// 两个字段级联选择的示意代码

var coaChoices = {
    'common': [null],
    '销售费用': [
        '车辆费',
        '市内交通',
        '差旅费',
        '招待费',
        '运营费',
        '运输费',
        '其它费用'
    ],
    '销售成本': [
        '材料（13%税率专票）',
        '材料（普票）',
        '服务费（6%税率专票）',
        '工程费（9%税率专票）',
        '维修费（13%税率专票）',
        '工程费（3%税率专票）',
        '其他成本'
    ]
};

$(document).ready(function () {
    $.fn.coaPopulate = function (category) {
        let eleCoa = this;
        let current = $(eleCoa).val();
        $(eleCoa).empty();
        let choices = coaChoices['common'];
        if (coaChoices[category]) choices = choices.concat(coaChoices[category]);
        $.each(choices, function (index, value) {
            if (!!value) {
                $(eleCoa).append('<option value="' + value + '">' + value + '</option>')
            } else {
                $(eleCoa).append('<option value' + '">---------</option>')
            }

        });
        if (coaChoices[category]) {
            if (coaChoices[category].indexOf(current) < 0) {
                $(eleCoa).children().first().attr('selected', true);
            } else {
                $(eleCoa).val(current);
            }
        } else {
            $(eleCoa).children().first().attr('selected', true);
        }
    };


    $(document).on('category', function (e) {
        console.log(e);
        let category_selected = e.target.value;
        let prefix = e.target.dataset.prefix;
        let target = '#' + e.target.id.replace('category', 'coa');
        $(target).coaPopulate(category_selected);
    });

    function init() {
        // console.log('-->', $('select[id$="category"]').html());
        $('select[id$="category"]').trigger('change');
    }

    init()

});
