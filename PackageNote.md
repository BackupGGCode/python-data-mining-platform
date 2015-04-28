# 项目的packages的构成 #

## common ##
  * global\_info.py
> (通用的全局原始文本表示模块)
  * configuration.py
> (通用的配置信息加载模块)

## io ##
  * (未来跟矩阵的load、save等打交道的地方都放在这儿)

## math ##
  * matrix
> (目前就是项目内部使用的csr格式，未来可能会扩展为普通的dense matrix，或者其他的矩阵格式)
  * text2matrix
> (从普通的文本通过分词等操作转换为矩阵的一个类，可以看做是matrix的一种构造函数)
  * scipy\_interface (与scipy的接口）
  * PCA (主成分提取)

## clustering ##
  * k-means
> (目前实现了一个非常简单的聚类算法，能够简单的输出聚类的结果，但是没有对聚类的指标进行评价的类，以后可以加入)
  * 其他的聚类方法以及聚类评价器

## classifier ##
  * naive\_bayes
> (普通的naive\_bayes)
  * twc\_naive\_bayes
> (基于补集、以及进行了一些规范化处理的naive\_bayes)
  * 其他的分类器以及分类评价器

## preprocessor ##
  * chisquare
> （卡方过滤器）

## cf ##
  * 协同过滤的方法