import sys
sys.stdout.reconfigure(encoding='utf-8')

"""
==============================================================================
第十四章：文本分类 — 完整演示
==============================================================================
G-one NLP 学院
日期：2026-05-16
==============================================================================
"""

try:
    import numpy as np
except ImportError:
    print("本课需要 numpy 库，请运行：pip install numpy")
    print("安装后重新运行本文件即可。")
    exit(1)

from text_classifier import (
    BagOfWords, TFIDFVectorizer, NaiveBayesClassifier,
    TextClassifier, explain_svm, demo_sklearn_pipeline
)


def print_separator(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def lesson_feature_extraction():
    """14.1 特征提取：把文本变成数字"""
    print_separator("14.1 特征提取 — 把文本变成数字")

    print("""
    机器学习模型不认识文字，只认识数字！
    所以第一步是把文本转换为数字向量。

    ━━━━━━━ 词袋模型（Bag of Words）━━━━━━━
    生活类比：购物清单
    "苹果 香蕉 苹果" → {苹果:2, 香蕉:1}

    ━━━━━━━ TF-IDF 特征 ━━━━━━━
    在词袋基础上，用 TF-IDF 加权
    稀有词的权重更高，更能区分文档
    """)

    # 词袋模型演示
    docs = [
        ["我", "喜欢", "吃", "苹果"],
        ["我", "喜欢", "喝", "牛奶"],
        ["他", "喜欢", "吃", "香蕉"],
    ]

    print("\n  词袋模型演示：")
    bow = BagOfWords()
    X_bow = bow.fit_transform(docs)
    print(f"    词表: {bow.get_feature_names()}")
    for i, doc in enumerate(docs):
        print(f"    {doc} → {X_bow[i].astype(int).tolist()}")

    # TF-IDF 演示
    print("\n  TF-IDF 特征演示：")
    tfidf = TFIDFVectorizer()
    X_tfidf = tfidf.fit_transform(docs)
    for i, doc in enumerate(docs):
        print(f"    {doc} → [{', '.join(f'{v:.3f}' for v in X_tfidf[i])}]")


def lesson_naive_bayes():
    """14.2 朴素贝叶斯分类器"""
    print_separator("14.2 朴素贝叶斯 — 最经典的分类算法")

    print("""
    核心思想：根据特征出现的概率判断类别

    ━━━━━━━ 生活类比 ━━━━━━━
    医生根据症状诊断疾病：
    症状：发烧 + 咳嗽 + 流鼻涕

    P(感冒|症状) ∝ P(发烧|感冒) × P(咳嗽|感冒) × P(感冒)
    P(肺炎|症状) ∝ P(发烧|肺炎) × P(咳嗽|肺炎) × P(肺炎)

    哪个概率大就诊断为哪个！

    ━━━━━━━ 为什么叫"朴素"？ ━━━━━━━
    因为它假设所有特征（词）之间是独立的。
    这个假设在现实中不成立（"机器"和"学习"相关），
    但神奇的是，效果依然很好！
    """)

    # 准备数据
    texts = [
        ["股市", "大涨", "投资", "收益"],
        ["股票", "下跌", "风险", "投资"],
        ["足球", "比赛", "进球", "胜利"],
        ["篮球", "比赛", "得分", "冠军"],
        ["股市", "行情", "投资", "分析"],
        ["足球", "联赛", "球队", "比赛"],
    ]
    labels = ["财经", "财经", "体育", "体育", "财经", "体育"]

    # 特征提取
    bow = BagOfWords()
    X = bow.fit_transform(texts)

    # 训练分类器
    print("  训练朴素贝叶斯分类器：")
    clf = NaiveBayesClassifier()
    clf.fit(X, labels, bow.get_feature_names())

    # 预测
    test_texts = [
        ["投资", "股市", "收益"],
        ["足球", "比赛", "进球"],
        ["股市", "比赛", "投资"],  # 混合特征
    ]
    print("\n  预测结果：")
    for text in test_texts:
        X_test = bow.transform([text])
        pred = clf.predict(X_test)
        print(f"    {text} → {pred[0]}")

    # 显示特征
    clf.show_top_features()


def lesson_svm():
    """14.3 支持向量机（SVM）"""
    print_separator("14.3 支持向量机 — 最大间隔分类器")

    print("""
    SVM 的核心目标：找一条线把数据分开，
    而且让这条线离两边的点都尽可能远。

    ━━━━━━━ 生活类比 ━━━━━━━
    在两个国家之间建墙：
    - 墙紧贴A国 → A国的人容易"越界"
    - 墙在正中间 → 两边都有足够的缓冲区
    SVM 选择"最公平"的方案！

    ━━━━━━━ 核函数 ━━━━━━━
    有些数据用直线分不开 → 用核函数映射到高维空间
    """)

    concepts = explain_svm()
    for name, explanation in concepts.items():
        print(f"\n  【{name}】")
        for line in explanation.strip().split("\n"):
            print(f"    {line.strip()}")

    print("""
    ━━━━━━━ SVM vs 朴素贝叶斯 ━━━━━━━

    ┌────────────────┬──────────────┬──────────────┐
    │                │ 朴素贝叶斯    │ SVM          │
    ├────────────────┼──────────────┼──────────────┤
    │ 训练速度       │ 非常快        │ 较慢          │
    │ 预测速度       │ 非常快        │ 较快          │
    │ 小数据集       │ 效果好        │ 效果好        │
    │ 大数据集       │ 效果一般      │ 效果好        │
    │ 可解释性       │ 高            │ 低            │
    │ 适合场景       │ 垃圾邮件过滤  │ 文本分类      │
    └────────────────┴──────────────┴──────────────┘
    """)


def lesson_sklearn_pipeline():
    """14.4 sklearn 文本分类流水线"""
    print_separator("14.4 sklearn 流水线 — 工业级方案")

    print("""
    在实际项目中，用 sklearn 构建文本分类系统：

    ━━━━━━━ 流水线 ━━━━━━━
    原始文本 → 分词 → 特征提取 → 分类器 → 预测结果

    就像工厂生产线：
    原材料 → 加工 → 质检 → 包装 → 成品

    ━━━━━━━ 核心代码 ━━━━━━━
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),    # 特征提取
        ('clf', MultinomialNB())          # 分类器
    ])
    pipeline.fit(X_train, y_train)        # 训练
    predictions = pipeline.predict(X_test) # 预测
    """)

    demo_sklearn_pipeline()


def lesson_full_practice():
    """14.5 完整文本分类实战"""
    print_separator("14.5 完整实战 — 从数据到预测")

    print("""
    现在让我们把所有学到的知识串起来，
    完成一个完整的文本分类项目！
    """)

    # 准备数据
    texts = [
        "今天股市大涨投资者信心满满",
        "梅西在比赛中进球了球队获胜",
        "新款iPhone发布科技界震动",
        "这部电影评分高达9.5分",
        "央行宣布降息利好股市",
        "CBA总决赛今晚开打",
        "人工智能技术取得重大突破",
        "明星离婚事件引发热议",
        "股票市场今天大幅波动",
        "世界杯预选赛中国队获胜",
        "新型芯片研发成功",
        "综艺节目收视率创新高",
    ]
    labels = ["财经", "体育", "科技", "娱乐", "财经", "体育",
              "科技", "娱乐", "财经", "体育", "科技", "娱乐"]

    # 训练分类器
    clf = TextClassifier(method="tfidf")
    clf.train(texts, labels)

    # 评估
    accuracy = clf.evaluate(texts, labels)
    print(f"\n  训练集准确率: {accuracy:.2%}")

    # 展示特征
    clf.show_analysis()

    # 预测新文本
    new_texts = [
        "央行宣布降准降息",
        "C罗又进球了",
        "5G技术广泛应用",
        "新电影票房破纪录",
    ]
    predictions = clf.predict(new_texts)
    print("\n  预测新文本：")
    for text, pred in zip(new_texts, predictions):
        print(f"    '{text}' → {pred}")


# ==============================================================================
# 主程序
# ==============================================================================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║          G-one NLP 学院 - 第十四章                        ║
    ║          文本分类                                        ║
    ╚══════════════════════════════════════════════════════════╝

    ████████╗███████╗██╗  ██╗████████╗ ██████╗██╗      █████╗ ███████╗███████╗
    ╚══██╔══╝██╔════╝╚██╗██╔╝╚══██╔══╝██╔════╝██║     ██╔══██╗██╔════╝██╔════╝
       ██║   █████╗   ╚███╔╝    ██║   ██║     ██║     ███████║███████╗███████╗
       ██║   ██╔══╝   ██╔██╗    ██║   ██║     ██║     ██╔══██║╚════██║╚════██║
       ██║   ███████╗██╔╝ ██╗   ██║   ╚██████╗███████╗██║  ██║███████║███████║
       ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝
    """)

    lesson_feature_extraction()
    lesson_naive_bayes()
    lesson_svm()
    lesson_sklearn_pipeline()
    lesson_full_practice()

    print("\n" + "=" * 60)
    print("  第十四章 总结")
    print("=" * 60)
    print("""
    [OK] 特征提取 — 词袋模型（购物清单）、TF-IDF
    [OK] 朴素贝叶斯 — 根据特征概率判断类别（医生诊断）
    [OK] SVM — 最大间隔分类器（两国之间建墙）
    [OK] sklearn 流水线 — 从文本到预测的一站式方案
    [OK] 完整实战 — 端到端的文本分类项目
    """)

    print("-" * 60)
    print("  下节预告：第十五章 — 文本聚类")
    print("-" * 60)
