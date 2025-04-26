def rerank_results(results: List[Dict], quality_weights: Dict, feedback_data: Dict) -> List[Dict]:
    """
    :param results: 原始检索结果
    :param quality_weights: 内容质量权重（如权威性、长度）
    :param feedback_data: 用户反馈数据（点击率、评分）
    """
    for doc in results:
        # 内容质量得分（示例逻辑）
        quality_score = (
                np.log(len(doc['text'])) * quality_weights.get('length', 0.3) +
                doc.get('authority_score', 1.0) * quality_weights.get('authority', 0.7)
        )

        # 用户反馈得分（需对接实际数据源）
        feedback_score = (
                0.6 * feedback_data.get(doc['doc_id'], {}).get('click_rate', 0) +
                0.4 * feedback_data.get(doc['doc_id'], {}).get('user_rating', 0)
        )

        # 总分 = 原始相关性 * 0.6 + 质量 * 0.3 + 反馈 * 0.1
        doc['final_score'] = (
                0.6 * doc['score'] +
                0.3 * quality_score +
                0.1 * feedback_score
        )

    return sorted(results, key=lambda x: x['final_score'], reverse=True)