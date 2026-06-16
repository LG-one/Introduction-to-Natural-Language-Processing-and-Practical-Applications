"""
==============================================================================
第十六章：关键词与摘要
==============================================================================
日期：2026-05-16

同学们好！这节课我们来学习两个非常实用的 NLP 技术 —— 关键词提取和文本摘要。

----------------------------------------------------------------------
生活类比：关键词提取就像给文章"划重点"
----------------------------------------------------------------------

想象你在读一篇很长的论文，老师说："划出最重要的 5 个词。"

你会怎么做？
  1. 先通读全文
  2. 找出反复出现的、重要的词
  3. 排除掉"的、是、在"这种没意义的词
  4. 留下最能概括文章主题的词

关键词提取就是让计算机做同样的事情。

----------------------------------------------------------------------
生活类比：文本摘要就像"写读书笔记"
----------------------------------------------------------------------

读完一本书，你需要写一份 200 字的读书笔记：
  1. 找出书中最重要的句子
  2. 把这些句子拼在一起
  3. 就是一份摘要！

文本摘要有两种方式：
  - 抽取式：从原文中"摘"出重要的句子（像剪报）
  - 生成式：用自己的话"写"出摘要（像读书笔记）

本章我们重点学习抽取式摘要。

----------------------------------------------------------------------
本章内容
----------------------------------------------------------------------

1. TF-IDF 关键词提取
2. TextRank 算法（Google PageRank 的文本版）
3. 抽取式文本摘要

==============================================================================
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import math
import re
from collections import Counter


# ==============================================================================
# 第一部分：TF-IDF 关键词提取
# ==============================================================================
#
# TF-IDF 是最经典的关键词提取方法。
#
# 核心思想：
#   - TF（词频）：一个词在文档中出现得越多，越重要
#   - IDF（逆文档频率）：一个词在越少的文档中出现，越独特
#   - TF-IDF = TF × IDF：既重要又独特的词就是关键词
#
# 生活类比：
#   想象你是一个老师，要判断一个学生作文的"主题词"：
#   - 如果"苹果"在作文里出现了 10 次 → TF 高（重要）
#   - 如果"苹果"只在这篇作文里出现，其他作文都没有 → IDF 高（独特）
#   - 那"苹果"很可能是这篇作文的关键词
#
# ==============================================================================


def build_vocab_from_docs(documents: list) -> list:
    """
    从文档集合中构建词汇表

    参数：
        documents: 文档列表

    返回：
        词汇表（排序后的词列表）
    """
    vocab = set()
    for doc in documents:
        for char in doc:
            if char.strip() and char not in "，。！？、；：""''（）【】《》\n\r\t":
                vocab.add(char)
    return sorted(list(vocab))


def compute_tf(document: str) -> dict:
    """
    计算词频（TF）

    ━━━━━━━ 生活类比 ━━━━━━━
    就像数一数你的购物车里每种商品买了几件，
    然后除以总件数，得到每种商品的"占比"。

    公式：
        TF(t, d) = 词 t 在文档 d 中出现的次数 / 文档 d 的总词数
    """
    char_count = Counter()
    total = 0
    for char in document:
        if char.strip() and char not in "，。！？、；：""''（）【】《》\n\r\t":
            char_count[char] += 1
            total += 1

    if total == 0:
        return {}
    return {word: count / total for word, count in char_count.items()}


def compute_idf(documents: list) -> dict:
    """
    计算逆文档频率（IDF）

    ━━━━━━━ 生活类比 ━━━━━━━
    想象全校有 100 篇作文：
    - "的" 出现在 100 篇里 → IDF = log(100/100) ≈ 0（不重要）
    - "量子" 只出现在 3 篇里 → IDF = log(100/3) ≈ 3.5（很重要）

    公式：
        IDF(t) = log(总文档数 / 包含词 t 的文档数)
    """
    n_docs = len(documents)
    doc_freq = Counter()

    for doc in documents:
        unique_chars = set()
        for char in doc:
            if char.strip() and char not in "，。！？、；：""''（）【】《》\n\r\t":
                unique_chars.add(char)
        for char in unique_chars:
            doc_freq[char] += 1

    return {word: math.log((n_docs + 1) / (df + 1)) + 1 for word, df in doc_freq.items()}


def extract_keywords_tfidf(document: str, documents: list, top_k: int = 5) -> list:
    """
    使用 TF-IDF 提取关键词

    ━━━━━━━ 生活类比 ━━━━━━━
    就像一个老师批改作文：
    1. 数一数每个词出现了几次（TF）
    2. 看看这个词在全年级作文里有多常见（IDF）
    3. 两相比较，找出"这篇作文里用得多，但别人很少用"的词

    参数：
        document: 目标文档
        documents: 所有文档（包含目标文档）
        top_k: 返回前 k 个关键词

    返回：
        关键词列表，每个元素是 (词, TF-IDF 分数)
    """
    # 计算 TF
    tf = compute_tf(document)

    # 计算 IDF
    idf = compute_idf(documents)

    # 计算 TF-IDF
    tfidf = {}
    for word, tf_val in tf.items():
        idf_val = idf.get(word, 1.0)
        tfidf[word] = tf_val * idf_val

    # 按 TF-IDF 分数降序排列
    sorted_words = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)

    return sorted_words[:top_k]


# ==============================================================================
# 第二部分：TextRank 算法
# ==============================================================================
#
# TextRank 是 Google PageRank 算法在文本领域的应用。
#
# 核心思想：
#   - 把文档中的词看作"网页"
#   - 词与词之间的共现关系看作"链接"
#   - 被越多"重要词"链接的词，自己也越重要
#
# 生活类比：
#   想象你在学校里：
#   - 如果全校最受欢迎的人都说"张三很厉害"
#   - 那张三一定也很厉害！
#   - TextRank 就是这个道理：被重要的人认可，你也重要。
#
# ==============================================================================


def build_word_graph(text: str, window_size: int = 5) -> dict:
    """
    构建词共现图

    ━━━━━━━ 生活类比 ━━━━━━━
    想象你在看一部电影，记录每个场景里同时出现的角色：
    - 场景 1：张三、李四、王五 → 他们之间有"共现关系"
    - 场景 2：李四、赵六 → 他们之间也有关系

    共现图就是记录"哪些词经常一起出现"。

    参数：
        text: 文本
        window_size: 滑动窗口大小

    返回：
        图的邻接表 {词: {相邻词: 权重}}
    """
    # 分词（简单的按字符分词）
    words = []
    for char in text:
        if char.strip() and char not in "，。！？、；：""''（）【】《》\n\r\t":
            words.append(char)

    # 构建共现图
    graph = {}
    for i, word in enumerate(words):
        if word not in graph:
            graph[word] = {}

        # 窗口内的其他词
        start = max(0, i - window_size)
        end = min(len(words), i + window_size + 1)
        for j in range(start, end):
            if i != j:
                neighbor = words[j]
                if neighbor not in graph[word]:
                    graph[word][neighbor] = 0
                graph[word][neighbor] += 1

    return graph


def textrank(graph: dict, damping: float = 0.85, max_iterations: int = 100,
             threshold: float = 1e-4) -> dict:
    """
    TextRank 算法

    ━━━━━━━ 生活类比 ━━━━━━━
    想象一个社交网络：
    - 每个人有一个"影响力分数"
    - 每轮更新：你的分数 = 朋友的影响力之和（加权）
    - 迭代多次后，分数会收敛
    - 最终，被最多"有影响力的人"认可的人，分数最高

    公式：
        WS(Vi) = (1-d) + d × Σ(Wji / ΣWjk) × WS(Vj)

        其中：
        - WS(Vi) = 词 Vi 的 TextRank 分数
        - d = 阻尼因子（通常 0.85）
        - Wji = 词 Vj 到 Vi 的边权重
        - ΣWjk = 词 Vj 的所有出边权重之和

    参数：
        graph: 词共现图 {词: {相邻词: 权重}}
        damping: 阻尼因子（0 到 1）
        max_iterations: 最大迭代次数
        threshold: 收敛阈值

    返回：
        TextRank 分数字典 {词: 分数}
    """
    # 初始化：每个词的分数 = 1
    scores = {word: 1.0 for word in graph}

    # 迭代更新
    for iteration in range(max_iterations):
        new_scores = {}
        max_diff = 0

        for word in graph:
            # 计算来自邻居的贡献
            neighbor_score = 0
            for neighbor, weight in graph.get(word, {}).items():
                # 邻居的总出边权重
                neighbor_total = sum(graph.get(neighbor, {}).values())
                if neighbor_total > 0:
                    neighbor_score += (weight / neighbor_total) * scores.get(neighbor, 0)

            # TextRank 公式
            new_scores[word] = (1 - damping) + damping * neighbor_score

            # 记录最大变化
            diff = abs(new_scores[word] - scores.get(word, 0))
            max_diff = max(max_diff, diff)

        scores = new_scores

        # 检查是否收敛
        if max_diff < threshold:
            break

    return scores


def extract_keywords_textrank(text: str, top_k: int = 5, window_size: int = 5) -> list:
    """
    使用 TextRank 提取关键词

    ━━━━━━━ 生活类比 ━━━━━━━
    就像在一个社交网络里找"最有影响力的人"：
    1. 先看看谁和谁是朋友（构建共现图）
    2. 然后用 PageRank 的方法计算每个人的影响力
    3. 影响力最大的人就是"关键人物"

    参数：
        text: 文本
        top_k: 返回前 k 个关键词
        window_size: 共现窗口大小

    返回：
        关键词列表，每个元素是 (词, TextRank 分数)
    """
    # 第一步：构建词共现图
    graph = build_word_graph(text, window_size)

    if not graph:
        return []

    # 第二步：运行 TextRank
    scores = textrank(graph)

    # 第三步：按分数降序排列
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return sorted_words[:top_k]


# ==============================================================================
# 第三部分：抽取式文本摘要
# ==============================================================================
#
# 抽取式摘要的核心思想：
#   从原文中选出最重要的几个句子，拼在一起就是摘要。
#
# 生活类比：
#   想象你在做"剪报"：
#   1. 读完整篇文章
#   2. 找出最重要的几句话
#   3. 把它们剪下来，贴在一起
#   4. 这就是一份摘要！
#
# ==============================================================================


def split_sentences(text: str) -> list:
    """
    中文分句

    ━━━━━━━ 生活类比 ━━━━━━━
    就像把一篇文章切成一个个"积木块"（句子），
    后面我们再从这些积木块中挑出最重要的几块。

    参数：
        text: 文本

    返回：
        句子列表
    """
    # 按中文标点和换行符分句
    sentences = re.split(r'[。！？\n]', text)
    # 去除空句子
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


def sentence_tfidf_score(sentence: str, document: str, all_documents: list) -> float:
    """
    计算句子的 TF-IDF 分数

    ━━━━━━━ 生活类比 ━━━━━━━
    句子的"重要性" = 句子里每个词的 TF-IDF 之和。
    包含越多"重要词"的句子，自己也越重要。

    参数：
        sentence: 句子
        document: 所在文档
        all_documents: 所有文档

    返回：
        句子的 TF-IDF 分数
    """
    # 计算 IDF（基于所有文档）
    idf = compute_idf(all_documents)

    # 计算句子中每个词的 TF-IDF，然后求和
    score = 0
    for char in sentence:
        if char.strip() and char not in "，。！？、；：""''（）【】《》\n\r\t":
            # TF：在句子中的频率
            tf = sentence.count(char) / len(sentence) if len(sentence) > 0 else 0
            # IDF：从所有文档中获取
            idf_val = idf.get(char, 1.0)
            score += tf * idf_val

    return score


def sentence_position_score(position: int, total_sentences: int) -> float:
    """
    计算句子的位置分数

    ━━━━━━━ 生活类比 ━━━━━━━
    新闻写作有一个原则："倒金字塔结构" ——
    最重要的信息放在最前面。

    所以：
    - 第一句通常包含最重要的信息（标题/导语）
    - 最后一句通常是总结
    - 中间的句子重要性递减

    参数：
        position: 句子位置（从 0 开始）
        total_sentences: 总句子数

    返回：
        位置分数（0 到 1）
    """
    if total_sentences <= 1:
        return 1.0

    # 第一句和最后一句给高分
    if position == 0:
        return 1.0
    elif position == total_sentences - 1:
        return 0.8
    else:
        # 中间句子按位置递减
        return 0.5 * (1 - position / total_sentences)


def sentence_length_score(sentence: str) -> float:
    """
    计算句子长度分数

    ━━━━━━━ 生活类比 ━━━━━━━
    太短的句子可能信息量不够（如"好的"），
    太长的句子可能太啰嗦。
    中等长度的句子通常信息密度最高。

    参数：
        sentence: 句子

    返回：
        长度分数（0 到 1）
    """
    length = len(sentence)
    if length < 5:
        return 0.3  # 太短
    elif length > 50:
        return 0.5  # 太长
    else:
        return 0.8  # 适中


def extract_summary(document: str, all_documents: list, top_k: int = 3) -> list:
    """
    抽取式文本摘要

    ━━━━━━━ 生活类比 ━━━━━━━
    就像一个老师在学生的长篇作文中划出"最重要的几句话"：
    1. 先把作文分成一个个句子
    2. 给每个句子打分（关键词、位置、长度）
    3. 选出得分最高的几个句子
    4. 按原文顺序排列，就是摘要

    参数：
        document: 目标文档
        all_documents: 所有文档
        top_k: 返回前 k 个句子

    返回：
        摘要句子列表（按原文顺序）
    """
    # 第一步：分句
    sentences = split_sentences(document)

    if len(sentences) <= top_k:
        return sentences

    # 第二步：给每个句子打分
    scored_sentences = []
    for i, sent in enumerate(sentences):
        # TF-IDF 分数（关键词重要性）
        tfidf_score = sentence_tfidf_score(sent, document, all_documents)

        # 位置分数（首尾句更重要）
        pos_score = sentence_position_score(i, len(sentences))

        # 长度分数（适中长度最好）
        len_score = sentence_length_score(sent)

        # 综合分数（加权平均）
        total_score = tfidf_score * 0.5 + pos_score * 0.3 + len_score * 0.2

        scored_sentences.append((i, sent, total_score))

    # 第三步：选出得分最高的 top_k 个句子
    scored_sentences.sort(key=lambda x: x[2], reverse=True)
    selected = scored_sentences[:top_k]

    # 第四步：按原文顺序排列
    selected.sort(key=lambda x: x[0])

    return [sent for _, sent, _ in selected]


# ==============================================================================
# 第四部分：TextRank 摘要
# ==============================================================================


def build_sentence_graph(sentences: list, window_size: int = 3) -> dict:
    """
    构建句子相似度图

    ━━━━━━━ 生活类比 ━━━━━━━
    想象一个班级里的"社交网络"：
    - 如果两个同学经常讨论同一个话题，他们之间有"连接"
    - 连接越多的同学，越可能是"班级核心人物"

    句子图也一样：
    - 如果两个句子包含很多相同的词，它们之间有"连接"
    - 连接越多的句子，越可能是"核心句子"

    参数：
        sentences: 句子列表
        window_size: 滑动窗口大小

    返回：
        图的邻接表 {句索引: {相邻句索引: 相似度}}
    """
    graph = {}

    for i in range(len(sentences)):
        graph[i] = {}
        # 窗口内的其他句子
        start = max(0, i - window_size)
        end = min(len(sentences), i + window_size + 1)
        for j in range(start, end):
            if i != j:
                # 计算两个句子的相似度（共同字符数）
                chars_i = set(c for c in sentences[i] if c.strip() and c not in "，。！？、；：""''（）【】《》")
                chars_j = set(c for c in sentences[j] if c.strip() and c not in "，。！？、；：""''（）【】《》")
                intersection = len(chars_i & chars_j)
                union = len(chars_i | chars_j)
                similarity = intersection / union if union > 0 else 0
                if similarity > 0:
                    graph[i][j] = similarity

    return graph


def textrank_summary(document: str, top_k: int = 3) -> list:
    """
    使用 TextRank 生成抽取式摘要

    ━━━━━━━ 生活类比 ━━━━━━━
    就像在一个班级里找"最有代表性的学生"：
    1. 先看看哪些学生之间关系密切（句子相似度）
    2. 然后用 PageRank 的方法找"核心学生"
    3. 这些核心学生就是班级的"代表"

    参数：
        document: 文档
        top_k: 返回前 k 个句子

    返回：
        摘要句子列表
    """
    # 第一步：分句
    sentences = split_sentences(document)

    if len(sentences) <= top_k:
        return sentences

    # 第二步：构建句子图
    graph = build_sentence_graph(sentences)

    # 第三步：运行 TextRank
    scores = textrank(graph)

    # 第四步：选出得分最高的 top_k 个句子
    scored = [(i, sentences[i], scores.get(i, 0)) for i in range(len(sentences))]
    scored.sort(key=lambda x: x[2], reverse=True)
    selected = scored[:top_k]

    # 按原文顺序排列
    selected.sort(key=lambda x: x[0])

    return [sent for _, sent, _ in selected]


# ==============================================================================
# 主程序入口
# ==============================================================================

if __name__ == "__main__":

    print("""
    ╔══════════════════════════════════════════════════════╗
    ║        G-one NLP 学院 - 第十六章                      ║
    ║        关键词与摘要                                  ║
    ╚══════════════════════════════════════════════════════╝
    """)

    # 测试数据
    doc1 = "自然语言处理是人工智能的重要方向。它让计算机能够理解和生成人类语言。深度学习技术推动了自然语言处理的发展。"
    doc2 = "机器学习是人工智能的核心技术。深度学习是机器学习的一个分支。神经网络是深度学习的基础。"
    doc3 = "今天股市大涨，上证指数突破三千点。投资者对经济前景持乐观态度。"

    documents = [doc1, doc2, doc3]

    # 测试 TF-IDF 关键词提取
    print("=" * 60)
    print("  1. TF-IDF 关键词提取")
    print("=" * 60)
    keywords = extract_keywords_tfidf(doc1, documents, top_k=5)
    print(f"  文档: {doc1[:30]}...")
    print(f"  关键词: {keywords}")

    # 测试 TextRank 关键词提取
    print("\n" + "=" * 60)
    print("  2. TextRank 关键词提取")
    print("=" * 60)
    keywords = extract_keywords_textrank(doc1, top_k=5)
    print(f"  文档: {doc1[:30]}...")
    print(f"  关键词: {keywords}")

    # 测试 TF-IDF 摘要
    print("\n" + "=" * 60)
    print("  3. TF-IDF 抽取式摘要")
    print("=" * 60)
    summary = extract_summary(doc1, documents, top_k=2)
    print(f"  原文: {doc1}")
    print(f"  摘要: {''.join(summary)}")

    # 测试 TextRank 摘要
    print("\n" + "=" * 60)
    print("  4. TextRank 摘要")
    print("=" * 60)
    summary = textrank_summary(doc1, top_k=2)
    print(f"  原文: {doc1}")
    print(f"  摘要: {''.join(summary)}")
