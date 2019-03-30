# 2019华为软件精英挑战赛

本代码是初赛训练和正式比赛使用的代码。文件夹中有任务书和赛制。4张map分别是训练和比赛使用地图。

A文件夹为训练地图使用的代码，并分开各个模块。B\C文件夹为为正式地图代码。

代码并没有使用判定器，只按照一定规则对小车进行排序发车，对地图使用一些反馈函数，对一些路径进行惩罚。在初赛训练赛中单图可以达到400-500，排名在前十几名。

## 总结

本来训练图调参调完还有些自信，在正式地图发布以后出现的一系列问题，让自己感受到了自己的不足，还是考虑的太少，coding能力不足。当一次经验教训吧。

## 问题

正式地图对于训练地图的变换在于两处：
* 一处是挖了一个小坑，把原本三张地图顺序的id打乱成了随机的id，该问题很好解决，只需要使用dict对其进行映射。
* 第二处在于数据量的增大，由于数据量增大很多，而自己开始前没有充分准备，导致一张地图跑完需要二十分钟。对此分析以后发现是迪杰斯拉特的算法在python中计算时间过长。解决办法主要有两个一个使用遍历更少的A*，不过在预期距离需要处理。第二就是用Java或者C++去编写。对此自己都考虑过，却没有实际去做，导致正式比赛python一直超时。