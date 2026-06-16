import sys
sys.stdout.reconfigure(encoding='utf-8')

"""
==============================================================================
第十五章：文本聚类 — 练习题
==============================================================================
G-one NLP 学院
日期：2026-05-16

本章练习：
    1. 实现 TF-IDF 计算
    2. 实现简单的 K-Means 聚类
    3. 实现聚类结果评估

运行方式：
    python exercises.py

提示：
    - 每个练习都有详细的提示，按照提示一步步来
    - 先自己写，写不出来再看注释中的参考答案
    - 运行后会自动检查你的答案是否正确
==============================================================================
"""

import math


# ==============================================================================
# 练习 1：实现 TF-IDF 计算
# ==============================================================================

def exercise_1_tfidf(documents: list, target_word: str) -> list:
    """
    练习 1：计算目标词在每篇文档中的 TF-IDF 值

    ━━━━━━━ 生活类比 ━━━━━━━
    想象你是一个图书管理员，要判断"机器"这个词在每篇文章里有多重要。
    - 如果"机器"在这篇文章里出现很多次 → TF 高
    - 如果"机器"只在少数文章里出现 → IDF 高
    - TF-IDF = TF × IDF

    ━━━━━━━ 提示 ━━━━━━━
    1. 计算 TF：目标词在文档中出现的次数 / 文档总词数
       - 用 char_count = document.count(target_word) 统计出现次数
       - 用 total = len([c for c in document if c.strip()]) 统计总字符数
       - TF = char_count / total（如果 total > 0）

    2. 计算 IDF：log(总文档数 / 包含目标词的文档数)
       - n_docs = len(documents)
       - doc_with_word = sum(1 for doc in documents if target_word in doc)
       - IDF = math.log((n_docs + 1) / (doc_with_word + 1)) + 1

    3. TF-IDF = TF × IDF

    4. 返回每篇文档的 TF-IDF 值列表

    参数：
        documents: 文档列表（字符串列表）
        target_word: 目标词（单个字符或词）

    返回：
        列表，每个元素是该文档中目标词的 TF-IDF 值

    示例：
        >>> docs = ["机器学习", "深度学习", "机器学习算法"]
        >>> exercise_1_tfidf(docs, "机器")
        [0.3..., 0.0, 0.2...]  （近似值）
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # n_docs = len(documents)
    # doc_with_word = sum(1 for doc in documents if target_word in doc)
    # idf = math.log((n_docs + 1) / (doc_with_word + 1)) + 1
    #
    # result = []
    # for doc in documents:
    #     total = len([c for c in doc if c.strip()])
    #     if total == 0:
    #         result.append(0.0)
    #         continue
    #     tf = doc.count(target_word) / total
    #     result.append(tf * idf)
    # return result
    pass


def test_exercise_1():
    """测试练习 1"""
    print("\n" + "=" * 60)
    print("练习 1：计算 TF-IDF")
    print("=" * 60)

    documents = ["机器学习入门", "深度学习基础", "机器学习算法详解"]
    target_word = "机"
    result = exercise_1_tfidf(documents, target_word)

    if result is None:
        print("[未完成] 请实现 exercise_1_tfidf 函数")
        return False

    if not isinstance(result, list) or len(result) != 3:
        print(f"[错误] 返回值应该是长度为 3 的列表，实际: {result}")
        return False

    # 检查：包含"机"的文档 TF-IDF 应该 > 0，不包含的应该是 0
    if result[0] > 0 and result[1] == 0.0 and result[2] > 0:
        print(f"[正确] 输入: 文档={documents}, 目标词='{target_word}'")
        print(f"       TF-IDF: {[round(x, 4) for x in result]}")
        print(f"       文档 1 包含'{target_word}'，TF-IDF={result[0]:.4f}")
        print(f"       文档 2 不包含'{target_word}'，TF-IDF=0.0")
        return True
    else:
        print(f"[错误] 输入: 文档={documents}, 目标词='{target_word}'")
        print(f"       期望: 文档 1 和 3 的 TF-IDF > 0，文档 2 的 TF-IDF = 0")
        print(f"       实际: {[round(x, 4) for x in result]}")
        return False


# ==============================================================================
# 练习 2：实现简单的 K-Means 聚类
# ==============================================================================

def exercise_2_kmeans(data: list, k: int, max_iterations: int = 50) -> list:
    """
    练习 2：实现简单的 K-Means 聚类算法

    ━━━━━━━ 生活类比 ━━━━━━━
    想象你是一个班主任，要把学生分成 K 个学习小组：
    1. 随机选 K 个学生当"组长"
    2. 每个学生选离自己最近的组长
    3. 每组重新选"最中间"的人当新组长
    4. 重复，直到组长不再换人

    ━━━━━━━ 提示 ━━━━━━━
    1. 初始化：随机选择 K 个点作为中心
       - import random
       - indices = random.sample(range(len(data)), k)
       - centroids = [data[i][:] for i in indices]

    2. 循环 max_iterations 次：
       a. 分配：对每个点，计算它到每个中心的距离
          - 距离 = sqrt(sum((a-b)^2))
          - 选择最近的中心，记录标签
       b. 更新：对每个簇，计算簇内所有点的平均值作为新中心

    3. 如果标签不再变化，提前退出循环

    4. 返回每个点的标签列表

    参数：
        data: 数据列表，每个元素是 [x, y] 坐标
        k: 聚类数量
        max_iterations: 最大迭代次数

    返回：
        标签列表，每个元素是 0 到 k-1 的整数
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # import random
    # n = len(data)
    # indices = random.sample(range(n), min(k, n))
    # centroids = [data[i][:] for i in indices]
    # labels = [0] * n
    #
    # for _ in range(max_iterations):
    #     new_labels = []
    #     for point in data:
    #         distances = []
    #         for c in centroids:
    #             d = math.sqrt(sum((a - b) ** 2 for a, b in zip(point, c)))
    #             distances.append(d)
    #         new_labels.append(distances.index(min(distances)))
    #     if new_labels == labels:
    #         break
    #     labels = new_labels
    #
    #     for j in range(k):
    #         cluster_points = [data[i] for i in range(n) if labels[i] == j]
    #         if cluster_points:
    #             dim = len(cluster_points[0])
    #             centroids[j] = [sum(p[d] for p in cluster_points) / len(cluster_points) for d in range(dim)]
    #
    # return labels
    pass


def test_exercise_2():
    """测试练习 2"""
    print("\n" + "=" * 60)
    print("练习 2：K-Means 聚类")
    print("=" * 60)

    # 明显分为 3 簇的数据
    data = [
        [1, 1], [1.5, 1.5], [1, 2],      # 簇 0（左下）
        [5, 5], [5.5, 5], [5, 5.5],       # 簇 1（中间）
        [9, 1], [9.5, 1], [9, 0.5],       # 簇 2（右下）
    ]

    result = exercise_2_kmeans(data, k=3)

    if result is None:
        print("[未完成] 请实现 exercise_2_kmeans 函数")
        return False

    if not isinstance(result, list) or len(result) != 9:
        print(f"[错误] 返回值应该是长度为 9 的列表")
        return False

    # 检查：同一簇内的点应该有相同的标签
    # 前 3 个点应该在同一簇，中间 3 个在同一簇，后 3 个在同一簇
    cluster_0 = result[0]
    cluster_1 = result[3]
    cluster_2 = result[6]

    same_cluster_0 = result[0] == result[1] == result[2]
    same_cluster_1 = result[3] == result[4] == result[5]
    same_cluster_2 = result[6] == result[7] == result[8]
    all_different = len(set([cluster_0, cluster_1, cluster_2])) == 3

    if same_cluster_0 and same_cluster_1 and same_cluster_2 and all_different:
        print(f"[正确] 3 簇数据正确聚类")
        print(f"       标签: {result}")
        return True
    else:
        print(f"[结果] 标签: {result}")
        print(f"       同簇一致性: {same_cluster_0}, {same_cluster_1}, {same_cluster_2}")
        return False


# ==============================================================================
# 练习 3：计算轮廓系数
# ==============================================================================

def exercise_3_silhouette(data: list, labels: list) -> float:
    """
    练习 3：计算轮廓系数（Silhouette Score）

    ━━━━━━━ 生活类比 ━━━━━━━
    轮廓系数衡量"你在这个组里待得舒不舒服"：
    - a(i) = 你和同组人的平均距离（越小越好）
    - b(i) = 你和最近的其他组的平均距离（越大越好）
    - s(i) = (b(i) - a(i)) / max(a(i), b(i))

    最终得分 = 所有点的 s(i) 的平均值

    ━━━━━━━ 提示 ━━━━━━━
    1. 对每个点 i：
       a. 找到同簇的其他点，计算平均距离 a(i)
       b. 对每个其他簇，计算点 i 到该簇所有点的平均距离
          取最小值作为 b(i)
       c. s(i) = (b(i) - a(i)) / max(a(i), b(i))（如果 max > 0）

    2. 返回所有 s(i) 的平均值

    参数：
        data: 数据列表，每个元素是 [x, y] 坐标
        labels: 标签列表，每个元素是 0 到 k-1 的整数

    返回：
        轮廓系数（-1 到 1 之间的浮点数）
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # n = len(data)
    # clusters = set(labels)
    # if len(clusters) <= 1:
    #     return 0.0
    #
    # scores = []
    # for i in range(n):
    #     same = [j for j in range(n) if labels[j] == labels[i] and j != i]
    #     a_i = sum(math.sqrt(sum((data[i][d] - data[j][d])**2 for d in range(len(data[i]))))
    #               for j in same) / len(same) if same else 0
    #
    #     b_i = float('inf')
    #     for c in clusters:
    #         if c == labels[i]:
    #             continue
    #         others = [j for j in range(n) if labels[j] == c]
    #         if others:
    #             avg = sum(math.sqrt(sum((data[i][d] - data[j][d])**2 for d in range(len(data[i]))))
    #                       for j in others) / len(others)
    #             b_i = min(b_i, avg)
    #     if b_i == float('inf'):
    #         b_i = 0
    #
    #     if max(a_i, b_i) == 0:
    #         scores.append(0)
    #     else:
    #         scores.append((b_i - a_i) / max(a_i, b_i))
    #
    # return sum(scores) / len(scores)
    pass


def test_exercise_3():
    """测试练习 3"""
    print("\n" + "=" * 60)
    print("练习 3：计算轮廓系数")
    print("=" * 60)

    # 明显分为 3 簇的数据
    data = [
        [1, 1], [1.5, 1.5], [1, 2],      # 簇 0
        [5, 5], [5.5, 5], [5, 5.5],       # 簇 1
        [9, 1], [9.5, 1], [9, 0.5],       # 簇 2
    ]
    labels = [0, 0, 0, 1, 1, 1, 2, 2, 2]

    result = exercise_3_silhouette(data, labels)

    if result is None:
        print("[未完成] 请实现 exercise_3_silhouette 函数")
        return False

    if not isinstance(result, (int, float)):
        print(f"[错误] 返回值应该是数字，实际: {type(result)}")
        return False

    # 好的聚类结果，轮廓系数应该接近 1
    if result > 0.5:
        print(f"[正确] 轮廓系数: {result:.4f}")
        print(f"       分数 > 0.5，说明聚类效果良好")
        return True
    else:
        print(f"[结果] 轮廓系数: {result:.4f}")
        print(f"       期望 > 0.5（好的聚类效果）")
        return False


# ==============================================================================
# 主程序：运行所有练习测试
# ==============================================================================

if __name__ == "__main__":

    print("""
    ╔══════════════════════════════════════════════════════╗
    ║        G-one NLP 学院 - 第十五章 练习                  ║
    ║        文本聚类                                      ║
    ╚══════════════════════════════════════════════════════╝
    """)

    # 运行所有练习测试
    results = []
    results.append(("练习1: TF-IDF 计算", test_exercise_1()))
    results.append(("练习2: K-Means 聚类", test_exercise_2()))
    results.append(("练习3: 轮廓系数计算", test_exercise_3()))

    # 练习清单
    print("\n" + "=" * 60)
    print("  练习清单")
    print("=" * 60)
    for name, passed in results:
        status = "[完成]" if passed else "[未完成]"
        print(f"  {status} {name}")

    # 计算完成率
    completed = sum(1 for _, p in results if p)
    total = len(results)
    print(f"\n  完成率: {completed}/{total}")

    if completed == total:
        print("\n  恭喜！所有练习都完成了！")
        print("  你已经掌握了文本聚类的核心技术。")
    else:
        print(f"\n  还有 {total - completed} 个练习未完成。")
        print("  不要着急，慢慢来，理解了再写代码。")
