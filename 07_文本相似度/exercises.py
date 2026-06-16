import sys
sys.stdout.reconfigure(encoding='utf-8')

"""
==============================================================================
第七章：文本相似度 — 练习题
==============================================================================
G-one NLP 学院
日期：2026-05-16

本章练习：
    1. 实现编辑距离算法
    2. 实现余弦相似度计算
    3. 实现简单的模糊搜索引擎

运行方式：
    python exercises.py
==============================================================================
"""


# ==============================================================================
# 练习 1：实现编辑距离算法
# ==============================================================================

def exercise_1_levenshtein(s1: str, s2: str) -> int:
    """
    练习 1：实现编辑距离（Levenshtein Distance）算法

    ━━━━━━━ 生活类比 ━━━━━━━
    想象你有一串珠子（字符串 s1），要把它变成另一串珠子（字符串 s2）。
    你可以：加一颗珠子、拿掉一颗珠子、换一颗珠子。
    问：最少需要操作几次？

    ━━━━━━━ 提示 ━━━━━━━
    使用动态规划：
    1. 创建 (m+1) x (n+1) 的表格 dp，m=len(s1), n=len(s2)
    2. 初始化：dp[i][0] = i（删除 i 次），dp[0][j] = j（插入 j 次）
    3. 对于每个位置 (i,j)：
       - 如果 s1[i-1] == s2[j-1]，cost = 0，否则 cost = 1
       - dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)
    4. 返回 dp[m][n]

    参数：
        s1: 第一个字符串
        s2: 第二个字符串

    返回：
        编辑距离（非负整数）
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # m, n = len(s1), len(s2)
    # dp = [[0] * (n + 1) for _ in range(m + 1)]
    # for i in range(m + 1):
    #     dp[i][0] = i
    # for j in range(n + 1):
    #     dp[0][j] = j
    # for i in range(1, m + 1):
    #     for j in range(1, n + 1):
    #         cost = 0 if s1[i - 1] == s2[j - 1] else 1
    #         dp[i][j] = min(
    #             dp[i - 1][j] + 1,
    #             dp[i][j - 1] + 1,
    #             dp[i - 1][j - 1] + cost
    #         )
    # return dp[m][n]
    pass


def test_exercise_1():
    """测试练习 1"""
    print("\n" + "=" * 60)
    print("练习 1：实现编辑距离算法")
    print("=" * 60)

    test_cases = [
        ("kitten", "sitting", 3),
        ("abc", "abc", 0),
        ("abc", "", 3),
        ("", "abc", 3),
        ("今天", "明天", 1),
    ]

    all_passed = True
    for s1, s2, expected in test_cases:
        result = exercise_1_levenshtein(s1, s2)
        if result is None:
            print(f"  [未完成] 请实现 exercise_1_levenshtein 函数")
            return False
        if result == expected:
            print(f"  [正确] levenshtein('{s1}', '{s2}') = {result}")
        else:
            print(f"  [错误] levenshtein('{s1}', '{s2}'): 期望 {expected}, 实际 {result}")
            all_passed = False

    return all_passed


# ==============================================================================
# 练习 2：实现余弦相似度计算
# ==============================================================================

def exercise_2_cosine_similarity(vec1: list, vec2: list) -> float:
    """
    练习 2：实现两个向量的余弦相似度

    ━━━━━━━ 生活类比 ━━━━━━━
    两个人各射了一支箭，箭的方向越接近，余弦相似度越高。
    - 完全同方向 → 1.0
    - 垂直 → 0.0
    - 完全反方向 → -1.0

    ━━━━━━━ 提示 ━━━━━━━
    1. 计算点积：dot = sum(a * b for a, b in zip(vec1, vec2))
    2. 计算两个向量的长度：
       norm1 = sqrt(sum(a^2 for a in vec1))
       norm2 = sqrt(sum(b^2 for b in vec2))
    3. 如果 norm1 == 0 或 norm2 == 0，返回 0.0
    4. 返回 dot / (norm1 * norm2)

    参数：
        vec1: 第一个向量
        vec2: 第二个向量

    返回：
        余弦相似度（-1 到 1 之间）
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # if len(vec1) != len(vec2):
    #     raise ValueError("向量维度不一致")
    # dot_product = sum(a * b for a, b in zip(vec1, vec2))
    # norm1 = sum(a * a for a in vec1) ** 0.5
    # norm2 = sum(b * b for b in vec2) ** 0.5
    # if norm1 == 0 or norm2 == 0:
    #     return 0.0
    # return dot_product / (norm1 * norm2)
    pass


def test_exercise_2():
    """测试练习 2"""
    print("\n" + "=" * 60)
    print("练习 2：实现余弦相似度")
    print("=" * 60)

    test_cases = [
        ([1, 2, 3], [1, 2, 3], 1.0),       # 完全相同
        ([1, 0], [0, 1], 0.0),              # 垂直
        ([1, 2, 3], [4, 5, 6], 0.9746),     # 相似方向
    ]

    all_passed = True
    for v1, v2, expected in test_cases:
        result = exercise_2_cosine_similarity(v1, v2)
        if result is None:
            print(f"  [未完成] 请实现 exercise_2_cosine_similarity 函数")
            return False
        # 允许 0.001 的误差
        if abs(result - expected) < 0.01:
            print(f"  [正确] cosine({v1}, {v2}) = {result:.4f}")
        else:
            print(f"  [错误] cosine({v1}, {v2}): 期望 {expected:.4f}, 实际 {result:.4f}")
            all_passed = False

    return all_passed


# ==============================================================================
# 练习 3：实现模糊搜索引擎
# ==============================================================================

def exercise_3_fuzzy_search(query: str, candidates: list, top_k: int = 3) -> list:
    """
    练习 3：实现一个简单的模糊搜索引擎

    ━━━━━━━ 生活类比 ━━━━━━━
    你在手机通讯录里找人，输入了名字的一部分。
    手机帮你找到最匹配的几个联系人。

    ━━━━━━━ 提示 ━━━━━━━
    1. 对于每个候选词，计算与 query 的编辑距离相似度
       - 编辑距离相似度 = 1 - 编辑距离 / max(len(query), len(candidate))
    2. 将结果存入列表 [(候选词, 相似度), ...]
    3. 按相似度降序排列
    4. 返回前 top_k 个结果

    参数：
        query: 查询文本
        candidates: 候选文本列表
        top_k: 返回前 k 个结果

    返回：
        列表，每个元素是 (候选文本, 相似度)
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # results = []
    # for candidate in candidates:
    #     # 计算编辑距离
    #     m, n = len(query), len(candidate)
    #     dp = [[0] * (n + 1) for _ in range(m + 1)]
    #     for i in range(m + 1):
    #         dp[i][0] = i
    #     for j in range(n + 1):
    #         dp[0][j] = j
    #     for i in range(1, m + 1):
    #         for j in range(1, n + 1):
    #             cost = 0 if query[i - 1] == candidate[j - 1] else 1
    #             dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)
    #     distance = dp[m][n]
    #     # 归一化
    #     max_len = max(m, n)
    #     similarity = 1.0 - distance / max_len if max_len > 0 else 1.0
    #     results.append((candidate, similarity))
    # # 排序并返回前 top_k 个
    # results.sort(key=lambda x: x[1], reverse=True)
    # return results[:top_k]
    pass


def test_exercise_3():
    """测试练习 3"""
    print("\n" + "=" * 60)
    print("练习 3：模糊搜索引擎")
    print("=" * 60)

    candidates = ["机器学习", "深度学习", "自然语言处理", "计算机视觉", "数据挖掘", "机器学习入门"]
    query = "机器学习"

    result = exercise_3_fuzzy_search(query, candidates, top_k=3)

    if result is None:
        print("  [未完成] 请实现 exercise_3_fuzzy_search 函数")
        return False

    print(f"  查询: '{query}'")
    print(f"  Top-3 结果:")
    for text, score in result:
        print(f"    {score:.4f}  {text}")

    # 检查结果是否合理
    if len(result) == 3 and result[0][0] == "机器学习":
        print("  [正确] 完全匹配排在第一位")
        return True
    elif len(result) == 3:
        print("  [部分正确] 返回了 3 个结果，但排序可能需要调整")
        return True
    else:
        print("  [错误] 结果数量不正确")
        return False


# ==============================================================================
# 主程序
# ==============================================================================

if __name__ == "__main__":

    print("""
    ╔══════════════════════════════════════════════════════╗
    ║        G-one NLP 学院 - 第七章 练习                    ║
    ║        文本相似度                                    ║
    ╚══════════════════════════════════════════════════════╝
    """)

    results = []
    results.append(("练习1: 编辑距离", test_exercise_1()))
    results.append(("练习2: 余弦相似度", test_exercise_2()))
    results.append(("练习3: 模糊搜索", test_exercise_3()))

    print("\n" + "=" * 60)
    print("  练习清单")
    print("=" * 60)
    for name, passed in results:
        status = "[完成]" if passed else "[未完成]"
        print(f"  {status} {name}")

    completed = sum(1 for _, p in results if p)
    total = len(results)
    print(f"\n  完成率: {completed}/{total}")

    if completed == total:
        print("\n  所有练习完成！你已经掌握了文本相似度的核心技术。")
    else:
        print(f"\n  还有 {total - completed} 个练习未完成。")
