import sys
sys.stdout.reconfigure(encoding='utf-8')

"""
==============================================================================
第五章：依存句法分析 — 练习题
==============================================================================
G-one NLP 学院
日期：2026-05-16

本章练习：
    1. 构建依存弧
    2. 查找依存树中的关系
    3. 简单的依存分析器

运行方式：
    python exercises.py

提示：
    - 每个练习都有详细的提示，按照提示一步步来
    - 先自己写，写不出来再看注释中的参考答案
    - 运行后会自动检查你的答案是否正确
==============================================================================
"""

from dependency import DependencyArc, DependencyTree


# ==============================================================================
# 练习 1：构建依存弧
# ==============================================================================

def exercise_1_build_arcs(words: list, relations: list) -> list:
    """
    练习 1：根据给定的词和关系，构建依存弧列表

    ━━━━━━━ 生活类比 ━━━━━━━
    想象你在画家族树，你需要在每两个人之间画一条线，
    并在线上标注关系（父子、兄弟等）。

    ━━━━━━━ 提示 ━━━━━━━
    1. relations 是一个列表，每个元素是 (孩子索引, 父亲索引, 关系类型)
    2. 遍历 relations，用 DependencyArc 创建每条弧
    3. 返回 DependencyArc 对象的列表

    参数：
        words: 词列表，如 ["小明", "吃", "苹果"]
        relations: 关系列表，如 [(0, 1, "SBV"), (1, -1, "HED"), (2, 1, "VOB")]

    返回：
        DependencyArc 对象的列表
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # arcs = []
    # for dep_idx, head_idx, rel in relations:
    #     arcs.append(DependencyArc(dep_idx, head_idx, rel))
    # return arcs
    pass


def test_exercise_1():
    """测试练习 1"""
    print("\n" + "=" * 60)
    print("练习 1：构建依存弧")
    print("=" * 60)

    words = ["小明", "吃", "苹果"]
    relations = [(0, 1, "SBV"), (1, -1, "HED"), (2, 1, "VOB")]

    result = exercise_1_build_arcs(words, relations)

    if result is None:
        print("[未完成] 请实现 exercise_1_build_arcs 函数")
        return False

    # 检查结果
    if len(result) != 3:
        print(f"[错误] 期望 3 条弧，实际 {len(result)} 条")
        return False

    # 检查每条弧
    expected = [(0, 1, "SBV"), (1, -1, "HED"), (2, 1, "VOB")]
    for i, (arc, (exp_dep, exp_head, exp_rel)) in enumerate(zip(result, expected)):
        if arc.dependent_index != exp_dep or arc.head_index != exp_head or arc.relation != exp_rel:
            print(f"[错误] 第 {i+1} 条弧不匹配")
            print(f"       期望: Arc({exp_dep} <--{exp_rel}-- {exp_head})")
            print(f"       实际: {arc}")
            return False

    print(f"[正确] 构建了 {len(result)} 条依存弧")
    for arc in result:
        print(f"       {arc}")
    return True


# ==============================================================================
# 练习 2：查找依存关系
# ==============================================================================

def exercise_2_find_relation(tree: DependencyTree, word: str) -> str:
    """
    练习 2：在依存树中查找指定词的依存关系类型

    ━━━━━━━ 生活类比 ━━━━━━━
    想象你在查族谱，想知道"张三"和他父亲是什么关系。
    你需要在族谱中找到"张三"，然后看连线上写的关系。

    ━━━━━━━ 提示 ━━━━━━━
    1. 先找到 word 在 tree.words 中的索引
    2. 遍历 tree.arcs，找到 dependent_index 等于该索引的弧
    3. 返回该弧的 relation（关系类型）
    4. 如果找不到，返回 "UNKNOWN"

    参数：
        tree: 依存树对象
        word: 要查找的词

    返回：
        关系类型的字符串
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # try:
    #     idx = tree.words.index(word)
    # except ValueError:
    #     return "UNKNOWN"
    # for arc in tree.arcs:
    #     if arc.dependent_index == idx:
    #         return arc.relation
    # return "UNKNOWN"
    pass


def test_exercise_2():
    """测试练习 2"""
    print("\n" + "=" * 60)
    print("练习 2：查找依存关系")
    print("=" * 60)

    # 构建测试用的依存树
    words = ["我", "喜欢", "吃", "苹果"]
    arcs = [
        DependencyArc(0, 1, "SBV"),
        DependencyArc(1, -1, "HED"),
        DependencyArc(2, 1, "COO"),
        DependencyArc(3, 2, "VOB"),
    ]
    tree = DependencyTree(words, arcs)

    test_cases = [
        ("我", "SBV"),
        ("喜欢", "HED"),
        ("吃", "COO"),
        ("苹果", "VOB"),
        ("香蕉", "UNKNOWN"),  # 不存在的词
    ]

    all_correct = True
    for word, expected in test_cases:
        result = exercise_2_find_relation(tree, word)
        if result is None:
            print("[未完成] 请实现 exercise_2_find_relation 函数")
            return False
        if result == expected:
            print(f"  [正确] \"{word}\" 的关系: {result}")
        else:
            print(f"  [错误] \"{word}\" 的关系: 期望 {expected}, 实际 {result}")
            all_correct = False

    return all_correct


# ==============================================================================
# 练习 3：简单的依存分析器
# ==============================================================================

def exercise_3_simple_parse(words: list, pos_tags: list) -> list:
    """
    练习 3：实现一个简单的依存分析器

    ━━━━━━━ 生活类比 ━━━━━━━
    想象你在读一句话，需要判断每个词和哪个词有关系。
    就像做连线题：把相关的词连起来。

    ━━━━━━━ 提示 ━━━━━━━
    规则：
    1. 找到第一个动词(v)作为核心词，它依存于 ROOT（head_index=-1）
    2. 核心词左边的代词(r)和人名(nr) → 主语关系（SBV），依存于核心词
    3. 核心词右边的名词(n) → 宾语关系（VOB），依存于核心词
    4. 其他词默认依存于核心词，关系为 "DEP"（未指定关系）

    参数：
        words: 词列表
        pos_tags: 词性列表

    返回：
        DependencyArc 对象的列表
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # arcs = []
    # # 找核心词
    # root_idx = 0
    # for i, pos in enumerate(pos_tags):
    #     if pos == "v":
    #         root_idx = i
    #         break
    # arcs.append(DependencyArc(root_idx, -1, "HED"))
    #
    # # 分析其他词
    # for i, (word, pos) in enumerate(zip(words, pos_tags)):
    #     if i == root_idx:
    #         continue
    #     if pos in ("r", "nr") and i < root_idx:
    #         arcs.append(DependencyArc(i, root_idx, "SBV"))
    #     elif pos == "n" and i > root_idx:
    #         arcs.append(DependencyArc(i, root_idx, "VOB"))
    #     else:
    #         arcs.append(DependencyArc(i, root_idx, "DEP"))
    #
    # return arcs
    pass


def test_exercise_3():
    """测试练习 3"""
    print("\n" + "=" * 60)
    print("练习 3：简单的依存分析器")
    print("=" * 60)

    words = ["小明", "吃", "苹果"]
    pos_tags = ["nr", "v", "n"]

    result = exercise_3_simple_parse(words, pos_tags)

    if result is None:
        print("[未完成] 请实现 exercise_3_simple_parse 函数")
        return False

    # 检查结果
    if len(result) != 3:
        print(f"[错误] 期望 3 条弧，实际 {len(result)} 条")
        return False

    # 建立索引
    result_map = {}
    for arc in result:
        result_map[arc.dependent_index] = (arc.head_index, arc.relation)

    # 检查核心词
    if 1 not in result_map or result_map[1] != (-1, "HED"):
        print(f"[错误] \"吃\" 应该是核心词，依存于 ROOT")
        return False

    # 检查主语
    if 0 not in result_map or result_map[0][1] != "SBV":
        print(f"[错误] \"小明\" 应该是主语关系（SBV）")
        return False

    # 检查宾语
    if 2 not in result_map or result_map[2][1] != "VOB":
        print(f"[错误] \"苹果\" 应该是宾语关系（VOB）")
        return False

    print(f"[正确] 分析结果：")
    for arc in result:
        head_str = "ROOT" if arc.head_index == -1 else words[arc.head_index]
        print(f"       {words[arc.dependent_index]} --{arc.relation}--> {head_str}")
    return True


# ==============================================================================
# 主程序：运行所有练习测试
# ==============================================================================

if __name__ == "__main__":

    print("""
    ╔══════════════════════════════════════════════════════╗
    ║        G-one NLP 学院 - 第五章 练习                    ║
    ║        依存句法分析                                   ║
    ╚══════════════════════════════════════════════════════╝
    """)

    # 运行所有练习测试
    results = []
    results.append(("练习1: 构建依存弧", test_exercise_1()))
    results.append(("练习2: 查找依存关系", test_exercise_2()))
    results.append(("练习3: 简单依存分析器", test_exercise_3()))

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
        print("  你已经掌握了依存句法分析的基础。")
        print("  下一章我们将学习语义角色标注。")
    else:
        print(f"\n  还有 {total - completed} 个练习未完成。")
        print("  不要着急，依存句法分析需要多练习才能理解。")
        print("  如果实在写不出来，可以查看注释中的参考答案。")
