/**
 * 计算输入字段的合计金额
 *
 * 示例：calcTotal('input', 'PV', '.field-pv input', '.column-pv')
 *
 * @param tag: 如果是 input 类，就输入 input，如果是 只读字段，就输入 p
 * @param name
 * @param field_class
 * @param columnClass
 */
function calcTotal(tag, name, field_class, columnClass) {
    var total = 0.0;
    $(field_class).each(function (index) {
        var value = 0;
        if (tag === "input") {
            value = parseFloat($(this).val())
        } else {
            value = parseFloat($(this).html())
        }
        if (!isNaN(value)) total += value
    });
    total = total.toFixed(2)
    console.log('total', name, total)
    var rowTemplate = "<div style='font-weight: 300; font-size: 12px; width: 100%;display: flex'><span style='width: 60px;'>$name$</span><span style='text-align: right; width: 60%'>$value$</span></div>";
    var output = "<div style='width: 100%'>";
    output += rowTemplate.replace('$name$', '合计').replace('$value$', total);
    output += "</div>";

    // 下面是需要加 button 的时候的代码
    // template2 = "<button type='button' onclick='calcTotal(\"$tag$\", \"$name$\", \"$field$\", \"$column$\")'>合计</button>";
    // $(columnClass).html(name + template2.replace('$tag$', tag).replace('$name$', name).replace('$field$', field_class).replace('$column$', columnClass) + output);
    $(columnClass).html(name + output);
}
