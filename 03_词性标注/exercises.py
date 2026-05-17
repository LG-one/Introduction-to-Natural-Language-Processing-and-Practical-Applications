import sys
sys.stdout.reconfigure(encoding='utf-8')

"""
==============================================================================
第三章：词性标注 — 练习题
==============================================================================
G-one NLP 学院
日期：2026-05-16
==============================================================================
"""


# ==============================================================================
# 练习 1：查词典词性标注
# ==============================================================================

def exercise_1_dict_tag(words: list, dictionary: dict) -> list:
    """
    练习 1：使用词典进行词性标注

    ━━━━━━━ 提示 ━━━━━━━
    1. 遍历 words 中的每个词
    2. 用 dictionary.get(word, "n") 获取词性（默认为名词）
    3. 返回 [(词, 词性), ...] 列表

    参数：
        words: 词列表
        dictionary: 词典 {词: 词性}

    返回：
        [(词, 词性), ...] 列表
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # return [(w, dictionary.get(w, "n")) for w in words]
    pass


def test_exercise_1():
    print("\n" + "=" * 60)
    print("练习 1：查词典词性标注")
    print("=" * 60)

    dictionary = {"我": "r", "喜欢": "v", "吃": "v", "苹果": "n", "很": "d", "好": "a"}
    words = ["我", "喜欢", "吃", "苹果"]
    result = exercise_1_dict_tag(words, dictionary)

    if result is None:
        print("[未完成] 请实现 exercise_1_dict_tag 函数")
        return False

    expected = [("我", "r"), ("喜欢", "v"), ("吃", "v"), ("苹果", "n")]
    if result == expected:
        print(f"[正确] {result}")
        return True
    else:
        print(f"[错误] 期望 {expected}, 实际 {result}")
        return False


# ==============================================================================
# 练习 2：识别词性类别
# ==============================================================================

def exercise_2_classify_pos(word: str) -> str:
    """
    练习 2：判断一个词最可能的词性类别

    ━━━━━━━ 提示 ━━━━━━━
    根据词的特征判断：
    - 如果以"地"结尾（如"高兴地"）→ "d"（副词）
    - 如果以"的"结尾（如"美丽的"）→ "a"（形容词）
    - 如果以"了"或"着"结尾 → "u"（助词）
    - 否则 → "n"（名词）

    参数：
        word: 一个词

    返回：
        词性标签
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # if word.endswith("地"):
    #     return "d"
    # elif word.endswith("的"):
    #     return "a"
    # elif word.endswith(("了", "着", "过")):
    #     return "u"
    # else:
    #     return "n"
    pass


def test_exercise_2():
    print("\n" + "=" * 60)
    print("练习 2：识别词性类别")
    print("=" * 60)

    test_cases = [("高兴地", "d"), ("美丽的", "a"), ("吃了", "u"), ("苹果", "n")]
    all_correct = True
    for word, expected in test_cases:
        result = exercise_2_classify_pos(word)
        if result is None:
            print("[未完成] 请实现 exercise_2_classify_pos 函数")
            return False
        if result == expected:
            print(f"  [正确] '{word}' → {result}")
        else:
            print(f"  [错误] '{word}' → 期望 {expected}, 实际 {result}")
            all_correct = False
    return all_correct


# ==============================================================================
# 练习 3：HMM 转移概率查询
# ==============================================================================

def exercise_3_transition(prev_tag: str, curr_tag: str) -> float:
    """
    练习 3：返回词性之间的转移概率

    ━━━━━━━ 提示 ━━━━━━━
    使用以下简化的转移概率表：
    - 代词(r) → 动词(v): 0.6
    - 动词(v) → 名词(n): 0.3
    - 副词(d) → 形容词(a): 0.4
    - 其他组合: 0.1

    参数：
        prev_tag: 前一个词的词性
        curr_tag: 当前词的词性

    返回：
        转移概率（浮点数）
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # table = {
    #     ("r", "v"): 0.6, ("v", "n"): 0.3, ("d", "a"): 0.4,
    # }
    # return table.get((prev_tag, curr_tag), 0.1)
    pass


def test_exercise_3():
    print("\n" + "=" * 60)
    print("练习 3：HMM 转移概率查询")
    print("=" * 60)

    test_cases = [("r", "v", 0.6), ("v", "n", 0.3), ("d", "a", 0.4), ("n", "n", 0.1)]
    all_correct = True
    for prev, curr, expected in test_cases:
        result = exercise_3_transition(prev, curr)
        if result is None:
            print("[未完成] 请实现 exercise_3_transition 函数")
            return False
        if abs(result - expected) < 0.01:
            print(f"  [正确] {prev}→{curr}: {result}")
        else:
            print(f"  [错误] {prev}→{curr}: 期望 {expected}, 实际 {result}")
            all_correct = False
    return all_correct


# ==============================================================================
# 主程序
# ==============================================================================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║        G-one NLP 学院 - 第三章 练习                    ║
    ║        词性标注                                      ║
    ╚══════════════════════════════════════════════════════╝
    """)

    results = []
    results.append(("练习1: 查词典标注", test_exercise_1()))
    results.append(("练习2: 识别词性类别", test_exercise_2()))
    results.append(("练习3: 转移概率查询", test_exercise_3()))

    print("\n" + "=" * 60)
    print("  练习清单")
    print("=" * 60)
    for name, passed in results:
        status = "[完成]" if passed else "[未完成]"
        print(f"  {status} {name}")

    completed = sum(1 for _, p in results if p)
    print(f"\n  完成率: {completed}/{len(results)}")
