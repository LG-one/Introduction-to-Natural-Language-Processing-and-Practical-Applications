"""
==============================================================================
第三章：词性标注（Part-of-Speech Tagging）
==============================================================================
日期：2026-05-16

同学们好！上一章我们学会了把句子切成词，这节课我们来给每个词"贴标签"。

----------------------------------------------------------------------
生活类比：词性标注就像给商品贴标签
----------------------------------------------------------------------

想象你是一家超市的理货员，货架上有一堆商品需要分类：

  ┌──────────────────────────────────────────────┐
  │  苹果 → 水果区                                │
  │  牛奶 → 饮料区                                │
  │  洗衣液 → 日用品区                             │
  │  薯片 → 零食区                                │
  └──────────────────────────────────────────────┘

词性标注也是同样的道理：给每个词贴上它的"词性标签"：

  ┌──────────────────────────────────────────────┐
  │  小明  →  人名（nr）                          │
  │  喜欢  →  动词（v）                           │
  │  吃    →  动词（v）                           │
  │  苹果  →  名词（n）                           │
  └──────────────────────────────────────────────┘

----------------------------------------------------------------------
什么是词性？
----------------------------------------------------------------------

词性就是一个词在句子中扮演的角色。常见的中文词性有：

  ┌──────────────────────────────────────────────┐
  │  标签  │  含义       │  例子                   │
  ├────────┼────────────┼───────────────────────┤
  │  n     │  名词       │  人民、教育、水平        │
  │  v     │  动词       │  学习、喜欢、研究        │
  │  a     │  形容词     │  美丽、高兴、优秀        │
  │  d     │  副词       │  很、非常、已经          │
  │  r     │  代词       │  我、你、他             │
  │  p     │  介词       │  在、从、对于            │
  │  c     │  连词       │  和、但是、因为          │
  │  u     │  助词       │  的、了、着             │
  │  m     │  数词       │  一、二、百             │
  │  q     │  量词       │  个、只、条             │
  │  t     │  时间词     │  今天、去年、上午        │
  │  s     │  处所词     │  门口、桌上、北京        │
  │  nr    │  人名       │  张三、李四、小明        │
  │  ns    │  地名       │  北京、上海、中国        │
  │  nt    │  机构名     │  清华大学、阿里巴巴      │
  └────────┴────────────┴───────────────────────┘

==============================================================================
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')


# ==============================================================================
# 第一部分：基于规则的词性标注
# ==============================================================================
#
# 最简单的词性标注方法：查词典。
# 维护一个"词 → 词性"的词典，遇到词直接查表。
#
# 就像查字典：不认识的字，查一下就知道怎么读了。
#
# ==============================================================================

# 简化的词性词典
# 在实际项目中，这个词典可能有几十万个词条
POS_DICTIONARY = {
    # 代词
    "我": "r", "你": "r", "他": "r", "她": "r", "它": "r",
    "我们": "r", "你们": "r", "他们": "r",
    "这": "r", "那": "r", "什么": "r", "谁": "r",

    # 动词
    "喜欢": "v", "吃": "v", "喝": "v", "看": "v", "听": "v",
    "学习": "v", "研究": "v", "工作": "v", "去": "v", "来": "v",
    "是": "v", "有": "v", "在": "v", "做": "v", "写": "v",
    "读": "v", "说": "v", "想": "v", "知道": "v", "认识": "v",
    "跑": "v", "走": "v", "飞": "v", "打": "v", "买": "v",

    # 名词
    "苹果": "n", "香蕉": "n", "牛奶": "n", "面包": "n",
    "书": "n", "笔": "n", "电脑": "n", "手机": "n",
    "学校": "n", "公司": "n", "家": "n", "公园": "n",
    "人": "n", "学生": "n", "老师": "n", "医生": "n",
    "天气": "n", "时间": "n", "地方": "n", "问题": "n",
    "自然语言处理": "n", "机器学习": "n", "深度学习": "n",

    # 形容词
    "好": "a", "坏": "a", "大": "a", "小": "a",
    "美丽": "a", "漂亮": "a", "聪明": "a", "可爱": "a",
    "高兴": "a", "难过": "a", "开心": "a", "生气": "a",
    "优秀": "a", "厉害": "a", "简单": "a", "困难": "a",
    "红": "a", "蓝": "a", "绿": "a", "白": "a", "黑": "a",

    # 副词
    "很": "d", "非常": "d", "特别": "d", "太": "d",
    "已经": "d", "都": "d", "也": "d", "就": "d",
    "不": "d", "没": "d", "没有": "d",

    # 介词
    "在": "p", "从": "p", "到": "p", "对": "p",
    "用": "p", "把": "p", "被": "p", "给": "p",

    # 连词
    "和": "c", "但是": "c", "因为": "c", "所以": "c",
    "如果": "c", "虽然": "c", "而且": "c", "或者": "c",

    # 助词
    "的": "u", "了": "u", "着": "u", "过": "u",
    "得": "u", "地": "u",

    # 数词
    "一": "m", "二": "m", "三": "m", "四": "m", "五": "m",
    "六": "m", "七": "m", "八": "m", "九": "m", "十": "m",
    "百": "m", "千": "m", "万": "m",

    # 量词
    "个": "q", "只": "q", "条": "q", "本": "q",
    "张": "q", "块": "q", "杯": "q", "瓶": "q",

    # 时间词
    "今天": "t", "明天": "t", "昨天": "t",
    "上午": "t", "下午": "t", "晚上": "t",
    "去年": "t", "今年": "t", "明年": "t",

    # 人名
    "小明": "nr", "小红": "nr", "张三": "nr", "李四": "nr",

    # 地名
    "北京": "ns", "上海": "ns", "广州": "ns", "深圳": "ns",
    "中国": "ns", "美国": "ns", "日本": "ns",

    # 机构名
    "清华大学": "nt", "北京大学": "nt", "阿里巴巴": "nt", "腾讯": "nt",
}


def rule_based_pos_tag(words: list) -> list:
    """
    基于词典的词性标注

    ━━━━━━━ 生活类比 ━━━━━━━
    就像查字典：遇到不认识的字，翻字典就知道怎么读了。
    如果字典里没有，就猜一个（默认标为名词）。

    ━━━━━━━ 算法步骤 ━━━━━━━
    1. 遍历每个词
    2. 在词典中查找它的词性
    3. 如果找到了，返回词性
    4. 如果没找到，默认标记为名词（n）

    参数：
        words: 词列表，如 ["我", "喜欢", "吃", "苹果"]

    返回：
        词性标注结果列表，如 [("我", "r"), ("喜欢", "v"), ("吃", "v"), ("苹果", "n")]
    """
    result = []
    for word in words:
        # 在词典中查找
        pos = POS_DICTIONARY.get(word, "n")  # 默认为名词
        result.append((word, pos))
    return result


# ==============================================================================
# 第二部分：基于 HMM 的词性标注
# ==============================================================================
#
# HMM 词性标注的核心思想：
#   - 每个词的词性不仅取决于这个词本身，还取决于前一个词的词性
#   - 例如："我"后面很可能是动词（我吃、我看、我学）
#   - "很"后面很可能是形容词（很好、很大、很美）
#
# 就像读小说：前面的情节会影响你对后面情节的猜测。
#
# ==============================================================================

class HMMPOSTagger:
    """
    基于 HMM 的词性标注器

    ━━━━━━━ 核心概念 ━━━━━━━
    在 HMM 中：
    - 观测值 = 我们看到的词（如"喜欢"）
    - 隐藏状态 = 词性（如"v"）
    - 我们要做的：根据观测到的词，推断最可能的词性序列

    ━━━━━━━ 三个概率 ━━━━━━━
    1. 初始概率：句子开头的词性概率
       比如：句子开头很可能是代词（我、你）或名词

    2. 转移概率：从一个词性转移到另一个词性的概率
       比如：代词后面很可能是动词（我 → 吃）

    3. 发射概率：某个词性下出现某个词的概率
       比如：动词词性下出现"吃"的概率很高
    """

    def __init__(self):
        """初始化 HMM 词性标注器"""
        # 词性标签集合
        self.pos_tags = ["n", "v", "a", "d", "r", "p", "c", "u", "m", "q",
                         "t", "s", "nr", "ns", "nt"]

        # 初始概率（简化版）
        self.start_prob = {tag: 1.0 / len(self.pos_tags) for tag in self.pos_tags}
        # 句子开头更可能是代词或名词
        self.start_prob["r"] = 0.3
        self.start_prob["n"] = 0.2
        self.start_prob["nr"] = 0.1

        # 转移概率（简化版）
        # key=前一个词性, value=当前词性的概率
        self.trans_prob = {
            "r": {"v": 0.6, "n": 0.1, "d": 0.1, "p": 0.1, "a": 0.1},
            "v": {"n": 0.3, "r": 0.2, "u": 0.15, "p": 0.1, "d": 0.1, "v": 0.15},
            "n": {"v": 0.3, "u": 0.2, "c": 0.1, "p": 0.1, "d": 0.1, "n": 0.2},
            "d": {"v": 0.4, "a": 0.4, "n": 0.1, "d": 0.1},
            "a": {"n": 0.3, "u": 0.2, "c": 0.15, "d": 0.15, "v": 0.2},
            "p": {"n": 0.4, "r": 0.3, "v": 0.1, "ns": 0.2},
            "c": {"n": 0.2, "v": 0.3, "r": 0.2, "d": 0.15, "a": 0.15},
            "u": {"n": 0.3, "v": 0.3, "a": 0.2, "r": 0.2},
            "m": {"q": 0.6, "n": 0.2, "v": 0.1, "m": 0.1},
            "q": {"n": 0.5, "v": 0.2, "u": 0.15, "c": 0.15},
            "t": {"v": 0.4, "n": 0.2, "d": 0.2, "p": 0.2},
            "nr": {"v": 0.5, "n": 0.2, "p": 0.1, "d": 0.1, "u": 0.1},
            "ns": {"v": 0.3, "n": 0.3, "p": 0.2, "u": 0.2},
            "nt": {"v": 0.4, "n": 0.3, "p": 0.15, "u": 0.15},
            "s": {"v": 0.3, "n": 0.3, "p": 0.2, "u": 0.2},
        }

        # 发射概率：词 → 词性的概率
        # 这里用词典作为简化版本
        self.emit_prob = POS_DICTIONARY

    def _get_trans_prob(self, prev_tag, curr_tag):
        """获取转移概率"""
        if prev_tag in self.trans_prob:
            return self.trans_prob[prev_tag].get(curr_tag, 0.01)
        return 0.01

    def _get_emit_prob(self, word, tag):
        """获取发射概率"""
        # 如果词典中有这个词，检查词性是否匹配
        if word in self.emit_prob:
            return 0.9 if self.emit_prob[word] == tag else 0.01
        # 未知词：根据词性猜测
        # 名词是最常见的词性，概率稍高
        if tag == "n":
            return 0.3
        return 0.1

    def viterbi(self, words: list) -> list:
        """
        维特比算法找最优词性序列

        参数：
            words: 词列表

        返回：
            词性列表
        """
        if not words:
            return []

        n = len(words)

        # dp[t][tag] = 到达第 t 个词、词性为 tag 的最大概率
        dp = [{} for _ in range(n)]
        # path[t][tag] = 到达第 t 个词、词性为 tag 的最优前驱路径
        path = [{} for _ in range(n)]

        # 初始化第一个词
        for tag in self.pos_tags:
            emit_p = self._get_emit_prob(words[0], tag)
            dp[0][tag] = self.start_prob.get(tag, 0.01) * emit_p
            path[0][tag] = [tag]

        # 递推
        for t in range(1, n):
            new_path = {}
            for tag in self.pos_tags:
                max_prob = 0
                best_prev = "n"
                for prev_tag in self.pos_tags:
                    prob = (dp[t - 1].get(prev_tag, 0) *
                            self._get_trans_prob(prev_tag, tag))
                    if prob > max_prob:
                        max_prob = prob
                        best_prev = prev_tag

                emit_p = self._get_emit_prob(words[t], tag)
                dp[t][tag] = max_prob * emit_p
                new_path[tag] = path[t - 1][best_prev] + [tag]

            path[t] = new_path

        # 找最优路径
        best_last = max(dp[n - 1], key=dp[n - 1].get)
        return path[n - 1][best_last]

    def tag(self, words: list) -> list:
        """
        对词列表进行词性标注

        参数：
            words: 词列表

        返回：
            [(词, 词性), ...] 列表
        """
        pos_tags = self.viterbi(words)
        return list(zip(words, pos_tags))


# ==============================================================================
# 第三部分：jieba 词性标注实战
# ==============================================================================

def demo_jieba_pos_tagging():
    """演示 jieba 的词性标注功能"""

    print("=" * 60)
    print("jieba 词性标注实战")
    print("=" * 60)

    try:
        import jieba.posseg as pseg
    except ImportError:
        print("\n[提示] jieba 未安装，请运行: pip install jieba")
        return

    test_sentences = [
        "小明在北京大学学习自然语言处理",
        "今天天气非常好",
        "我喜欢吃苹果",
        "清华大学是中国最好的大学之一",
    ]

    for sentence in test_sentences:
        print(f"\n句子: {sentence}")
        words_pos = pseg.cut(sentence)
        result = []
        for word, flag in words_pos:
            result.append(f"{word}/{flag}")
        print(f"  标注: {' '.join(result)}")


# ==============================================================================
# 演示函数
# ==============================================================================

def demo_rule_based():
    """演示基于规则的词性标注"""

    print("=" * 60)
    print("基于规则的词性标注")
    print("=" * 60)

    test_cases = [
        ["我", "喜欢", "吃", "苹果"],
        ["今天", "天气", "很", "好"],
        ["小明", "在", "北京大学", "学习"],
    ]

    for words in test_cases:
        result = rule_based_pos_tag(words)
        print(f"\n输入: {words}")
        tags_str = " ".join([f"{w}/{t}" for w, t in result])
        print(f"输出: {tags_str}")


def demo_hmm_tagger():
    """演示 HMM 词性标注"""

    print("\n" + "=" * 60)
    print("HMM 词性标注")
    print("=" * 60)

    tagger = HMMPOSTagger()

    test_cases = [
        ["我", "喜欢", "学习"],
        ["今天", "天气", "很好"],
        ["小明", "在", "清华大学", "学习"],
    ]

    for words in test_cases:
        result = tagger.tag(words)
        print(f"\n输入: {words}")
        tags_str = " ".join([f"{w}/{t}" for w, t in result])
        print(f"输出: {tags_str}")


# ==============================================================================
# 第四部分：可训练的 HMM 词性标注器
# ==============================================================================
#
# 前面的 HMM 标注器用的是手工编写的概率，就像"死记硬背"。
# 真正的 HMM 应该从标注数据中自动学习概率，就像"做题总结规律"。
#
# ━━━━━━━ 生活类比 ━━━━━━━
# 想象你在学英语语法：
# - 手工编写概率 = 老师直接告诉你"主语后面一般跟谓语"
# - 从数据学习 = 你读了100篇文章，自己总结出"主语后面一般跟谓语"
#
# 从数据中学习的好处：
# - 更准确：反映真实语言的统计规律
# - 更灵活：换个语料库就能适应不同领域
# - 更客观：不依赖人的主观判断
#
# ==============================================================================

class TrainedHMMPOSTagger:
    """
    可训练的 HMM 词性标注器

    ━━━━━━━ 核心思想 ━━━━━━━
    从标注好的语料中学习三个概率：
    1. 初始概率 P(tag|<START>) — 句子开头的词性分布
    2. 转移概率 P(tag_i|tag_{i-1}) — 前一个词性到当前词性的概率
    3. 发射概率 P(word|tag) — 某个词性下出现某个词的概率

    ━━━━━━━ 训练过程 ━━━━━━━
    就像做统计题：
    - 读100个标注好的句子
    - 统计"句子开头是名词"出现了多少次 → 初始概率
    - 统计"名词后面跟动词"出现了多少次 → 转移概率
    - 统计"名词词性下出现'苹果'"出现了多少次 → 发射概率

    ━━━━━━━ 拉普拉斯平滑 ━━━━━━━
    如果某个组合在训练数据中没出现过怎么办？
    比如训练数据中没有"代词→量词"的转移，概率就是0吗？
    不行！0概率会导致整个计算崩塌。

    解决方法：给每个计数加1（拉普拉斯平滑），就像"每种情况至少出现1次"。
    这样即使没见过的组合，也有一个很小的概率，而不是0。
    """

    def __init__(self):
        """
        初始化可训练的 HMM 标注器

        创建空的计数器，等待训练数据来填充。
        """
        # ── 所有出现过的词性标签集合 ──
        # 训练后会自动收集所有见过的词性
        self.pos_tags = set()

        # ── 词汇表 ──
        # 训练后会收集所有见过的词
        self.vocab = set()

        # ── 初始概率计数 ──
        # key=词性, value=该词性出现在句子开头的次数
        self.start_counts = {}

        # ── 转移概率计数 ──
        # key=(前一个词性, 当前词性), value=转移次数
        self.trans_counts = {}

        # ── 发射概率计数 ──
        # key=(词性, 词), value=该词性下出现该词的次数
        self.emit_counts = {}

        # ── 词性总计数 ──
        # key=词性, value=该词性出现的总次数（用于计算发射概率的分母）
        self.tag_counts = {}

        # ── 训练状态标记 ──
        self.trained = False

    def train(self, tagged_sentences: list):
        """
        从标注数据中学习 HMM 参数

        ━━━━━━━ 生活类比 ━━━━━━━
        就像一个勤奋的学生，做完100道标注题后，
        统计各种规律出现的频率：
        - "句子开头是代词"出现了30次
        - "代词后面跟动词"出现了25次
        - "动词词性下出现'吃'"出现了10次

        参数：
            tagged_sentences: 标注好的句子列表
                每个句子是 [(词, 词性), (词, 词性), ...] 的列表
                例如: [[("我", "r"), ("吃", "v"), ("苹果", "n")], ...]
        """
        for sentence in tagged_sentences:
            if not sentence:
                continue

            # ── 统计初始概率 ──
            # 句子第一个词的词性
            first_tag = sentence[0][1]
            self.start_counts[first_tag] = self.start_counts.get(first_tag, 0) + 1

            # ── 逐词统计 ──
            for i, (word, tag) in enumerate(sentence):
                # 收集词性和词汇
                self.pos_tags.add(tag)
                self.vocab.add(word)

                # 统计词性总出现次数
                self.tag_counts[tag] = self.tag_counts.get(tag, 0) + 1

                # 统计发射计数：词性tag下出现词word的次数
                self.emit_counts[(tag, word)] = self.emit_counts.get((tag, word), 0) + 1

                # 统计转移计数：从tag_{i-1}转移到tag_i的次数
                if i > 0:
                    prev_tag = sentence[i - 1][1]
                    key = (prev_tag, tag)
                    self.trans_counts[key] = self.trans_counts.get(key, 0) + 1

        self.trained = True
        num_tags = len(self.pos_tags)
        print(f"  [训练完成] 共学习 {len(tagged_sentences)} 个句子")
        print(f"  [训练完成] 词性种类: {num_tags}")
        print(f"  [训练完成] 词汇量: {len(self.vocab)}")

    def _get_start_prob(self, tag: str) -> float:
        """
        计算初始概率 P(tag|<START>)

        ━━━━━━━ 公式 ━━━━━━━
        P(tag|<START>) = (tag出现在句首的次数 + 1) / (总句数 + 词性种类数)

        加1就是拉普拉斯平滑，确保没见过的词性也有非零概率。
        """
        total_sentences = sum(self.start_counts.values())
        num_tags = len(self.pos_tags)
        # 拉普拉斯平滑：分子加1，分母加词性种类数
        count = self.start_counts.get(tag, 0)
        return (count + 1) / (total_sentences + num_tags)

    def _get_trans_prob(self, prev_tag: str, curr_tag: str) -> float:
        """
        计算转移概率 P(curr_tag|prev_tag)

        ━━━━━━━ 公式 ━━━━━━━
        P(curr|prev) = (prev→curr的转移次数 + 1) / (prev出现的总次数 + 词性种类数)

        分母加词性种类数是拉普拉斯平滑，保证所有可能的转移都有非零概率。
        """
        total_prev = self.tag_counts.get(prev_tag, 0)
        num_tags = len(self.pos_tags)
        count = self.trans_counts.get((prev_tag, curr_tag), 0)
        return (count + 1) / (total_prev + num_tags)

    def _get_emit_prob(self, word: str, tag: str) -> float:
        """
        计算发射概率 P(word|tag)

        ━━━━━━━ 公式 ━━━━━━━
        P(word|tag) = (tag下出现word的次数 + 1) / (tag的总次数 + 词汇表大小)

        对于训练时没见过的词（OOV词），词汇表大小会起到平滑作用，
        让所有词性都有一个很小但非零的发射概率。
        """
        total_tag = self.tag_counts.get(tag, 0)
        vocab_size = len(self.vocab) if self.vocab else 1
        count = self.emit_counts.get((tag, word), 0)
        return (count + 1) / (total_tag + vocab_size)

    def viterbi(self, words: list) -> list:
        """
        维特比算法：用学到的概率找最优词性序列

        ━━━━━━━ 算法核心 ━━━━━━━
        维特比算法是动态规划的一种：
        - dp[t][tag] = 前t个词，第t个词性为tag时，最优路径的概率
        - 每一步只保留到达每个词性的最优路径
        - 最终回溯得到全局最优的词性序列

        ━━━━━━━ 生活类比 ━━━━━━━
        想象你在迷宫中找最短路径：
        - 每到一个岔路口，你只保留到达每个位置的最短路径
        - 不用记录所有可能的路径（那样太多了）
        - 最后从终点回溯，就能得到最短路径

        参数：
            words: 词列表

        返回：
            最优的词性标签列表
        """
        if not words:
            return []

        n = len(words)
        tags = list(self.pos_tags)

        # ── dp[t][tag] = 到达第t个词、词性为tag的最大对数概率 ──
        # 用对数概率避免连乘导致的数值下溢
        dp = [{} for _ in range(n)]
        # ── backpointer[t][tag] = 最优前驱词性 ──
        bp = [{} for _ in range(n)]

        # ── 初始化：第一个词 ──
        for tag in tags:
            start_p = self._get_start_prob(tag)
            emit_p = self._get_emit_prob(words[0], tag)
            import math
            dp[0][tag] = math.log(start_p) + math.log(emit_p)

        # ── 递推：第2个词到最后一个词 ──
        for t in range(1, n):
            for tag in tags:
                best_score = float('-inf')
                best_prev = tags[0]

                # 遍历所有可能的前驱词性，找最优的
                for prev_tag in tags:
                    score = (dp[t - 1].get(prev_tag, float('-inf')) +
                             math.log(self._get_trans_prob(prev_tag, tag)) +
                             math.log(self._get_emit_prob(words[t], tag)))
                    if score > best_score:
                        best_score = score
                        best_prev = prev_tag

                dp[t][tag] = best_score
                bp[t][tag] = best_prev

        # ── 回溯：找最优路径 ──
        # 先找最后一个词的最优词性
        best_last_tag = max(dp[n - 1], key=dp[n - 1].get)

        # 从后往前回溯
        result = [best_last_tag]
        for t in range(n - 1, 0, -1):
            result.append(bp[t][result[-1]])
        result.reverse()

        return result

    def tag(self, words: list) -> list:
        """
        对词列表进行词性标注（接口方法）

        参数：
            words: 词列表，如 ["我", "喜欢", "吃", "苹果"]

        返回：
            [(词, 词性), ...] 列表
        """
        if not self.trained:
            print("  [警告] 模型尚未训练，请先调用 train() 方法！")
            return [(w, "n") for w in words]

        pos_tags = self.viterbi(words)
        return list(zip(words, pos_tags))


# ==============================================================================
# 第五部分：简化的 CRF 词性标注器
# ==============================================================================
#
# CRF（条件随机场）是比 HMM 更强大的序列标注模型。
#
# ━━━━━━━ HMM vs CRF ━━━━━━━
#
# HMM 的限制：
# - 假设当前词性只依赖前一个词性（马尔可夫假设）
# - 假设每个词只依赖自己的词性（观测独立假设）
# - 特征很有限：只能用"前一个词性"和"当前词"
#
# CRF 的优势：
# - 可以使用任意特征：前后词、词缀、是否数字等
# - 没有严格的独立性假设
# - 直接建模 P(标签序列|词序列)，而不是联合概率
#
# ━━━━━━━ 生活类比 ━━━━━━━
#
# HMM 就像只看"前一个人的回答"来答题：
#   前面的人说C → 你猜这道题可能是B
#
# CRF 就像综合考虑多种线索来答题：
#   前面的人说C + 题目中有"不"字 + 这个词以"地"结尾 → 你猜B
#
# 特征越多，判断越准确！
#
# ==============================================================================

class CRFPOSTagger:
    """
    简化的 CRF 词性标注器（基于平均感知机）

    ━━━━━━━ 核心思想 ━━━━━━━
    CRF 的核心是"特征函数"：
    - 每个特征函数检查一种模式，返回0或1
    - 每个特征函数有权重，表示这个模式的重要程度
    - 最终得分 = 所有特征函数的加权和

    ━━━━━━━ 训练方法：平均感知机 ━━━━━━━
    感知机的训练就像"纠错学习"：
    1. 看一个训练样本
    2. 用当前模型预测词性
    3. 如果预测正确 → 不做修改
    4. 如果预测错误 →
       - 增加正确标签的特征权重（让正确答案更可能）
       - 减少错误标签的特征权重（让错误答案更不可能）

    平均感知机：把所有迭代的权重取平均，避免过拟合。

    ━━━━━━━ 贪心解码 ━━━━━━━
    逐词选择得分最高的词性，不考虑全局最优。
    虽然不如维特比精确，但速度快，适合演示。
    """

    def __init__(self):
        """
        初始化 CRF 词性标注器

        创建特征权重字典，等待训练。
        """
        # ── 特征权重 ──
        # key=(特征名, 特征值, 词性标签), value=权重值
        # 例如: ("word", "苹果", "n") → 2.5 表示"苹果作为名词"的权重是2.5
        self.weights = {}

        # ── 累积权重（用于平均感知机） ──
        # 训练过程中累加所有迭代的权重，最后取平均
        self.total_weights = {}

        # ── 词性标签集合 ──
        self.pos_tags = set()

        # ── 训练状态 ──
        self.trained = False

    def _extract_features(self, sentence: list, i: int) -> list:
        """
        提取位置 i 处的特征

        ━━━━━━━ 生活类比 ━━━━━━━
        想象你在判断一个人的职业，你会观察他的特征：
        - 穿白大褂 → 可能是医生
        - 拿着粉笔 → 可能是老师
        - 西装革履 → 可能是商务人士

        CRF 的特征提取也是同样的道理：
        从当前词和上下文中提取各种"线索"。

        提取的特征包括：
        1. 当前词本身 — "苹果"很可能是名词
        2. 前一个词 — "吃苹果"中"吃"暗示后面是名词
        3. 后一个词 — "苹果好吃"中"好吃"暗示前面是名词
        4. 词的后缀 — 以"地"结尾很可能是副词
        5. 词的前缀 — 以"第"开头很可能是数词
        6. 是否数字 — 纯数字很可能是数词
        7. 是否标点 — 标点符号有特殊词性

        参数：
            sentence: 词列表
            i: 当前词的位置索引

        返回：
            特征列表，每个特征是 (特征名, 特征值) 的元组
        """
        word = sentence[i]
        features = []

        # ── 特征1: 当前词 ──
        # 词本身就是最强的特征：看到"苹果"就大概知道是名词
        features.append(("word", word))

        # ── 特征2: 前一个词（如果存在） ──
        # 前面的词提供上下文：在"吃苹果"中，"吃"暗示后面是名词
        if i > 0:
            features.append(("prev_word", sentence[i - 1]))
        else:
            features.append(("prev_word", "<START>"))  # 句首标记

        # ── 特征3: 后一个词（如果存在） ──
        # 后面的词也提供上下文：在"苹果好吃"中，"好吃"暗示前面是名词
        if i < len(sentence) - 1:
            features.append(("next_word", sentence[i + 1]))
        else:
            features.append(("next_word", "<END>"))  # 句尾标记

        # ── 特征4: 词的后缀（最后2个字符） ──
        # 后缀是判断词性的重要线索：
        # "高兴地" → "地" → 可能是副词
        # "美丽的" → "的" → 可能是形容词
        # "跑了" → "了" → 可能是助词
        if len(word) >= 2:
            features.append(("suffix", word[-2:]))
        else:
            features.append(("suffix", word))

        # ── 特征5: 词的前缀（前2个字符） ──
        # 前缀也能提供线索：
        # "第一名" → "第" → 可能是数词
        # "老师" → "老" → 可能是名词
        if len(word) >= 2:
            features.append(("prefix", word[:2]))
        else:
            features.append(("prefix", word))

        # ── 特征6: 是否为纯数字 ──
        # 纯数字很可能是数词：123、2026、100
        features.append(("is_digit", word.isdigit()))

        # ── 特征7: 是否为标点符号 ──
        # 标点符号有特殊的词性（标点类）
        punctuations = "，。！？、；：""''（）【】《》——……"
        features.append(("is_punct", word in punctuations))

        # ── 特征8: 词的长度 ──
        # 不同长度的词可能有不同的词性偏好
        # 单字词很可能是助词或代词，多字词很可能是名词或动词
        if len(word) == 1:
            features.append(("word_len", "single"))
        elif len(word) == 2:
            features.append(("word_len", "double"))
        else:
            features.append(("word_len", "long"))

        return features

    def _score(self, features: list, tag: str) -> float:
        """
        计算给定特征和词性的得分

        ━━━━━━━ 公式 ━━━━━━━
        score = sum(权重[(特征名, 特征值, tag)] for 每个特征)

        就像打分：每个特征投一票，每票的权重不同。
        总分最高的词性就是预测结果。

        参数：
            features: 特征列表
            tag: 候选词性

        返回：
            得分（浮点数）
        """
        score = 0.0
        for feat_name, feat_value in features:
            # 查找该特征在该词性下的权重
            key = (feat_name, feat_value, tag)
            score += self.weights.get(key, 0.0)
        return score

    def train(self, tagged_sentences: list, num_iterations: int = 5):
        """
        使用平均感知机训练 CRF 模型

        ━━━━━━━ 训练过程 ━━━━━━━
        就像老师批改作业：
        1. 拿一份作业（一个标注句子）
        2. 学生（模型）给出自己的答案（预测词性）
        3. 对照标准答案：
           - 答对了 → 不做修改（已经很好了）
           - 答错了 → 调整权重：
             * 增加正确答案的特征权重（强化正确模式）
             * 减少错误答案的特征权重（抑制错误模式）
        4. 重复多轮（num_iterations），直到学好

        ━━━━━━━ 平均感知机 ━━━━━━━
        为什么取平均？
        - 单次迭代的权重可能波动很大
        - 取平均可以平滑波动，减少过拟合
        - 就像期末成绩 = 平时成绩的平均分

        参数：
            tagged_sentences: 标注好的句子列表
            num_iterations: 训练轮数
        """
        import copy

        for iteration in range(num_iterations):
            errors = 0
            total = 0

            for sentence in tagged_sentences:
                if not sentence:
                    continue

                words = [w for w, t in sentence]
                gold_tags = [t for w, t in sentence]  # 标准答案

                for i, (word, gold_tag) in enumerate(sentence):
                    # 收集词性
                    self.pos_tags.add(gold_tag)

                    # 提取特征
                    features = self._extract_features(words, i)

                    # ── 用当前模型预测 ──
                    # 对每个候选词性计算得分，选最高分的
                    best_tag = None
                    best_score = float('-inf')
                    for tag in self.pos_tags:
                        s = self._score(features, tag)
                        if s > best_score:
                            best_score = s
                            best_tag = tag

                    # ── 如果预测错误，更新权重 ──
                    total += 1
                    if best_tag != gold_tag:
                        errors += 1

                        # 增加正确标签的特征权重（+1）
                        for feat_name, feat_value in features:
                            key = (feat_name, feat_value, gold_tag)
                            self.weights[key] = self.weights.get(key, 0.0) + 1.0
                            self.total_weights[key] = self.total_weights.get(key, 0.0) + self.weights[key]

                        # 减少错误标签的特征权重（-1）
                        for feat_name, feat_value in features:
                            key = (feat_name, feat_value, best_tag)
                            self.weights[key] = self.weights.get(key, 0.0) - 1.0
                            self.total_weights[key] = self.total_weights.get(key, 0.0) + self.weights[key]

            # 打印每轮的训练误差
            error_rate = errors / total if total > 0 else 0
            print(f"  [训练] 第{iteration + 1}轮: 错误率={error_rate:.2%} ({errors}/{total})")

        # ── 计算平均权重 ──
        # 平均感知机的核心：把累积权重除以总步数
        total_steps = num_iterations * len(tagged_sentences)
        for key in self.total_weights:
            self.weights[key] = self.total_weights[key] / max(total_steps, 1)

        self.trained = True
        print(f"  [训练完成] 学习了 {len(self.weights)} 个特征权重")

    def tag(self, words: list) -> list:
        """
        对词列表进行词性标注（贪心解码）

        ━━━━━━━ 贪心解码 ━━━━━━━
        逐词选择得分最高的词性，不考虑全局最优。
        就像考试时每道题独立作答，不考虑题目之间的关系。

        优点：速度快，实现简单
        缺点：可能不是全局最优（但实际效果通常够用）

        参数：
            words: 词列表

        返回：
            [(词, 词性), ...] 列表
        """
        if not self.trained:
            print("  [警告] 模型尚未训练，请先调用 train() 方法！")
            return [(w, "n") for w in words]

        result = []
        for i, word in enumerate(words):
            # 提取当前位置的特征
            features = self._extract_features(words, i)

            # 对每个候选词性计算得分
            best_tag = None
            best_score = float('-inf')
            for tag in self.pos_tags:
                score = self._score(features, tag)
                if score > best_score:
                    best_score = score
                    best_tag = tag

            result.append((word, best_tag if best_tag else "n"))

        return result


# ==============================================================================
# 主程序入口
# ==============================================================================

if __name__ == "__main__":

    print("""
    ╔══════════════════════════════════════════════════════╗
    ║        G-one NLP 学院 - 第三章                        ║
    ║        词性标注                                      ║
    ╚══════════════════════════════════════════════════════╝
    """)

    demo_rule_based()
    demo_hmm_tagger()
    demo_jieba_pos_tagging()

    # 课程总结
    print("\n" + "=" * 60)
    print("第三章 总结")
    print("=" * 60)
    print("""
    本章我们学习了词性标注：

    [OK] 什么是词性 — 名词、动词、形容词等词的类别
    [OK] 基于规则的标注 — 查词典，简单直接
    [OK] HMM 词性标注 — 用概率推断词性
         - 初始概率：句子开头的词性
         - 转移概率：词性之间的转移
         - 发射概率：词性下出现某个词的概率
         - 维特比算法：找最优词性序列
    [OK] jieba 词性标注实战
    """)

    print("-" * 60)
    print("下节预告：第四章 — 命名实体识别")
    print("-" * 60)
    print("""
    下一章我们将学习：
    - 什么是命名实体（人名、地名、机构名）
    - HMM 命名实体识别
    - CRF 命名实体识别
    """)
