"""
==============================================================================
第十五章：文本聚类
==============================================================================
日期：2026-05-16

同学们好！这节课我们来学习文本聚类 —— 让计算机自动把相似的文本归到一起。

----------------------------------------------------------------------
生活类比：文本聚类就像整理文件柜
----------------------------------------------------------------------

想象你是一个刚入职的秘书，老板给了你一箱子文件，让你整理归档。

这些文件有：合同、发票、报告、通知、合同、报告、发票……

你会怎么做？
  1. 先大概看一遍所有文件
  2. 把"看起来差不多"的文件放在一起
  3. 每一堆给它贴个标签（比如"财务类"、"合同类"）

文本聚类就是让计算机做同样的事情：
  - 输入：一堆没有标签的文本
  - 输出：自动分成几组，每组内的文本尽量相似

----------------------------------------------------------------------
两种主要的聚类方法
----------------------------------------------------------------------

1. K-Means 聚类（划分法）
   → 就像把人分成 N 个小组
   → 先确定要分几组（K 值）
   → 然后不断调整，让每组内的人都尽量相似

2. LDA 主题模型（概率法）
   → 就像发现"隐藏的主题"
   → 每篇文档是多个主题的混合
   → 每个主题是一组相关的词

----------------------------------------------------------------------
本章内容
----------------------------------------------------------------------

1. K-Means 聚类算法（从零实现 + sklearn 版本）
2. 文本向量化（TF-IDF）
3. LDA 主题模型
4. 聚类效果评估

==============================================================================
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import math
import random
from collections import Counter


# ==============================================================================
# 第一部分：文本向量化 —— 把文字变成数字
# ==============================================================================
#
# 计算机不认识文字，只认识数字。
# 所以聚类的第一步是把文本转换成向量（一组数字）。
#
# 生活类比：
#   想象你要比较两个人的"口味偏好"：
#   - 小明：喜欢甜 3 分，喜欢咸 2 分，喜欢辣 1 分 → [3, 2, 1]
#   - 小红：喜欢甜 2 分，喜欢咸 3 分，喜欢辣 2 分 → [2, 3, 2]
#
#   有了这些数字，你就可以计算他们口味的"距离"了。
#
# TF-IDF 就是把文本变成这种数字向量的方法。
#
# ==============================================================================


def build_vocabulary(documents: list) -> list:
    """
    从文档集合中构建词汇表

    ━━━━━━━ 生活类比 ━━━━━━━
    就像整理一本"字典"，把所有文档中出现过的不重复的词都记录下来。

    参数：
        documents: 文档列表，每个文档是一个字符串

    返回：
        词汇表（词列表）
    """
    vocab = set()
    for doc in documents:
        # 简单的按字符分词（中文场景）
        for char in doc:
            if char.strip() and char not in "，。！？、；：""''（）【】《》\n":
                vocab.add(char)
    return sorted(list(vocab))


def compute_tf(document: str, vocabulary: list) -> list:
    """
    计算词频（Term Frequency, TF）

    ━━━━━━━ 生活类比 ━━━━━━━
    就像数一数你的购物车里每种商品买了几件。
    TF = 某个词在文档中出现的次数 / 文档总词数

    公式：
        TF(t, d) = 词 t 在文档 d 中出现的次数 / 文档 d 的总词数

    参数：
        document: 单个文档（字符串）
        vocabulary: 词汇表

    返回：
        TF 向量（每个词的词频）
    """
    # 统计词频
    char_count = Counter()
    total = 0
    for char in document:
        if char.strip() and char not in "，。！？、；：""''（）【】《》\n":
            char_count[char] += 1
            total += 1

    # 计算 TF：词频 / 总词数
    if total == 0:
        return [0.0] * len(vocabulary)

    tf_vector = []
    for word in vocabulary:
        tf = char_count.get(word, 0) / total
        tf_vector.append(tf)

    return tf_vector


def compute_idf(documents: list, vocabulary: list) -> list:
    """
    计算逆文档频率（Inverse Document Frequency, IDF）

    ━━━━━━━ 生活类比 ━━━━━━━
    想象你是一个老师，要判断一个词"重不重要"：
    - "的" 在每篇作文里都出现 → 不重要 → IDF 低
    - "量子" 只在几篇作文里出现 → 很重要 → IDF 高

    公式：
        IDF(t) = log(总文档数 / 包含词 t 的文档数)

    参数：
        documents: 文档列表
        vocabulary: 词汇表

    返回：
        IDF 向量（每个词的 IDF 值）
    """
    n_docs = len(documents)

    # 统计每个词出现在多少篇文档中
    doc_freq = Counter()
    for doc in documents:
        # 用 set 去重，每个词在一篇文档中只计一次
        unique_chars = set()
        for char in doc:
            if char.strip() and char not in "，。！？、；：""''（）【】《》\n":
                unique_chars.add(char)
        for char in unique_chars:
            doc_freq[char] += 1

    # 计算 IDF
    idf_vector = []
    for word in vocabulary:
        df = doc_freq.get(word, 0)
        # 使用平滑：+1 避免除以 0
        idf = math.log((n_docs + 1) / (df + 1)) + 1
        idf_vector.append(idf)

    return idf_vector


def compute_tfidf(documents: list) -> tuple:
    """
    计算所有文档的 TF-IDF 向量

    ━━━━━━━ 生活类比 ━━━━━━━
    TF-IDF 就像给每篇文章生成一个"指纹"：
    - TF 看的是"这篇文章里什么词用得多"
    - IDF 看的是"这个词在整个文库里稀不稀有"
    - 两者相乘 = 既重要又独特的词得分高

    公式：
        TF-IDF(t, d) = TF(t, d) * IDF(t)

    参数：
        documents: 文档列表

    返回：
        (tfidf_matrix, vocabulary)
        tfidf_matrix: 二维列表，每行是一个文档的 TF-IDF 向量
        vocabulary: 词汇表
    """
    # 第一步：构建词汇表
    vocabulary = build_vocabulary(documents)

    # 第二步：计算 IDF（所有文档共享同一个 IDF）
    idf = compute_idf(documents, vocabulary)

    # 第三步：计算每篇文档的 TF-IDF
    tfidf_matrix = []
    for doc in documents:
        tf = compute_tf(doc, vocabulary)
        # TF-IDF = TF * IDF（逐元素相乘）
        tfidf = [tf[i] * idf[i] for i in range(len(vocabulary))]
        tfidf_matrix.append(tfidf)

    return tfidf_matrix, vocabulary


# ==============================================================================
# 第二部分：K-Means 聚类算法
# ==============================================================================
#
# K-Means 是最经典的聚类算法。
#
# 核心思想：
#   1. 选 K 个点作为初始"中心"
#   2. 把每个数据点分配到最近的中心
#   3. 重新计算每个组的中心
#   4. 重复 2-3 步，直到中心不再变化
#
# 生活类比：
#   想象你在操场上随机放了 3 面旗子（K=3）：
#   1. 每个学生跑到离自己最近的旗子旁边
#   2. 每组学生重新算一个"中心位置"
#   3. 把旗子移到新的中心位置
#   4. 重复，直到没有人再换组
#
# ==============================================================================


def euclidean_distance(vec1: list, vec2: list) -> float:
    """
    计算两个向量的欧几里得距离

    ━━━━━━━ 生活类比 ━━━━━━━
    就像用尺子量两个点之间的直线距离。

    公式：
        d = sqrt(sum((a[i] - b[i])^2))
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))


def cosine_distance(vec1: list, vec2: list) -> float:
    """
    计算两个向量的余弦距离（1 - 余弦相似度）

    ━━━━━━━ 生活类比 ━━━━━━━
    不看"远近"，看"方向"是否一致。
    两个向量方向越接近，距离越小。
    """
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 1.0
    return 1.0 - dot / (norm1 * norm2)


def kmeans(data: list, k: int, max_iterations: int = 100, distance_fn=None) -> tuple:
    """
    K-Means 聚类算法

    ━━━━━━━ 生活类比 ━━━━━━━
    想象你是一个班主任，要把学生分成 K 个学习小组：
    1. 随机选 K 个学生当"组长"
    2. 每个学生选离自己最近的组长，加入他的组
    3. 每组重新选一个"最中间"的人当新组长
    4. 重复，直到组长不再换人

    参数：
        data: 数据列表，每个元素是一个向量（数字列表）
        k: 聚类数量（要分成几组）
        max_iterations: 最大迭代次数
        distance_fn: 距离计算函数（默认欧几里得距离）

    返回：
        (labels, centroids)
        labels: 每个数据点的簇标签（0 到 k-1）
        centroids: 最终的簇中心
    """
    if distance_fn is None:
        distance_fn = euclidean_distance

    n = len(data)
    if n == 0 or k <= 0:
        return [], []

    # 第一步：随机选择 K 个初始中心点
    # 从数据中随机选 K 个不同的点
    indices = random.sample(range(n), min(k, n))
    centroids = [data[i][:] for i in indices]  # 深拷贝

    labels = [0] * n  # 每个点的簇标签

    for iteration in range(max_iterations):
        # 第二步：分配 —— 把每个点分配到最近的中心
        new_labels = []
        for point in data:
            # 计算到每个中心的距离
            distances = [distance_fn(point, c) for c in centroids]
            # 选择距离最小的中心
            new_labels.append(distances.index(min(distances)))

        # 检查是否收敛（标签不再变化）
        if new_labels == labels:
            print(f"  K-Means 在第 {iteration + 1} 轮迭代后收敛")
            break
        labels = new_labels

        # 第三步：更新 —— 重新计算每个簇的中心
        for j in range(k):
            # 找到属于第 j 簇的所有点
            cluster_points = [data[i] for i in range(n) if labels[i] == j]

            if cluster_points:
                # 新中心 = 簇内所有点的平均值
                dim = len(cluster_points[0])
                new_centroid = []
                for d in range(dim):
                    avg = sum(p[d] for p in cluster_points) / len(cluster_points)
                    new_centroid.append(avg)
                centroids[j] = new_centroid

    return labels, centroids


def kmeans_pp_init(data: list, k: int, distance_fn=None) -> list:
    """
    K-Means++ 初始化方法 —— 更聪明的初始中心选择

    ━━━━━━━ 生活类比 ━━━━━━━
    普通 K-Means 随机选初始中心，可能选到"扎堆"的点。
    K-Means++ 的策略是：尽量选"离已有中心远"的点。

    就像开连锁店：
    - 第 1 家店随便选个位置
    - 第 2 家店尽量选离第 1 家远的位置
    - 第 3 家店尽量选离前 2 家都远的位置
    - 这样覆盖范围最大

    参数：
        data: 数据列表
        k: 聚类数量
        distance_fn: 距离函数

    返回：
        初始中心列表
    """
    if distance_fn is None:
        distance_fn = euclidean_distance

    n = len(data)

    # 第一个中心：随机选
    centroids = [data[random.randint(0, n - 1)][:]]

    for _ in range(1, k):
        # 计算每个点到最近已有中心的距离的平方
        distances_sq = []
        for point in data:
            min_dist = min(distance_fn(point, c) for c in centroids)
            distances_sq.append(min_dist ** 2)

        # 按概率选择下一个中心（距离越远，概率越大）
        total = sum(distances_sq)
        if total == 0:
            centroids.append(data[random.randint(0, n - 1)][:])
            continue

        # 轮盘赌选择
        r = random.random() * total
        cumulative = 0
        for i, d in enumerate(distances_sq):
            cumulative += d
            if cumulative >= r:
                centroids.append(data[i][:])
                break

    return centroids


# ==============================================================================
# 第三部分：LDA 主题模型
# ==============================================================================
#
# LDA（Latent Dirichlet Allocation）是一种"主题发现"算法。
#
# 核心思想：
#   每篇文档是多个"主题"的混合
#   每个主题是一组"词"的概率分布
#
# 生活类比：
#   想象你是一个图书管理员，要把书分类：
#   - 《Python编程》→ 70% 编程 + 20% 教育 + 10% 科技
#   - 《三国演义》→ 80% 历史 + 15% 文学 + 5% 战争
#
#   LDA 就是自动发现这些"隐藏的主题"。
#
# ==============================================================================


def simple_lda(documents: list, n_topics: int = 3, n_iterations: int = 50) -> tuple:
    """
    简化版 LDA 主题模型（Gibbs 采样）

    ━━━━━━━ 生活类比 ━━━━━━━
    想象你是一个图书管理员，要把书按主题分类。
    先随机分配，然后不断调整：经常一起出现的词属于同一主题。
    """
    vocabulary = build_vocabulary(documents)
    vocab_size = len(vocabulary)
    word_to_idx = {w: i for i, w in enumerate(vocabulary)}
    if vocab_size == 0:
        return [], [], []

    # 将文档转换为词索引序列
    doc_words = []
    for doc in documents:
        words = [word_to_idx[c] for c in doc
                 if c.strip() and c not in "，。！？、；：""''（）【】《》\n" and c in word_to_idx]
        doc_words.append(words)

    # 初始化：为每个词随机分配主题
    doc_topic_counts = []
    topic_word_counts = [[0] * vocab_size for _ in range(n_topics)]
    topic_counts = [0] * n_topics
    word_topics = []

    for doc_idx, words in enumerate(doc_words):
        topic_dist = [0] * n_topics
        word_topic_list = []
        for word_idx in words:
            topic = random.randint(0, n_topics - 1)
            word_topic_list.append(topic)
            topic_dist[topic] += 1
            topic_word_counts[topic][word_idx] += 1
            topic_counts[topic] += 1
        word_topics.append(word_topic_list)
        doc_topic_counts.append(topic_dist)

    # Gibbs 采样迭代
    for _ in range(n_iterations):
        for doc_idx, words in enumerate(doc_words):
            for word_pos, word_idx in enumerate(words):
                old_topic = word_topics[doc_idx][word_pos]
                doc_topic_counts[doc_idx][old_topic] -= 1
                topic_word_counts[old_topic][word_idx] -= 1
                topic_counts[old_topic] -= 1

                # 计算每个主题的概率并采样
                probs = []
                for t in range(n_topics):
                    p_doc = doc_topic_counts[doc_idx][t] + 0.1
                    p_word = (topic_word_counts[t][word_idx] + 0.01) / (topic_counts[t] + vocab_size * 0.01)
                    probs.append(p_doc * p_word)
                total_p = sum(probs)
                probs = [p / total_p for p in probs]

                r = random.random()
                cumulative = 0
                new_topic = 0
                for t, p in enumerate(probs):
                    cumulative += p
                    if cumulative >= r:
                        new_topic = t
                        break

                word_topics[doc_idx][word_pos] = new_topic
                doc_topic_counts[doc_idx][new_topic] += 1
                topic_word_counts[new_topic][word_idx] += 1
                topic_counts[new_topic] += 1

    # 计算主题-词分布和文档-主题分布
    topic_word_dist = []
    for t in range(n_topics):
        total = topic_counts[t] + vocab_size * 0.01
        topic_word_dist.append([(topic_word_counts[t][w] + 0.01) / total for w in range(vocab_size)])

    doc_topic_dist = []
    for doc_idx in range(len(documents)):
        total = sum(doc_topic_counts[doc_idx]) + n_topics * 0.1
        doc_topic_dist.append([(doc_topic_counts[doc_idx][t] + 0.1) / total for t in range(n_topics)])

    return topic_word_dist, doc_topic_dist, vocabulary


def get_top_words_per_topic(topic_word_dist: list, vocabulary: list, n_words: int = 5) -> list:
    """
    获取每个主题的 Top-N 关键词

    ━━━━━━━ 生活类比 ━━━━━━━
    就像给每个主题贴"标签"，看看这个主题主要讲什么。

    参数：
        topic_word_dist: 主题-词分布
        vocabulary: 词汇表
        n_words: 每个主题取前 N 个词

    返回：
        列表，每个元素是一个主题的关键词列表
    """
    top_words = []
    for t, dist in enumerate(topic_word_dist):
        # 按概率降序排列
        word_probs = [(vocabulary[i], dist[i]) for i in range(len(vocabulary))]
        word_probs.sort(key=lambda x: x[1], reverse=True)
        top = [w for w, p in word_probs[:n_words]]
        top_words.append(top)
    return top_words


# ==============================================================================
# 第四部分：sklearn 实现
# ==============================================================================
#
# 在实际项目中，我们通常使用 sklearn 库来实现聚类。
# sklearn 提供了完整的 K-Means 和各种聚类算法。
#
# ==============================================================================


def sklearn_kmeans_demo(documents: list, n_clusters: int = 3):
    """
    使用 sklearn 实现 K-Means 文本聚类

    ━━━━━━━ 生活类比 ━━━━━━━
    就像用洗衣机洗衣服 —— 你不需要手动搓，机器帮你搞定。
    sklearn 就是 NLP 的"洗衣机"，帮你处理各种复杂计算。

    参数：
        documents: 文档列表
        n_clusters: 聚类数量
    """
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score
    except ImportError:
        print("  [提示] 需要安装 sklearn: pip install scikit-learn")
        return None

    # 第一步：TF-IDF 向量化
    # TfidfVectorizer 自动完成分词、计算 TF-IDF
    vectorizer = TfidfVectorizer(analyzer='char', max_features=100)
    tfidf_matrix = vectorizer.fit_transform(documents)

    # 第二步：K-Means 聚类
    kmeans_model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans_model.fit_predict(tfidf_matrix)

    # 第三步：评估聚类效果
    if n_clusters > 1 and len(documents) > n_clusters:
        score = silhouette_score(tfidf_matrix, labels)
        print(f"  轮廓系数: {score:.4f}（越接近 1 越好）")

    # 第四步：输出每个簇的文档
    for cluster_id in range(n_clusters):
        cluster_docs = [documents[i] for i in range(len(documents)) if labels[i] == cluster_id]
        print(f"\n  簇 {cluster_id}（{len(cluster_docs)} 篇文档）:")
        for doc in cluster_docs[:3]:  # 只显示前 3 篇
            print(f"    - {doc[:30]}...")
        if len(cluster_docs) > 3:
            print(f"    ... 还有 {len(cluster_docs) - 3} 篇")

    return labels


def sklearn_lda_demo(documents: list, n_topics: int = 3):
    """
    使用 sklearn 实现 LDA 主题模型

    ━━━━━━━ 生活类比 ━━━━━━━
    就像让 AI 帮你整理图书馆 —— 它会告诉你：
    "这几本书都是关于科技的，那几本都是关于历史的。"

    参数：
        documents: 文档列表
        n_topics: 主题数量
    """
    try:
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.decomposition import LatentDirichletAllocation
    except ImportError:
        print("  [提示] 需要安装 sklearn: pip install scikit-learn")
        return None

    # 第一步：词频向量化（LDA 使用词频，不是 TF-IDF）
    vectorizer = CountVectorizer(analyzer='char', max_features=100)
    count_matrix = vectorizer.fit_transform(documents)

    # 第二步：LDA 主题模型
    lda_model = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=42,
        max_iter=20
    )
    doc_topic_dist = lda_model.fit_transform(count_matrix)

    # 第三步：输出每个主题的关键词
    feature_names = vectorizer.get_feature_names_out()
    print("\n  LDA 主题关键词:")
    for topic_idx, topic in enumerate(lda_model.components_):
        top_indices = topic.argsort()[-5:][::-1]
        top_words = [feature_names[i] for i in top_indices]
        print(f"    主题 {topic_idx}: {' '.join(top_words)}")

    # 第四步：输出每篇文档的主题分布
    print("\n  文档主题分布:")
    for i, doc in enumerate(documents):
        topic_probs = doc_topic_dist[i]
        dominant_topic = topic_probs.argmax()
        print(f"    文档 {i}: 主要主题={dominant_topic}, 分布={[f'{p:.2f}' for p in topic_probs]}")

    return doc_topic_dist


# ==============================================================================
# 第五部分：聚类评估
# ==============================================================================


def silhouette_score_manual(data: list, labels: list) -> float:
    """
    手动计算轮廓系数（Silhouette Score）

    ━━━━━━━ 生活类比 ━━━━━━━
    轮廓系数衡量"你在这个组里待得舒不舒服"：
    - a(i) = 你和同组人的平均距离（越小越好，说明你们很像）
    - b(i) = 你和最近的其他组的平均距离（越大越好，说明你们不同）
    - 轮廓系数 = (b - a) / max(a, b)

    值的范围是 -1 到 1：
    - 接近 1：聚类效果很好（组内紧密，组间分离）
    - 接近 0：聚类效果一般（边界模糊）
    - 接近 -1：聚类效果很差（可能分错了）

    参数：
        data: 数据列表
        labels: 簇标签列表

    返回：
        轮廓系数（-1 到 1）
    """
    n = len(data)
    if n <= 1:
        return 0.0

    # 获取所有簇
    clusters = set(labels)
    if len(clusters) <= 1:
        return 0.0

    scores = []
    for i in range(n):
        # a(i): 同簇内其他点的平均距离
        same_cluster = [j for j in range(n) if labels[j] == labels[i] and j != i]
        if same_cluster:
            a_i = sum(euclidean_distance(data[i], data[j]) for j in same_cluster) / len(same_cluster)
        else:
            a_i = 0

        # b(i): 到最近其他簇的平均距离
        b_i = float('inf')
        for c in clusters:
            if c == labels[i]:
                continue
            other_cluster = [j for j in range(n) if labels[j] == c]
            if other_cluster:
                avg_dist = sum(euclidean_distance(data[i], data[j]) for j in other_cluster) / len(other_cluster)
                b_i = min(b_i, avg_dist)

        if b_i == float('inf'):
            b_i = 0

        # 轮廓系数
        if max(a_i, b_i) == 0:
            s = 0
        else:
            s = (b_i - a_i) / max(a_i, b_i)
        scores.append(s)

    return sum(scores) / len(scores)


# ==============================================================================
# 主程序入口
# ==============================================================================

if __name__ == "__main__":

    print("""
    ╔══════════════════════════════════════════════════════╗
    ║        G-one NLP 学院 - 第十五章                      ║
    ║        文本聚类                                      ║
    ╚══════════════════════════════════════════════════════╝
    """)

    # 测试数据：几篇不同主题的文档
    documents = [
        "机器学习是人工智能的一个分支，它让计算机能够从数据中学习",
        "深度学习使用神经网络来模拟人脑的工作方式",
        "自然语言处理让计算机能够理解和生成人类语言",
        "今天股市大涨，上证指数突破三千点",
        "央行宣布降息，刺激经济增长",
        "投资者对市场前景持乐观态度",
        "春天是播种的季节，农民开始耕种田地",
        "秋天是收获的季节，稻谷金黄一片",
        "现代农业使用机械化提高生产效率",
    ]

    print("=" * 60)
    print("  1. 手动实现 TF-IDF")
    print("=" * 60)
    tfidf_matrix, vocabulary = compute_tfidf(documents)
    print(f"  词汇表大小: {len(vocabulary)}")
    print(f"  文档数量: {len(tfidf_matrix)}")
    print(f"  第一篇文档的 TF-IDF 向量（前 10 维）: {[round(x, 3) for x in tfidf_matrix[0][:10]]}")

    print("\n" + "=" * 60)
    print("  2. 手动实现 K-Means 聚类")
    print("=" * 60)
    labels, centroids = kmeans(tfidf_matrix, k=3, max_iterations=50)
    print(f"  聚类结果: {labels}")
    for cluster_id in range(3):
        cluster_docs = [documents[i] for i in range(len(documents)) if labels[i] == cluster_id]
        print(f"\n  簇 {cluster_id}:")
        for doc in cluster_docs:
            print(f"    - {doc[:25]}...")

    print("\n" + "=" * 60)
    print("  3. 手动实现 LDA 主题模型")
    print("=" * 60)
    topic_word_dist, doc_topic_dist, vocab = simple_lda(documents, n_topics=3, n_iterations=30)
    if topic_word_dist:
        top_words = get_top_words_per_topic(topic_word_dist, vocab, n_words=5)
        for t, words in enumerate(top_words):
            print(f"  主题 {t}: {' '.join(words)}")

    print("\n" + "=" * 60)
    print("  4. sklearn K-Means 聚类")
    print("=" * 60)
    sklearn_kmeans_demo(documents, n_clusters=3)

    print("\n" + "=" * 60)
    print("  5. sklearn LDA 主题模型")
    print("=" * 60)
    sklearn_lda_demo(documents, n_topics=3)

    # =============================================
    # 课程总结
    # =============================================
    """
    核心收获：
    - 文本向量化是聚类的前提 —— TF-IDF 把文字变成可计算的数字向量
    - K-Means 聚类的核心是"分配-更新"交替迭代 —— 像操场上分小组
    - LDA 主题模型用概率方法发现隐藏主题 —— 每篇文档是多个主题的混合

    常见陷阱：
    - K 值选择不当 —— K 太大导致碎片化，K 太小导致信息丢失，可用轮廓系数辅助判断
    - 初始中心点随机性 —— 不同初始化可能得到不同结果，K-Means++ 能改善这个问题
    - 忽略文本预处理 —— 停用词和标点会严重干扰聚类效果

    下节课预告：
    - 下一章我们将学习关键词提取与文本摘要 —— 从文档中自动提取最重要的信息
    """
