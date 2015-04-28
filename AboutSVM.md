# 计划 #

在分类算法中加入C-SVC,首先可先实现2分类算法.


# 目标 #

加入与SVM算法相关内容，主要有
  * 确定输入样本格式
  * 实现用于样本数据归一化的接口
  * 算法支持若干核函数，例如Linear Kernel、Gaussian Kernel、Sigmoid Kernel、Polynomial Kernel、String Kernel
  * 实现样本训练接口，支持dense matrix和sparse matrix，对dot product的操作在实现上可能有所不同，针对不同核函数可以有不同的优化方法
  * 实现模型应用接口，可以对测试集进行测试也可以对某一样本进行预测
  * 最后，接口命名和算法实现要合理，注释要准确有效，用户使用和理解起来要方便