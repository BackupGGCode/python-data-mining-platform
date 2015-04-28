## Objective ##
This is a platform writing in Python that can use variant data-mining algorithms to get results from a source (like matrix, text documents). Algorithms can using xml configuration to make them run one-by-one. <p>
E.g. at first, we may run PCA(principle components analysis) for feature selection, then we may run random forest for classification.<br>
Now, algorithms are mainly design for tasks can be done in a single computer, good scalability of the architecture allows you in a very short period of time to complete the algorithm you want, and use it in your project (believe me, it's faster, better, and easier than Weka). <p>
The another important feature is this platfrom can support text classification or clustering operation very good.<br>
<br>
<br>
<h2>Get start</h2>
<b>Just write code like this, you will get amazing result (a naive-bayes training and testing),</b>
<pre><code>    # load configuratuon from xml file<br>
    config = Configuration.FromFile("conf/test.xml")<br>
    GlobalInfo.Init(config, "__global__")<br>
<br>
    # init module that can create matrix from text file<br>
    txt2mat = Text2Matrix(config, "__matrix__")<br>
<br>
    # create matrix for training (with tag) from a text file "train.txt"<br>
    [trainx, trainy] = txt2mat.CreateTrainMatrix("data/train.txt")<br>
<br>
    # create a chisquare filter from config file<br>
    chiFilter = ChiSquareFilter(config, "__filter__")<br>
<br>
    # get filter model from training matrix<br>
    chiFilter.TrainFilter(trainx, trainy)<br>
<br>
    # filter training matrix<br>
    [trainx, trainy] = chiFilter.MatrixFilter(trainx, trainy)<br>
<br>
    # train naive bayes model<br>
    nbModel = NaiveBayes(config, "naive_bayes")<br>
    nbModel.Train(trainx, trainy)<br>
<br>
    # create matrix for test<br>
    [testx, testy] = txt2mat.CreatePredictMatrix("data/test.txt")<br>
<br>
    # using chisquare filter do filtering<br>
    [testx, testy] = chiFilter.MatrixFilter(testx, testy)<br>
<br>
    # test matrix and get result (save in resultY) and precision<br>
    [resultY, precision] = nbModel.Test(testx, testy)<br>
<br>
    print precision<br>
</code></pre>

And you need define some paramters in a configuration file (It will be loaded by Configuration.FromFile(...xml)).<br>
<br>
<pre><code>    &lt;config&gt;<br>
        &lt;__segmenter__&gt;<br>
            &lt;main_dict&gt;dict/dict.main&lt;/main_dict&gt;<br>
        &lt;/__segmenter__&gt;<br>
<br>
        &lt;__matrix__&gt;<br>
        &lt;/__matrix__&gt;<br>
<br>
        &lt;__global__&gt;<br>
            &lt;term_to_id&gt;mining/term_to_id&lt;/term_to_id&gt;<br>
            &lt;id_to_term&gt;mining/id_to_term&lt;/id_to_term&gt;<br>
            &lt;id_to_doc_count&gt;mining/id_to_doc_count&lt;/id_to_doc_count&gt;<br>
            &lt;class_to_doc_count&gt;mining/class_to_doc_count&lt;/class_to_doc_count&gt;<br>
            &lt;id_to_idf&gt;mining/id_to_idf&lt;/id_to_idf&gt;<br>
            &lt;newid_to_id&gt;mining/newid_to_id&lt;/newid_to_id&gt;<br>
        &lt;/__global__&gt;<br>
<br>
        &lt;__filter__&gt;<br>
            &lt;rate&gt;0.2&lt;/rate&gt;<br>
            &lt;method&gt;max&lt;/method&gt;<br>
            &lt;log_path&gt;mining/filter.log&lt;/log_path&gt;<br>
            &lt;model_path&gt;mining/filter.model&lt;/model_path&gt;<br>
        &lt;/__filter__&gt;<br>
<br>
        &lt;naive_bayes&gt;<br>
            &lt;model_path&gt;mining/naive_bayes.model&lt;/model_path&gt;<br>
            &lt;log_path&gt;mining/naive_bayes.log&lt;/log_path&gt;<br>
        &lt;/naive_bayes&gt;<br>
<br>
        &lt;twc_naive_bayes&gt;<br>
            &lt;model_path&gt;mining/naive_bayes.model&lt;/model_path&gt;<br>
            &lt;log_path&gt;mining/naive_bayes.log&lt;/log_path&gt;<br>
        &lt;/twc_naive_bayes&gt;<br>
        <br>
        &lt;smo_csvc&gt;<br>
          &lt;model_path&gt;mining/smo_csvc.model&lt;/model_path&gt;<br>
          &lt;log_path&gt;mining/smo_csvc.log&lt;/log_path&gt;<br>
          &lt;c&gt;100&lt;/c&gt;<br>
          &lt;eps&gt;0.001&lt;/eps&gt;<br>
          &lt;tolerance&gt;0.000000000001&lt;/tolerance&gt;<br>
          &lt;times&gt;50&lt;/times&gt;<br>
          &lt;kernel&gt;<br>
            &lt;name&gt;RBF&lt;/name&gt;<br>
            &lt;parameters&gt;10&lt;/parameters&gt;<br>
          &lt;/kernel&gt;<br>
          &lt;cachesize&gt;300&lt;/cachesize&gt;<br>
        &lt;/smo_csvc&gt;<br>
    &lt;/config&gt;<br>
</code></pre>

<h2>Features</h2>
<b>Clustering algorithm</b>
<ul><li>KMeans</li></ul>

<b>Classification algorithm</b>
<ul><li>Random forest<br>
</li><li>Naive Bayes<br>
</li><li>TWC Naive Bayes<br>
</li><li>SVM</li></ul>

<b>Feature selector</b>
<ul><li>Chisquare<br>
</li><li>PCA</li></ul>

<b>Mathematic</b>
<ul><li>Basic operations (like bagging, transpose, etc.)</li></ul>

<b>Data source support</b>
<ul><li>Matrix (with csv format)<br>
</li><li>Raw text (now only support Chinese, English to be added)