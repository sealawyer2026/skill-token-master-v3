#!/usr/bin/env python3
"""
Multi-Round Compressor - 多轮迭代压缩器 v3.5.0
核心: 重复应用压缩规则直至收敛
"""

import re
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass

@dataclass
class IterationResult:
    """迭代结果"""
    iteration: int
    text: str
    compression_ratio: float
    converged: bool


class MultiRoundCompressor:
    """
    多轮迭代压缩器
    重复应用压缩规则，直到达到目标压缩率或收敛
    """
    
    def __init__(self, max_iterations: int = 10, convergence_threshold: float = 0.01):
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
        self.rules_engine = RulesEngine()
        
    def compress(self, text: str, target_ratio: float = 0.80,
                 compressor_func: Optional[Callable] = None) -> Tuple[str, List[IterationResult]]:
        """
        多轮迭代压缩
        
        Args:
            text: 输入文本
            target_ratio: 目标压缩率
            compressor_func: 外部压缩器函数 (可选)
            
        Returns:
            (最终文本, 迭代历史)
        """
        original_len = len(text)
        current_text = text
        history = []
        
        for i in range(1, self.max_iterations + 1):
            prev_len = len(current_text)
            
            # 应用压缩
            if compressor_func:
                current_text = compressor_func(current_text)
            else:
                current_text = self.rules_engine.apply_rules(current_text, iteration=i)
            
            current_len = len(current_text)
            ratio = (original_len - current_len) / original_len if original_len > 0 else 0
            
            # 检查收敛
            change_ratio = (prev_len - current_len) / prev_len if prev_len > 0 else 0
            converged = change_ratio < self.convergence_threshold
            
            result = IterationResult(
                iteration=i,
                text=current_text,
                compression_ratio=ratio,
                converged=converged
            )
            history.append(result)
            
            # 达到目标或收敛
            if ratio >= target_ratio or converged:
                break
        
        return current_text, history
    
    def compress_with_adaptive_rules(self, text: str, target_ratio: float = 0.80) -> Tuple[str, Dict]:
        """
        使用自适应规则的多轮压缩
        
        每轮根据当前状态动态调整规则权重
        """
        original_len = len(text)
        current_text = text
        iteration_stats = []
        
        for i in range(1, self.max_iterations + 1):
            prev_len = len(current_text)
            
            # 根据迭代轮次选择规则集
            rules = self.rules_engine.get_rules_for_iteration(i)
            
            # 应用规则
            current_text = self._apply_rule_set(current_text, rules)
            
            current_len = len(current_text)
            ratio = (original_len - current_len) / original_len
            change = prev_len - current_len
            
            iteration_stats.append({
                'iteration': i,
                'before_len': prev_len,
                'after_len': current_len,
                'change': change,
                'total_ratio': ratio,
                'rules_applied': len(rules)
            })
            
            # 检查是否收敛
            if change == 0 or ratio >= target_ratio:
                break
        
        stats = {
            'iterations': len(iteration_stats),
            'original_len': original_len,
            'final_len': len(current_text),
            'total_savings': original_len - len(current_text),
            'final_ratio': (original_len - len(current_text)) / original_len,
            'iteration_details': iteration_stats
        }
        
        return current_text, stats
    
    def _apply_rule_set(self, text: str, rules: List[Tuple[str, str]]) -> str:
        """应用规则集"""
        result = text
        for pattern, replacement in rules:
            result = result.replace(pattern, replacement)
        return result
    
    def get_stats(self, original: str, history: List[IterationResult]) -> Dict:
        """获取压缩统计"""
        if not history:
            return {}
        
        final = history[-1]
        
        return {
            'total_iterations': len(history),
            'original_len': len(original),
            'final_len': len(final.text),
            'total_savings': len(original) - len(final.text),
            'final_ratio': final.compression_ratio,
            'converged': final.converged,
            'iteration_progress': [
                {'round': r.iteration, 'ratio': r.compression_ratio}
                for r in history
            ]
        }


class RulesEngine:
    """规则引擎 - 管理不同迭代轮次的规则集"""
    
    def __init__(self):
        self.rules_db = self._build_rules_database()
    
    def _build_rules_database(self) -> Dict[int, List[Tuple[str, str]]]:
        """构建规则数据库"""
        return {
            # 第1轮: 基础压缩
            1: [
                ('请帮我', ''), ('帮我', ''), ('给我', ''), ('为我', ''),
                ('我需要', '需'), ('我想要', '要'), ('我希望', '望'),
                ('以及', ''), ('还有', ''), ('另外', ''), ('此外', ''),
                ('而且', ''), ('并且', ''), ('同时', ''), ('然后', ''),
                ('接着', ''), ('随后', ''), ('之后', ''), ('之前', ''),
                ('首先', ''), ('最后', ''), ('最终', ''), ('总之', ''),
                ('所以', ''), ('因此', ''), ('因而', ''), ('于是', ''),
                ('从而', ''), ('因为', ''), ('由于', ''), ('鉴于', ''),
                ('虽然', ''), ('尽管', ''), ('即使', ''), ('但是', ''),
                ('然而', ''), ('不过', ''), ('可是', ''), ('只是', ''),
            ],
            # 第2轮: 动词简化
            2: [
                ('进行', ''), ('予以', ''), ('加以', ''), ('给予', ''),
                ('提供', '供'), ('使', ''), ('让', ''), ('令', ''),
                ('促使', ''), ('导致', ''), ('引起', ''), ('造成', ''),
                ('分析', '析'), ('处理', '处'), ('检查', '检'), ('整理', '理'),
                ('查询', '询'), ('搜索', '搜'), ('获取', '取'), ('创建', '建'),
                ('删除', '删'), ('更新', '更'), ('修改', '改'), ('添加', '加'),
                ('插入', '插'), ('替换', '换'), ('转换', '转'), ('计算', '算'),
                ('验证', '验'), ('确认', '认'), ('执行', '行'), ('运行', '运'),
                ('调用', '调'), ('返回', '返'), ('输出', '出'), ('输入', '入'),
                ('导入', '导'), ('加载', '载'), ('保存', '存'), ('读取', '读'),
                ('写入', '写'), ('解析', '解'), ('生成', '生'), ('构建', '构'),
            ],
            # 第3轮: 名词压缩
            3: [
                ('用户', '户'), ('数据', '据'), ('信息', '息'), ('结果', '果'),
                ('内容', '容'), ('文本', '文'), ('文件', '档'), ('目录', '录'),
                ('路径', '径'), ('地址', '址'), ('名称', '名'), ('标题', '题'),
                ('描述', '述'), ('说明', '明'), ('详情', '详'), ('摘要', '摘'),
                ('概要', '概'), ('总结', '总'), ('列表', '表'), ('集合', '集'),
                ('数组', '组'), ('对象', '象'), ('实例', '例'), ('变量', '量'),
                ('参数', '参'), ('属性', '性'), ('方法', '法'), ('函数', '函'),
                ('类名', '类'), ('模块', '模'), ('组件', '件'), ('元素', '元'),
                ('节点', '点'), ('标签', '签'), ('样式', '样'), ('布局', '布'),
                ('界面', '面'), ('页面', '页'), ('窗口', '口'), ('按钮', '钮'),
                ('链接', '链'), ('图片', '图'), ('图标', '标'), ('颜色', '色'),
                ('字体', '字'), ('尺寸', '寸'), ('大小', '寸'), ('宽度', '宽'),
                ('高度', '高'), ('长度', '长'), ('距离', '距'), ('位置', '位'),
                ('坐标', '坐'), ('区域', '区'), ('范围', '围'), ('边界', '边'),
            ],
            # 第4轮: 标点压缩
            4: [
                ('，', '、'), ('。', ''), ('！', ''), ('？', ''), ('：', ''),
                ('；', '、'), ('"', ''), ('"', ''), ('「', ''), ('」', ''),
                ('『', ''), ('』', ''), ('（', '('), ('）', ')'), ('【', '['),
                ('】', ']'), ('《', '<'), ('》', '>'), ('……', '…'), ('——', '-'),
            ],
            # 第5轮: 激进压缩
            5: [
                ('的', ''), ('了', ''), ('着', ''), ('过', ''),
                ('是', ''), ('有', ''), ('在', ''), ('和', ''),
                ('与', ''), ('或', ''), ('及', ''), ('对', ''),
                ('为', ''), ('将', ''), ('把', ''), ('被', ''),
            ],
            # 第6轮+: 清理空格
            6: [(' ', ''), ('\t', ''), ('\n', '')],
            7: [('  ', ''), ('   ', '')],
            8: [],  # 动态规则轮
            9: [],
            10: [],
        }
    
    def apply_rules(self, text: str, iteration: int = 1) -> str:
        """应用指定轮次的规则"""
        result = text
        
        # 应用当前轮次及之前的所有规则
        for i in range(1, min(iteration + 1, max(self.rules_db.keys()) + 1)):
            rules = self.rules_db.get(i, [])
            for pattern, replacement in rules:
                result = result.replace(pattern, replacement)
        
        return result
    
    def get_rules_for_iteration(self, iteration: int) -> List[Tuple[str, str]]:
        """获取指定轮次的规则"""
        # 如果超过预定义轮次，返回第6轮的清理规则
        if iteration > max(self.rules_db.keys()):
            return self.rules_db.get(6, [])
        return self.rules_db.get(iteration, [])


# 便捷函数
def multi_round_compress(text: str, target_ratio: float = 0.80,
                         max_iterations: int = 10) -> Tuple[str, Dict]:
    """多轮压缩便捷函数"""
    compressor = MultiRoundCompressor(max_iterations=max_iterations)
    compressed, stats = compressor.compress_with_adaptive_rules(text, target_ratio)
    return compressed, stats


if __name__ == '__main__':
    # 测试
    test_text = """请帮我详细地分析一下这个复杂的数据处理任务，需要对用户提供的信息进行全面的检查和验证，然后根据分析结果生成相应的报告。"""
    
    compressor = MultiRoundCompressor(max_iterations=5)
    result, history = compressor.compress(test_text, target_ratio=0.80)
    stats = compressor.get_stats(test_text, history)
    
    print(f"原文 ({len(test_text)} 字符): {test_text}")
    print(f"\n压缩后 ({len(result)} 字符): {result}")
    print(f"\n统计: {stats}")
