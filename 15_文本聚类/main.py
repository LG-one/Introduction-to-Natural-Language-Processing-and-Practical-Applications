import sys
sys.stdout.reconfigure(encoding='utf-8')

"""
==============================================================================
第十五章：文本聚类 — 完整演示
==============================================================================
G-one NLP 学院
日期：2026-05-16

运行方式：
    python main.py

前置知识：
    - Python 基础（列表、字典、函数）
    - 第七章：文本相似度
    - 第十四章：TF-IDF（可选）

本章内容：
    1. 文本向量化（TF-IDF）
    2. K-Means 聚类算法
    3. LDA 主题模型
    4. sklearn 实战
    5. 聚类效果评估
==============================================================================
"""

from text_clustering import (
    compute_tfidf,
    kmeans,
    kmeans_pp_init,
    simple_lda,
    get_top_words_per_topic,
    silhouette_score_manual,
    sklearn_kmeans_demo,
    sklearn_lda_demo,
)


def print_separator(title: str):
    """打印分隔线和标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def lesson_what_is_clustering():
    """第一部分：什么是文本聚类"""

    print_separator("15.1 什么是文本聚类？")

    print("""
    ┌─────────────────────────────────────────────────────────┐
    │                 文本聚类 = 自动分组                       │
    │                                                         │
    │   输入：一堆没有标签的文本                                │
    │   输出：自动分成几组，每组内的文本尽量相似                 │
    │                                                         │
    │   ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐           │
    │   │文1│ │文2│ │文3│ │文4│ │文5│ │文6│ │文7│  ← 原始文档 │
    │   └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘           │
    │      ↓     ↓     ↓     ↓     ↓     ↓     ↓             │
    │   ┌─────────────────┐ ┌──────────┐ ┌──────────┐        │
    │   │  簇0: 科技类     │ │  簇1: 财经│ │  簇2: 农业│        │
    │   │  文1, 文2, 文3   │ │  文4, 文5│ │  文6, 文7│        │
    │   └─────────────────┘ └──────────┘ └──────────┘        │
    └─────────────────────────────────────────────────────────┘

    聚类 vs 分类：
    ┌────────────┬─────────────────────────────────────────┐
    │  分类       │  先有标签，再分类（监督学习）             │
    │  聚类       │  没有标签，自动发现分组（无监督学习）     │
    └────────────┴─────────────────────────────────────────┘
    """)


def lesson_text_vectorization():
    """第二部分：文本向量化"""

    print_separator("15.2 文本向量化（TF-IDF）")

    print("""
    计算机不认识文字，只认识数字。
    所以聚类的第一步是把文本变成向量（一组数字）。

    TF-IDF 向量化：
    ┌──────────────────────────────────────────────────┐
    │  TF（词频）  = 某个词在文档中出现的频率            │
    │  IDF（逆文档频率）= 这个词有多"稀有"               │
    │  TF-IDF = TF × IDF                               │
    │                                                  │
    │  效果：常见词（的、是）权重低                      │
    │        独特词（量子、聚类）权重高                  │
    └──────────────────────────────────────────────────┘
    """)

    # 演示 TF-IDF 计算
    documents = [
        "机器学习是人工智能的重要分支",
        "深度学习使用神经网络处理数据",
        "股市今天大涨投资者很开心",
        "央行降息刺激经济增长",
    ]

    print("  示例文档:")
    for i, doc in enumerate(documents):
        print(f"    文档 {i}: {doc}")

    tfidf_matrix, vocabulary = compute_tfidf(documents)
    print(f"\n  词汇表大小: {len(vocabulary)}")
    print(f"  TF-IDF 矩阵维度: {len(tfidf_matrix)} x {len(tfidf_matrix[0])}")


def lesson_kmeans():
    """第三部分：K-Means 聚类"""

    print_separator("15.3 K-Means 聚类算法")

    print("""
    K-Means 是最经典的聚类算法：

    ┌─────────────────────────────────────────────────────┐
    │  步骤 1：选择 K 个初始中心点                          │
    │  步骤 2：把每个点分配到最近的中心                     │
    │  步骤 3：重新计算每个簇的中心                         │
    │  步骤 4：重复 2-3，直到中心不再变化                   │
    └─────────────────────────────────────────────────────┘

    K-Means++ 改进：
    - 普通 K-Means：随机选初始中心（可能选到"扎堆"的点）
    - K-Means++：尽量选"离已有中心远"的点（更均匀）

    K 值选择：
    - 肘部法则：画 K-SSE 曲线，找"拐点"
    - 轮廓系数：越接近 1 越好
    """)

    # 演示 K-Means
    documents = [
        "机器学习是人工智能的一个分支",
        "深度学习使用神经网络来模拟人脑",
        "自然语言处理让计算机理解语言",
        "今天股市大涨上证指数突破三千点",
        "央行宣布降息刺激经济增长",
        "投资者对市场前景持乐观态度",
        "春天是播种的季节农民开始耕种",
        "秋天是收获的季节稻谷金黄",
        "现代农业使用机械化提高效率",
    ]

    print("  示例文档:")
    for i, doc in enumerate(documents):
        print(f"    {i}: {doc}")

    tfidf_matrix, vocab = compute_tfidf(documents)

    print("\n  运行 K-Means (K=3):")
    labels, centroids = kmeans(tfidf_matrix, k=3, max_iterations=50)

    for cluster_id in range(3):
        cluster_docs = [documents[i] for i in range(len(documents)) if labels[i] == cluster_id]
        print(f"\n  簇 {cluster_id} ({len(cluster_docs)} 篇):")
        for doc in cluster_docs:
            print(f"    - {doc}")


def lesson_lda():
    """第四部分：LDA 主题模型"""

    print_separator("15.4 LDA 主题模型")

    print("""
    LDA（Latent Dirichlet Allocation）是一种"主题发现"算法：

    ┌─────────────────────────────────────────────────────┐
    │  核心假设：                                          │
    │  - 每篇文档是多个"主题"的混合                         │
    │  - 每个主题是一组"词"的概率分布                       │
    │                                                     │
    │  例如：                                              │
    │  《Python编程》→ 70% 编程 + 20% 教育 + 10% 科技      │
    │  《三国演义》→ 80% 历史 + 15% 文学 + 5% 战争         │
    └─────────────────────────────────────────────────────┘

    LDA 的应用：
    1. 新闻分类：自动发现新闻的主题
    2. 学术论文分析：发现研究热点
    3. 推荐系统：根据主题推荐相似文章
    4. 舆情监控：追踪热点话题
    """)

    # 演示 LDA
    documents = [
        "机器学习算法包括决策树和支持向量机",
        "深度学习的卷积神经网络用于图像识别",
        "自然语言处理使用循环神经网络",
        "股票市场今天表现强劲指数上涨",
        "债券收益率下降投资者转向安全资产",
        "央行货币政策影响通货膨胀",
        "水稻种植需要充足的水源和阳光",
        "农业机械化提高了粮食产量",
        "有机农业越来越受到消费者青睐",
    ]

    print("  示例文档:")
    for i, doc in enumerate(documents):
        print(f"    {i}: {doc}")

    topic_word_dist, doc_topic_dist, vocab = simple_lda(documents, n_topics=3, n_iterations=50)

    if topic_word_dist:
        print("\n  LDA 发现的主题关键词:")
        top_words = get_top_words_per_topic(topic_word_dist, vocab, n_words=6)
        for t, words in enumerate(top_words):
            print(f"    主题 {t}: {' '.join(words)}")


def lesson_sklearn_demo():
    """第五部分：sklearn 实战"""

    print_separator("15.5 sklearn 实战")

    documents = [
        "机器学习是人工智能的一个分支",
        "深度学习使用神经网络来模拟人脑",
        "自然语言处理让计算机理解语言",
        "今天股市大涨上证指数突破三千点",
        "央行宣布降息刺激经济增长",
        "投资者对市场前景持乐观态度",
        "春天是播种的季节农民开始耕种",
        "秋天是收获的季节稻谷金黄",
        "现代农业使用机械化提高效率",
    ]

    print("  sklearn K-Means 聚类:")
    sklearn_kmeans_demo(documents, n_clusters=3)

    print("\n  sklearn LDA 主题模型:")
    sklearn_lda_demo(documents, n_topics=3)


def lesson_evaluation():
    """第六部分：聚类评估"""

    print_separator("15.6 聚类效果评估")

    print("""
    如何评价聚类效果好不好？

    ┌─────────────────────────────────────────────────────┐
    │  1. 轮廓系数（Silhouette Score）                     │
    │     - 范围：-1 到 1                                 │
    │     - 越接近 1：组内紧密，组间分离                    │
    │     - 越接近 -1：可能分错了                          │
    │                                                     │
    │  2. 肘部法则（Elbow Method）                         │
    │     - 画 K vs 总距离的曲线                           │
    │     - 找"拐点"作为最佳 K 值                          │
    │                                                     │
    │  3. 人工评估                                         │
    │     - 看看分组结果是否符合直觉                       │
    │     - 最终还是要靠人的判断                           │
    └─────────────────────────────────────────────────────┘
    """)

    # 演示轮廓系数计算
    data = [
        [1, 1], [1.5, 1.5], [1, 1.5],  # 簇 0
        [5, 5], [5.5, 5], [5, 5.5],    # 簇 1
        [9, 1], [9.5, 1], [9, 0.5],    # 簇 2
    ]
    labels = [0, 0, 0, 1, 1, 1, 2, 2, 2]

    score = silhouette_score_manual(data, labels)
    print(f"  示例数据的轮廓系数: {score:.4f}")


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

    lesson_what_is_clustering()
    lesson_text_vectorization()
    lesson_kmeans()
    lesson_lda()
    lesson_sklearn_demo()
    lesson_evaluation()

    # 课程总结
    print("\n" + "=" * 60)
    print("  第十五章 总结")
    print("=" * 60)
    print("""
    [OK] 文本向量化 — TF-IDF 把文本变成数字向量
    [OK] K-Means 聚类 — 经典的划分聚类算法
    [OK] K-Means++ — 更聪明的初始化方法
    [OK] LDA 主题模型 — 发现隐藏主题
    [OK] sklearn 实战 — 使用现成的工具库
    [OK] 聚类评估 — 轮廓系数衡量聚类效果
    """)

    print("-" * 60)
    print("  下节预告：第十六章 — 关键词与摘要")
    print("-" * 60)
    print("""
    下一章我们将学习：
    - TF-IDF 关键词提取
    - TextRank 算法
    - 抽取式文本摘要

    预习建议：
    - 思考：如何从一篇文章中自动提取最重要的句子？
    - 了解 PageRank 算法的基本思想
    """)
