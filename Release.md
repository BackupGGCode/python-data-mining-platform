# 2011 5.29 Ver 0.2 第三个开发版 #
## Add Features ##
  * 加入对scipy、numpy的支持，加入一个matplotlib的接口（并且能够在tutorial上面show出来）
  * 加入了PCA（主成分提取）算法，并且加入了pca的example

## Changes ##
  * 更新项目的组织方式，让package的组织、example的组织等等更合理一点

## Fix Bugs ##
  * 修正了chi-square在example调用中的一个错误

# 2011 2.26 Ver 0.0.0.1 第一个开发版 #
## Add Features ##
  * 能够支持中文文本输入，并且对其进行分词等操作，作为分类的源数据
  * 带有卡方检测(chi square test)的特征词选择器(feature selector)
  * 参数的调整(parameter tuning)支持通过xml配置文件进行
  * 能够支持批量文本的训练与批量文本的测试（训练或者测试用的文档放在同一个文件中）

# 2011 5.15 Ver 0.1 第二个开发版 #
## Add Features ##
  * 加入了K-Means算法，能够对文本进行聚类
  * 加入了基于补集的朴素贝叶斯算法，大大提升了分类的准确率，目前该算法在搜狗实验室文本分类数据中，对20000篇、8分类左右的数据的预测准确率在90%左右
  * 现在能够对单行的文本进行预测（以str为类型传入，上一版仅接受文件路径的传入）
  * 加入了Sogou实验室文本分类数据的导入器，可以进行更多的实验

## Fix Bugs ##
  * 修正了在Chi-Square test中的一个错误