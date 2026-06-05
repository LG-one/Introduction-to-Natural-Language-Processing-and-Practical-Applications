import sys
sys.stdout.reconfigure(encoding='utf-8')

"""
==============================================================================
第四章：命名实体识别 — 练习题
==============================================================================
G-one NLP 学院
日期：2026-05-16
==============================================================================
"""


# ==============================================================================
# 练习 1：BIO 标签转换
# ==============================================================================

def exercise_1_bio_convert(entities: list, sentence_length: int) -> list:
    """
    练习 1：将实体列表转换为 BIO 标签序列

    ━━━━━━━ 提示 ━━━━━━━
    1. 创建一个长度为 sentence_length 的列表，所有元素初始化为 "O"
    2. 遍历 entities 中的每个实体 (实体文本, 实体类型, 起始位置, 结束位置)
    3. 将起始位置设为 "B-{类型}"
    4. 将后续位置设为 "I-{类型}"
    5. 返回 BIO 标签列表

    参数：
        entities: 实体列表 [(实体文本, 实体类型, 起始位置, 结束位置), ...]
                  例如 [("小明", "PER", 0, 2), ("北京", "LOC", 3, 5)]
        sentence_length: 句子长度

    返回：
        BIO 标签列表，例如 ["B-PER", "I-PER", "O", "B-LOC", "I-LOC"]

    示例：
        entities = [("小明", "PER", 0, 2), ("北京", "LOC", 3, 5)]
        sentence_length = 7
        返回: ["B-PER", "I-PER", "O", "B-LOC", "I-LOC", "O", "O"]
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # bio_tags = ["O"] * sentence_length
    # for ent_text, ent_type, start, end in entities:
    #     bio_tags[start] = f"B-{ent_type}"
    #     for j in range(start + 1, end):
    #         bio_tags[j] = f"I-{ent_type}"
    # return bio_tags
    pass


def test_exercise_1():
    print("\n" + "=" * 60)
    print("练习 1：BIO 标签转换")
    print("=" * 60)

    test_cases = [
        {
            "entities": [("小明", "PER", 0, 2), ("北京", "LOC", 3, 5)],
            "length": 7,
            "expected": ["B-PER", "I-PER", "O", "B-LOC", "I-LOC", "O", "O"],
            "desc": "小明去北京旅游"
        },
        {
            "entities": [("清华大学", "ORG", 3, 7)],
            "length": 9,
            "expected": ["O", "O", "O", "B-ORG", "I-ORG", "I-ORG", "I-ORG", "O", "O"],
            "desc": "他在清华大学读书"
        },
        {
            "entities": [],
            "length": 4,
            "expected": ["O", "O", "O", "O"],
            "desc": "今天天气好"
        },
    ]

    all_correct = True
    for tc in test_cases:
        result = exercise_1_bio_convert(tc["entities"], tc["length"])
        if result is None:
            print("[未完成] 请实现 exercise_1_bio_convert 函数")
            return False
        if result == tc["expected"]:
            print(f"  [正确] '{tc['desc']}' → {result}")
        else:
            print(f"  [错误] '{tc['desc']}' → 期望 {tc['expected']}, 实际 {result}")
            all_correct = False
    return all_correct


# ==============================================================================
# 练习 2：从 BIO 标签提取实体
# ==============================================================================

def exercise_2_extract_entities(bio_tags: list) -> list:
    """
    练习 2：从 BIO 标签序列中提取实体

    ━━━━━━━ 提示 ━━━━━━━
    1. 遍历 bio_tags 中的每个 (字, 标签) 对
    2. 遇到 B-xxx 时：开始新实体，记录实体文本和类型
    3. 遇到 I-xxx 时：继续当前实体，追加字
    4. 遇到 O 时：结束当前实体，保存到结果列表
    5. 别忘了处理最后一个实体！

    参数：
        bio_tags: [(字, BIO标签), ...] 列表
                  例如 [("小", "B-PER"), ("明", "I-PER"), ("在", "O")]

    返回：
        实体列表 [(实体文本, 实体类型), ...]
        例如 [("小明", "PER")]

    示例：
        bio_tags = [("小", "B-PER"), ("明", "I-PER"), ("在", "O"), ("北", "B-LOC"), ("京", "I-LOC")]
        返回: [("小明", "PER"), ("北京", "LOC")]
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # entities = []
    # current_entity = ""
    # current_type = ""
    # for char, tag in bio_tags:
    #     if tag.startswith("B-"):
    #         if current_entity:
    #             entities.append((current_entity, current_type))
    #         current_entity = char
    #         current_type = tag[2:]
    #     elif tag.startswith("I-") and current_entity:
    #         current_entity += char
    #     else:
    #         if current_entity:
    #             entities.append((current_entity, current_type))
    #             current_entity = ""
    #             current_type = ""
    # if current_entity:
    #     entities.append((current_entity, current_type))
    # return entities
    pass


def test_exercise_2():
    print("\n" + "=" * 60)
    print("练习 2：从 BIO 标签提取实体")
    print("=" * 60)

    test_cases = [
        {
            "bio_tags": [("小", "B-PER"), ("明", "I-PER"), ("在", "O"),
                         ("北", "B-LOC"), ("京", "I-LOC")],
            "expected": [("小明", "PER"), ("北京", "LOC")],
            "desc": "人名+地名"
        },
        {
            "bio_tags": [("清", "B-ORG"), ("华", "I-ORG"), ("大", "I-ORG"), ("学", "I-ORG")],
            "expected": [("清华大学", "ORG")],
            "desc": "机构名"
        },
        {
            "bio_tags": [("今", "O"), ("天", "O"), ("天", "O"), ("气", "O")],
            "expected": [],
            "desc": "无实体"
        },
    ]

    all_correct = True
    for tc in test_cases:
        result = exercise_2_extract_entities(tc["bio_tags"])
        if result is None:
            print("[未完成] 请实现 exercise_2_extract_entities 函数")
            return False
        if result == tc["expected"]:
            print(f"  [正确] '{tc['desc']}' → {result}")
        else:
            print(f"  [错误] '{tc['desc']}' → 期望 {tc['expected']}, 实际 {result}")
            all_correct = False
    return all_correct


# ==============================================================================
# 练习 3：规则匹配人名
# ==============================================================================

def exercise_3_match_person(sentence: str, surnames: set, given_names: set) -> list:
    """
    练习 3：用规则匹配句子中的人名

    ━━━━━━━ 提示 ━━━━━━━
    规则：姓氏 + 名字（从 given_names 中找）
    1. 遍历句子中的每个位置
    2. 检查当前位置的字是否是姓氏（在 surnames 中）
    3. 如果是姓氏，检查后面1-2个字是否在 given_names 中
    4. 如果匹配成功，记录这个人名
    5. 返回所有找到的人名列表

    参数：
        sentence: 输入句子
        surnames: 姓氏集合，例如 {"张", "李", "王"}
        given_names: 名字集合，例如 {"三", "四", "明", "红", "小明"}

    返回：
        人名列表，例如 ["张三", "小明"]

    示例：
        sentence = "张三和小明去玩"
        surnames = {"张", "李", "王", "小"}
        given_names = {"三", "四", "明", "红", "小明"}
        返回: ["张三", "小明"]
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # persons = []
    # i = 0
    # while i < len(sentence):
    #     if sentence[i] in surnames:
    #         # 尝试匹配 "姓+名"（2-3个字）
    #         for name_len in [3, 2]:
    #             if i + name_len <= len(sentence):
    #                 candidate = sentence[i:i + name_len]
    #                 given = candidate[1:]  # 去掉姓氏
    #                 if given in given_names:
    #                     persons.append(candidate)
    #                     i += name_len
    #                     break
    #         else:
    #             i += 1
    #     else:
    #         i += 1
    # return persons
    pass


def test_exercise_3():
    print("\n" + "=" * 60)
    print("练习 3：规则匹配人名")
    print("=" * 60)

    surnames = {"张", "李", "王", "赵", "小"}
    given_names = {"三", "四", "五", "明", "红", "华", "小明", "小红"}

    test_cases = [
        {
            "sentence": "张三和李四去玩",
            "expected": ["张三", "李四"],
            "desc": "两个两字人名"
        },
        {
            "sentence": "小明和小红是朋友",
            "expected": ["小明", "小红"],
            "desc": "两个三字人名"
        },
        {
            "sentence": "今天天气好",
            "expected": [],
            "desc": "无人名"
        },
    ]

    all_correct = True
    for tc in test_cases:
        result = exercise_3_match_person(tc["sentence"], surnames, given_names)
        if result is None:
            print("[未完成] 请实现 exercise_3_match_person 函数")
            return False
        if result == tc["expected"]:
            print(f"  [正确] '{tc['sentence']}' → {result}")
        else:
            print(f"  [错误] '{tc['sentence']}' → 期望 {tc['expected']}, 实际 {result}")
            all_correct = False
    return all_correct


# ==============================================================================
# 主程序
# ==============================================================================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║        G-one NLP 学院 - 第四章 练习                    ║
    ║        命名实体识别                                  ║
    ╚══════════════════════════════════════════════════════╝
    """)

    results = []
    results.append(("练习1: BIO标签转换", test_exercise_1()))
    results.append(("练习2: 从BIO提取实体", test_exercise_2()))
    results.append(("练习3: 规则匹配人名", test_exercise_3()))

    print("\n" + "=" * 60)
    print("  练习清单")
    print("=" * 60)
    for name, passed in results:
        status = "[完成]" if passed else "[未完成]"
        print(f"  {status} {name}")

    completed = sum(1 for _, p in results if p)
    print(f"\n  完成率: {completed}/{len(results)}")
