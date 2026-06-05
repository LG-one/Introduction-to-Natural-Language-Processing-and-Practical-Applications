import sys
sys.stdout.reconfigure(encoding='utf-8')

"""
==============================================================================
第五章：依存句法分析 — 完整演示
==============================================================================
G-one NLP 学院
日期：2026-05-16

运行方式：
    python main.py

前置知识：
    - 第三章：词性标注
    - 第四章：命名实体识别（可选）

本章内容：
    1. 依存句法分析的概念
    2. 依存关系的类型
    3. 基于规则的依存分析
    4. 依存树的操作与可视化
    5. 评估指标（UAS / LAS）
==============================================================================
"""

from dependency import (
    DependencyArc,
    DependencyTree,
    RuleBasedDependencyParser,
    TransitionParser,
    evaluate_dependency,
    demo_dependency_concept,
    demo_rule_based_parsing,
    demo_tree_operations,
    demo_evaluation,
)


def print_separator(title: str):
    """打印分隔线和标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def lesson_what_is_dependency():
    """第一部分：什么是依存句法分析"""

    print_separator("5.1 什么是依存句法分析")

    print("""
    依存句法分析（Dependency Parsing）是分析句子中词与词之间
    "依存关系"的技术。

    ━━━━━━━ 生活类比 ━━━━━━━
    想象你在读一句话："小明在学校学习自然语言处理"

    你需要回答这些问题：
    - "小明"在做什么？→ 学习（小明依存于"学习"）
    - "学习"什么？→ 自然语言处理（自然语言处理依存于"学习"）
    - 在哪里学习？→ 在学校（学校依存于"学习"）

    这就是依存分析：找出每个词和哪个词有关系，是什么关系。

    ┌──────────────────────────────────────────────┐
    │  依存句法分析 vs 成分句法分析                    │
    ├──────────────────┬───────────────────────────┤
    │  依存分析         │  成分分析                   │
    │  (Dependency)     │  (Constituency)            │
    ├──────────────────┼───────────────────────────┤
    │  词与词之间的关系   │  短语结构                   │
    │  "谁修饰谁"       │  "哪些词组成短语"             │
    │  扁平结构          │  嵌套结构                    │
    │  适合中文          │  适合英文                    │
    └──────────────────┴───────────────────────────┘
    """)

    demo_dependency_concept()


def lesson_relation_types():
    """第二部分：依存关系的类型"""

    print_separator("5.2 依存关系的类型")

    print("""
    中文依存句法分析中常见的关系类型：

    ┌──────────────────────────────────────────────────┐
    │  关系    │  名称        │  含义         │  例子      │
    ├─────────┼─────────────┼──────────────┼──────────┤
    │  SBV    │  主谓关系     │  主语→谓语    │ 小明←吃   │
    │  VOB    │  动宾关系     │  动词→宾语    │ 吃→苹果   │
    │  ATT    │  定中关系     │  定语→中心语  │ 红色←苹果 │
    │  ADV    │  状中关系     │  状语→中心语  │ 很←快     │
    │  CMP    │  动补关系     │  动词→补语    │ 跑→得快   │
    │  COO    │  并列关系     │  并列成分     │ 苹果↔香蕉 │
    │  HED    │  核心关系     │  ROOT→核心词  │ ROOT→吃   │
    │  POB    │  介宾关系     │  介词→宾语    │ 在→学校   │
    │  RAD    │  右附加关系   │  中心词→助词  │ 吃→了     │
    │  LAD    │  左附加关系   │  连词→中心词  │ 和←苹果   │
    │  IC     │  独立分句     │  分句关系     │ 他说,我做 │
    └─────────┴─────────────┴──────────────┴──────────┘

    关键理解：
    - SBV (Subject-Verb): 谁在做？
    - VOB (Verb-Object): 做什么？
    - ATT (Attribute): 什么样的？
    - ADV (Adverbial): 怎么做？
    """)


def lesson_rule_based():
    """第三部分：基于规则的依存分析"""

    print_separator("5.3 基于规则的依存分析")

    print("""
    基于规则的依存分析就像按照"交通规则"来判断关系：

    规则 1: 代词(r)在动词(v)左边 → 主语关系 (SBV)
    规则 2: 名词(n)在动词(v)右边 → 宾语关系 (VOB)
    规则 3: 形容词(a)在名词(n)左边 → 定中关系 (ATT)
    规则 4: 副词(d)在动词(v)左边 → 状中关系 (ADV)
    规则 5: 动词通常是句子的核心 (HED)
    """)

    demo_rule_based_parsing()


def lesson_tree_operations():
    """第四部分：依存树的操作"""

    print_separator("5.4 依存树的操作与可视化")

    demo_tree_operations()

    print("""
    依存树的常用操作：
    1. get_root()     — 找到核心词
    2. get_children() — 获取某个词的所有孩子
    3. get_head()     — 获取某个词的父亲
    4. display()      — 可视化显示树结构

    这些操作在实际 NLP 应用中非常有用：
    - 问答系统：找动词的宾语 → 回答"做了什么"
    - 情感分析：找形容词修饰的名词 → 判断情感对象
    - 信息抽取：找主语和宾语 → 提取事件三元组
    """)


def lesson_evaluation():
    """第五部分：评估指标"""

    print_separator("5.5 依存分析的评估指标")

    demo_evaluation()

    print("""
    UAS 和 LAS 是依存分析最常用的评估指标：

    ┌──────────────────────────────────────────────┐
    │  指标  │  含义                    │  要求      │
    ├────────┼─────────────────────────┼──────────┤
    │  UAS   │  无标记依存正确率         │  核心词对  │
    │  LAS   │  有标记依存正确率         │  核心词+  │
    │        │                         │  关系都对  │
    └────────┴─────────────────────────┴──────────┘

    LAS 比 UAS 更严格，因为不仅要找对核心词，还要标对关系类型。
    """)


def lesson_advanced_demo():
    """第六部分：综合示例"""

    print_separator("5.6 综合示例：分析复杂句子")

    parser = RuleBasedDependencyParser()

    complex_sentences = [
        (["小明", "在", "北京大学", "努力", "学习", "自然语言处理"],
         ["nr", "p", "nt", "d", "v", "n"]),
        (["红色", "的", "苹果", "和", "黄色", "的", "香蕉", "都", "很", "好吃"],
         ["a", "u", "n", "c", "a", "u", "n", "d", "d", "a"]),
        (["我", "的", "妈妈", "在", "医院", "工作"],
         ["r", "u", "n", "p", "n", "v"]),
    ]

    for words, pos_tags in complex_sentences:
        sentence = "".join(words)
        print(f"\n句子: {sentence}")

        tree = parser.parse(words, pos_tags)
        tree.display()


def lesson_transition_parser():
    """演示基于转移的依存句法分析器"""

    print_separator("5.7 基于转移的依存句法分析器（Arc-Eager）")

    print("""
    基于转移的分析是一种系统化的依存分析方法：

    ━━━━━━━ 核心思想 ━━━━━━━
    将依存分析看作一系列"动作"的决策：
    - SHIFT:     从 buffer 取词压入 stack（拿起一本书）
    - LEFT-ARC:  建立 buffer[0] → stack[-1] 的弧（地上的书是手里书的父亲）
    - RIGHT-ARC: 建立 stack[-1] → buffer[0] 的弧（手里的书是地上书的父亲）
    - REDUCE:    弹出 stack 顶部（书已处理完毕）

    ━━━━━━━ 特征提取 ━━━━━━━
    每次决策时，观察：
    - 栈顶的词和词性（手里拿着什么？）
    - buffer第一个词和词性（地上最前面是什么？）
    - 两者的组合（这两本书有什么关系？）

    ━━━━━━━ 训练方式 ━━━━━━━
    使用感知机训练：
    1. Oracle 告诉每步正确动作
    2. 模型预测错误时更新权重
    """)

    parser = TransitionParser()

    # ── 准备训练数据 ──
    # 每个元素: (words, pos_tags, gold_arcs)
    training_data = [
        (
            ["小明", "吃", "苹果"],
            ["nr", "v", "n"],
            [
                DependencyArc(0, 1, "SBV"),
                DependencyArc(2, 1, "VOB"),
                DependencyArc(1, -1, "HED"),
            ],
        ),
        (
            ["我", "喜欢", "学习"],
            ["r", "v", "v"],
            [
                DependencyArc(0, 1, "SBV"),
                DependencyArc(2, 1, "VOB"),
                DependencyArc(1, -1, "HED"),
            ],
        ),
        (
            ["今天", "天气", "很", "好"],
            ["t", "n", "d", "a"],
            [
                DependencyArc(0, 1, "ATT"),
                DependencyArc(2, 3, "ADV"),
                DependencyArc(3, 1, "VOB"),
                DependencyArc(1, -1, "HED"),
            ],
        ),
        (
            ["她", "是", "学生"],
            ["r", "v", "n"],
            [
                DependencyArc(0, 1, "SBV"),
                DependencyArc(2, 1, "VOB"),
                DependencyArc(1, -1, "HED"),
            ],
        ),
        (
            ["老师", "喜欢", "这个", "学生"],
            ["n", "v", "r", "n"],
            [
                DependencyArc(0, 1, "SBV"),
                DependencyArc(2, 3, "ATT"),
                DependencyArc(3, 1, "VOB"),
                DependencyArc(1, -1, "HED"),
            ],
        ),
        (
            ["他", "在", "学校", "学习"],
            ["r", "p", "n", "v"],
            [
                DependencyArc(0, 3, "SBV"),
                DependencyArc(1, 3, "ADV"),
                DependencyArc(2, 1, "POB"),
                DependencyArc(3, -1, "HED"),
            ],
        ),
    ]

    print("\n  训练转移解析器...")
    parser.train(training_data, num_iterations=10)

    # ── 测试解析 ──
    test_cases = [
        (["小明", "吃", "苹果"], ["nr", "v", "n"]),
        (["我", "喜欢", "学习"], ["r", "v", "v"]),
        (["今天", "天气", "很好"], ["t", "n", "d"]),
        (["她", "是", "学生"], ["r", "v", "n"]),
    ]

    print("\n  测试结果:")
    for words, pos_tags in test_cases:
        tree = parser.parse(words, pos_tags)
        print(f"\n  句子: {''.join(words)}")
        for arc in tree.arcs:
            head_str = "ROOT" if arc.head_index == -1 else words[arc.head_index]
            print(f"    {words[arc.dependent_index]} --{arc.relation}--> {head_str}")

    # ── 展示解析过程 ──
    print("\n  ━━━━━━━ 详细解析过程演示 ━━━━━━━")
    parser.parse_with_demo(["小明", "吃", "苹果"], ["nr", "v", "n"])


# ==============================================================================
# 主程序入口
# ==============================================================================

if __name__ == "__main__":

    # 打印课程标题
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║        G-one NLP 学院 - 第五章                        ║
    ║        依存句法分析（Dependency Parsing）              ║
    ╚══════════════════════════════════════════════════════╝
    """)

    # 按顺序运行所有课程内容
    lesson_what_is_dependency()
    lesson_relation_types()
    lesson_rule_based()
    lesson_tree_operations()
    lesson_evaluation()
    lesson_advanced_demo()
    lesson_transition_parser()

    # 课程总结
    print("\n" + "=" * 60)
    print("  第五章 总结")
    print("=" * 60)
    print("""
    [OK] 依存句法分析 — 分析词与词之间的"谁修饰谁"关系
    [OK] 依存关系三要素 — 核心词、依存词、关系类型
    [OK] 常见关系类型 — SBV(主语)、VOB(宾语)、ATT(定语)等
    [OK] 基于规则的分析 — 用词性规则判断依存关系
    [OK] 依存树操作 — 查找核心词、孩子、父亲
    [OK] 评估指标 — UAS(无标记)和 LAS(有标记)
    [OK] 转移解析器 — Arc-Eager 系统，特征打分，感知机训练
    """)

    # 下节预告
    print("-" * 60)
    print("  下节预告：第六章 — 语义角色标注")
    print("-" * 60)
    print("""
    下一章我们将学习语义角色标注（SRL）：
    - "谁对谁做了什么"的深层语义分析
    - 谓词-论元结构
    - 施事、受事、时间、地点等语义角色

    预习建议：
    - 思考："小明在公园用球踢了小狗"中，谁是施事？谁是受事？
    - 依存分析和语义角色标注有什么联系？
    """)
