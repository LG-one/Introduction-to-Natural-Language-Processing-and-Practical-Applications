"""
==============================================================================
第十四章：文本分类（Text Classification）
==============================================================================
日期：2026-05-16

同学们好！前面我们学了分词、词向量等基础技术，
今天我们来学习 NLP 中最实用的任务之一 —— 文本分类。

----------------------------------------------------------------------
生活类比：文本分类就像邮局的分拣机器
----------------------------------------------------------------------

想象你是一个邮局的分拣员，每天有成千上万封信件需要分类：

  ┌──────────────────────────────────────────────┐
  │  信封上写着 "北京市海淀区..."  → 投入 北京 箱子 │
  │  信封上写着 "上海市浦东区..."  → 投入 上海 箱子 │
  │  信封上写着 "广州市天河区..."  → 投入 广州 箱子 │
  └──────────────────────────────────────────────┘

文本分类也是同样的道理：

  ┌──────────────────────────────────────────────┐
  │  "今天股市大涨"       → 财经                   │
  │  "梅西进球了"         → 体育                   │
  │  "新款iPhone发布"     → 科技                   │
  │  "电影评分9.5"        → 娱乐                   │
  └──────────────────────────────────────────────┘

关键问题：计算机怎么知道"今天股市大涨"属于"财经"？
→ 这就是我们要学的！

==============================================================================
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import numpy as np
import math
from collections import defaultdict, Counter


# ==============================================================================
# 第一部分：特征提取（Feature Extraction）
# ==============================================================================
#
# 机器学习模型不认识文字，只认识数字。
# 所以第一步是把文本转换为数字向量 —— 这叫"特征提取"。
#
# 常见的特征提取方法：
#
# 1. 词袋模型（Bag of Words, BoW）
#    生活类比：购物清单
#    "我 喜欢 吃 苹果" → {我:1, 喜欢:1, 吃:1, 苹果:1}
#    "我 喜欢 吃 香蕉" → {我:1, 喜欢:1, 吃:1, 香蕉:1}
#
#    优点：简单直观
#    缺点：丢失词序信息（"我吃苹果"和"苹果吃我"表示一样）
#
# 2. TF-IDF 特征
#    在词袋基础上，用 TF-IDF 加权
#    → 稀有词的权重更高
#
# ==============================================================================

class BagOfWords:
    """
    词袋模型（Bag of Words）

    ━━━━━━━ 生活类比 ━━━━━━━
    词袋模型就像购物清单：
    - 不管你买了什么东西、按什么顺序拿的
    - 只关心你最终买了几样东西、每样买了多少个

    "苹果 香蕉 苹果" → {苹果:2, 香蕉:1}

    ━━━━━━━ 工作原理 ━━━━━━━
    1. 建立词表（所有不重复的词）
    2. 每个文档表示为一个向量
    3. 向量的第i个分量 = 第i个词在文档中出现的次数
    """

    def __init__(self):
        """初始化词袋模型"""
        self.vocabulary = []          # 词表
        self.vocab_to_idx = {}        # 词到索引的映射
        self.is_fitted = False        # 是否已经训练

    def fit(self, documents: list):
        """
        从文档集合中建立词表

        参数：
            documents: 分词后的文档列表，如 [["我", "喜欢"], ["他", "喜欢", "吃"]]
        """
        word_set = set()
        for doc in documents:
            word_set.update(doc)

        self.vocabulary = sorted(word_set)
        self.vocab_to_idx = {w: i for i, w in enumerate(self.vocabulary)}
        self.is_fitted = True

        print(f"    词表大小: {len(self.vocabulary)}")

    def transform(self, documents: list) -> np.ndarray:
        """
        将文档转换为词袋向量

        参数：
            documents: 分词后的文档列表

        返回：
            (n_docs, vocab_size) 的矩阵
        """
        if not self.is_fitted:
            raise ValueError("请先调用 fit() 方法建立词表")

        n_docs = len(documents)
        vocab_size = len(self.vocabulary)
        matrix = np.zeros((n_docs, vocab_size))

        for i, doc in enumerate(documents):
            for word in doc:
                if word in self.vocab_to_idx:
                    matrix[i][self.vocab_to_idx[word]] += 1

        return matrix

    def fit_transform(self, documents: list) -> np.ndarray:
        """fit + transform 一步到位"""
        self.fit(documents)
        return self.transform(documents)

    def get_feature_names(self) -> list:
        """获取特征名（词表）"""
        return self.vocabulary


class TFIDFVectorizer:
    """
    TF-IDF 特征提取器

    ━━━━━━━ 与词袋模型的区别 ━━━━━━━
    词袋模型：词频（出现次数）
    TF-IDF：TF × IDF（出现次数 × 稀有度权重）

    生活类比：
    在一个班级里，"穿校服"是大家都做的事（IDF低），
    而"用左手写字"是少数人的特征（IDF高）。
    后者更能区分一个人！
    """

    def __init__(self):
        """初始化 TF-IDF 向量化器"""
        self.vocabulary = []
        self.vocab_to_idx = {}
        self.idf = {}  # 每个词的 IDF 值
        self.is_fitted = False

    def fit(self, documents: list):
        """
        从文档集合中学习 IDF 权重

        参数：
            documents: 分词后的文档列表
        """
        # 建立词表
        word_set = set()
        for doc in documents:
            word_set.update(doc)

        self.vocabulary = sorted(word_set)
        self.vocab_to_idx = {w: i for i, w in enumerate(self.vocabulary)}

        # 计算每个词的 IDF
        n_docs = len(documents)
        doc_freq = defaultdict(int)  # 包含每个词的文档数

        for doc in documents:
            unique_words = set(doc)
            for word in unique_words:
                doc_freq[word] += 1

        # IDF = log(总文档数 / 包含该词的文档数) + 1
        for word in self.vocabulary:
            df = doc_freq.get(word, 0)
            self.idf[word] = math.log(n_docs / (df + 1)) + 1

        self.is_fitted = True
        print(f"    词表大小: {len(self.vocabulary)}")

    def transform(self, documents: list) -> np.ndarray:
        """
        将文档转换为 TF-IDF 向量

        参数：
            documents: 分词后的文档列表

        返回：
            TF-IDF 矩阵 (n_docs, vocab_size)
        """
        if not self.is_fitted:
            raise ValueError("请先调用 fit() 方法")

        n_docs = len(documents)
        vocab_size = len(self.vocabulary)
        matrix = np.zeros((n_docs, vocab_size))

        for i, doc in enumerate(documents):
            # 统计词频
            word_counts = Counter(doc)
            doc_len = len(doc)

            for word, count in word_counts.items():
                if word in self.vocab_to_idx:
                    idx = self.vocab_to_idx[word]
                    tf = count / doc_len  # 归一化TF
                    matrix[i][idx] = tf * self.idf[word]

        return matrix

    def fit_transform(self, documents: list) -> np.ndarray:
        """fit + transform 一步到位"""
        self.fit(documents)
        return self.transform(documents)

    def get_feature_names(self) -> list:
        """获取特征名（词表）"""
        return self.vocabulary


# ==============================================================================
# 第二部分：朴素贝叶斯分类器（从零实现）
# ==============================================================================
#
# 朴素贝叶斯是最经典的文本分类算法之一。
#
# ━━━━━━━ 核心思想 ━━━━━━━
#
# 假设我们要判断一封邮件是不是垃圾邮件：
#
#   P(垃圾邮件 | 包含"免费") = P(包含"免费" | 垃圾邮件) × P(垃圾邮件)
#                              ─────────────────────────────────────────
#                                          P(包含"免费")
#
# 用更多的词：
#   P(垃圾邮件 | "免费", "中奖", "点击") ∝ P("免费"|垃圾) × P("中奖"|垃圾) × P("点击"|垃圾) × P(垃圾)
#
# ━━━━━━━ 生活类比 ━━━━━━━
#
# 你是一个医生，根据症状诊断疾病：
#
#   症状：发烧 + 咳嗽 + 流鼻涕
#
#   感冒的概率 = P(发烧|感冒) × P(咳嗽|感冒) × P(流鼻涕|感冒) × P(感冒)
#   肺炎的概率 = P(发烧|肺炎) × P(咳嗽|肺炎) × P(流鼻涕|肺炎) × P(肺炎)
#
#   哪个概率大就诊断为哪个病！
#
# ━━━━━━━ 为什么叫"朴素"？ ━━━━━━━
#
# 因为它假设所有特征（词）之间是独立的。
# 这个假设在现实中几乎不成立（比如"机器"和"学习"显然相关），
# 但神奇的是，即使假设不成立，朴素贝叶斯在实际任务中效果依然很好！
#
# ==============================================================================

class NaiveBayesClassifier:
    """
    朴素贝叶斯文本分类器

    ━━━━━━━ 算法步骤 ━━━━━━━

    训练阶段：
    1. 统计每个类别下每个词出现的次数
    2. 计算每个类别的先验概率 P(类别)
    3. 计算每个类别下每个词的条件概率 P(词|类别)

    预测阶段：
    1. 对于新文档，计算它属于每个类别的概率
    2. P(类别|文档) ∝ P(类别) × ∏ P(词i|类别)
    3. 选择概率最大的类别作为预测结果
    """

    def __init__(self, alpha: float = 1.0):
        """
        初始化朴素贝叶斯分类器

        参数：
            alpha: 拉普拉斯平滑系数（防止概率为0）
                   alpha=1 称为 Laplace 平滑
                   alpha<1 称为 Lidstone 平滑
        """
        self.alpha = alpha
        self.class_probs = {}      # P(类别)
        self.word_probs = {}       # P(词|类别)
        self.vocabulary = set()    # 词表
        self.classes = []          # 类别列表
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: list, feature_names: list = None):
        """
        训练朴素贝叶斯分类器

        ━━━━━━━ 训练过程 ━━━━━━━

        1. 统计每个类别的文档数 → 计算 P(类别)
        2. 统计每个类别下每个词的总出现次数 → 计算 P(词|类别)
        3. 使用拉普拉斯平滑避免零概率

        参数：
            X: 特征矩阵 (n_docs, n_features)，如词袋矩阵
            y: 标签列表，如 ["体育", "财经", "体育", ...]
            feature_names: 特征名列表（词表），用于展示
        """
        n_docs, n_features = X.shape
        self.classes = list(set(y))
        self.vocabulary = set(range(n_features))

        if feature_names:
            self.feature_names = feature_names
        else:
            self.feature_names = [f"特征{i}" for i in range(n_features)]

        # 统计每个类别的文档数
        class_counts = Counter(y)
        total_docs = n_docs

        # 计算先验概率 P(类别) = 类别文档数 / 总文档数
        for c in self.classes:
            self.class_probs[c] = class_counts[c] / total_docs

        # 统计每个类别下每个词的总出现次数
        # word_counts[c] 是一个数组，第i个元素 = 类别c中第i个词的总出现次数
        word_counts = {}
        for c in self.classes:
            # 找到属于类别c的文档
            class_mask = np.array([yi == c for yi in y])
            # 对这些文档的特征列求和，得到每个词在类别c中的总出现次数
            word_counts[c] = X[class_mask].sum(axis=0)

        # 计算条件概率 P(词i|类别c)
        # 使用拉普拉斯平滑：P(词i|类别c) = (count + alpha) / (total + alpha * vocab_size)
        for c in self.classes:
            total_words = word_counts[c].sum()  # 类别c中所有词的总出现次数
            vocab_size = n_features
            # 应用拉普拉斯平滑
            self.word_probs[c] = (word_counts[c] + self.alpha) / (total_words + self.alpha * vocab_size)

        self.is_fitted = True
        print(f"    训练完成！类别: {self.classes}")
        for c in self.classes:
            print(f"    P({c}) = {self.class_probs[c]:.3f}")

    def predict_single(self, x: np.ndarray) -> str:
        """
        预测单个文档的类别

        ━━━━━━━ 预测过程 ━━━━━━━
        对于每个类别，计算：
            log P(类别|文档) ∝ log P(类别) + Σ xi × log P(词i|类别)

        使用 log 是为了防止概率连乘导致下溢（太小变成0）

        参数：
            x: 单个文档的特征向量

        返回：
            预测的类别
        """
        best_class = None
        best_score = float('-inf')

        for c in self.classes:
            # 起始分数 = log P(类别)
            score = math.log(self.class_probs[c])

            # 加上每个词的贡献：xi × log P(词i|类别)
            # 只考虑出现过的词（xi > 0）
            for i in range(len(x)):
                if x[i] > 0:
                    score += x[i] * math.log(self.word_probs[c][i])

            if score > best_score:
                best_score = score
                best_class = c

        return best_class

    def predict(self, X: np.ndarray) -> list:
        """
        预测多个文档的类别

        参数：
            X: 特征矩阵 (n_docs, n_features)

        返回：
            预测的类别列表
        """
        if not self.is_fitted:
            raise ValueError("请先调用 fit() 方法训练模型")

        return [self.predict_single(X[i]) for i in range(len(X))]

    def score(self, X: np.ndarray, y: list) -> float:
        """
        计算准确率

        参数：
            X: 特征矩阵
            y: 真实标签

        返回：
            准确率 (0-1)
        """
        predictions = self.predict(X)
        correct = sum(1 for p, t in zip(predictions, y) if p == t)
        return correct / len(y)

    def show_top_features(self, n: int = 5):
        """
        显示每个类别最具代表性的词

        这些词在该类别中出现概率最高（相对于其他类别）
        """
        if not self.is_fitted:
            raise ValueError("请先调用 fit() 方法")

        print("\n  每个类别最具代表性的词：")
        for c in self.classes:
            # 获取该类别下概率最高的词
            top_indices = np.argsort(self.word_probs[c])[::-1][:n]
            words = [self.feature_names[i] for i in top_indices]
            probs = [self.word_probs[c][i] for i in top_indices]
            print(f"    {c}: {list(zip(words, [f'{p:.4f}' for p in probs]))}")


# ==============================================================================
# 第三部分：支持向量机（SVM）概念讲解
# ==============================================================================
#
# SVM（Support Vector Machine）是另一个非常强大的分类算法。
#
# ━━━━━━━ 核心思想 ━━━━━━━
#
# 在平面上有红点和蓝点，SVM 要找一条线把它们分开，
# 而且要让这条线离两边的点都尽可能远。
#
# 红点：● ● ●            蓝点：○ ○ ○
#
#     ● ● ●  |  ○ ○ ○        ← 这条线很好，离两边都很远
#            ↑
#        分割线（超平面）
#
#     ● ● ●○| ○ ○            ← 这条线不好，太靠近蓝点了
#
# ━━━━━━━ 生活类比 ━━━━━━━
#
# 想象你要在两个国家之间建一道墙（国界）：
#
#   方案一：墙紧贴A国 → A国的人容易"越界"
#   方案二：墙在正中间 → 两边都有足够的缓冲区
#
# SVM 选择方案二！找一条"最公平"的分割线。
#
# ━━━━━━━ 核函数 ━━━━━━━
#
# 有些数据用直线分不开，怎么办？
# 用"核函数"把数据映射到更高维的空间，就能分开了！
#
# 二维分不开：       映射到三维就分开了：
#   ● ● ○ ○           ●  ●
#   ● ○ ○ ●           ●    ○  ○
#                      ○    ○
#
# 常见的核函数：
# - 线性核（linear）：直接画直线
# - RBF核（径向基）：可以画曲线
# - 多项式核（poly）：画多项式曲线
#
# ==============================================================================

def explain_svm():
    """
    SVM 核心概念讲解（纯文字，不需要代码）

    这个函数用详细的文字说明 SVM 的工作原理，
    帮助同学们理解 SVM 的核心思想。
    """
    explanation = {
        "最大间隔": """
        SVM 的核心目标：找到一个分割超平面，使得它到最近的
        数据点（支持向量）的距离最大化。这个距离叫"间隔"（margin）。

        直觉：间隔越大，分类器越"自信"，泛化能力越强。
        """,

        "支持向量": """
        支持向量是离分割线最近的那些数据点。
        它们"支撑"着分割线的位置。
        去掉其他点不影响分割线，但去掉支持向量就会改变。

        生活类比：就像拔河比赛中站在最前面的那几个人，
        他们决定了绳子的位置。
        """,

        "软间隔": """
        现实中数据往往有噪声，不可能完美分开。
        软间隔允许少量数据点"越界"，但会受到惩罚。

        参数 C 控制惩罚力度：
        - C 很大：严格要求每个点都分对（可能过拟合）
        - C 较小：允许一些错误（更泛化）
        """,

        "核函数技巧": """
        低维空间分不开的数据，映射到高维空间就能分开。

        核函数不需要真正做映射，而是直接在低维空间计算
        高维空间的内积（"核技巧"），大大节省计算量。

        常用核函数：
        - linear: 线性核，适合线性可分的数据
        - rbf: 高斯核，最常用，适合大多数数据
        - poly: 多项式核，适合多项式关系的数据
        """,
    }

    return explanation


# ==============================================================================
# 第四部分：sklearn 文本分类流水线
# ==============================================================================
#
# 在实际项目中，我们通常使用 sklearn 来构建文本分类系统。
#
# sklearn 的流水线（Pipeline）把多个步骤串在一起：
#
#   原始文本 → 分词 → 特征提取 → 分类器 → 预测结果
#
# 就像工厂的生产线：
#   原材料 → 加工 → 质检 → 包装 → 成品
#
# ==============================================================================

def demo_sklearn_pipeline():
    """
    演示 sklearn 文本分类流水线

    这个函数尝试使用 sklearn 的各种组件来构建文本分类系统。
    如果 sklearn 未安装，则用文字说明用法。
    """
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.svm import SVC
        from sklearn.pipeline import Pipeline
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import classification_report
    except ImportError:
        print("  [提示] sklearn 未安装，请运行: pip install scikit-learn")
        print("  以下为 sklearn 文本分类用法说明：")
        print("""
    ━━━━━━━ sklearn 文本分类流水线 ━━━━━━━

    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.svm import SVC
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import train_test_split

    # 1. 准备数据
    texts = ["今天股市大涨", "梅西进球了", "新款iPhone发布", ...]
    labels = ["财经", "体育", "科技", ...]

    # 2. 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42
    )

    # 3. 构建流水线
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),    # 特征提取
        ('clf', MultinomialNB())          # 分类器
    ])

    # 4. 训练
    pipeline.fit(X_train, y_train)

    # 5. 预测
    predictions = pipeline.predict(X_test)

    # 6. 评估
    print(classification_report(y_test, predictions))
        """)
        return

    # 准备数据
    texts = [
        "今天股市大涨，投资者信心满满",
        "梅西在比赛中进球了，球队获胜",
        "新款iPhone发布，科技界震动",
        "这部电影评分高达9.5分",
        "央行宣布降息，利好股市",
        "CBA总决赛今晚开打",
        "人工智能技术取得重大突破",
        "明星离婚事件引发热议",
        "股票市场今天大幅波动",
        "世界杯预选赛中国队获胜",
        "新型芯片研发成功",
        "综艺节目收视率创新高",
    ]

    labels = [
        "财经", "体育", "科技", "娱乐",
        "财经", "体育", "科技", "娱乐",
        "财经", "体育", "科技", "娱乐",
    ]

    # 构建流水线
    print("  构建 sklearn 文本分类流水线...")

    # 朴素贝叶斯流水线
    nb_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', MultinomialNB())
    ])

    # SVM 流水线
    svm_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', SVC(kernel='linear'))
    ])

    # 训练和评估
    print("\n  --- 朴素贝叶斯分类器 ---")
    nb_pipeline.fit(texts, labels)
    predictions = nb_pipeline.predict(texts)
    correct = sum(1 for p, t in zip(predictions, labels) if p == t)
    print(f"  训练集准确率: {correct}/{len(labels)} = {correct / len(labels):.2%}")

    print("\n  --- SVM 分类器 ---")
    svm_pipeline.fit(texts, labels)
    predictions = svm_pipeline.predict(texts)
    correct = sum(1 for p, t in zip(predictions, labels) if p == t)
    print(f"  训练集准确率: {correct}/{len(labels)} = {correct / len(labels):.2%}")

    # 预测新文本
    new_texts = ["央行宣布降准降息", "C罗又进球了", "5G技术广泛应用"]
    print("\n  预测新文本：")
    for text in new_texts:
        nb_pred = nb_pipeline.predict([text])[0]
        svm_pred = svm_pipeline.predict([text])[0]
        print(f"    '{text}'")
        print(f"      朴素贝叶斯: {nb_pred}, SVM: {svm_pred}")


# ==============================================================================
# 第五部分：完整的文本分类实战
# ==============================================================================

class TextClassifier:
    """
    完整的文本分类器 —— 整合所有功能

    ━━━━━━━ 工作流程 ━━━━━━━

    1. 文本预处理（分词）
    2. 特征提取（词袋 或 TF-IDF）
    3. 训练分类器（朴素贝叶斯）
    4. 预测新文本
    """

    def __init__(self, method: str = "tfidf"):
        """
        初始化文本分类器

        参数：
            method: 特征提取方法，"bow"（词袋）或 "tfidf"
        """
        self.method = method

        if method == "bow":
            self.vectorizer = BagOfWords()
        elif method == "tfidf":
            self.vectorizer = TFIDFVectorizer()
        else:
            raise ValueError(f"未知方法: {method}")

        self.classifier = NaiveBayesClassifier()

    def _tokenize(self, text: str) -> list:
        """简单的分词（按字符切分）"""
        return list(text.replace(" ", ""))

    def train(self, texts: list, labels: list):
        """
        训练分类器

        参数：
            texts: 文本列表
            labels: 标签列表
        """
        print(f"\n  训练文本分类器（{self.method} + 朴素贝叶斯）：")

        # 分词
        tokenized_texts = [self._tokenize(text) for text in texts]

        # 特征提取
        print("  特征提取...")
        X = self.vectorizer.fit_transform(tokenized_texts)

        # 训练分类器
        print("  训练分类器...")
        self.classifier.fit(X, labels, self.vectorizer.get_feature_names())

    def predict(self, texts: list) -> list:
        """
        预测文本类别

        参数：
            texts: 文本列表

        返回：
            预测的类别列表
        """
        tokenized_texts = [self._tokenize(text) for text in texts]
        X = self.vectorizer.transform(tokenized_texts)
        return self.classifier.predict(X)

    def evaluate(self, texts: list, labels: list) -> float:
        """
        评估分类器

        参数：
            texts: 文本列表
            labels: 真实标签

        返回：
            准确率
        """
        tokenized_texts = [self._tokenize(text) for text in texts]
        X = self.vectorizer.transform(tokenized_texts)
        return self.classifier.score(X, labels)

    def show_analysis(self):
        """展示分类器分析结果"""
        self.classifier.show_top_features(n=5)


# ==============================================================================
# 演示函数
# ==============================================================================

def demo_feature_extraction():
    """演示特征提取"""
    print("=" * 60)
    print("特征提取演示")
    print("=" * 60)

    docs = [
        ["我", "喜欢", "吃", "苹果"],
        ["我", "喜欢", "喝", "牛奶"],
        ["他", "喜欢", "吃", "香蕉"],
    ]

    # 词袋模型
    print("\n  词袋模型（Bag of Words）：")
    bow = BagOfWords()
    X_bow = bow.fit_transform(docs)
    print(f"    词表: {bow.get_feature_names()}")
    print(f"    矩阵形状: {X_bow.shape}")
    for i, doc in enumerate(docs):
        print(f"    {doc} → {X_bow[i].astype(int).tolist()}")

    # TF-IDF
    print("\n  TF-IDF 特征：")
    tfidf = TFIDFVectorizer()
    X_tfidf = tfidf.fit_transform(docs)
    print(f"    矩阵形状: {X_tfidf.shape}")
    for i, doc in enumerate(docs):
        print(f"    {doc} → [{', '.join(f'{v:.3f}' for v in X_tfidf[i])}]")


def demo_naive_bayes():
    """演示朴素贝叶斯分类"""
    print("\n" + "=" * 60)
    print("朴素贝叶斯分类演示")
    print("=" * 60)

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
    print("\n  训练朴素贝叶斯分类器：")
    clf = NaiveBayesClassifier()
    clf.fit(X, labels, bow.get_feature_names())

    # 预测
    test_texts = [
        ["投资", "股市", "收益"],
        ["足球", "比赛", "进球"],
    ]
    print("\n  预测结果：")
    for text in test_texts:
        X_test = bow.transform([text])
        pred = clf.predict(X_test)
        print(f"    {text} → {pred[0]}")

    # 显示特征
    clf.show_top_features()


def demo_svm_concept():
    """演示 SVM 概念"""
    print("\n" + "=" * 60)
    print("支持向量机（SVM）概念")
    print("=" * 60)

    concepts = explain_svm()
    for name, explanation in concepts.items():
        print(f"\n  【{name}】")
        for line in explanation.strip().split("\n"):
            print(f"    {line.strip()}")

    print("""
    ━━━━━━━ SVM 在文本分类中的优势 ━━━━━━━

    1. 在高维空间表现好（文本特征通常是高维的）
    2. 不容易过拟合（有正则化）
    3. 核函数灵活（可以处理非线性问题）

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


def demo_sklearn():
    """演示 sklearn 流水线"""
    print("\n" + "=" * 60)
    print("sklearn 文本分类流水线")
    print("=" * 60)
    demo_sklearn_pipeline()


def demo_full_pipeline():
    """演示完整分类流水线"""
    print("\n" + "=" * 60)
    print("完整文本分类实战")
    print("=" * 60)

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
    ]
    labels = ["财经", "体育", "科技", "娱乐", "财经", "体育", "科技", "娱乐"]

    # 训练分类器
    clf = TextClassifier(method="tfidf")
    clf.train(texts, labels)

    # 评估
    accuracy = clf.evaluate(texts, labels)
    print(f"\n  训练集准确率: {accuracy:.2%}")

    # 展示分析
    clf.show_analysis()

    # 预测新文本
    new_texts = ["央行宣布降准降息", "C罗又进球了", "5G技术广泛应用"]
    predictions = clf.predict(new_texts)
    print("\n  预测新文本：")
    for text, pred in zip(new_texts, predictions):
        print(f"    '{text}' → {pred}")


# ==============================================================================
# 主程序入口
# ==============================================================================

if __name__ == "__main__":

    print("""
    ╔══════════════════════════════════════════════════════╗
    ║        G-one NLP 学院 - 第十四章                      ║
    ║        文本分类                                      ║
    ╚══════════════════════════════════════════════════════╝
    """)

    demo_feature_extraction()
    demo_naive_bayes()
    demo_svm_concept()
    demo_sklearn()
    demo_full_pipeline()

    # 总结
    print("\n" + "=" * 60)
    print("第十四章 总结")
    print("=" * 60)
    print("""
    本章我们学习了文本分类：

    [OK] 特征提取 — 词袋模型、TF-IDF
    [OK] 朴素贝叶斯 — 从零实现，理解原理
    [OK] SVM — 最大间隔分类器，核函数技巧
    [OK] sklearn 流水线 — 工业界的标准方案
    [OK] 完整实战 — 从数据到预测的全流程
    """)

    # =============================================
    # 下节课预告
    # =============================================
    """
    下节课我们将学习文本聚类（Text Clustering）：
    - K-Means 聚类算法 —— 把相似文本自动分成几组
    - LDA 主题模型 —— 发现文档中隐藏的主题
    - 聚类评估 —— 用轮廓系数衡量聚类效果
    """
