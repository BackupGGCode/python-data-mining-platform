# 项目概述 #
**项目目前主要关注中文文本的数据挖掘算法**。由于每种数据挖掘算法的局限性都很大，就拿分类算法一样，决策树、朴素贝叶斯这两种算法都有着自己的特性，只能在某一种类型的类型的数据上应用比较良好，比如朴素贝叶斯，就对于那些短文本的分类比较适合，而决策树对于短文本、稀疏情况下就效果欠佳了，特别是在数据比较稀疏的情况。在这种情况下，当有一个数据挖掘任务的时候，怎样去找到一个合适的算法就非常重要了。如果从头开发算法，是一个成本很高的事情，特别是对文本来说就更麻烦，需要在前面做一些如分词、去停用词等等操作。如果有一个平台，可以支持快速的开发，让用户能够快速的看到，针对自己的数据，什么样的算法比较合适，就是本项目的一个初衷。

在这个角度上来说，还是有一些开源的数据挖掘工具，如weka是一个很全面的工具，里面支持几十上百种数据挖掘（机器学习）的算法。不过从我之前使用weka的经验来说，weka对于中文的支持非常糟糕，而且对于稍大一点的数据，就直接罢工不干了（我记得尝试过一个40M左右的文本的聚类任务，weka直接死掉了）。所以开发出一个支持中文、能够支持更大数据量的平台就很有必要了。

**项目目前规划上来说，主要是针对单机上能够运行的任务**。虽然分布式机器学习算法（换个更fashion的名字是云计算），是目前最热门的一个话题，但是对于大多数的任务来说，单机版也足够了。对于算法的学习、试验来说，单机版可以更简单、方便的将算法的特性展示出来。当了解了怎样写单机版后，将其改写为简单的分布式版本(比如mpi或者map-reduce)，并不是那么复杂的一个事情。

目前项目使用Python作为开发语言，虽然之前基本只写过++，但是从接触Python开始，就觉得Python语言在快速开发、可读性方面非常的适合，而且极其良好的跨平台型也是Python的优势，我平时的开发环境是在linux(ubuntu)下进行。

项目的名字是PyMining，这个取这个名字是为了能够简单的说明项目的开发语言与用途，Py是指的Python，Mining是指的Data Mining（数据挖掘）。

**另外**：对于分词词典、测试数据等比较“贵重”的内容，我也不会使用任何受保护的数据，**我会选择那些网上比较容易找到的内容并且加以提炼与修改作为项目的一部分**。

# License #
目前使用BSD作为项目的License，简单来说，就是**本项目的源代码可以被商业、非商业自由的使用，也可以将其修改作为二进制和源代码再次发布，但是保留原源代码（或者原源代码编译的二进制程序）的BSD协议，并且不能使用原作者（机构）名字来作为产品的市场推广，更详细的信息请参见发布包内的文档。**

# 中文文本的数据挖掘基础 #
还是先科普一下中文文本的数据挖掘基础吧。**一个典型的文本分类的数据挖掘流程**：

![http://images.cnblogs.com/cnblogs_com/LeftNotEasy/201102/201102271433165574.png](http://images.cnblogs.com/cnblogs_com/LeftNotEasy/201102/201102271433165574.png)

我这里解释一下，红色的部分是训练时候调用的模块，绿色是测试时候调用的模块，而蓝色的部分是训练的时候生成的中间文件，它们联系着训练、测试两个部分。

从左到右看是算法运行的流程，首先用户给出原始的用于训练的中文文本，然后进行分词等操作。

经过了**生成矩阵\*这个步骤，文本就转化成了数学语言（矩阵）了，**之后的算法都是运行在矩阵之上，不再关心输入的数据是否是文档了**，换句话来说，生成矩阵这个模块相当于是一道门，门内是作用在矩阵之上的算法，门外是原始的文本语料。**

图上的特征选择、朴素贝叶斯分类器就是属于门内的内容，具体的算法具体分析。对于特征选择算法(feature selection)和朴素贝叶斯(naive bayes)分类器，可以看看wikipedia的定义。

## 如何使用项目 ##
### 给出一段示例代码: ###

**更多的代码请参考代码中的example目录下的**

```
import math
import sys

from matrix import Matrix
from classifier_matrix import ClassifierMatrix
from segmenter import Segmenter
from py_mining import PyMining
from configuration import Configuration 
from chisquare_filter import ChiSquareFilter
from twc_naive_bayes import TwcNaiveBayes

if __name__ == "__main__":
    config = Configuration.FromFile("conf/test.xml")
    PyMining.Init(config, "__global__")
    matCreater = ClassifierMatrix(config, "__matrix__")
    [trainx, trainy] = matCreater.CreateTrainMatrix("data/train.txt")
    chiFilter = ChiSquareFilter(config, "__filter__")
    chiFilter.TrainFilter(trainx, trainy)
    [trainx, trainy] = chiFilter.MatrixFilter(trainx, trainy)
    nbModel = TwcNaiveBayes(config, "twc_naive_bayes")
    nbModel.Train(trainx, trainy)

    [testx, testy] = matCreater.CreatePredictMatrix("data/test.txt")
    [testx, testy] = chiFilter.MatrixFilter(testx, testy)
    retY = nbModel.TestMatrix(testx, testy)
```

这段代码分成了训练和测试两个阶段，首先值得注意的是，项目的模块需要的参数都是从一个\_xml\_格式的配置文件中得到的，也就是代码中的`test.xml`。代码最开始，调用`Configuration.FromFile`函数，从xml配置文件中解析出需要的Dom Tree，生成Configuration的实例。

**之后的模块初始化，都将获取这个Configuration的实例中指定的tag的信息。**(重要)

比如ClassifiterMatrix类初始化的时候，将读取标签为matrix的信息（**某些模块如果不需要读取某种标签的信息，这个标签下面将是无内容的**，具体请见后面的xml）。初始化的时候，需要指定最后一个布尔参数(**isFromFile**)，**表示是否这个模块从配置类中指定的文件中载入得到**。一般在训练的时候，指定这个参数为False，而在单独测试的时候，需要指定这个参数为True，因为需要从训练的时候生成的文件中载入训练的模型才能够进行测试。

### 训练的过程： ###
PyMining是全局可见的静态类，里面放置着一些在全局中都有用的一些参数，目前里面有4个dictionary：
  * term-to-id(从单词的str到单词的id)
  * id-to-term(从单词的id到单词的str)
  * id-to-doc-count(某一个单词的id对应了多少篇文档)
  * class-to-doc-count(某一个分类里面有多少篇文档)

**这些信息在特征选择、预测、以及结果的展示中将起到很重要的作用**，这个类的名字跟项目的名字一样，第一是因为这个类的信息着实重要，第二是确实不知道取什么名字了-_-。_

接下来的ClassifierMatrix就是前面图片中的“**构成矩阵\*”这个模块，在其CreateTrainMatrix方法中，将会从原始的训练语料train.txt中，进行分词等操作，生成矩阵trainx, trainy，并且会填充上面提到的PyMining中的4个dictionary。**

trainx是一个m `*` n的矩阵，表示数据的部分，每一行表示一篇文档，每一列表示一个feature（单词）。trainy是一个m `*` 1的矩阵，表示每篇文档对应的分类id。**从生成矩阵之后，算法看到的信息就只有矩阵了与PyMining了**。

接下来生成了一个chiFilter，也就是卡方(chi-square)的特征选择器，**chiFilter将使用卡方检测算法来看看哪些特征（词）是没有什么必要的**，并且将其过滤掉，其Create方法传入的参数就是之前的trainx, trainy，**结果将是一个保存在chiFilter实例中的一个黑名单**，表示哪些term-id是需要过滤掉的。其TestFilter方法就是使用之前得到的黑名单来过滤掉矩阵中不重要的列。

最后就是分类算法了，这里是使用的是带补偿的朴素贝叶斯(TwcNaiveBayes)算法。调用其Train方法可以得到一个模型并且保存到实例中。请参考论文：**Tackling the Poor Assumptions of Naive Bayes Text Classifers\*，这里注意一下，这个算法是0.1版本新加入的，测试发现比最基础的朴素贝叶斯算法更好。**

### 预测的过程： ###
PyMining的训练、测试的过程可以独立的运行，可以先训练出一个模型，等到有需要的时候再进行测试，所以在训练的过程中，有一些数据（比如说chi-square filter）中的黑名单，将会保存到文件中去。如果想单独的运行测试程序，请参考下面的一段代码，调用了NaiveBayes.Test方法后，返回的resultY就是一个m `*` 1的矩阵（m是测试文档的个数），表示对于每一篇测试文档使用模型测试得到的标签（属于0，1，2，3）中的哪一个，precision是测试的准确率。

### 下面是配置文件，这里大概的讲讲： ###

```
<?xml version="1.0" encoding="utf-8"?>
<config>
    <__segmenter__>
        <main_dict>dict/dict.main</main_dict>
    </__segmenter__>

    <__matrix__>
    </__matrix__>

    <__global__>
        <term_to_id>mining/term_to_id</term_to_id>
        <id_to_term>mining/id_to_term</id_to_term>
        <id_to_doc_count>mining/id_to_doc_count</id_to_doc_count>
        <class_to_doc_count>mining/class_to_doc_count</class_to_doc_count>
        <id_to_idf>mining/id_to_idf</id_to_idf>
    </__global__>

    <__filter__>
        <rate>0.8</rate>
        <method>max</method>
        <log_path>mining/filter.log</log_path>
        <model_path>mining/filter.model</model_path>
    </__filter__>

    <naive_bayes>
        <model_path>mining/naive_bayes.model</model_path>
        <log_path>mining/naive_bayes.log</log_path>
    </naive_bayes>

    <twc_naive_bayes>
        <model_path>mining/naive_bayes.model</model_path>
        <log_path>mining/naive_bayes.log</log_path>
    </twc_naive_bayes>
</config>

```

里面的每一个二级标签就是一个模块的熟悉，比如说`__segmenter__`里面的信息就是分词器所需要的一些配置信息，有些名字是加上了`__  word __`的样子，表示是默认的模块，segmenter里面main\_dict为主词典所在的路径。

> global里面是几个全局的表，也就是之前提到的PyMining模块中的4个dictionary，mining/term\_to\_id表示保存到文件的路径。

filter表示过滤器，rate表示选择百分之多少的feature，method有两种max与avg，这里具体请参考wiki中的文档，log\_path表示该模块运行的时候，输出的日志信息的路径。

model\_path表示训练过程中得到的黑名单的输出的路径。如果有需要，我们可以从文件中载入训练的结果。

naive\_bayes跟filter差不多，这里就不再多说了。

### PyMining中有哪些模块： ###
目前PyMining中具有下面的模块。具体的api请参考源文件，
  * Segmenter: 一个非常简单的分词器，采用贪心法进行分词。
  * ClassifierMatrix: 生成分类算法中需要的矩阵
  * ChisquareFilter: chi-square 的feature selector
  * NaiveBayes: (基本的）朴素贝叶斯分类器
  * TwcNaiveBayes：(带补偿)朴素贝叶斯分类器（相比上者，更推荐这个）
  * KMeans：可以用来做文本聚类的K-Means聚类器（例子请见kmeans.py）
  * Pca: 主成分提取的模块
  * Sogou-Data-Importer：可以用来导入搜狗公布的新闻数据，具体使用方法请见另一篇wiki：[Sogou Importer](http://code.google.com/p/python-data-mining-platform/wiki/Additional_Tools?ts=1305465189&updated=Additional_Tools)

### 运行PyMining： ###
调用python naive\_bayes\_train\_test.py，将会输出 0.86。这是分类的准确率。PyMining中目前的训练测试数据是由Koala Team提供的，来自团购网站的标题的分类，0表示美食、1表示美容美发、2表示休闲娱乐、3表示其他，训练数据看起来是这个样子：

```
仅售28元！原价最高466元的“兰彩鸣量贩KTV”两小时豪华欢唱套餐一份：两个小时不限时段欢唱+不限包房类型+可连续累计消费+爆米花一份+VC一扎！（豪华包最多容纳45人，最小包可容纳4人）邀请好友返利10元！    2 
仅售39元！原价113元的“北京铭豪苑火锅烧烤城”馋嘴锅双人套餐一份：干锅鸭翅（2.5斤左右）+羊肉（300g）+野山笋（300g）+鱼丸虾丸双拼（500g）+7元双拼+6元双拼+杂面一份！邀请好友返利10元！    0 
仅售10元！原价176元的“水星健身”双日健身体验卡一张！    2
```

运行完后，将会在mining目录下得到一些文件，这就是在训练过程中的一些日志、模型文件，可以打开来看看训练的结果。

filter.log里面记录的是chisquare feature selector的结果，看起来是下面的样子：

```
chiSquare info: 
'=======selected======== '
护理 139.541924743 
美容 109.728270833 
美发 99.0576860046 
染发 80.5718475073 
入住 65.4600301659 
烫发 62.3015873016 
面部 61.8500831431 
早餐 54.3178973717 
欧莱雅 53.246124031 
男女 45.6000719014
…
豆沙 2.71349224717 
水煮鱼 2.71349224717 
琵琶 2.71349224717 
蛋挞 2.71349224717 
新增 2.71349224717 
接待 2.71349224717 
酒楼 2.71349224717 
12人 2.71349224717 
吉列 2.71349224717 
香菜 2.71349224717 
鸡排 2.71349224717 
'========unselected======= '
春卷 2.71349224717 
木瓜 2.71349224717 
鳕鱼 2.71349224717 
鳗鱼 2.71349224717 
手卷 2.71349224717
…
广场店 0.441547518923 
实惠 0.441547518923 
亲情 0.441547518923 
青岛 0.441547518923 
百纳 0.441547518923 
米兰 0.441547518923 
感受 0.441547518923 
大海 0.441547518923 
旗 0.441547518923 
亚洲 0.441547518923
```

这个列表上，越往上越是对分类有帮助的词，越往下，越是没有什么意义的词，单词后面的数字表示chisquare分数，越高说明单词越有意义。`=====unselected=======`表示一个分界线，分界线下面的词是被过滤掉的词。

其他模块的信息可以看看其他的log文件，也会发现一些有趣的地方，这里不再一一解释了。

# PyMining下一步的开发计划（需要更多你的参与） #
PyMining之后会支持更多的算法（包括分类、聚类等算法），会支持更多的用法，会支持更丰富的文本格式。另外，之后可能会调用NumPy与SciPy，以进行更强大的矩阵计算。

如果对希望参与开发的朋友可以联系我：wheeleast@gmail.com，**要求Python有一定的开发经验**，对\*机器学习**or**数据挖掘**or**模式识别算法**有兴趣。**

对项目有任何其他问题的朋友可以联系我。