import sys
sys.stdout.reconfigure(encoding='utf-8')

"""
==============================================================================
第一章：自然语言处理技术概述 — 练习题
==============================================================================
G-one NLP 学院
日期：2026-05-16

本章练习：
    1. 字符串基本操作
    2. 中文分词基础
    3. 文本预处理
    4. NLP 应用场景分析

运行方式：
    python exercises.py

提示：
    - 每个练习都有详细的提示，按照提示一步步来
    - 先自己写，写不出来再看注释中的参考答案
    - 运行后会自动检查你的答案是否正确
==============================================================================
"""


# ==============================================================================
# 练习 1：字符串基本操作
# ==============================================================================

def exercise_1_count_chars(text: str) -> dict:
    """
    练习 1：统计字符串中每个字符出现的次数

    ━━━━━━━ 生活类比 ━━━━━━━
    想象你面前有一大堆积木，你需要数一数每种颜色的积木有多少块。
    这个练习就是让你数一数每个字符出现了多少次。

    ━━━━━━━ 提示 ━━━━━━━
    1. 创建一个空字典 result = {}
    2. 遍历 text 中的每个字符 char
    3. 如果 char 不在字典中，设置 result[char] = 1
    4. 如果 char 已在字典中，设置 result[char] += 1
    5. 返回 result

    参数：
        text: 输入的字符串

    返回：
        一个字典，键是字符，值是出现次数
        例如：输入 "hello" → {'h': 1, 'e': 1, 'l': 2, 'o': 1}
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # result = {}
    # for char in text:
    #     if char in result:
    #         result[char] += 1
    #     else:
    #         result[char] = 1
    # return result
    pass


def test_exercise_1():
    """测试练习 1"""
    print("\n" + "=" * 60)
    print("练习 1：统计字符出现次数")
    print("=" * 60)

    text = "自然语言处理"
    result = exercise_1_count_chars(text)

    if result is None:
        print("[未完成] 请实现 exercise_1_count_chars 函数")
        return False

    expected = {'自': 1, '然': 1, '语': 1, '言': 1, '处': 1, '理': 1}
    if result == expected:
        print(f"[正确] 输入: '{text}'")
        print(f"       输出: {result}")
        return True
    else:
        print(f"[错误] 输入: '{text}'")
        print(f"       期望: {expected}")
        print(f"       实际: {result}")
        return False


# ==============================================================================
# 练习 2：简单中文分词
# ==============================================================================

def exercise_2_simple_segment(text: str, word_list: list) -> list:
    """
    练习 2：使用词典进行简单的中文正向最大匹配分词

    ━━━━━━━ 生活类比 ━━━━━━━
    想象你有一把尺子，上面刻着不同长度的刻度。
    你从句子的左边开始，每次都找最长的、能匹配上的词。
    就像切蛋糕：每次都尽量切最大的一块。

    ━━━━━━━ 提示 ━━━━━━━
    1. 创建一个空列表 result = []
    2. 设置当前位置 i = 0
    3. 当 i < len(text) 时，循环：
       a. 从最长的词开始尝试匹配（从 word_list 中找）
       b. 如果 text[i:i+len(word)] 在 word_list 中，就切出来
       c. i 向后移动这个词的长度
       d. 如果没有匹配的词，就把当前字当作一个词，i += 1
    4. 返回 result

    参数：
        text: 待分词的中文句子，如 "我爱自然语言处理"
        word_list: 词典列表，如 ["我", "爱", "自然", "语言", "自然语言", "处理"]

    返回：
        分词结果列表，如 ["我", "爱", "自然语言", "处理"]
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # result = []
    # i = 0
    # max_len = max(len(w) for w in word_list) if word_list else 1
    # while i < len(text):
    #     matched = False
    #     for length in range(max_len, 0, -1):
    #         if i + length > len(text):
    #             continue
    #         word = text[i:i+length]
    #         if word in word_list:
    #             result.append(word)
    #             i += length
    #             matched = True
    #             break
    #     if not matched:
    #         result.append(text[i])
    #         i += 1
    # return result
    pass


def test_exercise_2():
    """测试练习 2"""
    print("\n" + "=" * 60)
    print("练习 2：正向最大匹配分词")
    print("=" * 60)

    word_list = ["我", "爱", "自然", "语言", "自然语言", "处理", "自然语言处理"]
    text = "我爱自然语言处理"
    result = exercise_2_simple_segment(text, word_list)

    if result is None:
        print("[未完成] 请实现 exercise_2_simple_segment 函数")
        return False

    # 正向最大匹配应该得到 ["我", "爱", "自然语言处理"]
    expected = ["我", "爱", "自然语言处理"]
    if result == expected:
        print(f"[正确] 输入: '{text}'")
        print(f"       词典: {word_list}")
        print(f"       输出: {result}")
        return True
    else:
        print(f"[结果] 输入: '{text}'")
        print(f"       词典: {word_list}")
        print(f"       你的输出: {result}")
        print(f"       期望(正向最大匹配): {expected}")
        return False


# ==============================================================================
# 练习 3：去除停用词
# ==============================================================================

def exercise_3_remove_stopwords(words: list, stopwords: set) -> list:
    """
    练习 3：从词列表中去除停用词

    ━━━━━━━ 生活类比 ━━━━━━━
    想象你在洗菜，篮子里有菜也有杂草。
    你需要把杂草挑出来扔掉，只留下蔬菜。
    停用词就是"杂草"，它们出现频率高但对分析没有帮助。

    ━━━━━━━ 提示 ━━━━━━━
    1. 创建一个空列表 result = []
    2. 遍历 words 中的每个词 word
    3. 如果 word 不在 stopwords 中，就加入 result
    4. 返回 result

    参数：
        words: 词列表，如 ["我", "喜欢", "在", "北京", "学习"]
        stopwords: 停用词集合，如 {"我", "在", "的", "了"}

    返回：
        去除停用词后的列表，如 ["喜欢", "北京", "学习"]
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # return [w for w in words if w not in stopwords]
    pass


def test_exercise_3():
    """测试练习 3"""
    print("\n" + "=" * 60)
    print("练习 3：去除停用词")
    print("=" * 60)

    words = ["我", "喜欢", "在", "北京", "的", "大学", "学习", "了"]
    stopwords = {"我", "在", "的", "了", "是"}
    result = exercise_3_remove_stopwords(words, stopwords)

    if result is None:
        print("[未完成] 请实现 exercise_3_remove_stopwords 函数")
        return False

    expected = ["喜欢", "北京", "大学", "学习"]
    if result == expected:
        print(f"[正确] 输入: {words}")
        print(f"       停用词: {stopwords}")
        print(f"       输出: {result}")
        return True
    else:
        print(f"[错误] 输入: {words}")
        print(f"       停用词: {stopwords}")
        print(f"       期望: {expected}")
        print(f"       实际: {result}")
        return False


# ==============================================================================
# 练习 4：文本预处理流水线
# ==============================================================================

def exercise_4_preprocess(text: str) -> list:
    """
    练习 4：实现一个简单的文本预处理流水线

    ━━━━━━━ 生活类比 ━━━━━━━
    想象你在做一道菜：
    1. 先洗菜（去除多余空白）
    2. 再切菜（按空格分词）
    3. 最后挑出不能吃的（去除标点符号）

    ━━━━━━━ 提示 ━━━━━━━
    1. 用 strip() 去除首尾空格
    2. 用 replace("  ", " ") 把多个空格变成一个（循环执行）
    3. 用 split(" ") 按空格分词
    4. 从结果中去除标点符号（用 str.isalnum() 判断是否是字母或数字）
       注意：中文字符的 isalnum() 返回 True
    5. 返回清洗后的词列表

    参数：
        text: 原始文本，如 "  今天  天气  真好  ！  "

    返回：
        清洗后的词列表，如 ["今天", "天气", "真好"]
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # text = text.strip()
    # while "  " in text:
    #     text = text.replace("  ", " ")
    # words = text.split(" ")
    # result = [w for w in words if w.strip() and any(c.isalnum() for c in w)]
    # return result
    pass


def test_exercise_4():
    """测试练习 4"""
    print("\n" + "=" * 60)
    print("练习 4：文本预处理流水线")
    print("=" * 60)

    text = "  今天  天气  真好  ！  "
    result = exercise_4_preprocess(text)

    if result is None:
        print("[未完成] 请实现 exercise_4_preprocess 函数")
        return False

    # 至少应该去除了空白和标点
    has_no_punctuation = all(w.isalnum() for w in result)
    has_content = len(result) > 0

    if has_no_punctuation and has_content:
        print(f"[正确] 输入: '{text}'")
        print(f"       输出: {result}")
        print(f"       已去除空白和标点 ✓")
        return True
    else:
        print(f"[结果] 输入: '{text}'")
        print(f"       你的输出: {result}")
        if not has_no_punctuation:
            print(f"       提示: 结果中仍包含标点符号")
        if not has_content:
            print(f"       提示: 结果为空")
        return False


# ==============================================================================
# 练习 5：识别 NLP 任务类型
# ==============================================================================

def exercise_5_identify_task(description: str) -> str:
    """
    练习 5：根据描述识别 NLP 任务类型

    ━━━━━━━ 生活类比 ━━━━━━━
    想象你是一个医生，病人描述了症状，你需要判断他得了什么病。
    这个练习就是让你根据"症状"（描述）判断是哪种 NLP 任务。

    ━━━━━━━ 提示 ━━━━━━━
    判断 description 中包含哪些关键词，返回对应的 NLP 任务：
    - 如果包含"分词"或"切词" → "分词"
    - 如果包含"词性"或"标注" → "词性标注"
    - 如果包含"实体"或"人名"或"地名" → "命名实体识别"
    - 如果包含"情感"或"好评"或"差评" → "情感分析"
    - 如果包含"分类"或"类别" → "文本分类"
    - 如果包含"翻译" → "机器翻译"
    - 如果包含"摘要"或"总结" → "文本摘要"
    - 以上都不匹配 → "未知任务"

    参数：
        description: NLP 任务的中文描述

    返回：
        任务类型的字符串
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # keywords_map = {
    #     "分词": "分词", "切词": "分词",
    #     "词性": "词性标注", "标注": "词性标注",
    #     "实体": "命名实体识别", "人名": "命名实体识别", "地名": "命名实体识别",
    #     "情感": "情感分析", "好评": "情感分析", "差评": "情感分析",
    #     "分类": "文本分类", "类别": "文本分类",
    #     "翻译": "机器翻译",
    #     "摘要": "文本摘要", "总结": "文本摘要",
    # }
    # for keyword, task in keywords_map.items():
    #     if keyword in description:
    #         return task
    # return "未知任务"
    pass


def test_exercise_5():
    """测试练习 5"""
    print("\n" + "=" * 60)
    print("练习 5：识别 NLP 任务类型")
    print("=" * 60)

    test_cases = [
        ("把句子切成一个个词", "分词"),
        ("判断每个词是名词还是动词", "词性标注"),
        ("找出句子中的人名和地名", "命名实体识别"),
        ("判断评论是好评还是差评", "情感分析"),
        ("把新闻分成体育、财经等类别", "文本分类"),
        ("把中文翻译成英文", "机器翻译"),
        ("把长文章压缩成短摘要", "文本摘要"),
    ]

    all_correct = True
    for desc, expected in test_cases:
        result = exercise_5_identify_task(desc)
        if result is None:
            print("[未完成] 请实现 exercise_5_identify_task 函数")
            return False
        if result == expected:
            print(f"  [正确] '{desc}' → {result}")
        else:
            print(f"  [错误] '{desc}' → 期望: {expected}, 实际: {result}")
            all_correct = False

    return all_correct


# ==============================================================================
# 主程序：运行所有练习测试
# ==============================================================================

if __name__ == "__main__":

    print("""
    ╔══════════════════════════════════════════════════════╗
    ║        G-one NLP 学院 - 第一章 练习                    ║
    ║        自然语言处理技术概述                             ║
    ╚══════════════════════════════════════════════════════╝
    """)

    # 运行所有练习测试
    results = []
    results.append(("练习1: 统计字符次数", test_exercise_1()))
    results.append(("练习2: 正向最大匹配分词", test_exercise_2()))
    results.append(("练习3: 去除停用词", test_exercise_3()))
    results.append(("练习4: 文本预处理", test_exercise_4()))
    results.append(("练习5: 识别NLP任务", test_exercise_5()))

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
        print("  你已经掌握了 NLP 的基本概念。")
        print("  下一章我们将学习中文分词。")
    else:
        print(f"\n  还有 {total - completed} 个练习未完成。")
        print("  不要着急，慢慢来，理解了再写代码。")
        print("  如果实在写不出来，可以查看注释中的参考答案。")
