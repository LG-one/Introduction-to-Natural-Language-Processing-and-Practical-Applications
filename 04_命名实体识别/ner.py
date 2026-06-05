"""
==============================================================================
第四章：命名实体识别（Named Entity Recognition, NER）
==============================================================================
日期：2026-05-16

同学们好！上一章我们学会了给词贴词性标签，这节课我们来识别句子中的"名字"。

----------------------------------------------------------------------
生活类比：NER 就像用荧光笔在文章里画重点
----------------------------------------------------------------------

想象你在读一篇新闻报道：

  "习近平主席在北京会见了来自清华大学的教授代表团。"

你会用不同颜色的荧光笔标记：

  ┌──────────────────────────────────────────────────────┐
  │  [习近平主席]  ← 红色（人名）                         │
  │  [北京]        ← 蓝色（地名）                         │
  │  [清华大学]    ← 绿色（机构名）                       │
  └──────────────────────────────────────────────────────┘

NER 就是让计算机自动完成这个"画重点"的过程！

----------------------------------------------------------------------
什么是命名实体？
----------------------------------------------------------------------

命名实体是指文本中具有特定意义的专有名词：

  ┌──────────────────────────────────────────────────────┐
  │  类型    │  标签   │  例子                            │
  ├──────────┼────────┼─────────────────────────────────┤
  │  人名    │  PER   │  张三、李四、小明、习近平          │
  │  地名    │  LOC   │  北京、上海、中国、太平洋          │
  │  机构名  │  ORG   │  清华大学、阿里巴巴、联合国        │
  │  时间    │  TIME  │  2026年、上午、昨天               │
  │  数值    │  NUM   │  一百万、30%、三个               │
  └──────────┴────────┴─────────────────────────────────┘

----------------------------------------------------------------------
BIO 标注体系
----------------------------------------------------------------------

NER 通常使用 BIO 标注体系来标记每个字/词：

  B = Begin（实体的开始）
  I = Inside（实体的内部）
  O = Outside（不属于任何实体）

例子："小明在北京大学学习"

  ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
  │  小  │  明  │  在  │  北  │  京  │  大  │  学  │ 学习 │
  ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
  │B-PER │I-PER │  O   │B-LOC │I-LOC │I-LOC │I-LOC │  O   │
  └──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘

==============================================================================
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import re
from collections import defaultdict


# ==============================================================================
# 第一部分：基于规则的命名实体识别
# ==============================================================================
#
# 最简单的 NER 方法：用规则和词典匹配。
#
# 就像查电话簿：你要找"张三"的电话，直接翻到"张"开头的地方找。
# 如果你知道所有姓氏和常见名字模式，就能识别出人名。
#
# ==============================================================================

# ---- 实体词典 ----
# 在实际项目中，这些词典可能有几十万甚至上百万个词条

# 人名词典
PERSON_NAMES = {
    "小明", "小红", "小华", "张三", "李四", "王五",
    "习近平", "李克强", "毛泽东", "邓小平",
    "李白", "杜甫", "苏轼", "鲁迅",
    "马云", "马化腾", "任正非", "雷军",
}

# 地名词典
LOCATION_NAMES = {
    "北京", "上海", "广州", "深圳", "杭州", "南京",
    "中国", "美国", "日本", "韩国", "英国", "法国",
    "亚洲", "欧洲", "太平洋", "大西洋",
    "北京市", "上海市", "广东省", "浙江省",
}

# 机构名词典
ORGANIZATION_NAMES = {
    "清华大学", "北京大学", "浙江大学", "复旦大学",
    "阿里巴巴", "腾讯", "百度", "华为", "小米",
    "联合国", "世界银行", "世界卫生组织",
    "中国科学院", "中国工程院",
}

# ---- 常见姓氏（用于识别未知人名） ----
CHINESE_SURNAMES = {
    "赵", "钱", "孙", "李", "周", "吴", "郑", "王",
    "冯", "陈", "褚", "卫", "蒋", "沈", "韩", "杨",
    "朱", "秦", "尤", "许", "何", "吕", "施", "张",
    "孔", "曹", "严", "华", "金", "魏", "陶", "姜",
    "习", "马", "刘", "徐", "黄", "林", "高", "罗",
}


def rule_based_ner(sentence: str) -> list:
    """
    基于规则和词典的命名实体识别

    ━━━━━━━ 生活类比 ━━━━━━━
    就像查电话簿：先在词典里找完全匹配的，再用规则（姓氏+名字模式）找新词。

    ━━━━━━━ 算法步骤 ━━━━━━━
    1. 最长匹配优先：优先匹配较长的实体（"清华大学"优先于"清华"）
    2. 词典匹配：在人名/地名/机构名词典中查找
    3. 规则匹配：用姓氏+名字模式识别未知人名

    参数：
        sentence: 输入句子（已分词的字符串）

    返回：
        实体列表 [(实体文本, 实体类型, 起始位置, 结束位置), ...]
    """
    entities = []
    i = 0
    n = len(sentence)

    while i < n:
        matched = False

        # ---- 第一步：最长匹配（从长到短尝试） ----
        # 为什么从长到短？因为"北京大学"应该被匹配为一个整体，
        # 而不是拆成"北京"（地名）+"大学"（普通词）
        for length in range(min(6, n - i), 0, -1):
            word = sentence[i:i + length]

            # 检查是否是机构名（优先级最高，因为最长）
            if word in ORGANIZATION_NAMES:
                entities.append((word, "ORG", i, i + length))
                i += length
                matched = True
                break

            # 检查是否是地名
            if word in LOCATION_NAMES:
                entities.append((word, "LOC", i, i + length))
                i += length
                matched = True
                break

            # 检查是否是人名
            if word in PERSON_NAMES:
                entities.append((word, "PER", i, i + length))
                i += length
                matched = True
                break

        # ---- 第二步：规则匹配（识别未知人名） ----
        if not matched:
            # 规则：姓 + 名（1-2个字）
            # 例如："张三丰" → "张"是姓，"三丰"是名
            # 注意：需要排除常见动词/介词/助词开头的情况，避免误判
            # 例如："学习" 的 "习" 虽然是姓，但不应被识别为人名
            common_non_name_chars = set("在是有的不了会能要对把被从到和但是因为所以如果虽然而且或者的地得着过"
                                       "然经已正很也非常特别都也就才刚将曾被让叫令使自它这那谁何什")
            if sentence[i] in CHINESE_SURNAMES:
                # 检查下一个字是否像名字（不是常见功能词）
                if i + 1 < n and sentence[i + 1] not in common_non_name_chars:
                    # 尝试匹配 "姓+名"（2-3个字的人名）
                    for name_len in [3, 2]:
                        if i + name_len <= n:
                            candidate = sentence[i:i + name_len]
                            # 检查是否像人名（姓后面跟1-2个字）
                            if (len(candidate) >= 2 and
                                    candidate not in LOCATION_NAMES and
                                    candidate not in ORGANIZATION_NAMES):
                                entities.append((candidate, "PER", i, i + name_len))
                                i += name_len
                                matched = True
                                break

        if not matched:
            i += 1

    return entities


def sentence_to_bio(sentence: str, entities: list) -> list:
    """
    将实体标注结果转换为 BIO 标签序列

    ━━━━━━━ 生活类比 ━━━━━━━
    就像给文章做标记：先画好哪些字属于哪个实体，再给每个字贴上 B/I/O 标签。

    参数：
        sentence: 原始句子
        entities: 实体列表 [(实体文本, 类型, 起始, 结束), ...]

    返回：
        BIO 标签列表 [(字, BIO标签), ...]
    """
    # 初始化所有字为 O 标签
    bio_tags = ["O"] * len(sentence)

    # 按照实体标注 BIO 标签
    for entity_text, entity_type, start, end in entities:
        bio_tags[start] = f"B-{entity_type}"  # 实体开始
        for j in range(start + 1, end):
            bio_tags[j] = f"I-{entity_type}"  # 实体内部

    return list(zip(list(sentence), bio_tags))


# ==============================================================================
# 第二部分：基于 HMM 的命名实体识别
# ==============================================================================
#
# HMM NER 和 HMM 词性标注的思路类似，只是：
#   - 状态变成了 BIO 标签（B-PER, I-PER, B-LOC, I-LOC, O, ...）
#   - 观测值还是字/词
#
# 就像猜谜语：你看到一个字（观测值），猜它属于哪种实体（隐藏状态），
# 而且前面的猜测会影响后面的猜测。
#
# ==============================================================================

class HMMNERModel:
    """
    基于 HMM 的命名实体识别模型

    ━━━━━━━ 核心思想 ━━━━━━━
    把 NER 看作序列标注问题：
    - 观测序列：句子中的每个字
    - 隐藏状态：每个字的 BIO 标签
    - 目标：找到最可能的 BIO 标签序列

    ━━━━━━━ 三个概率 ━━━━━━━
    1. 初始概率：句子第一个字的 BIO 标签概率
    2. 转移概率：BIO 标签之间的转移概率
       例如：B-PER 后面很可能是 I-PER（人名通常不止一个字）
    3. 发射概率：某个 BIO 标签下出现某个字的概率
       例如：B-PER 标签下出现"张"的概率很高（很多姓张的人）
    """

    def __init__(self):
        """初始化 HMM NER 模型"""
        # ---- BIO 标签集合 ----
        self.bio_tags = [
            "O",          # 非实体
            "B-PER", "I-PER",  # 人名
            "B-LOC", "I-LOC",  # 地名
            "B-ORG", "I-ORG",  # 机构名
        ]

        # ---- 初始概率 ----
        # 句子开头更可能是实体的开始（B-xxx）或非实体（O）
        self.start_prob = {
            "O": 0.5,
            "B-PER": 0.15, "I-PER": 0.01,
            "B-LOC": 0.15, "I-LOC": 0.01,
            "B-ORG": 0.15, "I-ORG": 0.01,
        }

        # ---- 转移概率 ----
        # 描述 BIO 标签之间的转移规律
        self.trans_prob = {
            # O 后面可以是任何 B-xxx（开始新实体）或继续是 O
            "O":     {"O": 0.5, "B-PER": 0.15, "B-LOC": 0.15, "B-ORG": 0.15,
                      "I-PER": 0.01, "I-LOC": 0.01, "I-ORG": 0.01},
            # B-PER 后面很可能是 I-PER（人名通常不止一个字）
            "B-PER": {"O": 0.2, "I-PER": 0.7, "B-PER": 0.02,
                       "B-LOC": 0.03, "B-ORG": 0.03, "I-LOC": 0.01, "I-ORG": 0.01},
            # I-PER 后面可以继续 I-PER 或回到 O
            "I-PER": {"O": 0.3, "I-PER": 0.5, "B-PER": 0.05,
                       "B-LOC": 0.05, "B-ORG": 0.05, "I-LOC": 0.02, "I-ORG": 0.02},
            # B-LOC 后面很可能是 I-LOC
            "B-LOC": {"O": 0.2, "I-LOC": 0.7, "B-PER": 0.02,
                       "B-LOC": 0.02, "B-ORG": 0.03, "I-PER": 0.01, "I-ORG": 0.01},
            "I-LOC": {"O": 0.3, "I-LOC": 0.5, "B-PER": 0.05,
                       "B-LOC": 0.05, "B-ORG": 0.05, "I-PER": 0.02, "I-ORG": 0.02},
            # B-ORG 后面很可能是 I-ORG
            "B-ORG": {"O": 0.2, "I-ORG": 0.7, "B-PER": 0.02,
                       "B-LOC": 0.03, "B-ORG": 0.02, "I-PER": 0.01, "I-LOC": 0.01},
            "I-ORG": {"O": 0.3, "I-ORG": 0.5, "B-PER": 0.05,
                       "B-LOC": 0.05, "B-ORG": 0.05, "I-PER": 0.02, "I-LOC": 0.02},
        }

        # ---- 发射概率 ----
        # 用字典记录：某个字在某个 BIO 标签下出现的概率
        # 这里用简化版本：常见字 → 标签的映射
        self._build_emit_prob()

    def _build_emit_prob(self):
        """
        构建发射概率表

        发射概率回答的问题是：
        "如果某个字的标签是 B-PER（人名开始），那这个字最可能是谁？"

        例如：
        - "张" 在 B-PER 下的概率很高（很多姓张的人）
        - "北" 在 B-LOC 下的概率很高（北京、北平等地名）
        - "清" 在 B-ORG 下的概率很高（清华大学等）

        注意：默认概率设得很低（0.001），只有特定字才给高概率，
        这样可以减少误判。
        """
        # 姓氏字 → B-PER 概率高
        surname_chars = set("赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张"
                           "孔曹严华金魏陶姜马刘徐黄林高罗")

        # 人名常用字（名字部分）→ I-PER 概率高
        name_chars = set("明红华伟强磊洋勇军杰娟敏静丽芳婷超飞鹏涛鑫")

        # 地名首字 → B-LOC 概率高
        loc_start_chars = set("北京上海广深杭南京州武汉成都重庆天津西安长沙")

        # 地名字 → I-LOC 概率高
        loc_chars = set("省市县镇村山河湖海江川东南西北中")

        # 机构首字 → B-ORG 概率高
        org_start_chars = set("清华北大浙复旦公司集团银行")

        # 机构字 → I-ORG 概率高
        org_chars = set("学公集团银行委员会局院所中心协会")

        # 构建发射概率字典，默认概率很低
        self.emit_prob = defaultdict(lambda: defaultdict(lambda: 0.001))

        for ch in surname_chars:
            self.emit_prob[ch]["B-PER"] = 0.4
            self.emit_prob[ch]["I-PER"] = 0.05

        for ch in name_chars:
            self.emit_prob[ch]["B-PER"] = 0.1
            self.emit_prob[ch]["I-PER"] = 0.3

        for ch in loc_start_chars:
            self.emit_prob[ch]["B-LOC"] = 0.4
            self.emit_prob[ch]["I-LOC"] = 0.1

        for ch in loc_chars:
            self.emit_prob[ch]["B-LOC"] = 0.1
            self.emit_prob[ch]["I-LOC"] = 0.3

        for ch in org_start_chars:
            self.emit_prob[ch]["B-ORG"] = 0.4
            self.emit_prob[ch]["I-ORG"] = 0.1

        for ch in org_chars:
            self.emit_prob[ch]["B-ORG"] = 0.1
            self.emit_prob[ch]["I-ORG"] = 0.3

    def _get_trans_prob(self, prev_tag, curr_tag):
        """获取转移概率"""
        if prev_tag in self.trans_prob:
            return self.trans_prob[prev_tag].get(curr_tag, 0.01)
        return 0.01

    def _get_emit_prob(self, char, tag):
        """获取发射概率"""
        return self.emit_prob[char][tag]

    def viterbi(self, chars: list) -> list:
        """
        维特比算法找最优 BIO 标签序列

        ━━━━━━━ 生活类比 ━━━━━━━
        想象你在走迷宫：
        - 每一层是一个字
        - 每层有7个门（7种 BIO 标签）
        - 每条路有一个"得分"（概率）
        - 目标：找到从起点到终点得分最高的路径

        参数：
            chars: 字列表（句子拆成的字）

        返回：
            BIO 标签列表
        """
        if not chars:
            return []

        n = len(chars)
        tags = self.bio_tags

        # dp[t][tag] = 到达第 t 个字、标签为 tag 的最大概率
        dp = [{} for _ in range(n)]
        # backpointer[t][tag] = 第 t 个字标签为 tag 时，前一个字的最优标签
        backpointer = [{} for _ in range(n)]

        # ---- 初始化第一个字 ----
        for tag in tags:
            emit_p = self._get_emit_prob(chars[0], tag)
            dp[0][tag] = self.start_prob.get(tag, 0.01) * emit_p
            backpointer[0][tag] = None

        # ---- 递推：从第2个字开始 ----
        for t in range(1, n):
            for tag in tags:
                max_prob = 0
                best_prev = "O"
                for prev_tag in tags:
                    # 概率 = 前一个字的概率 × 转移概率
                    prob = dp[t - 1].get(prev_tag, 0) * self._get_trans_prob(prev_tag, tag)
                    if prob > max_prob:
                        max_prob = prob
                        best_prev = prev_tag

                # 乘以发射概率
                emit_p = self._get_emit_prob(chars[t], tag)
                dp[t][tag] = max_prob * emit_p
                backpointer[t][tag] = best_prev

        # ---- 回溯找最优路径 ----
        # 找最后一个字的最优标签
        best_last_tag = max(dp[n - 1], key=dp[n - 1].get)
        best_path = [best_last_tag]

        # 从后往前回溯
        for t in range(n - 1, 0, -1):
            best_path.append(backpointer[t][best_path[-1]])
        best_path.reverse()

        return best_path

    def predict(self, sentence: str) -> list:
        """
        对句子进行命名实体识别

        参数：
            sentence: 输入句子

        返回：
            [(字, BIO标签), ...] 列表
        """
        chars = list(sentence)
        bio_tags = self.viterbi(chars)
        return list(zip(chars, bio_tags))

    def extract_entities(self, sentence: str) -> list:
        """
        从句子中提取命名实体

        参数：
            sentence: 输入句子

        返回：
            实体列表 [(实体文本, 实体类型), ...]
        """
        bio_result = self.predict(sentence)
        entities = []
        current_entity = ""
        current_type = ""

        for char, tag in bio_result:
            if tag.startswith("B-"):
                # 开始新实体
                if current_entity:
                    entities.append((current_entity, current_type))
                current_entity = char
                current_type = tag[2:]
            elif tag.startswith("I-") and current_entity:
                # 继续当前实体
                current_entity += char
            else:
                # O 标签，结束当前实体
                if current_entity:
                    entities.append((current_entity, current_type))
                    current_entity = ""
                    current_type = ""

        # 处理最后一个实体
        if current_entity:
            entities.append((current_entity, current_type))

        return entities


# ==============================================================================
# 第三部分：基于 CRF 的命名实体识别
# ==============================================================================
#
# CRF（条件随机场）比 HMM 更强大，因为它可以使用更丰富的特征：
#   - 当前字本身
#   - 前一个字、后一个字
#   - 字的特征（是否是姓氏、是否是数字等）
#
# 就像法官判案：不仅看当前证据，还要看前后关联的证据，
# 综合所有证据做出最合理的判断。
#
# ==============================================================================

class SimpleCRFNER:
    """
    简化版 CRF 命名实体识别

    ━━━━━━━ 核心思想 ━━━━━━━
    CRF 和 HMM 的区别：
    - HMM：需要建模联合概率 P(字, 标签)，假设字之间独立
    - CRF：直接建模条件概率 P(标签|字)，可以用任意特征

    CRF 的优势：
    - 可以使用上下文特征（前一个字、后一个字）
    - 可以使用字的属性特征（是否姓氏、是否数字等）
    - 不需要假设字之间独立

    ━━━━━━━ 特征函数 ━━━━━━━
    CRF 通过"特征函数"来捕捉字和标签之间的关系：
    - 当前字是否在人名词典中 → 更可能是 B-PER
    - 前一个字标签是 B-PER → 当前字更可能是 I-PER
    - 当前字是数字 → 更可能是 O（数字通常不是命名实体）
    """

    def __init__(self):
        """初始化简化版 CRF NER 模型"""
        # 特征权重（简化版，实际中通过训练学习）
        self.weights = {
            # 词典特征
            "in_person_dict": {"B-PER": 2.0, "I-PER": 1.5},
            "in_location_dict": {"B-LOC": 2.0, "I-LOC": 1.5},
            "in_org_dict": {"B-ORG": 2.0, "I-ORG": 1.5},
            # 姓氏特征
            "is_surname": {"B-PER": 1.5, "I-PER": 0.5},
            # 转移特征
            "transition": {
                ("O", "B-PER"): 1.0, ("O", "B-LOC"): 1.0, ("O", "B-ORG"): 1.0,
                ("B-PER", "I-PER"): 2.0, ("B-LOC", "I-LOC"): 2.0, ("B-ORG", "I-ORG"): 2.0,
                ("I-PER", "I-PER"): 1.5, ("I-LOC", "I-LOC"): 1.5, ("I-ORG", "I-ORG"): 1.5,
            }
        }

    def _extract_features(self, chars: list, position: int, prev_tag: str) -> dict:
        """
        提取某个位置的特征

        ━━━━━━━ 生活类比 ━━━━━━━
        就像警察破案时收集线索：
        - 当前嫌疑人是谁？（当前字）
        - 他前面的人是谁？（前一个字）
        - 他后面的人是谁？（后一个字）
        - 他有什么特征？（是否姓氏、是否数字等）

        参数：
            chars: 字列表
            position: 当前位置
            prev_tag: 前一个字的标签

        返回：
            特征字典 {特征名: 特征值}
        """
        features = {}
        char = chars[position]

        # 当前字特征
        features["char"] = char
        features["is_surname"] = char in CHINESE_SURNAMES

        # 检查当前位置开始是否能匹配词典中的实体（最长匹配）
        features["in_person_dict"] = False
        features["in_location_dict"] = False
        features["in_org_dict"] = False

        for length in range(min(4, len(chars) - position), 0, -1):
            word = "".join(chars[position:position + length])
            if word in PERSON_NAMES:
                features["in_person_dict"] = True
            if word in LOCATION_NAMES:
                features["in_location_dict"] = True
            if word in ORGANIZATION_NAMES:
                features["in_org_dict"] = True

        # 上下文特征
        if position > 0:
            features["prev_char"] = chars[position - 1]
        if position < len(chars) - 1:
            features["next_char"] = chars[position + 1]

        # 转移特征
        features["prev_tag"] = prev_tag

        return features

    def _score_tag(self, features: dict, tag: str) -> float:
        """
        计算某个标签的得分

        得分 = 所有相关特征的权重之和
        """
        score = 0.0

        # 词典特征得分
        if features.get("in_person_dict") and tag in self.weights["in_person_dict"]:
            score += self.weights["in_person_dict"][tag]
        if features.get("in_location_dict") and tag in self.weights["in_location_dict"]:
            score += self.weights["in_location_dict"][tag]
        if features.get("in_org_dict") and tag in self.weights["in_org_dict"]:
            score += self.weights["in_org_dict"][tag]

        # 姓氏特征得分
        if features.get("is_surname") and tag in self.weights["is_surname"]:
            score += self.weights["is_surname"][tag]

        # 转移特征得分
        prev_tag = features.get("prev_tag", "O")
        trans_key = (prev_tag, tag)
        if trans_key in self.weights["transition"]:
            score += self.weights["transition"][trans_key]

        return score

    def predict(self, sentence: str) -> list:
        """
        使用简化版 CRF 进行 NER 预测

        ━━━━━━━ 算法 ━━━━━━━
        使用贪心策略（简化版）：
        1. 对每个字，计算所有可能标签的得分
        2. 选择得分最高的标签

        注意：真正的 CRF 使用维特比算法找全局最优，
        这里为了教学简化使用贪心策略。

        参数：
            sentence: 输入句子

        返回：
            [(字, BIO标签), ...] 列表
        """
        chars = list(sentence)
        bio_tags = ["O", "B-PER", "I-PER", "B-LOC", "I-LOC", "B-ORG", "I-ORG"]
        result = []
        prev_tag = "O"

        for i in range(len(chars)):
            features = self._extract_features(chars, i, prev_tag)

            # 计算每个标签的得分
            best_tag = "O"
            best_score = float("-inf")
            for tag in bio_tags:
                score = self._score_tag(features, tag)
                if score > best_score:
                    best_score = score
                    best_tag = tag

            result.append((chars[i], best_tag))
            prev_tag = best_tag

        return result

    def extract_entities(self, sentence: str) -> list:
        """
        从句子中提取命名实体

        参数：
            sentence: 输入句子

        返回：
            实体列表 [(实体文本, 实体类型), ...]
        """
        bio_result = self.predict(sentence)
        entities = []
        current_entity = ""
        current_type = ""

        for char, tag in bio_result:
            if tag.startswith("B-"):
                if current_entity:
                    entities.append((current_entity, current_type))
                current_entity = char
                current_type = tag[2:]
            elif tag.startswith("I-") and current_entity:
                current_entity += char
            else:
                if current_entity:
                    entities.append((current_entity, current_type))
                    current_entity = ""
                    current_type = ""

        if current_entity:
            entities.append((current_entity, current_type))

        return entities


# ==============================================================================
# 第四部分：jieba 命名实体识别实战
# ==============================================================================

def demo_jieba_ner(sentence: str) -> list:
    """
    使用 jieba 进行命名实体识别

    ━━━━━━━ 生活类比 ━━━━━━━
    jieba 就像一个经验丰富的编辑：
    - 它已经"读过"大量的文章
    - 它知道哪些词通常是人名、地名、机构名
    - 你给它一篇文章，它就能帮你标出来

    参数：
        sentence: 输入句子

    返回：
        实体列表 [(实体文本, 实体类型), ...]
    """
    try:
        import jieba.posseg as pseg
    except ImportError:
        print("[提示] jieba 未安装，请运行: pip install jieba")
        return []

    # jieba 的词性标注中：
    # nr = 人名, ns = 地名, nt = 机构名
    entity_map = {
        "nr": "PER",   # 人名
        "ns": "LOC",   # 地名
        "nt": "ORG",   # 机构名
    }

    entities = []
    words_pos = pseg.cut(sentence)

    for word, flag in words_pos:
        if flag in entity_map:
            entities.append((word, entity_map[flag]))

    return entities


# ==============================================================================
# 演示函数
# ==============================================================================

def demo_rule_based():
    """演示基于规则的 NER"""
    print("=" * 60)
    print("基于规则的命名实体识别")
    print("=" * 60)

    sentences = [
        "小明在北京大学学习自然语言处理",
        "马云创办了阿里巴巴",
        "张三去了上海旅游",
    ]

    for sent in sentences:
        print(f"\n句子: {sent}")
        entities = rule_based_ner(sent)
        if entities:
            for ent_text, ent_type, start, end in entities:
                print(f"  [{ent_text}] → {ent_type}")
        else:
            print("  未识别到实体")


def demo_hmm_ner():
    """演示 HMM NER"""
    print("\n" + "=" * 60)
    print("HMM 命名实体识别")
    print("=" * 60)

    model = HMMNERModel()

    sentences = [
        "小明在北京大学学习",
        "马云创办了阿里巴巴",
        "张三去上海旅游",
    ]

    for sent in sentences:
        print(f"\n句子: {sent}")

        # 显示 BIO 标注
        bio_result = model.predict(sent)
        bio_str = " ".join([f"{ch}/{tag}" for ch, tag in bio_result])
        print(f"  BIO: {bio_str}")

        # 提取实体
        entities = model.extract_entities(sent)
        if entities:
            for ent_text, ent_type in entities:
                print(f"  [{ent_text}] → {ent_type}")


def demo_crf_ner():
    """演示 CRF NER"""
    print("\n" + "=" * 60)
    print("CRF 命名实体识别（简化版）")
    print("=" * 60)

    model = SimpleCRFNER()

    sentences = [
        "小明在北京大学学习",
        "马云创办了阿里巴巴",
        "张三去上海旅游",
    ]

    for sent in sentences:
        print(f"\n句子: {sent}")

        # 显示 BIO 标注
        bio_result = model.predict(sent)
        bio_str = " ".join([f"{ch}/{tag}" for ch, tag in bio_result])
        print(f"  BIO: {bio_str}")

        # 提取实体
        entities = model.extract_entities(sent)
        if entities:
            for ent_text, ent_type in entities:
                print(f"  [{ent_text}] → {ent_type}")


# ==============================================================================
# 主程序入口
# ==============================================================================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║        G-one NLP 学院 - 第四章                        ║
    ║        命名实体识别                                  ║
    ╚══════════════════════════════════════════════════════╝
    """)

    demo_rule_based()
    demo_hmm_ner()
    demo_crf_ner()

    print("\n" + "=" * 60)
    print("第四章 总结")
    print("=" * 60)
    print("""
    本章我们学习了命名实体识别（NER）：

    [OK] 什么是 NER — 识别文本中的人名、地名、机构名
    [OK] BIO 标注体系 — B（开始）、I（内部）、O（非实体）
    [OK] 基于规则的 NER — 用词典和规则匹配实体
    [OK] HMM NER — 用概率模型推断实体
    [OK] CRF NER — 用条件随机场，支持更丰富的特征
    [OK] jieba NER — 开箱即用的 NER 工具
    """)
