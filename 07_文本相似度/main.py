import sys
sys.stdout.reconfigure(encoding='utf-8')

"""
==============================================================================
第七章：文本相似度 — 完整演示
==============================================================================
G-one NLP 学院
日期：2026-05-16

运行方式：
    python main.py

前置知识：
    - 第一章：NLP 概述
    - 第二章：中文分词

本章内容：
    1. 编辑距离（Levenshtein Distance）
    2. 余弦相似度（Cosine Similarity）
    3. Jaccard 相似度
    4. 模糊搜索实战
==============================================================================
"""

from text_similarity import (
    levenshtein_distance,
    levenshtein_similarity,
    cosine_similarity_manual,
    cosine_similarity_text,
    jaccard_similarity,
    jaccard_similarity_text,
    fuzzy_search,
    fuzzy_search_advanced,
    compare_all_methods,
)


def print_separator(title: str):
    """打印分隔线和标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def lesson_edit_distance():
    """第一部分：编辑距离"""

    print_separator("7.1 编辑距离（Levenshtein Distance）")

    print("""
    编辑距离是衡量两个字符串"差异程度"的经典方法。

    核心问题：把字符串 A 变成字符串 B，最少需要多少步操作？

    三种操作：
      1. 插入一个字符
      2. 删除一个字符
      3. 替换一个字符

    生活类比：
      就像"变身游戏" ——
      "kitten" 要变成 "sitting"：
        kitten → sitten  （k → s）      第1步
        sitten → sittin  （e → i）      第2步
        sittin → sitting  （+g）        第3步
      编辑距离 = 3
    """)

    # 演示 1：英文单词
    print("-" * 40)
    print("示例 1：英文单词")
    pairs = [
        ("kitten", "sitting"),
        ("hello", "world"),
        ("python", "python"),   # 完全相同
        ("abc", "xyz"),         # 完全不同
    ]

    for s1, s2 in pairs:
        dist = levenshtein_distance(s1, s2)
        sim = levenshtein_similarity(s1, s2)
        print(f"\n  '{s1}' → '{s2}'")
        print(f"    编辑距离: {dist}")
        print(f"    相似度: {sim:.2%}")

    # 演示 2：中文文本
    print("\n" + "-" * 40)
    print("示例 2：中文文本")
    pairs = [
        ("今天天气好", "今天天气不错"),
        ("自然语言处理", "自然语言理解"),
        ("机器学习", "深度学习"),
        ("苹果", "苹果公司"),
    ]

    for s1, s2 in pairs:
        dist = levenshtein_distance(s1, s2)
        sim = levenshtein_similarity(s1, s2)
        print(f"\n  '{s1}' vs '{s2}'")
        print(f"    编辑距离: {dist}, 相似度: {sim:.2%}")

    # 演示 3：编辑距离矩阵（可视化）
    print("\n" + "-" * 40)
    print("示例 3：编辑距离矩阵")
    print("  对比多组文本的编辑距离：")

    texts = ["苹果", "苹果公司", "香蕉", "苹果手机"]
    print(f"\n  {'':>8}", end="")
    for t in texts:
        print(f"{t:>8}", end="")
    print()

    for t1 in texts:
        print(f"  {t1:>8}", end="")
        for t2 in texts:
            dist = levenshtein_distance(t1, t2)
            print(f"{dist:>8}", end="")
        print()


def lesson_cosine_similarity():
    """第二部分：余弦相似度"""

    print_separator("7.2 余弦相似度（Cosine Similarity）")

    print("""
    余弦相似度衡量两个向量"方向"的相似性。

    核心思想：
      把文本变成向量（一组数字），然后计算向量夹角的余弦值。

    生活类比：
      两个人各拿一个指南针：
      - 都指北方 → 夹角 0° → cos(0°) = 1（完全一致）
      - 一个指北一个指南 → 夹角 180° → cos(180°) = -1（完全相反）
      - 一个指东一个指北 → 夹角 90° → cos(90°) = 0（无关）
    """)

    # 演示 1：简单的向量
    print("-" * 40)
    print("示例 1：向量相似度")

    vec_pairs = [
        ([1, 2, 3], [1, 2, 3]),     # 完全相同
        ([1, 0, 0], [0, 1, 0]),     # 完全正交
        ([1, 2, 3], [4, 5, 6]),     # 相似方向
        ([1, 0], [0, 1]),           # 垂直
    ]

    for v1, v2 in vec_pairs:
        sim = cosine_similarity_manual(v1, v2)
        print(f"\n  {v1} vs {v2}")
        print(f"    余弦相似度: {sim:.4f}")

    # 演示 2：文本相似度
    print("\n" + "-" * 40)
    print("示例 2：文本余弦相似度")
    print("  原理：把文本转成词频向量，然后计算余弦相似度")
    print("  '我喜欢吃苹果' → {'我':1, '喜':1, '欢':1, '吃':1, '苹':1, '果':1}")

    text_pairs = [
        ("今天天气好", "今天天气不错"),
        ("自然语言处理", "自然语言理解"),
        ("机器学习", "深度学习"),
        ("我喜欢猫", "我喜欢狗"),
    ]

    for t1, t2 in text_pairs:
        sim = cosine_similarity_text(t1, t2)
        print(f"\n  '{t1}' vs '{t2}'")
        print(f"    余弦相似度: {sim:.4f}")


def lesson_jaccard():
    """第三部分：Jaccard 相似度"""

    print_separator("7.3 Jaccard 相似度")

    print("""
    Jaccard 相似度是最直观的相似度计算方法。

    核心思想：
      相似度 = 交集大小 / 并集大小

    生活类比：
      两个人的购物清单：
      - 小明：{苹果, 香蕉, 牛奶, 面包}
      - 小红：{苹果, 面包, 鸡蛋, 水}
      - 交集（都买的）：{苹果, 面包} → 2 种
      - 并集（总共提到的）：6 种
      - Jaccard = 2/6 = 0.33
      → 购物习惯有 33% 相似
    """)

    # 演示 1：集合相似度
    print("-" * 40)
    print("示例 1：集合 Jaccard 相似度")

    set_pairs = [
        ({"苹果", "香蕉", "牛奶"}, {"苹果", "香蕉", "鸡蛋"}),
        ({"机器", "学习"}, {"深度", "学习"}),
        ({1, 2, 3, 4}, {3, 4, 5, 6}),
        ({"A", "B", "C"}, {"D", "E", "F"}),
    ]

    for s1, s2 in set_pairs:
        sim = jaccard_similarity(s1, s2)
        print(f"\n  {s1}")
        print(f"  {s2}")
        print(f"    Jaccard 相似度: {sim:.4f}")

    # 演示 2：文本 Jaccard 相似度
    print("\n" + "-" * 40)
    print("示例 2：文本 Jaccard 相似度")

    text_pairs = [
        ("今天天气好", "今天天气真好"),
        ("自然语言处理", "自然语言理解"),
        ("我喜欢苹果", "苹果很好吃"),
        ("Python编程", "Java编程"),
    ]

    for t1, t2 in text_pairs:
        sim = jaccard_similarity_text(t1, t2)
        print(f"\n  '{t1}' vs '{t2}'")
        print(f"    Jaccard 相似度: {sim:.4f}")


def lesson_fuzzy_search():
    """第四部分：模糊搜索实战"""

    print_separator("7.4 模糊搜索实战")

    print("""
    模糊搜索就是"差不多就行"的搜索方式。

    生活类比：
      你在手机通讯录里找"张三"，但记不清确切名字。
      输入"张三"，手机可能会提示：
      - 张三（完全匹配）
      - 张三丰（多一个字）
      - 张山（少一个字）

    在 NLP 中，模糊搜索常用于：
      1. 搜索引擎的"你是不是想搜..."
      2. 输入法的候选词推荐
      3. 命名实体识别中的实体匹配
    """)

    # 演示 1：基本模糊搜索
    print("-" * 40)
    print("示例 1：基本模糊搜索")

    candidates = [
        "机器学习入门", "机器学习基础", "深度学习",
        "自然语言处理", "机器学习算法", "人工智能",
        "统计学习方法", "数据挖掘", "机器学习实战",
        "Python机器学习", "机器学习与深度学习",
    ]

    query = "机器学习"
    print(f"\n  查询: '{query}'")
    print(f"  候选集: {len(candidates)} 个")

    results = fuzzy_search(query, candidates, threshold=0.3)
    print(f"\n  搜索结果（阈值=0.3，基于编辑距离）:")
    for text, score in results:
        bar = "#" * int(score * 20)
        print(f"    {score:.2%} {bar:>20} {text}")

    # 演示 2：高级模糊搜索（综合多种方法）
    print("\n" + "-" * 40)
    print("示例 2：高级模糊搜索（综合评分）")
    print("  综合编辑距离(40%) + Jaccard(30%) + 余弦(30%)")

    results = fuzzy_search_advanced(query, candidates, top_k=5)
    print(f"\n  Top-5 结果:")
    for text, score in results:
        bar = "#" * int(score * 20)
        print(f"    {score:.2%} {bar:>20} {text}")

    # 演示 3：实际应用场景
    print("\n" + "-" * 40)
    print("示例 3：实际应用场景 — 联系人搜索")

    contacts = [
        "张三", "张三丰", "张山", "李四", "李四五",
        "王小明", "王小民", "赵六", "钱七", "孙八",
    ]

    query = "张三"
    print(f"\n  搜索联系人: '{query}'")

    results = fuzzy_search_advanced(query, contacts, top_k=5)
    print(f"  匹配结果:")
    for text, score in results:
        bar = "#" * int(score * 20)
        print(f"    {score:.2%} {bar:>20} {text}")


def lesson_comprehensive():
    """第五部分：综合对比"""

    print_separator("7.5 三种方法综合对比")

    print("""
    我们来对比三种相似度方法：

    | 方法         | 关注点           | 优点               | 缺点               |
    |-------------|-----------------|--------------------|--------------------|
    | 编辑距离     | 字符级操作次数    | 直观、易于理解       | 不考虑语义          |
    | 余弦相似度   | 向量方向         | 适合高维文本         | 依赖分词质量        |
    | Jaccard     | 集合重叠程度      | 简单快速             | 忽略词频信息        |
    """)

    test_pairs = [
        ("今天天气好", "今天天气真好", "很相似"),
        ("机器学习", "深度学习", "领域相近"),
        ("我喜欢猫", "猫很可爱", "主题相同"),
        ("苹果好吃", "苹果公司", "一词多义"),
        ("自然语言处理", "计算机视觉", "不同领域"),
    ]

    print("-" * 60)
    print(f"  {'文本1':<10} {'文本2':<10} {'编辑距离':>8} {'Jaccard':>8} {'余弦':>8}  {'直觉':<6}")
    print("-" * 60)

    for t1, t2, intuition in test_pairs:
        result = compare_all_methods(t1, t2)
        edit_sim = result["编辑距离相似度"]
        jac_sim = result["Jaccard相似度"]
        cos_sim = result["余弦相似度"]
        print(f"  {t1:<10} {t2:<10} {edit_sim:>8.4f} {jac_sim:>8.4f} {cos_sim:>8.4f}  {intuition}")


# ==============================================================================
# 主程序入口
# ==============================================================================

if __name__ == "__main__":

    print("""
    ╔══════════════════════════════════════════════════════╗
    ║        G-one NLP 学院 - 第七章                        ║
    ║                                                      ║
    ║        ████████╗███████╗██╗  ██╗████████╗            ║
    ║        ╚══██╔══╝██╔════╝╚██╗██╔╝╚══██╔══╝            ║
    ║           ██║   █████╗   ╚███╔╝    ██║               ║
    ║           ██║   ██╔══╝   ██╔██╗    ██║               ║
    ║           ██║   ███████╗██╔╝ ██╗   ██║               ║
    ║           ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝               ║
    ║                                                      ║
    ║              文 本 相 似 度                            ║
    ╚══════════════════════════════════════════════════════╝
    """)

    lesson_edit_distance()
    lesson_cosine_similarity()
    lesson_jaccard()
    lesson_fuzzy_search()
    lesson_comprehensive()

    # 课程总结
    print("\n" + "=" * 60)
    print("  第七章 总结")
    print("=" * 60)
    print("""
    [OK] 编辑距离（Levenshtein Distance）
         把一个字符串变成另一个字符串需要的最少操作数
         三种操作：插入、删除、替换
         动态规划算法，时间复杂度 O(m*n)

    [OK] 余弦相似度（Cosine Similarity）
         把文本变成向量，计算向量夹角的余弦值
         关注"方向"的相似性，忽略长度差异
         适合高维文本数据

    [OK] Jaccard 相似度
         交集大小 / 并集大小
         最简单直观的相似度计算方法
         适合快速筛选

    [OK] 模糊搜索实战
         综合多种相似度指标
         可设置阈值过滤低质量结果
         应用于搜索引擎、输入法等场景
    """)

    print("-" * 60)
    print("  下节预告：第八章 — 语义相似度")
    print("-" * 60)
    print("""
    下一章我们将学习：
    - 基于同义词典的语义相似度
    - 词向量相似度（Word2Vec 思想）
    - 句子级别的语义相似度

    本章学的是"表面相似"，下章学的是"意思相似"！
    """)
