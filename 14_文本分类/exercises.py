import sys
sys.stdout.reconfigure(encoding='utf-8')

"""
==============================================================================
第十四章：文本分类 — 练习题
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
import math


# ==============================================================================
# 练习 1：词袋模型实现
# ==============================================================================

def exercise_1_bag_of_words(documents: list) -> tuple:
    """
    练习 1：实现简单的词袋模型

    ━━━━━━━ 提示 ━━━━━━━
    1. 遍历所有文档，建立词表（所有不重复的词）
    2. 词表排序
    3. 将每个文档转换为向量：
       向量的第i个分量 = 第i个词在文档中出现的次数

    例如：
    输入: [["我", "喜欢", "苹果"], ["我", "喜欢", "香蕉"]]
    词表: ["喜欢", "我", "苹果", "香蕉"]  (排序后)
    输出: [[1, 1, 1, 0], [1, 1, 0, 1]]

    参数：
        documents: 分词后的文档列表

    返回：
        (词表列表, 特征矩阵)
        词表列表: ["词1", "词2", ...]
        特征矩阵: (n_docs, vocab_size) 的列表
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # # 建立词表
    # word_set = set()
    # for doc in documents:
    #     word_set.update(doc)
    # vocab = sorted(word_set)
    # word_to_idx = {w: i for i, w in enumerate(vocab)}
    #
    # # 转换为向量
    # matrix = []
    # for doc in documents:
    #     vec = [0] * len(vocab)
    #     for word in doc:
    #         if word in word_to_idx:
    #             vec[word_to_idx[word]] += 1
    #     matrix.append(vec)
    #
    # return vocab, matrix
    pass


def test_exercise_1():
    print("\n" + "=" * 60)
    print("练习 1：词袋模型实现")
    print("=" * 60)

    docs = [["我", "喜欢", "苹果"], ["我", "喜欢", "香蕉"]]
    result = exercise_1_bag_of_words(docs)

    if result is None:
        print("[未完成] 请实现 exercise_1_bag_of_words 函数")
        return False

    vocab, matrix = result

    # 检查词表
    expected_vocab = ["喜欢", "我", "苹果", "香蕉"]
    if vocab != expected_vocab:
        print(f"[错误] 期望词表 {expected_vocab}, 实际 {vocab}")
        return False

    # 检查矩阵
    expected_matrix = [[1, 1, 1, 0], [1, 1, 0, 1]]
    if matrix == expected_matrix:
        print(f"[正确] 词表: {vocab}")
        for i, doc in enumerate(docs):
            print(f"  {doc} → {matrix[i]}")
        return True
    else:
        print(f"[错误] 期望矩阵 {expected_matrix}, 实际 {matrix}")
        return False


# ==============================================================================
# 练习 2：朴素贝叶斯预测
# ==============================================================================

def exercise_2_naive_bayes_predict(class_probs: dict,
                                   word_probs: dict,
                                   feature_vector: list) -> str:
    """
    练习 2：实现朴素贝叶斯的预测（单个样本）

    ━━━━━━━ 提示 ━━━━━━━
    对于每个类别，计算：
        score = log(P(类别)) + Σ xi × log(P(词i|类别))

    选择分数最高的类别作为预测结果。

    注意：
    - 使用 math.log() 计算对数
    - 只考虑 xi > 0 的特征（词出现过才计算）
    - class_probs = {"财经": 0.5, "体育": 0.5}
    - word_probs = {"财经": [0.1, 0.3, ...], "体育": [0.3, 0.1, ...]}

    参数：
        class_probs: 类别先验概率 {类别: 概率}
        word_probs: 条件概率 {类别: [P(词1|类别), P(词2|类别), ...]}
        feature_vector: 特征向量 [出现次数1, 出现次数2, ...]

    返回：
        预测的类别
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # best_class = None
    # best_score = float('-inf')
    # for c in class_probs:
    #     score = math.log(class_probs[c])
    #     for i, xi in enumerate(feature_vector):
    #         if xi > 0:
    #             score += xi * math.log(word_probs[c][i])
    #     if score > best_score:
    #         best_score = score
    #         best_class = c
    # return best_class
    pass


def test_exercise_2():
    print("\n" + "=" * 60)
    print("练习 2：朴素贝叶斯预测")
    print("=" * 60)

    # 假设词表: ["投资", "足球", "比赛"]
    class_probs = {"财经": 0.5, "体育": 0.5}
    word_probs = {
        "财经": [0.4, 0.1, 0.1],  # "投资"概率高
        "体育": [0.1, 0.4, 0.4],  # "足球"和"比赛"概率高
    }

    test_cases = [
        ([1, 0, 0], "财经"),   # 只有"投资"→ 财经
        ([0, 1, 1], "体育"),   # "足球"+"比赛"→ 体育
        ([1, 1, 1], None),     # 混合特征（不确定）
    ]

    all_correct = True
    for features, expected in test_cases:
        result = exercise_2_naive_bayes_predict(class_probs, word_probs, features)
        if result is None:
            print("[未完成] 请实现 exercise_2_naive_bayes_predict 函数")
            return False
        if expected is not None:
            if result == expected:
                print(f"  [正确] 特征{features} → {result}")
            else:
                print(f"  [错误] 特征{features} → 期望 {expected}, 实际 {result}")
                all_correct = False
        else:
            print(f"  [信息] 特征{features} → {result}（混合特征，接受任何结果）")

    return all_correct


# ==============================================================================
# 练习 3：计算 TF-IDF
# ==============================================================================

def exercise_3_tfidf_matrix(documents: list) -> list:
    """
    练习 3：给定分词后的文档列表，计算 TF-IDF 矩阵

    ━━━━━━━ 提示 ━━━━━━━
    1. 建立词表
    2. 对每个文档，计算每个词的 TF-IDF：
       TF = 词在文档中出现的次数 / 文档总词数
       IDF = log(总文档数 / 包含该词的文档数 + 1) + 1
       TF-IDF = TF × IDF
    3. 返回 TF-IDF 矩阵

    参数：
        documents: 分词后的文档列表
                   例如: [["我", "喜欢", "苹果"], ["他", "喜欢", "香蕉"]]

    返回：
        (词表, TF-IDF矩阵)
        词表: 排序后的词列表
        TF-IDF矩阵: (n_docs, vocab_size) 的列表
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # # 建立词表
    # word_set = set()
    # for doc in documents:
    #     word_set.update(doc)
    # vocab = sorted(word_set)
    # word_to_idx = {w: i for i, w in enumerate(vocab)}
    #
    # n_docs = len(documents)
    #
    # # 计算文档频率
    # doc_freq = {}
    # for word in vocab:
    #     doc_freq[word] = sum(1 for doc in documents if word in doc)
    #
    # # 计算 TF-IDF 矩阵
    # matrix = []
    # for doc in documents:
    #     vec = [0.0] * len(vocab)
    #     word_counts = {}
    #     for w in doc:
    #         word_counts[w] = word_counts.get(w, 0) + 1
    #     for word, count in word_counts.items():
    #         if word in word_to_idx:
    #             tf = count / len(doc)
    #             idf = math.log(n_docs / (doc_freq[word] + 1)) + 1
    #             vec[word_to_idx[word]] = tf * idf
    #     matrix.append(vec)
    #
    # return vocab, matrix
    pass


def test_exercise_3():
    print("\n" + "=" * 60)
    print("练习 3：计算 TF-IDF 矩阵")
    print("=" * 60)

    docs = [["我", "喜欢", "苹果"], ["他", "喜欢", "香蕉"]]
    result = exercise_3_tfidf_matrix(docs)

    if result is None:
        print("[未完成] 请实现 exercise_3_tfidf_matrix 函数")
        return False

    vocab, matrix = result

    # 检查基本结构
    if len(vocab) != 5 or len(matrix) != 2:
        print(f"[错误] 词表大小应为5，矩阵行数应为2")
        return False

    # 检查 TF-IDF 值是否合理（都大于0）
    all_positive = all(v >= 0 for row in matrix for v in row)
    # 检查共同词"喜欢"在两个文档中都有值
    like_idx = vocab.index("喜欢") if "喜欢" in vocab else -1

    if like_idx >= 0 and matrix[0][like_idx] > 0 and matrix[1][like_idx] > 0:
        print(f"[正确] 词表: {vocab}")
        for i, doc in enumerate(docs):
            print(f"  {doc} → [{', '.join(f'{v:.3f}' for v in matrix[i])}]")
        return True
    else:
        print(f"[错误] TF-IDF 矩阵值不正确")
        print(f"  词表: {vocab}")
        print(f"  矩阵: {matrix}")
        return False


# ==============================================================================
# 主程序
# ==============================================================================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║          G-one NLP 学院 - 第十四章 练习                    ║
    ║          文本分类                                        ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    results = []
    results.append(("练习1: 词袋模型", test_exercise_1()))
    results.append(("练习2: 朴素贝叶斯预测", test_exercise_2()))
    results.append(("练习3: TF-IDF矩阵", test_exercise_3()))

    print("\n" + "=" * 60)
    print("  练习清单")
    print("=" * 60)
    for name, passed in results:
        status = "[完成]" if passed else "[未完成]"
        print(f"  {status} {name}")

    completed = sum(1 for _, p in results if p)
    print(f"\n  完成率: {completed}/{len(results)}")
