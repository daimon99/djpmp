# 项目挣值估算工具

## 使用说明

在做软件开发外包工作时，实际的人工投入，是报价的依据。但人工投入不易估算。也非常受客户配合度的影响。

但在初始报价时，在需求、配合不明确的情况下，又必须给出计划人工，以给出报价。

因此在实际操作中，往往先估算一个略偏高的工时，之后再商定，以实际投入为准。

此工具就是辅助这一流程，以PMP 为核心思想，最大程度裁剪后的挣值估算工具。

## 特点

* 人力资源投入，可以根据投入的项目，自动按比例，把每人每天的投入，映射到 WBS 的任务上

### 使用方法：

1. 建项目：新建一个 `项目`
2. 建任务：在 `wbs` 中创建 `WBS`，这时只需要输入任务名
3. 建任务层次结构：在 `wbs` 列表页中，调整 `wbs任务` 的分解结构
4. 估算任务计划工时：在 `wbs` 中，估算每个 `明细任务`(没有子节点的任务），估算需要投入的 `计划工时`（即 `PV`），然后再点击 `计算父节点PV`, 自动可计算出父节点的PV
4. 做人力资源计划：在 `员工` 中，创建项目相关人力资源
5. 记录人力资源实际投入：在 `资源日历` 中, 记录人力资源的真实使用情况，以及每投入对应的 `wbs 任务`。注意，资源的使用，以 `半日` 为最小单位。一天最多可以有 4 个 `半日` 的投入。报价上，两个 `半日` 为一工作日
6. 计算任务挣值：在 `资源日历` 中，点击 `计算挣值`，更新 `wbs` 中的 `挣值`（即 `EV`）。这里会以任务的PV 为基础，按比例分配 EV
7. 在 `资源日历` 中，浏览 各项任务及合计 的 PV / EV / SPI

### 名词解释：

* pv: 计划工时
* ev: 挣值。实际完成的工作量
* ac: 实际成功。完成工作所实际花费的工时。为简化挣值管理模型，也为便于报价，这里假定：`ac = ev`
* spi: 进度绩效指数。截止到某时点衡量进度绩效的一种指标，也就是实际完成的工作量与计划完成工作量之比，SPI=EV/PV


## 安装

### 环境要求

* python 3.6 以上
* 最好 mac 或 linux 环境

### 安装说明

```
git clone https://github.com/daimon99/djpmp
cd djpmp
make init
make upgrade
python src/manage.py createsuperuser # 创建超级账户
make run
```

之后打开浏览器，访问 http://localhost:9091/admin 即可。

## FAQ

1. pycharm debug 失败

注意跟下代码。一般来讲如果代码中引入：eventlet.monkey_patch()，就会导致不能debug。
如 nameko 的 testing/pytest.py 中就有相应代码。注释掉后，pycharm 的 debug 就正常了。

2. `pg` 数据库创建脚本

	* `postgres`

```sql
CREATE USER djpmp_prd WITH PASSWORD '<password>';
CREATE DATABASE djpmp_prd OWNER djpmp_prd;
```

3. 代码调试

```
from IPython import embed; embed()
```
