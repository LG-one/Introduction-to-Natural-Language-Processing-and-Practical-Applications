"""
==============================================================================
第五章：依存句法分析（Dependency Parsing）
==============================================================================
日期：2026-05-16

同学们好！前面我们学了分词、词性标注、命名实体识别，这些都是在"词"的层面。
今天我们上升到"句子结构"的层面 —— 依存句法分析。

----------------------------------------------------------------------
生活类比：依存句法分析就像画一棵家族树
----------------------------------------------------------------------

想象你是一个家族 historian，要画一棵家族树：

  爷爷（一家之主）
    ├── 爸爸（儿子）
    │     ├── 我（孙子）
    │     └── 妹妹（孙女）
    └── 叔叔（儿子）

每个人都有一个"父亲"，这就是"依存关系"。
依存句法分析也是这样：找出句子中每个词的"父亲"（被谁支配）。

例如句子："小明吃苹果"

        吃（核心动词，一家之主）
       / \
      /   \
    小明   苹果
   (主语)  (宾语)

  - "吃"是核心词（ROOT 的孩子）
  - "小明"依存于"吃"（小明是吃的主语）
  - "苹果"依存于"吃"（苹果是吃的宾语）

----------------------------------------------------------------------
什么是依存关系？
----------------------------------------------------------------------

依存关系（Dependency Relation）描述的是词与词之间的"支配"关系：
  - 核心词（Head）：被依赖的词，是"父亲"
  - 依存词（Dependent）：依赖别人的词，是"孩子"
  - 关系类型（Relation）：描述依存的类型（主语、宾语、修饰等）

  ┌──────────────────────────────────────────────┐
  │  依存关系的基本要素                              │
  ├──────────────────────────────────────────────┤
  │  核心词（Head）     →  被依赖的词（父亲）        │
  │  依存词（Dependent） →  依赖别人的词（孩子）      │
  │  关系类型（Rel）     →  主语？宾语？修饰？        │
  └──────────────────────────────────────────────┘

----------------------------------------------------------------------
常见的依存关系类型
----------------------------------------------------------------------

  ┌──────────────────────────────────────────────────┐
  │  关系标签    │  含义            │  例子              │
  ├─────────────┼─────────────────┼──────────────────┤
  │  SBV        │  主谓关系        │  小明 ← 吃         │
  │  VOB        │  动宾关系        │  吃 → 苹果         │
  │  ATT        │  定中关系        │  红色 ← 苹果       │
  │  ADV        │  状中关系        │  快速 ← 跑         │
  │  CMP        │  动补关系        │  跑 → 得快         │
  │  COO        │  并列关系        │  苹果 ↔ 香蕉       │
  │  HED        │  核心关系        │  ROOT → 吃         │
  │  POB        │  介宾关系        │  在 → 学校         │
  │  FOB        │  前置宾语        │  把 → 苹果         │
  │  LAD        │  左附加关系      │  和 ← 苹果         │
  │  RAD        │  右附加关系      │  吃 → 了           │
  │  IS         │  独立结构        │  据说 ...          │
  └─────────────┴─────────────────┴──────────────────┘

==============================================================================
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')


# ==============================================================================
# 第一部分：依存关系的数据结构
# ==============================================================================
#
# 我们用一个简单的类来表示依存关系中的"弧"（arc）。
#
# 就像家族树中的一条线：从父亲指向孩子，线上标注着关系。
#
# ==============================================================================

class DependencyArc:
    """
    依存弧：表示一条依存关系

    ━━━━━━━ 生活类比 ━━━━━━━
    想象家族树中的一条连线：
    - head_index: 父亲的位置（在句子中的第几个词）
    - dependent_index: 孩子的位置
    - relation: 关系类型（比如"父子"、"祖孙"）

    属性：
        dependent_index: 依存词的位置（孩子）
        head_index: 核心词的位置（父亲），-1 表示 ROOT
        relation: 依存关系类型（如 SBV、VOB、ATT 等）
    """

    def __init__(self, dependent_index: int, head_index: int, relation: str):
        """
        初始化一条依存弧

        参数：
            dependent_index: 依存词的索引（孩子节点）
            head_index: 核心词的索引（父亲节点），-1 表示 ROOT
            relation: 依存关系类型
        """
        self.dependent_index = dependent_index  # 孩子的位置
        self.head_index = head_index            # 父亲的位置
        self.relation = relation                # 关系类型

    def __repr__(self):
        """打印依存弧的信息"""
        head_str = "ROOT" if self.head_index == -1 else str(self.head_index)
        return f"Arc({self.dependent_index} <--{self.relation}-- {head_str})"


class DependencyTree:
    """
    依存树：一个句子的完整依存分析结果

    ━━━━━━━ 生活类比 ━━━━━━━
    想象一棵家族树：
    - words: 家族成员名单（句子中的词）
    - arcs: 所有的连线（依存关系）
    - root_index: 族长的位置（核心词）

    属性：
        words: 词列表
        arcs: 依存弧列表
        pos_tags: 词性列表（可选）
    """

    def __init__(self, words: list, arcs: list = None, pos_tags: list = None):
        """
        初始化依存树

        参数：
            words: 词列表
            arcs: 依存弧列表
            pos_tags: 词性列表（可选）
        """
        self.words = words           # 句子中的词
        self.arcs = arcs or []       # 依存弧列表
        self.pos_tags = pos_tags     # 词性标签（可选）

    def get_root(self) -> int:
        """
        找到依存树的根节点（核心词）

        返回：
            根节点在 words 中的索引
        """
        for arc in self.arcs:
            if arc.head_index == -1:
                return arc.dependent_index
        return 0  # 默认返回第一个词

    def get_children(self, index: int) -> list:
        """
        获取某个词的所有孩子节点

        参数：
            index: 词的索引

        返回：
            [(孩子索引, 关系类型), ...] 列表
        """
        children = []
        for arc in self.arcs:
            if arc.head_index == index:
                children.append((arc.dependent_index, arc.relation))
        return children

    def get_head(self, index: int) -> tuple:
        """
        获取某个词的父亲节点

        参数：
            index: 词的索引

        返回：
            (父亲索引, 关系类型) 或 (-1, "HED") 如果是根节点
        """
        for arc in self.arcs:
            if arc.dependent_index == index:
                return (arc.head_index, arc.relation)
        return (-1, "HED")

    def display(self):
        """
        可视化显示依存树

        用 ASCII 字符画出依存树的结构
        """
        if not self.words:
            print("  (空句子)")
            return

        root_idx = self.get_root()

        # 打印每个词及其依存关系
        print(f"  {'索引':<6}{'词':<10}{'词性':<8}{'核心词':<10}{'关系':<8}")
        print(f"  {'─' * 42}")

        for i, word in enumerate(self.words):
            head_idx, rel = self.get_head(i)
            pos = self.pos_tags[i] if self.pos_tags else "-"
            head_word = "ROOT" if head_idx == -1 else self.words[head_idx]
            marker = " ★" if i == root_idx else ""
            print(f"  {i:<6}{word:<10}{pos:<8}{head_word:<10}{rel:<8}{marker}")

        # 打印树形结构
        print(f"\n  树形结构：")
        self._print_tree(root_idx, "  ", True)

    def _print_tree(self, index: int, prefix: str, is_last: bool):
        """递归打印树形结构"""
        connector = "└── " if is_last else "├── "
        word = self.words[index]
        head_idx, rel = self.get_head(index)
        rel_str = f"({rel})" if rel != "HED" else "(核心)"
        print(f"{prefix}{connector}{word} {rel_str}")

        children = self.get_children(index)
        for i, (child_idx, child_rel) in enumerate(children):
            is_last_child = (i == len(children) - 1)
            extension = "    " if is_last else "│   "
            self._print_tree(child_idx, prefix + extension, is_last_child)


# ==============================================================================
# 第二部分：基于规则的依存句法分析器
# ==============================================================================
#
# 最简单的依存分析方法：用规则来判断词与词之间的依存关系。
#
# 就像家族关系的判断规则：
#   - 如果一个词是代词（我、你、他），它很可能是主语
#   - 如果一个词是名词，它很可能是宾语
#   - 动词通常是句子的核心
#
# ==============================================================================

class RuleBasedDependencyParser:
    """
    基于规则的依存句法分析器

    ━━━━━━━ 核心思想 ━━━━━━━
    1. 找到句子的核心词（通常是动词）
    2. 核心词左边的代词/名词 → 主语关系（SBV）
    3. 核心词右边的名词 → 宾语关系（VOB）
    4. 形容词修饰名词 → 定中关系（ATT）
    5. 副词修饰动词/形容词 → 状中关系（ADV）
    """

    def __init__(self):
        """初始化规则分析器"""
        # 词性到角色的映射规则
        self.rules = {
            # 代词在动词左边 → 主语
            ("r", "left", "v"): "SBV",
            # 名词在动词左边 → 主语
            ("n", "left", "v"): "SBV",
            # 人名在动词左边 → 主语
            ("nr", "left", "v"): "SBV",
            # 名词在动词右边 → 宾语
            ("n", "right", "v"): "VOB",
            # 形容词在名词左边 → 定语
            ("a", "left", "n"): "ATT",
            # 副词在动词左边 → 状语
            ("d", "left", "v"): "ADV",
            # 副词在形容词左边 → 状语
            ("d", "left", "a"): "ADV",
            # 介词后面的名词 → 介宾
            ("n", "right", "p"): "POB",
            # 助词附着在动词右边 → 右附加
            ("u", "right", "v"): "RAD",
        }

    def parse(self, words: list, pos_tags: list) -> DependencyTree:
        """
        对句子进行依存分析

        ━━━━━━━ 算法步骤 ━━━━━━━
        1. 找到核心词（通常是第一个动词，或句子中心词）
        2. 遍历其他词，根据规则判断依存关系
        3. 没有匹配规则的词，默认依存于核心词

        参数：
            words: 词列表，如 ["小明", "吃", "苹果"]
            pos_tags: 词性列表，如 ["nr", "v", "n"]

        返回：
            DependencyTree 对象
        """
        if not words:
            return DependencyTree(words)

        arcs = []

        # ---------------------------------------------------------------
        # 第一步：找到核心词（动词或第一个词）
        # ---------------------------------------------------------------
        # 核心词就像家族的族长，是整棵树的根
        root_idx = 0
        for i, pos in enumerate(pos_tags):
            if pos == "v":
                root_idx = i
                break

        # 核心词依存于 ROOT（head_index = -1）
        arcs.append(DependencyArc(root_idx, -1, "HED"))

        # ---------------------------------------------------------------
        # 第二步：分析其他词的依存关系
        # ---------------------------------------------------------------
        for i, (word, pos) in enumerate(zip(words, pos_tags)):
            if i == root_idx:
                continue  # 跳过核心词

            # 判断这个词在核心词的左边还是右边
            direction = "left" if i < root_idx else "right"

            # 获取核心词的词性
            root_pos = pos_tags[root_idx]

            # 尝试匹配规则
            rel = self.rules.get((pos, direction, root_pos))

            if rel:
                # 找到匹配的规则
                arcs.append(DependencyArc(i, root_idx, rel))
            else:
                # 没有匹配的规则，尝试找最近的合适核心词
                best_head = self._find_best_head(i, pos, words, pos_tags, root_idx)
                rel = self._infer_relation(i, pos, best_head, pos_tags[best_head])
                arcs.append(DependencyArc(i, best_head, rel))

        return DependencyTree(words, arcs, pos_tags)

    def _find_best_head(self, dep_idx: int, dep_pos: str,
                        words: list, pos_tags: list, root_idx: int) -> int:
        """
        为依存词找最佳的核心词

        ━━━━━━━ 生活类比 ━━━━━━━
        就像找最近的亲戚：如果父亲不在，就找叔叔、伯伯。
        """
        # 优先依存于核心词
        # 如果是形容词，尝试依存于右边最近的名词
        if dep_pos == "a":
            for i in range(dep_idx + 1, len(words)):
                if pos_tags[i] in ("n", "nr", "ns", "nt"):
                    return i

        # 如果是副词，尝试依存于右边最近的动词或形容词
        if dep_pos == "d":
            for i in range(dep_idx + 1, len(words)):
                if pos_tags[i] in ("v", "a"):
                    return i

        # 默认依存于核心词
        return root_idx

    def _infer_relation(self, dep_idx: int, dep_pos: str,
                        head_idx: int, head_pos: str) -> str:
        """
        推断依存关系类型

        ━━━━━━━ 生活类比 ━━━━━━━
        就像判断两个人的关系：看他们的年龄、性别、辈分。
        """
        direction = "left" if dep_idx < head_idx else "right"

        # 查表
        rel = self.rules.get((dep_pos, direction, head_pos))
        if rel:
            return rel

        # 默认关系
        if dep_pos in ("n", "nr", "ns", "nt"):
            return "ATT"  # 名词修饰
        if dep_pos == "v":
            return "COO"  # 并列
        return "ADV"      # 默认为状语


# ==============================================================================
# 第三部分：依存分析的评估指标
# ==============================================================================
#
# 如何评价依存分析的好坏？有两个常用指标：
#
#   1. UAS（Unlabeled Attachment Score）：无标记依存正确率
#      - 只看"谁依存于谁"对不对，不管关系类型
#
#   2. LAS（Labeled Attachment Score）：有标记依存正确率
#      - 既看"谁依存于谁"，也看关系类型对不对
#
# 就像考试：
#   - UAS = 选择题只看答案对不对
#   - LAS = 选择题既看答案对不对，也看解题过程对不对
#
# ==============================================================================

def evaluate_dependency(gold_tree: DependencyTree,
                        pred_tree: DependencyTree) -> dict:
    """
    评估依存分析的结果

    ━━━━━━━ 生活类比 ━━━━━━━
    就像对照标准答案批改试卷：
    - gold_tree: 标准答案
    - pred_tree: 学生的答案

    参数：
        gold_tree: 标准依存树
        pred_tree: 预测依存树

    返回：
        {"UAS": 正确率, "LAS": 正确率, "total": 总词数}
    """
    total = len(gold_tree.words)
    if total == 0:
        return {"UAS": 0.0, "LAS": 0.0, "total": 0}

    uas_correct = 0  # 无标记正确数
    las_correct = 0  # 有标记正确数

    # 建立标准答案的索引：{依存词索引: (核心词索引, 关系)}
    gold_map = {}
    for arc in gold_tree.arcs:
        gold_map[arc.dependent_index] = (arc.head_index, arc.relation)

    # 建立预测结果的索引
    pred_map = {}
    for arc in pred_tree.arcs:
        pred_map[arc.dependent_index] = (arc.head_index, arc.relation)

    # 逐词比较
    for i in range(total):
        gold_head, gold_rel = gold_map.get(i, (-1, "HED"))
        pred_head, pred_rel = pred_map.get(i, (-1, "HED"))

        # UAS：只看核心词是否正确
        if gold_head == pred_head:
            uas_correct += 1
            # LAS：核心词和关系都正确
            if gold_rel == pred_rel:
                las_correct += 1

    return {
        "UAS": uas_correct / total,
        "LAS": las_correct / total,
        "total": total,
    }


# ==============================================================================
# 第四部分：演示函数
# ==============================================================================

def demo_dependency_concept():
    """演示依存句法分析的基本概念"""

    print("=" * 60)
    print("依存句法分析基本概念")
    print("=" * 60)

    print("""
    依存句法分析的核心思想：
    ┌──────────────────────────────────────────────┐
    │  句子中每个词都"依存于"另一个词                │
    │  被依存的词叫"核心词"（Head）                  │
    │  依存别人的词叫"依存词"（Dependent）            │
    │  它们之间的关系叫"依存关系"（Relation）          │
    └──────────────────────────────────────────────┘

    例句："小明吃苹果"

              吃 (核心)
             /  \\
           /      \\
         小明      苹果
        (SBV)     (VOB)
        主语       宾语

    依存弧表示：
      Arc(0 <--SBV-- 1)  "小明" 依存于 "吃"，关系是主语
      Arc(2 <--VOB-- 1)  "苹果" 依存于 "吃"，关系是宾语
      Arc(1 <--HED-- ROOT) "吃" 是核心词
    """)


def demo_rule_based_parsing():
    """演示基于规则的依存分析"""

    print("=" * 60)
    print("基于规则的依存分析")
    print("=" * 60)

    parser = RuleBasedDependencyParser()

    test_cases = [
        (["小明", "吃", "苹果"], ["nr", "v", "n"]),
        (["我", "喜欢", "学习", "自然语言处理"], ["r", "v", "v", "n"]),
        (["今天", "天气", "很", "好"], ["t", "n", "d", "a"]),
        (["红色", "的", "苹果", "很", "好吃"], ["a", "u", "n", "d", "a"]),
    ]

    for words, pos_tags in test_cases:
        sentence = "".join(words)
        print(f"\n句子: {sentence}")
        print(f"词:   {words}")
        print(f"词性: {pos_tags}")

        tree = parser.parse(words, pos_tags)
        tree.display()
        print()


def demo_tree_operations():
    """演示依存树的基本操作"""

    print("=" * 60)
    print("依存树的基本操作")
    print("=" * 60)

    # 手动构建一棵依存树
    words = ["我", "喜欢", "吃", "苹果"]
    pos_tags = ["r", "v", "v", "n"]

    arcs = [
        DependencyArc(0, 1, "SBV"),   # 我 ← 喜欢 (主语)
        DependencyArc(1, -1, "HED"),   # 喜欢 ← ROOT (核心)
        DependencyArc(2, 1, "COO"),    # 吃 ← 喜欢 (并列)
        DependencyArc(3, 2, "VOB"),    # 苹果 ← 吃 (宾语)
    ]

    tree = DependencyTree(words, arcs, pos_tags)

    print(f"\n句子: {''.join(words)}")
    tree.display()

    # 查询操作
    print(f"\n查询操作：")
    print(f"  核心词索引: {tree.get_root()} → {words[tree.get_root()]}")
    print(f"  \"喜欢\"的孩子: {tree.get_children(1)}")
    print(f"  \"苹果\"的父亲: {tree.get_head(3)}")


def demo_evaluation():
    """演示依存分析的评估"""

    print("=" * 60)
    print("依存分析的评估指标")
    print("=" * 60)

    print("""
    UAS (Unlabeled Attachment Score):
      = 核心词判断正确的词数 / 总词数
      只看"谁依存于谁"对不对

    LAS (Labeled Attachment Score):
      = 核心词和关系都正确的词数 / 总词数
      既看"谁依存于谁"，也看关系类型

    例：
      标准答案：小明(SBV←吃)  吃(HED←ROOT)  苹果(VOB←吃)
      学生答案：小明(SBV←吃)  吃(HED←ROOT)  苹果(ADV←吃)

      UAS = 3/3 = 100%  (核心词都判断对了)
      LAS = 2/3 = 66.7% (苹果的关系标错了)
    """)

    # 演示评估
    words = ["小明", "吃", "苹果"]
    gold_tree = DependencyTree(words, [
        DependencyArc(0, 1, "SBV"),
        DependencyArc(1, -1, "HED"),
        DependencyArc(2, 1, "VOB"),
    ])

    # 模拟一个有错误的预测
    pred_tree = DependencyTree(words, [
        DependencyArc(0, 1, "SBV"),
        DependencyArc(1, -1, "HED"),
        DependencyArc(2, 1, "ADV"),  # 错误：应该是 VOB
    ])

    result = evaluate_dependency(gold_tree, pred_tree)
    print(f"  标准答案: 小明(SBV←吃) 吃(HED←ROOT) 苹果(VOB←吃)")
    print(f"  预测结果: 小明(SBV←吃) 吃(HED←ROOT) 苹果(ADV←吃)")
    print(f"  UAS = {result['UAS']:.1%}")
    print(f"  LAS = {result['LAS']:.1%}")


# ==============================================================================
# 第五部分：基于转移的依存句法分析器（Arc-Eager）
# ==============================================================================
#
# 基于规则的分析器虽然简单，但规则需要人工编写，而且很难覆盖所有情况。
# 现在我们学习一种更系统的方法：基于转移的分析（Transition-based Parsing）。
#
# ━━━━━━━ 生活类比 ━━━━━━━
# 想象你在整理书架：
#
#   你有两个区域：
#   - 手里（Stack）：正在处理的书
#   - 地上（Buffer）：还没处理的书
#
#   你的动作：
#   - SHIFT：从地上拿起一本书放到手里
#   - LEFT-ARC：手里的书A依存于地上的第一本书，把A放回去
#   - RIGHT-ARC：地上的第一本书依存于手里的书，把它放到手里
#   - REDUCE：手里的书已经处理完毕，放回书架
#
#   通过不断执行这些动作，最终所有的书都被整理好（建立依存关系）。
#
# ━━━━━━━ Arc-Eager 系统 ━━━━━━━
#
# Arc-Eager 是最常用的转移系统之一，有4种操作：
#
#   1. SHIFT: 从 buffer 取第一个词压入 stack
#      前提：buffer 不为空
#
#   2. LEFT-ARC: 添加弧 buffer[0] → stack[-1]，弹出 stack 顶部
#      前提：stack 不为空，stack[-1] 不是 ROOT
#
#   3. RIGHT-ARC: 添加弧 stack[-1] → buffer[0]，将 buffer[0] 压入 stack
#      前提：stack 不为空
#
#   4. REDUCE: 弹出 stack 顶部（该词的所有依存弧已建立）
#      前提：stack 不为空，stack[-1] 已经有父亲
#
# ==============================================================================

class TransitionState:
    """
    转移解析器的状态

    ━━━━━━━ 生活类比 ━━━━━━━
    想象你在做拼图：
    - stack: 你手里拿着的拼图块
    - buffer: 还没拿起来的拼图块
    - arcs: 已经拼好的连接

    属性：
        stack: 已处理词的索引栈
        buffer: 未处理词的索引缓冲区
        arcs: 已建立的依存弧列表
    """

    def __init__(self, words: list, pos_tags: list = None):
        """
        初始化解析状态

        初始状态：
        - stack 为空（手里没拿书）
        - buffer 包含所有词（地上全是书）
        - arcs 为空（还没建立任何关系）

        参数：
            words: 词列表
            pos_tags: 词性列表（可选）
        """
        self.stack = []                    # 手里拿着的词索引
        self.buffer = list(range(len(words)))  # 地上还没处理的词索引
        self.arcs = []                     # 已建立的依存弧
        self.words = words                 # 词列表
        self.pos_tags = pos_tags           # 词性列表
        self.is_final = False              # 是否解析完成

    def is_terminal(self) -> bool:
        """
        判断是否到达终止状态

        终止条件：buffer 为空 且 stack 最多只剩一个元素（ROOT的孩子）
        就像拼图：地上没拼图了，手里也只剩一块。
        """
        return len(self.buffer) == 0 and len(self.stack) <= 1

    def has_arc(self, dep_idx: int) -> bool:
        """
        检查某个词是否已经有父亲（已建立依存弧）

        参数：
            dep_idx: 词的索引

        返回：
            True 如果该词已经有父亲
        """
        for arc in self.arcs:
            if arc.dependent_index == dep_idx:
                return True
        return False

    def copy(self):
        """复制当前状态（用于尝试不同操作）"""
        new_state = TransitionState(self.words, self.pos_tags)
        new_state.stack = self.stack[:]
        new_state.buffer = self.buffer[:]
        new_state.arcs = self.arcs[:]
        return new_state


class TransitionParser:
    """
    基于转移的依存句法分析器（Arc-Eager 系统）

    ━━━━━━━ 核心思想 ━━━━━━━
    将依存分析建模为一系列"动作"的决策过程：
    1. 观察当前状态（stack、buffer、已有的弧）
    2. 提取特征
    3. 用特征的加权和给每个候选动作打分
    4. 选择得分最高的动作执行
    5. 重复直到所有词都被处理

    ━━━━━━━ 训练方式 ━━━━━━━
    使用感知机训练：
    - 看一个训练样本（正确的依存树）
    - 模拟正确的动作序列（Oracle）
    - 如果模型预测的动作和正确动作不同 → 更新权重

    ━━━━━━━ 生活类比 ━━━━━━━
    就像学骑自行车：
    - 初始：歪歪扭扭（权重随机）
    - 摔了（预测错误）→ 调整方向（更新权重）
    - 反复练习（迭代训练）→ 最终学会（权重收敛）
    """

    # ── 定义四种转移操作 ──
    SHIFT = "SHIFT"
    LEFT_ARC = "LEFT-ARC"
    RIGHT_ARC = "RIGHT-ARC"
    REDUCE = "REDUCE"

    def __init__(self):
        """
        初始化转移解析器

        创建特征权重字典，等待训练。
        """
        # ── 特征权重 ──
        # key=(特征名, 特征值, 动作), value=权重
        self.weights = {}

        # ── 所有可能的动作 ──
        self.actions = [self.SHIFT, self.LEFT_ARC, self.RIGHT_ARC, self.REDUCE]

        # ── 训练状态 ──
        self.trained = False

    def _extract_features(self, state: TransitionState) -> list:
        """
        从当前状态中提取特征

        ━━━━━━━ 生活类比 ━━━━━━━
        就像医生看病时观察的症状：
        - 栈顶的词（你手里拿着什么书？）
        - buffer第一个词（地上最前面是什么书？）
        - 它们的组合（这两本书有什么关系？）

        提取的特征：
        1. 栈顶词和词性 — 手里拿着什么？
        2. buffer第一个词和词性 — 地上最前面是什么？
        3. 词的组合特征 — 两个词的交互信息
        4. 栈的大小特征 — 手里拿了多少本书？

        参数：
            state: 当前解析状态

        返回：
            特征列表 [(特征名, 特征值), ...]
        """
        features = []

        # ── 栈顶特征 ──
        # 手里最上面的书是什么？
        if state.stack:
            top_idx = state.stack[-1]
            top_word = state.words[top_idx]
            features.append(("stack_top_word", top_word))
            # 如果有词性信息，也加入特征
            if state.pos_tags:
                features.append(("stack_top_pos", state.pos_tags[top_idx]))
                # 栈顶词 + 词性组合
                features.append(("stack_top_word_pos",
                                f"{top_word}_{state.pos_tags[top_idx]}"))
        else:
            features.append(("stack_top_word", "<EMPTY>"))
            features.append(("stack_top_pos", "<EMPTY>"))

        # ── Buffer 第一个词特征 ──
        # 地上最前面的书是什么？
        if state.buffer:
            first_idx = state.buffer[0]
            first_word = state.words[first_idx]
            features.append(("buffer_first_word", first_word))
            if state.pos_tags:
                features.append(("buffer_first_pos", state.pos_tags[first_idx]))
                features.append(("buffer_first_word_pos",
                                f"{first_word}_{state.pos_tags[first_idx]}"))
        else:
            features.append(("buffer_first_word", "<EMPTY>"))
            features.append(("buffer_first_pos", "<EMPTY>"))

        # ── 组合特征 ──
        # 栈顶和buffer第一个词的组合，捕捉两者之间的交互
        if state.stack and state.buffer:
            top_idx = state.stack[-1]
            first_idx = state.buffer[0]
            top_word = state.words[top_idx]
            first_word = state.words[first_idx]
            features.append(("combo_top_buffer", f"{top_word}_{first_word}"))
            if state.pos_tags:
                features.append(("combo_pos",
                                f"{state.pos_tags[top_idx]}_{state.pos_tags[first_idx]}"))

        # ── 栈大小特征 ──
        # 手里拿了多少书？这影响决策策略
        if len(state.stack) == 0:
            features.append(("stack_size", "empty"))
        elif len(state.stack) == 1:
            features.append(("stack_size", "one"))
        else:
            features.append(("stack_size", "many"))

        return features

    def _score_action(self, features: list, action: str) -> float:
        """
        计算某个动作的得分

        ━━━━━━━ 公式 ━━━━━━━
        score(action) = sum(权重[(特征名, 特征值, action)] for 每个特征)

        就像投票决定下一步怎么走：
        - 每个特征投一票
        - 每票的权重不同（有些特征更重要）
        - 总分最高的动作获胜

        参数：
            features: 特征列表
            action: 候选动作

        返回：
            得分（浮点数）
        """
        score = 0.0
        for feat_name, feat_value in features:
            key = (feat_name, feat_value, action)
            score += self.weights.get(key, 0.0)
        return score

    def _get_valid_actions(self, state: TransitionState) -> list:
        """
        获取当前状态下合法的动作列表

        ━━━━━━━ 合法性规则 ━━━━━━━
        不是所有动作在任何时候都能执行：
        - SHIFT:   buffer 不能为空（地上还有书）
        - LEFT-ARC: stack 不能为空，且栈顶不是ROOT的孩子
        - RIGHT-ARC: stack 不能为空
        - REDUCE:  stack 不能为空，且栈顶已经有父亲

        参数：
            state: 当前状态

        返回：
            合法动作列表
        """
        valid = []

        # SHIFT: buffer 不为空
        if state.buffer:
            valid.append(self.SHIFT)

        # LEFT-ARC: stack 不为空，栈顶没有父亲（不是ROOT直接孩子）
        if state.stack and not state.has_arc(state.stack[-1]):
            valid.append(self.LEFT_ARC)

        # RIGHT-ARC: stack 不为空
        if state.stack:
            valid.append(self.RIGHT_ARC)

        # REDUCE: stack 不为空，栈顶已经有父亲
        if state.stack and state.has_arc(state.stack[-1]):
            valid.append(self.REDUCE)

        return valid if valid else [self.SHIFT]

    def _do_action(self, state: TransitionState, action: str,
                   gold_arcs: list = None) -> TransitionState:
        """
        执行一个转移操作

        ━━━━━━━ 四种操作详解 ━━━━━━━

        SHIFT（拿起来）：
        从 buffer 取第一个词压入 stack。
        就像从地上拿起一本书放到手里。

        LEFT-ARC（左弧）：
        buffer[0] → stack[-1]，然后弹出 stack[-1]。
        就像说"地上的书是手里这本书的父亲"，然后把手里的放回去。

        RIGHT-ARC（右弧）：
        stack[-1] → buffer[0]，然后把 buffer[0] 压入 stack。
        就像说"手里的书是地上这本书的父亲"，然后把地上的也拿到手里。

        REDUCE（放下）：
        弹出 stack[-1]。
        就像说"手里这本书已经处理完毕了"，放回书架。

        参数：
            state: 当前状态
            action: 要执行的动作
            gold_arcs: 标准答案的弧（用于训练时确定正确的关系类型）

        返回：
            执行动作后的新状态
        """
        new_state = state.copy()

        if action == self.SHIFT:
            # ── SHIFT: buffer → stack ──
            new_state.stack.append(new_state.buffer.pop(0))

        elif action == self.LEFT_ARC:
            # ── LEFT-ARC: buffer[0] 是 stack[-1] 的父亲 ──
            dep_idx = new_state.stack.pop()  # 弹出栈顶（孩子）
            head_idx = new_state.buffer[0]    # buffer第一个（父亲）
            # 确定关系类型
            relation = "DEP"  # 默认关系
            if gold_arcs:
                for arc in gold_arcs:
                    if arc.dependent_index == dep_idx and arc.head_index == head_idx:
                        relation = arc.relation
                        break
            new_state.arcs.append(DependencyArc(dep_idx, head_idx, relation))

        elif action == self.RIGHT_ARC:
            # ── RIGHT-ARC: stack[-1] 是 buffer[0] 的父亲 ──
            head_idx = new_state.stack[-1]    # 栈顶（父亲）
            dep_idx = new_state.buffer.pop(0)  # buffer第一个（孩子）
            # 确定关系类型
            relation = "DEP"
            if gold_arcs:
                for arc in gold_arcs:
                    if arc.dependent_index == dep_idx and arc.head_index == head_idx:
                        relation = arc.relation
                        break
            new_state.arcs.append(DependencyArc(dep_idx, head_idx, relation))
            new_state.stack.append(dep_idx)  # 孩子也压入栈

        elif action == self.REDUCE:
            # ── REDUCE: 弹出栈顶 ──
            new_state.stack.pop()

        return new_state

    def _get_oracle_action(self, state: TransitionState,
                           gold_heads: dict) -> str:
        """
        Oracle：给定标准答案，计算当前状态下的正确动作

        ━━━━━━━ 生活类比 ━━━━━━━
        Oracle 就像一个"上帝视角"的教练：
        - 知道标准答案（正确的依存树）
        - 告诉你现在应该做什么动作

        Arc-Eager 的 Oracle 规则：
        1. 如果栈顶词的父亲在 buffer 中，且在 buffer[0] 之前 → LEFT-ARC
        2. 如果栈顶词是 buffer[0] 的父亲 → RIGHT-ARC
        3. 如果栈顶词已经有父亲 → REDUCE
        4. 否则 → SHIFT

        参数：
            state: 当前状态
            gold_heads: {孩子索引: 父亲索引} 的字典

        返回：
            正确的动作
        """
        if not state.stack:
            return self.SHIFT

        top = state.stack[-1]  # 栈顶词索引

        # 检查栈顶词的父亲是否在 buffer 中
        top_head = gold_heads.get(top, -1)

        # 如果栈顶没有父亲，且buffer不为空，检查是否应该LEFT-ARC
        if not state.has_arc(top):
            # 如果栈顶词的父亲是 buffer[0]
            if state.buffer and top_head == state.buffer[0]:
                return self.LEFT_ARC

        # 如果栈顶词是 buffer[0] 的父亲
        if state.buffer:
            buf_head = gold_heads.get(state.buffer[0], -1)
            if buf_head == top:
                return self.RIGHT_ARC

        # 如果栈顶词已经有父亲
        if state.has_arc(top):
            # 检查栈顶词的所有依赖是否已经在 buffer 之外
            # （简化版：直接 REDUCE）
            return self.REDUCE

        # 默认 SHIFT
        return self.SHIFT

    def train(self, gold_sentences: list, num_iterations: int = 5):
        """
        使用感知机训练转移解析器

        ━━━━━━━ 训练过程 ━━━━━━━
        就像学下棋：
        1. 看一盘棋（一个标注句子）
        2. 教练（Oracle）告诉你每步该怎么走
        3. 你（模型）用自己的判断走
        4. 如果走错了 → 调整判断标准（更新权重）
        5. 反复练习多轮

        参数：
            gold_sentences: 标注句子列表
                每个元素是 (words, pos_tags, arcs) 元组
                arcs: [DependencyArc, ...] 标准答案
            num_iterations: 训练轮数
        """
        for iteration in range(num_iterations):
            errors = 0
            total = 0

            for words, pos_tags, gold_arcs in gold_sentences:
                # 构建标准答案的映射
                gold_heads = {}
                for arc in gold_arcs:
                    gold_heads[arc.dependent_index] = arc.head_index

                # 初始化状态
                state = TransitionState(words, pos_tags)

                # 模拟解析过程
                max_steps = len(words) * 4  # 防止无限循环
                step = 0

                while not state.is_terminal() and step < max_steps:
                    step += 1

                    # 提取特征
                    features = self._extract_features(state)

                    # 获取合法动作
                    valid_actions = self._get_valid_actions(state)

                    # Oracle 告诉我们正确动作
                    gold_action = self._get_oracle_action(state, gold_heads)

                    # 模型选择得分最高的动作
                    best_action = None
                    best_score = float('-inf')
                    for action in valid_actions:
                        score = self._score_action(features, action)
                        if score > best_score:
                            best_score = score
                            best_action = action

                    # 如果预测错误，更新权重
                    total += 1
                    if best_action != gold_action:
                        errors += 1
                        # 增加正确动作的特征权重
                        for feat_name, feat_value in features:
                            key = (feat_name, feat_value, gold_action)
                            self.weights[key] = self.weights.get(key, 0.0) + 1.0
                        # 减少错误动作的特征权重
                        for feat_name, feat_value in features:
                            key = (feat_name, feat_value, best_action)
                            self.weights[key] = self.weights.get(key, 0.0) - 1.0

                    # 执行 Oracle 建议的动作（用标准答案的弧）
                    state = self._do_action(state, gold_action, gold_arcs)

            error_rate = errors / total if total > 0 else 0
            print(f"  [训练] 第{iteration + 1}轮: 错误率={error_rate:.2%} ({errors}/{total})")

        self.trained = True
        print(f"  [训练完成] 学习了 {len(self.weights)} 个特征权重")

    def parse(self, words: list, pos_tags: list = None) -> DependencyTree:
        """
        对句子进行依存分析

        ━━━━━━━ 解析过程 ━━━━━━━
        1. 初始化：stack 为空，buffer 包含所有词
        2. 循环：
           a. 提取当前状态的特征
           b. 对每个合法动作计算得分
           c. 执行得分最高的动作
        3. 终止：buffer 为空 且 stack 最多剩1个元素
        4. 返回建立的依存弧

        ━━━━━━━ 生活类比 ━━━━━━━
        就像在流水线上组装产品：
        - 初始：零件全在传送带上（buffer）
        - 每一步：拿起一个零件（SHIFT）、连接两个零件（ARC）、放下完成件（REDUCE）
        - 最终：所有零件都组装完毕

        参数：
            words: 词列表
            pos_tags: 词性列表（可选）

        返回：
            DependencyTree 对象
        """
        state = TransitionState(words, pos_tags)

        max_steps = len(words) * 4
        step = 0

        while not state.is_terminal() and step < max_steps:
            step += 1

            # 提取特征
            features = self._extract_features(state)

            # 获取合法动作
            valid_actions = self._get_valid_actions(state)

            # 选择得分最高的动作
            best_action = None
            best_score = float('-inf')
            for action in valid_actions:
                score = self._score_action(features, action)
                if score > best_score:
                    best_score = score
                    best_action = action

            # 执行动作（没有标准答案，关系类型用默认值）
            state = self._do_action(state, best_action)

        return DependencyTree(words, state.arcs, pos_tags)

    def parse_with_demo(self, words: list, pos_tags: list = None) -> DependencyTree:
        """
        带详细过程展示的依存分析

        和 parse() 功能相同，但会打印每一步的操作过程。
        适合教学演示。
        """
        print(f"\n  解析句子: {''.join(words)}")
        print(f"  词: {words}")
        print(f"  词性: {pos_tags}")
        print(f"  {'─' * 50}")

        state = TransitionState(words, pos_tags)

        max_steps = len(words) * 4
        step = 0

        while not state.is_terminal() and step < max_steps:
            step += 1

            features = self._extract_features(state)
            valid_actions = self._get_valid_actions(state)

            best_action = None
            best_score = float('-inf')
            action_scores = {}
            for action in valid_actions:
                score = self._score_action(features, action)
                action_scores[action] = score
                if score > best_score:
                    best_score = score
                    best_action = action

            # 打印当前状态
            stack_words = [state.words[i] for i in state.stack]
            buffer_words = [state.words[i] for i in state.buffer]
            print(f"  步骤{step}: stack={stack_words} buffer={buffer_words}")
            print(f"          动作得分: {action_scores}")
            print(f"          选择: {best_action}")

            state = self._do_action(state, best_action)

        print(f"  {'─' * 50}")
        print(f"  解析完成，共建立 {len(state.arcs)} 条依存弧")

        return DependencyTree(words, state.arcs, pos_tags)


# ==============================================================================
# 主程序入口
# ==============================================================================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║        G-one NLP 学院 - 第五章                        ║
    ║        依存句法分析                                   ║
    ╚══════════════════════════════════════════════════════╝
    """)

    demo_dependency_concept()
    demo_rule_based_parsing()
    demo_tree_operations()
    demo_evaluation()

    print("\n" + "=" * 60)
    print("第五章 总结")
    print("=" * 60)
    print("""
    [OK] 什么是依存句法分析 — 分析词与词之间的支配关系
    [OK] 依存关系的要素 — 核心词、依存词、关系类型
    [OK] 常见关系类型 — SBV(主语)、VOB(宾语)、ATT(定语)等
    [OK] 基于规则的分析器 — 用词性规则判断依存关系
    [OK] 评估指标 — UAS(无标记)和 LAS(有标记)
    """)
