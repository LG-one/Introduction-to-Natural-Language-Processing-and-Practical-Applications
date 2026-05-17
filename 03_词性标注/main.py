import sys
sys.stdout.reconfigure(encoding='utf-8')

"""
==============================================================================
第三章：词性标注 — 完整演示
==============================================================================
G-one NLP 学院
日期：2026-05-16
==============================================================================
"""

from pos_tagging import (
    rule_based_pos_tag, HMMPOSTagger, POS_DICTIONARY,
    TrainedHMMPOSTagger, CRFPOSTagger,
)


def print_separator(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def lesson_pos_concept():
    print_separator("3.1 什么是词性标注")

    print("""
    词性标注（POS Tagging）就是给句子中的每个词标注它的词性。

    常见词性：
    ┌────────┬────────┬──────────────────┐
    │ 标签   │ 含义   │ 例子              │
    ├────────┼────────┼──────────────────┤
    │ n      │ 名词   │ 苹果、学校、学生   │
    │ v      │ 动词   │ 吃、学习、研究     │
    │ a      │ 形容词 │ 好、美丽、聪明     │
    │ d      │ 副词   │ 很、非常、已经     │
    │ r      │ 代词   │ 我、你、他         │
    │ nr     │ 人名   │ 小明、张三         │
    │ ns     │ 地名   │ 北京、上海         │
    │ nt     │ 机构名 │ 清华大学、腾讯     │
    └────────┴────────┴──────────────────┘
    """)


def lesson_rule_based():
    print_separator("3.2 基于规则的词性标注")

    print("原理：维护一个\"词->词性\"的词典，遇到词直接查表。\n")

    test_cases = [
        ["我", "喜欢", "吃", "苹果"],
        ["今天", "天气", "很", "好"],
        ["小明", "在", "清华大学", "学习", "机器学习"],
    ]

    for words in test_cases:
        result = rule_based_pos_tag(words)
        tags = " ".join([f"{w}/{t}" for w, t in result])
        print(f"  {''.join(words)} → {tags}")


def lesson_hmm_tagger():
    print_separator("3.3 HMM 词性标注")

    print("""
    HMM 词性标注的核心思想：
    - 每个词的词性不仅取决于词本身，还取决于前一个词的词性
    - 用维特比算法找到最可能的词性序列

    三个概率：
    1. 初始概率：句子开头的词性概率
    2. 转移概率：词性之间的转移概率
    3. 发射概率：词性下出现某个词的概率
    """)

    tagger = HMMPOSTagger()

    test_cases = [
        ["我", "喜欢", "学习"],
        ["今天", "天气", "很好"],
        ["小明", "在", "清华大学", "学习"],
    ]

    for words in test_cases:
        result = tagger.tag(words)
        tags = " ".join([f"{w}/{t}" for w, t in result])
        print(f"  {''.join(words)} → {tags}")


def lesson_jieba():
    print_separator("3.4 jieba 词性标注实战")

    try:
        import jieba.posseg as pseg
    except ImportError:
        print("[提示] jieba 未安装，请运行: pip install jieba")
        return

    sentences = [
        "小明在北京大学学习自然语言处理",
        "今天天气非常好",
        "清华大学是中国最好的大学之一",
    ]

    for sent in sentences:
        print(f"\n句子: {sent}")
        words_pos = pseg.cut(sent)
        tags = " ".join([f"{w}/{f}" for w, f in words_pos])
        print(f"  标注: {tags}")


def lesson_trained_hmm():
    """演示可训练的 HMM 词性标注器"""

    print_separator("3.5 可训练的 HMM 词性标注器")

    print("""
    前面的 HMM 用手工编写的概率，现在我们从数据中自动学习！

    训练数据：一批已经标注好词性的句子
    学习目标：初始概率、转移概率、发射概率

    ━━━━━━━ 拉普拉斯平滑 ━━━━━━━
    没见过的组合怎么办？给每个计数加1，确保概率不为0。
    就像投票时每人至少有1票基础票。
    """)

    # ── 准备训练数据 ──
    # 每个句子是 [(词, 词性), ...] 的列表
    training_data = [
        [("我", "r"), ("喜欢", "v"), ("吃", "v"), ("苹果", "n")],
        [("他", "r"), ("喜欢", "v"), ("喝", "v"), ("牛奶", "n")],
        [("小明", "nr"), ("在", "p"), ("学校", "n"), ("学习", "v")],
        [("今天", "t"), ("天气", "n"), ("很", "d"), ("好", "a")],
        [("她", "r"), ("是", "v"), ("一个", "m"), ("好", "a"), ("学生", "n")],
        [("我们", "r"), ("都", "d"), ("喜欢", "v"), ("学习", "v")],
        [("苹果", "n"), ("是", "v"), ("好", "a"), ("水果", "n")],
        [("他", "r"), ("在", "p"), ("清华大学", "nt"), ("学习", "v"), ("机器学习", "n")],
        [("小红", "nr"), ("吃", "v"), ("了", "u"), ("一个", "m"), ("苹果", "n")],
        [("老师", "n"), ("很", "d"), ("喜欢", "v"), ("这个", "r"), ("学生", "n")],
        [("我", "r"), ("的", "u"), ("妈妈", "n"), ("在", "p"), ("医院", "n"), ("工作", "v")],
        [("他", "r"), ("买", "v"), ("了", "u"), ("三", "m"), ("本", "q"), ("书", "n")],
    ]

    tagger = TrainedHMMPOSTagger()
    tagger.train(training_data)

    # ── 测试 ──
    test_cases = [
        ["我", "喜欢", "学习"],
        ["今天", "天气", "很好"],
        ["小明", "在", "清华大学", "学习"],
        ["她", "吃", "苹果"],
    ]

    print("\n  测试结果:")
    for words in test_cases:
        result = tagger.tag(words)
        tags = " ".join([f"{w}/{t}" for w, t in result])
        print(f"  {''.join(words)} → {tags}")


def lesson_crf_tagger():
    """演示 CRF 词性标注器"""

    print_separator("3.6 CRF 词性标注器（基于平均感知机）")

    print("""
    CRF 比 HMM 更强大：
    - 可以使用多种特征（前后词、词缀、数字等）
    - 没有严格的独立性假设
    - 直接建模 P(标签序列|词序列)

    ━━━━━━━ 特征函数 ━━━━━━━
    CRF 的核心是"特征"：
    - 当前词："苹果" → 可能是名词
    - 前一个词："吃苹果" → "吃"暗示后面是名词
    - 后缀："高兴地" → "地"暗示是副词
    - 是否数字："123" → 可能是数词

    ━━━━━━━ 训练方法：平均感知机 ━━━━━━━
    1. 看一个样本，用当前模型预测
    2. 预测正确 → 不修改
    3. 预测错误 → 增加正确答案的权重，减少错误答案的权重
    4. 多轮训练后取平均权重
    """)

    # ── 准备训练数据 ──
    training_data = [
        [("我", "r"), ("喜欢", "v"), ("吃", "v"), ("苹果", "n")],
        [("他", "r"), ("喜欢", "v"), ("喝", "v"), ("牛奶", "n")],
        [("小明", "nr"), ("在", "p"), ("学校", "n"), ("学习", "v")],
        [("今天", "t"), ("天气", "n"), ("很", "d"), ("好", "a")],
        [("她", "r"), ("是", "v"), ("一个", "m"), ("好", "a"), ("学生", "n")],
        [("我们", "r"), ("都", "d"), ("喜欢", "v"), ("学习", "v")],
        [("苹果", "n"), ("是", "v"), ("好", "a"), ("水果", "n")],
        [("他", "r"), ("在", "p"), ("清华大学", "nt"), ("学习", "v"), ("机器学习", "n")],
        [("小红", "nr"), ("吃", "v"), ("了", "u"), ("一个", "m"), ("苹果", "n")],
        [("老师", "n"), ("很", "d"), ("喜欢", "v"), ("这个", "r"), ("学生", "n")],
        [("我", "r"), ("的", "u"), ("妈妈", "n"), ("在", "p"), ("医院", "n"), ("工作", "v")],
        [("他", "r"), ("买", "v"), ("了", "u"), ("三", "m"), ("本", "q"), ("书", "n")],
    ]

    tagger = CRFPOSTagger()
    tagger.train(training_data, num_iterations=10)

    # ── 测试 ──
    test_cases = [
        ["我", "喜欢", "学习"],
        ["今天", "天气", "很好"],
        ["小明", "在", "清华大学", "学习"],
        ["她", "吃", "苹果"],
        ["他", "买", "了", "两", "本", "书"],
    ]

    print("\n  测试结果:")
    for words in test_cases:
        result = tagger.tag(words)
        tags = " ".join([f"{w}/{t}" for w, t in result])
        print(f"  {''.join(words)} → {tags}")

    # ── 展示学到的特征权重 ──
    print("\n  部分特征权重示例:")
    shown = 0
    for (feat_name, feat_value, tag), weight in sorted(
        tagger.weights.items(), key=lambda x: abs(x[1]), reverse=True
    ):
        if shown >= 10:
            break
        if weight != 0:
            print(f"    ({feat_name}, {feat_value}, {tag}) → {weight:.2f}")
            shown += 1


# ==============================================================================
# 主程序
# ==============================================================================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║        G-one NLP 学院 - 第三章                        ║
    ║        词性标注                                      ║
    ╚══════════════════════════════════════════════════════╝
    """)

    lesson_pos_concept()
    lesson_rule_based()
    lesson_hmm_tagger()
    lesson_jieba()
    lesson_trained_hmm()
    lesson_crf_tagger()

    print("\n" + "=" * 60)
    print("  第三章 总结")
    print("=" * 60)
    print("""
    [OK] 词性标注 — 给每个词标注词性（名词、动词、形容词等）
    [OK] 规则方法 — 查词典，简单但依赖词典质量
    [OK] HMM 方法 — 用概率推断，能处理未知词
    [OK] 可训练 HMM — 从标注数据自动学习概率，拉普拉斯平滑
    [OK] CRF 方法 — 使用多特征的判别式模型，平均感知机训练
    [OK] jieba 实战 — 开箱即用的词性标注工具
    """)

    print("-" * 60)
    print("  下节预告：第四章 — 命名实体识别")
    print("-" * 60)
