import sys
sys.stdout.reconfigure(encoding='utf-8')

"""
==============================================================================
第十六章：关键词与摘要 — 练习题
==============================================================================
G-one NLP 学院
日期：2026-05-16

本章练习：
    1. 实现 TF-IDF 关键词提取
    2. 实现简单的 TextRank 关键词提取
    3. 实现抽取式文本摘要

运行方式：
    python exercises.py

提示：
    - 每个练习都有详细的提示，按照提示一步步来
    - 先自己写，写不出来再看注释中的参考答案
    - 运行后会自动检查你的答案是否正确
==============================================================================
"""

import math
import re
from collections import Counter


# ==============================================================================
# 练习 1：TF-IDF 关键词提取
# ==============================================================================

def exercise_1_tfidf_keywords(document: str, all_documents: list, top_k: int = 3) -> list:
    """
    练习 1：使用 TF-IDF 提取关键词

    ━━━━━━━ 生活类比 ━━━━━━━
    想象你是一个老师，要找出学生作文的"主题词"：
    1. 数一数每个字出现了几次（TF）
    2. 看看这个字在其他作文里是否常见（IDF）
    3. 既在这篇作文里出现多，又在其他作文里少见的字 → 关键词

    ━━━━━━━ 提示 ━━━━━━━
    1. 计算 TF：遍历 document 中的每个字符
       - 跳过空白和标点
       - TF = 字符出现次数 / 文档总字符数

    2. 计算 IDF：遍历 all_documents
       - 统计每个字符出现在多少篇文档中
       - IDF = log((总文档数 + 1) / (包含该字符的文档数 + 1)) + 1

    3. TF-IDF = TF × IDF

    4. 按 TF-IDF 降序排列，返回前 top_k 个

    参数：
        document: 目标文档
        all_documents: 所有文档（包含目标文档）
        top_k: 返回前 k 个关键词

    返回：
        关键词列表，每个元素是 (字符, TF-IDF 分数)
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # # 计算 TF
    # char_count = Counter()
    # total = 0
    # for char in document:
    #     if char.strip() and char not in "，。！？、；：""''（）【】《》\n\r\t":
    #         char_count[char] += 1
    #         total += 1
    # tf = {w: c / total for w, c in char_count.items()} if total > 0 else {}
    #
    # # 计算 IDF
    # n_docs = len(all_documents)
    # doc_freq = Counter()
    # for doc in all_documents:
    #     unique = set(c for c in doc if c.strip() and c not in "，。！？、；：""''（）【】《》\n\r\t")
    #     for c in unique:
    #         doc_freq[c] += 1
    # idf = {w: math.log((n_docs + 1) / (df + 1)) + 1 for w, df in doc_freq.items()}
    #
    # # 计算 TF-IDF
    # tfidf = {w: tf.get(w, 0) * idf.get(w, 1.0) for w in tf}
    # sorted_words = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)
    # return sorted_words[:top_k]
    pass


def test_exercise_1():
    """测试练习 1"""
    print("\n" + "=" * 60)
    print("练习 1：TF-IDF 关键词提取")
    print("=" * 60)

    doc1 = "机器学习是人工智能的重要分支"
    doc2 = "深度学习是机器学习的热门方向"
    all_docs = [doc1, doc2]

    result = exercise_1_tfidf_keywords(doc1, all_docs, top_k=3)

    if result is None:
        print("[未完成] 请实现 exercise_1_tfidf_keywords 函数")
        return False

    if not isinstance(result, list) or len(result) == 0:
        print(f"[错误] 返回值应该是非空列表")
        return False

    # 检查返回格式
    if not isinstance(result[0], tuple) or len(result[0]) != 2:
        print(f"[错误] 返回值应该是 (字符, 分数) 元组列表")
        return False

    print(f"[正确] 文档: '{doc1}'")
    print(f"       关键词: {result}")
    print(f"       Top-1 关键词: '{result[0][0]}' (分数: {result[0][1]:.4f})")
    return True


# ==============================================================================
# 练习 2：TextRank 关键词提取
# ==============================================================================

def exercise_2_textrank_keywords(text: str, top_k: int = 3) -> list:
    """
    练习 2：使用 TextRank 提取关键词

    ━━━━━━━ 生活类比 ━━━━━━━
    想象一个社交网络：
    - 每个人有一个"影响力分数"
    - 被越多"有影响力的人"认可的人，自己也越重要
    - TextRank 就是用这个思想找关键词

    ━━━━━━━ 提示 ━━━━━━━
    1. 构建词共现图：
       - 用滑动窗口（大小 5）扫描文本
       - 窗口内的字符之间有"共现关系"
       - graph[char_i][char_j] += 1

    2. 运行 TextRank：
       - 初始化每个词的分数 = 1.0
       - 迭代更新：new_score[word] = (1-0.85) + 0.85 * Σ(权重贡献)
       - 权重贡献 = Σ(weight / neighbor_total_weight * neighbor_score)
       - 重复直到收敛（变化 < 0.0001）

    3. 按分数降序排列，返回前 top_k 个

    参数：
        text: 文本
        top_k: 返回前 k 个关键词

    返回：
        关键词列表，每个元素是 (字符, TextRank 分数)
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # # 分词
    # words = [c for c in text if c.strip() and c not in "，。！？、；：""''（）【】《》\n\r\t"]
    #
    # # 构建共现图
    # graph = {}
    # window_size = 5
    # for i, word in enumerate(words):
    #     if word not in graph:
    #         graph[word] = {}
    #     start = max(0, i - window_size)
    #     end = min(len(words), i + window_size + 1)
    #     for j in range(start, end):
    #         if i != j:
    #             neighbor = words[j]
    #             if neighbor not in graph[word]:
    #                 graph[word][neighbor] = 0
    #             graph[word][neighbor] += 1
    #
    # if not graph:
    #     return []
    #
    # # TextRank
    # scores = {w: 1.0 for w in graph}
    # for _ in range(100):
    #     new_scores = {}
    #     max_diff = 0
    #     for word in graph:
    #         neighbor_score = 0
    #         for neighbor, weight in graph.get(word, {}).items():
    #             neighbor_total = sum(graph.get(neighbor, {}).values())
    #             if neighbor_total > 0:
    #                 neighbor_score += (weight / neighbor_total) * scores.get(neighbor, 0)
    #         new_scores[word] = (1 - 0.85) + 0.85 * neighbor_score
    #         max_diff = max(max_diff, abs(new_scores[word] - scores.get(word, 0)))
    #     scores = new_scores
    #     if max_diff < 0.0001:
    #         break
    #
    # sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    # return sorted_words[:top_k]
    pass


def test_exercise_2():
    """测试练习 2"""
    print("\n" + "=" * 60)
    print("练习 2：TextRank 关键词提取")
    print("=" * 60)

    text = "自然语言处理是人工智能的重要方向。深度学习推动了自然语言处理的发展。"
    result = exercise_2_textrank_keywords(text, top_k=3)

    if result is None:
        print("[未完成] 请实现 exercise_2_textrank_keywords 函数")
        return False

    if not isinstance(result, list) or len(result) == 0:
        print(f"[错误] 返回值应该是非空列表")
        return False

    if not isinstance(result[0], tuple) or len(result[0]) != 2:
        print(f"[错误] 返回值应该是 (字符, 分数) 元组列表")
        return False

    print(f"[正确] 文本: '{text[:30]}...'")
    print(f"       关键词: {result}")
    return True


# ==============================================================================
# 练习 3：抽取式文本摘要
# ==============================================================================

def exercise_3_extractive_summary(text: str, top_k: int = 2) -> list:
    """
    练习 3：实现抽取式文本摘要

    ━━━━━━━ 生活类比 ━━━━━━━
    想象你在做"剪报"：
    1. 把文章切成句子
    2. 给每个句子打分
    3. 选出最重要的几个句子
    4. 拼在一起就是摘要

    ━━━━━━━ 提示 ━━━━━━━
    1. 分句：用 re.split(r'[。！？\n]', text) 按标点分句

    2. 给每个句子打分（综合三个维度）：
       a. 关键词分数：句子中"重要字符"的数量
          - 统计整个文本中每个字符的频率
          - 句子分数 = 句子中所有字符的频率之和
       b. 位置分数：第一句 = 1.0，最后一句 = 0.8，中间 = 0.5
       c. 长度分数：适中长度（5-50 字符）= 0.8，太短 = 0.3，太长 = 0.5

    3. 综合分数 = 关键词分数 × 0.5 + 位置分数 × 0.3 + 长度分数 × 0.2

    4. 选出得分最高的 top_k 个句子，按原文顺序返回

    参数：
        text: 文本
        top_k: 返回前 k 个句子

    返回：
        摘要句子列表
    """
    # TODO: 请在这里写你的代码
    #
    # 参考答案：
    # import re
    # from collections import Counter
    #
    # # 分句
    # sentences = [s.strip() for s in re.split(r'[。！？\n]', text) if s.strip()]
    # if len(sentences) <= top_k:
    #     return sentences
    #
    # # 统计字符频率
    # all_chars = Counter()
    # for char in text:
    #     if char.strip() and char not in "，。！？、；：""''（）【】《》\n\r\t":
    #         all_chars[char] += 1
    #
    # # 给每个句子打分
    # scored = []
    # total_sentences = len(sentences)
    # for i, sent in enumerate(sentences):
    #     # 关键词分数
    #     kw_score = sum(all_chars.get(c, 0) for c in sent if c.strip())
    #     kw_score = kw_score / len(sent) if len(sent) > 0 else 0
    #
    #     # 位置分数
    #     if i == 0:
    #         pos_score = 1.0
    #     elif i == total_sentences - 1:
    #         pos_score = 0.8
    #     else:
    #         pos_score = 0.5
    #
    #     # 长度分数
    #     length = len(sent)
    #     if length < 5:
    #         len_score = 0.3
    #     elif length > 50:
    #         len_score = 0.5
    #     else:
    #         len_score = 0.8
    #
    #     total_score = kw_score * 0.5 + pos_score * 0.3 + len_score * 0.2
    #     scored.append((i, sent, total_score))
    #
    # # 选出得分最高的
    # scored.sort(key=lambda x: x[2], reverse=True)
    # selected = scored[:top_k]
    # selected.sort(key=lambda x: x[0])
    # return [sent for _, sent, _ in selected]
    pass


def test_exercise_3():
    """测试练习 3"""
    print("\n" + "=" * 60)
    print("练习 3：抽取式文本摘要")
    print("=" * 60)

    text = (
        "自然语言处理是人工智能的重要方向。"
        "它让计算机能够理解和生成人类语言。"
        "近年来深度学习技术推动了自然语言处理的快速发展。"
        "预训练语言模型取得了突破性进展。"
        "未来自然语言处理将在更多领域发挥重要作用。"
    )

    result = exercise_3_extractive_summary(text, top_k=2)

    if result is None:
        print("[未完成] 请实现 exercise_3_extractive_summary 函数")
        return False

    if not isinstance(result, list) or len(result) == 0:
        print(f"[错误] 返回值应该是非空列表")
        return False

    if not isinstance(result[0], str):
        print(f"[错误] 返回值应该是字符串列表")
        return False

    print(f"[正确] 原文: '{text[:40]}...'")
    print(f"       摘要 ({len(result)} 句):")
    for sent in result:
        print(f"         - {sent}")
    return True


# ==============================================================================
# 主程序：运行所有练习测试
# ==============================================================================

if __name__ == "__main__":

    print("""
    ╔══════════════════════════════════════════════════════╗
    ║        G-one NLP 学院 - 第十六章 练习                  ║
    ║        关键词与摘要                                  ║
    ╚══════════════════════════════════════════════════════╝
    """)

    # 运行所有练习测试
    results = []
    results.append(("练习1: TF-IDF 关键词提取", test_exercise_1()))
    results.append(("练习2: TextRank 关键词提取", test_exercise_2()))
    results.append(("练习3: 抽取式文本摘要", test_exercise_3()))

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
        print("  你已经掌握了关键词提取和文本摘要技术。")
    else:
        print(f"\n  还有 {total - completed} 个练习未完成。")
        print("  不要着急，慢慢来，理解了再写代码。")
