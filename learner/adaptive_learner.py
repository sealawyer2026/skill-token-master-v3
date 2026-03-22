#!/usr/bin/env python3
"""
Adaptive Learning System - 自适应学习系统 v3.5.0
核心: 根据输入类型自动选择最优策略 + 用户反馈驱动优化
"""

import json
import hashlib
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict
from collections import defaultdict
from datetime import datetime
from pathlib import Path

@dataclass
class InputProfile:
    """输入特征画像"""
    input_type: str  # 'prompt', 'code', 'mixed'
    domain: str  # 'general', 'tech', 'legal', 'medical'
    complexity: float  # 0-1 复杂度
    length_category: str  # 'short', 'medium', 'long'
    key_features: List[str] = field(default_factory=list)

@dataclass
class StrategyResult:
    """策略执行结果"""
    strategy_name: str
    compression_ratio: float
    quality_score: float  # 语义保留度
    execution_time: float
    success: bool = True

@dataclass
class LearningRecord:
    """学习记录"""
    input_hash: str
    input_profile: InputProfile
    selected_strategy: str
    result: StrategyResult
    user_feedback: Optional[float] = None  # 用户评分 0-1
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class AdaptiveLearner:
    """
    自适应学习引擎
    根据输入特征自动选择最优压缩策略
    """
    
    def __init__(self, data_dir: str = "./learning_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # 学习数据
        self.records: List[LearningRecord] = []
        self.strategy_performance: Dict[str, Dict] = defaultdict(lambda: {
            'total_uses': 0,
            'avg_compression': 0.0,
            'avg_quality': 0.0,
            'success_rate': 1.0
        })
        
        # 策略选择器
        self.strategy_selector = StrategySelector()
        
        # 反馈处理器
        self.feedback_processor = FeedbackProcessor()
        
        # 加载历史数据
        self._load_learning_data()
    
    def select_strategy(self, text: str, target_ratio: float) -> Tuple[str, Dict]:
        """
        为输入选择最优策略
        
        Returns:
            (策略名称, 策略参数)
        """
        # 1. 分析输入特征
        profile = self._analyze_input(text)
        
        # 2. 查找相似历史记录
        similar_records = self._find_similar_records(profile)
        
        # 3. 基于历史表现选择策略
        if similar_records:
            best_strategy = self._select_based_on_history(similar_records, target_ratio)
        else:
            # 没有历史记录，使用启发式选择
            best_strategy = self._heuristic_select(profile, target_ratio)
        
        # 4. 生成策略参数
        params = self._generate_params(best_strategy, profile, target_ratio)
        
        return best_strategy, params
    
    def record_result(self, text: str, strategy: str, result: StrategyResult):
        """记录执行结果"""
        input_hash = self._hash_input(text)
        profile = self._analyze_input(text)
        
        record = LearningRecord(
            input_hash=input_hash,
            input_profile=profile,
            selected_strategy=strategy,
            result=result
        )
        
        self.records.append(record)
        self._update_strategy_performance(strategy, result)
        self._save_learning_data()
    
    def add_feedback(self, input_hash: str, feedback: float):
        """添加用户反馈"""
        for record in self.records:
            if record.input_hash == input_hash:
                record.user_feedback = feedback
                
                # 基于反馈调整策略权重
                self.feedback_processor.process(record)
                break
        
        self._save_learning_data()
    
    def _analyze_input(self, text: str) -> InputProfile:
        """分析输入特征"""
        length = len(text)
        
        # 长度分类
        if length < 100:
            length_cat = 'short'
        elif length < 500:
            length_cat = 'medium'
        else:
            length_cat = 'long'
        
        # 类型检测
        code_indicators = ['def ', 'class ', 'import ', 'return ', '{', '}', 'var ', 'const ', 'function']
        prompt_indicators = ['请', '帮我', '需要', '分析', '处理', '生成']
        
        code_score = sum(1 for ind in code_indicators if ind in text)
        prompt_score = sum(1 for ind in prompt_indicators if ind in text)
        
        if code_score > prompt_score and code_score > 2:
            input_type = 'code'
        elif prompt_score > 0:
            input_type = 'prompt'
        else:
            input_type = 'mixed'
        
        # 领域检测
        domain = self._detect_domain(text)
        
        # 复杂度计算
        complexity = self._calculate_complexity(text)
        
        # 关键特征提取
        features = self._extract_features(text)
        
        return InputProfile(
            input_type=input_type,
            domain=domain,
            complexity=complexity,
            length_category=length_cat,
            key_features=features
        )
    
    def _detect_domain(self, text: str) -> str:
        """检测领域"""
        domain_keywords = {
            'tech': {'代码', '函数', 'API', '数据库', '服务器', '编程', 'Python', 'Java', 'JavaScript',
                    '系统', '算法', '数据结构', '接口', '框架', '库', '模块', '类', '方法'},
            'legal': {'合同', '法律', '条款', '协议', '诉讼', '法院', '律师', '当事人', '证据',
                     '判决', '裁定', '仲裁', '调解', '赔偿', '违约', '侵权', '知识产权'},
            'medical': {'疾病', '症状', '治疗', '药物', '医院', '医生', '诊断', '处方',
                       '手术', '检查', '化验', '病历', '患者', '病情', '康复'},
            'business': {'公司', '企业', '市场', '营销', '销售', '客户', '产品', '服务',
                        '战略', '运营', '管理', '财务', '投资', '盈利', '成本', '收入'},
            'academic': {'研究', '论文', '理论', '实验', '数据', '分析', '结论', '文献',
                        '方法', '模型', '假设', '验证', '学术', '期刊', '引用'}
        }
        
        scores = {domain: sum(1 for kw in keywords if kw in text) 
                  for domain, keywords in domain_keywords.items()}
        
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        return 'general'
    
    def _calculate_complexity(self, text: str) -> float:
        """计算复杂度"""
        # 基于多种指标
        length_factor = min(len(text) / 1000, 1.0)
        
        # 句子数量
        sentences = len([s for s in text.split('。') if s.strip()])
        sentence_factor = min(sentences / 20, 1.0)
        
        # 专业术语密度
        technical_terms = len(re.findall(r'[A-Za-z]+|[\u4e00-\u9fa5]{2,}', text))
        term_factor = min(technical_terms / 50, 1.0)
        
        # 嵌套层级 (括号深度)
        max_depth = 0
        current_depth = 0
        for char in text:
            if char in '([{《（【':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char in ')]}》）】':
                current_depth = max(0, current_depth - 1)
        
        depth_factor = min(max_depth / 5, 1.0)
        
        return (length_factor + sentence_factor + term_factor + depth_factor) / 4
    
    def _extract_features(self, text: str) -> List[str]:
        """提取关键特征"""
        features = []
        
        # 提取关键词 (简单实现)
        words = text.split()
        for word in words:
            if len(word) >= 2 and word not in ['的', '了', '在', '是', '有', '和', '与', '或']:
                features.append(word)
        
        return features[:10]  # 限制特征数量
    
    def _find_similar_records(self, profile: InputProfile) -> List[LearningRecord]:
        """查找相似历史记录"""
        similar = []
        
        for record in self.records:
            score = self._calculate_similarity(profile, record.input_profile)
            if score > 0.7:  # 相似度阈值
                similar.append((record, score))
        
        # 按相似度排序
        similar.sort(key=lambda x: x[1], reverse=True)
        return [r for r, s in similar[:10]]  # 取前10个
    
    def _calculate_similarity(self, p1: InputProfile, p2: InputProfile) -> float:
        """计算输入画像相似度"""
        score = 0.0
        
        # 类型相同
        if p1.input_type == p2.input_type:
            score += 0.3
        
        # 领域相同
        if p1.domain == p2.domain:
            score += 0.3
        
        # 长度类别相同
        if p1.length_category == p2.length_category:
            score += 0.2
        
        # 复杂度接近
        complexity_diff = abs(p1.complexity - p2.complexity)
        score += 0.2 * (1 - complexity_diff)
        
        return score
    
    def _select_based_on_history(self, records: List[LearningRecord], target_ratio: float) -> str:
        """基于历史表现选择策略"""
        # 统计各策略表现
        strategy_scores = defaultdict(lambda: {'total_score': 0, 'count': 0})
        
        for record in records:
            strategy = record.selected_strategy
            result = record.result
            
            # 计算综合得分
            score = (result.compression_ratio * 0.4 + 
                    result.quality_score * 0.4 +
                    (1 if result.success else 0) * 0.2)
            
            if record.user_feedback:
                score = score * 0.7 + record.user_feedback * 0.3
            
            strategy_scores[strategy]['total_score'] += score
            strategy_scores[strategy]['count'] += 1
        
        # 选择平均得分最高的策略
        best_strategy = max(strategy_scores.keys(),
                           key=lambda s: strategy_scores[s]['total_score'] / strategy_scores[s]['count'])
        
        return best_strategy
    
    def _heuristic_select(self, profile: InputProfile, target_ratio: float) -> str:
        """启发式策略选择"""
        # 基于规则的选择逻辑
        if profile.input_type == 'code':
            if target_ratio >= 0.85:
                return 'code_restructurer_aggressive'
            else:
                return 'code_restructurer'
        elif profile.input_type == 'prompt':
            if target_ratio >= 0.80:
                return 'neural_compressor_extreme'
            elif profile.length_category == 'long':
                return 'neural_compressor_multi_round'
            else:
                return 'neural_compressor'
        else:
            return 'semantic_compressor'
    
    def _generate_params(self, strategy: str, profile: InputProfile, target_ratio: float) -> Dict:
        """生成策略参数"""
        params = {
            'target_ratio': target_ratio,
            'domain': profile.domain
        }
        
        if 'neural' in strategy:
            params['max_iterations'] = 5 if 'multi_round' in strategy else 3
            params['aggressive'] = 'extreme' in strategy
        
        if 'code' in strategy:
            params['aggressive'] = 'aggressive' in strategy
            params['inline_threshold'] = 30 if 'aggressive' in strategy else 50
        
        return params
    
    def _update_strategy_performance(self, strategy: str, result: StrategyResult):
        """更新策略表现统计"""
        stats = self.strategy_performance[strategy]
        
        # 更新平均值
        n = stats['total_uses']
        stats['avg_compression'] = (stats['avg_compression'] * n + result.compression_ratio) / (n + 1)
        stats['avg_quality'] = (stats['avg_quality'] * n + result.quality_score) / (n + 1)
        stats['success_rate'] = (stats['success_rate'] * n + (1 if result.success else 0)) / (n + 1)
        stats['total_uses'] = n + 1
    
    def _hash_input(self, text: str) -> str:
        """生成输入哈希"""
        return hashlib.md5(text.encode()).hexdigest()[:16]
    
    def _load_learning_data(self):
        """加载学习数据"""
        data_file = self.data_dir / 'learning_records.json'
        if data_file.exists():
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.records = [LearningRecord(**r) for r in data.get('records', [])]
                    self.strategy_performance = defaultdict(lambda: {
                        'total_uses': 0,
                        'avg_compression': 0.0,
                        'avg_quality': 0.0,
                        'success_rate': 1.0
                    })
                    self.strategy_performance.update(data.get('performance', {}))
            except Exception as e:
                print(f"加载学习数据失败: {e}")
    
    def _save_learning_data(self):
        """保存学习数据"""
        data_file = self.data_dir / 'learning_records.json'
        try:
            data = {
                'records': [asdict(r) for r in self.records[-1000:]],  # 只保留最近1000条
                'performance': dict(self.strategy_performance),
                'last_updated': datetime.now().isoformat()
            }
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存学习数据失败: {e}")
    
    def get_learning_report(self) -> Dict:
        """获取学习报告"""
        return {
            'total_records': len(self.records),
            'strategy_performance': dict(self.strategy_performance),
            'domain_distribution': self._get_domain_distribution(),
            'type_distribution': self._get_type_distribution()
        }
    
    def _get_domain_distribution(self) -> Dict[str, int]:
        """获取领域分布"""
        dist = defaultdict(int)
        for record in self.records:
            dist[record.input_profile.domain] += 1
        return dict(dist)
    
    def _get_type_distribution(self) -> Dict[str, int]:
        """获取类型分布"""
        dist = defaultdict(int)
        for record in self.records:
            dist[record.input_profile.input_type] += 1
        return dict(dist)


class StrategySelector:
    """策略选择器"""
    
    def __init__(self):
        self.available_strategies = {
            'neural_compressor': '神经网络语义压缩',
            'neural_compressor_multi_round': '神经网络多轮压缩',
            'neural_compressor_extreme': '神经网络极致压缩',
            'code_restructurer': '代码结构重组',
            'code_restructurer_aggressive': '代码激进重组',
            'semantic_compressor': '语义压缩器'
        }


class FeedbackProcessor:
    """反馈处理器"""
    
    def process(self, record: LearningRecord):
        """处理用户反馈"""
        if record.user_feedback is None:
            return
        
        # 基于反馈调整
        feedback = record.user_feedback
        
        if feedback < 0.5:
            # 负面反馈: 降低该策略在该类输入上的权重
            print(f"收到负面反馈，调整策略 {record.selected_strategy} 权重")
        elif feedback > 0.8:
            # 正面反馈: 提升权重并记录为最佳实践
            print(f"收到正面反馈，策略 {record.selected_strategy} 表现优秀")


# 便捷函数
def select_best_strategy(text: str, target_ratio: float = 0.80) -> Tuple[str, Dict]:
    """选择最佳策略便捷函数"""
    learner = AdaptiveLearner()
    return learner.select_strategy(text, target_ratio)


if __name__ == '__main__':
    import re
    
    # 测试
    learner = AdaptiveLearner()
    
    test_inputs = [
        "请帮我分析数据处理任务",
        "def calculate(x, y): return x + y",
        "根据合同条款，当事人应当履行义务",
    ]
    
    for text in test_inputs:
        profile = learner._analyze_input(text)
        strategy, params = learner.select_strategy(text, 0.80)
        print(f"\n输入: {text[:30]}...")
        print(f"  类型: {profile.input_type}, 领域: {profile.domain}")
        print(f"  选择策略: {strategy}")
        print(f"  参数: {params}")
