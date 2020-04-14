# coding: utf-8
from functools import reduce

from .. import models as m


def assign_hr_cost_to_wbs(qs):
    """
    分配 hr dataset 到 wbs 任务上
    :param qs: hrcalendar dataset
    :return:
    """

    # 赋值 tasks_memo
    for i in qs:
        i.save()
    # pv按比例分配到wbs上
    task_calc_started = set()
    m.WBS.objects.update(ev=0)
    for calendar in qs:
        tasks = calendar.tasks.all()
        total_pv = reduce(lambda x, y: x + y.pv, tasks, 0)
        for task in tasks:
            if task.pk not in task_calc_started:
                task.ev = 0
                task_calc_started.add(task.pk)
            task.ev += round(calendar.ev * task.pv / total_pv, 2)
            task.save()
    # 以下是算法 1 .　不够精细。只能算出顶层 ev
    if False:
        # wbs pv 累加
        for root in m.WBS.objects.root_nodes():
            root: m.WBS
            root.ev = reduce(lambda x, y: x + y.ev, root.get_descendants(True), 0)
            root.save()

    # 算法 1 结束
    # 算法2，先向下拆，再向上合
    def go_down(node: m.WBS):
        if node.ev == 0:
            if node.is_leaf_node():
                return
            else:
                for child in node.get_children():
                    go_down(child)
        else:
            children = node.get_children()
            total_pv2 = reduce(lambda x, y: x + y.pv, children, 0)
            for child in children:
                child.ev += round(node.ev * child.pv / total_pv2, 2)
                child.save()
                if child.is_leaf_node():
                    continue
                else:
                    go_down(child)

    # 自上至下拆分
    for root in m.WBS.objects.root_nodes():
        go_down(root)
    # 自下至上合并
    for node in m.WBS.objects.filter(children__isnull=False).all():
        node: m.WBS
        node.ev = round(reduce(lambda x, y: x + y.ev, node.get_leafnodes(), 0), 2)
        node.save()
