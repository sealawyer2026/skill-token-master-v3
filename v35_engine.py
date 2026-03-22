#!/usr/bin/env python3
"""
Token经济大师 v3.5.0 - 超级压缩引擎
核心: 四大策略集成 + 目标突破 80%/85%

四大策略:
1. 神经网络语义压缩 (提示词 80%+)
2. 代码结构重组优化 (代码 85%+)
3. 自适应学习系统 (智能策略选择)
4. 多轮迭代压缩 (持续优化直至收敛)
"""

import sys
from pathlib import Path
from typing import Dict, Tuple, Optional
from dataclasses import dataclass

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from optimizer.neural_compressor import NeuralCompressor, compress_with_stats as neural_compress
from optimizer.code_restructurer import CodeRestructurer, optimize_with_stats as code_optimize
from optimizer.multi_round_compressor import MultiRoundCompressor, multi_round_compress
from learner.adaptive_learner import AdaptiveLearner, select_best_strategy


@dataclass
class V35Result:
    """v3.5.0 压缩结果"""
    original: str
    compressed: str
    strategy_used: str
    compression_ratio: float
    savings_percentage: float
    iterations: int
    time_ms: float


class TokenMasterV35:
    """
    Token经济大师 v3.5.0
    超级压缩引擎
    """
    
    def __init__(self):
        self.neural = NeuralCompressor()
        self.code = CodeRestructurer()
        self.multi_round = MultiRoundCompressor()
        self.learner = AdaptiveLearner()
        
    def compress(self, text: str, content_type: Optional[str] = None,
                 target_ratio: float = 0.80) -> V35Result:
        """
        智能压缩主入口
        
        Args:
            text: 输入文本
            content_type: 内容类型 ('prompt', 'code', 'auto')
            target_ratio: 目标压缩率
            
        Returns:
            压缩结果
        """
        import time
        start_time = time.time()
        
        # 自动检测内容类型
        if content_type is None or content_type == 'auto':
            content_type = self._detect_content_type(text)
        
        # 根据内容类型选择策略
        if content_type == 'code':
            result = self._compress_code(text, target_ratio)
        else:
            result = self._compress_prompt(text, target_ratio)
        
        elapsed_ms = (time.time() - start_time) * 1000
        
        return V35Result(
            original=text,
            compressed=result['compressed'],
            strategy_used=result['strategy'],
            compression_ratio=result['ratio'],
            savings_percentage=result['ratio'] * 100,
            iterations=result.get('iterations', 1),
            time_ms=elapsed_ms
        )
    
    def _detect_content_type(self, text: str) -> str:
        """检测内容类型"""
        code_indicators = ['def ', 'class ', 'import ', 'return ', 'function', 'var ', 'const ']
        code_score = sum(1 for ind in code_indicators if ind in text)
        
        if code_score >= 2:
            return 'code'
        return 'prompt'
    
    def _compress_prompt(self, text: str, target_ratio: float) -> Dict:
        """压缩提示词"""
        original_len = len(text)
        
        # 策略1: 神经网络压缩
        compressed = self.neural.compress(text, target_ratio=target_ratio)
        
        # 策略4: 多轮迭代优化
        if target_ratio >= 0.80:
            compressed, stats = self.multi_round.compress_with_adaptive_rules(
                compressed, target_ratio=target_ratio
            )
            iterations = stats['iterations']
        else:
            iterations = 1
        
        final_len = len(compressed)
        ratio = (original_len - final_len) / original_len if original_len > 0 else 0
        
        return {
            'compressed': compressed,
            'strategy': 'neural_multi_round',
            'ratio': ratio,
            'iterations': iterations
        }
    
    def _compress_code(self, text: str, target_ratio: float) -> Dict:
        """压缩代码"""
        # 策略2: 代码结构重组
        result = self.code.optimize(text, aggressive=(target_ratio >= 0.85))
        
        return {
            'compressed': result.code,
            'strategy': 'code_restructure_aggressive' if target_ratio >= 0.85 else 'code_restructure',
            'ratio': result.ratio,
            'iterations': 1
        }
    
    def smart_compress(self, text: str) -> V35Result:
        """
        智能压缩 - 自动选择最优策略
        
        策略3: 自适应学习系统选择最佳策略
        """
        # 使用自适应学习器选择策略
        strategy, params = self.learner.select_strategy(text, target_ratio=0.80)
        
        # 根据选择的策略执行
        content_type = 'code' if 'code' in strategy else 'prompt'
        target = params.get('target_ratio', 0.80)
        
        return self.compress(text, content_type=content_type, target_ratio=target)


# 便捷函数
def compress(text: str, content_type: Optional[str] = None,
             target_ratio: float = 0.80) -> str:
    """便捷压缩函数"""
    master = TokenMasterV35()
    result = master.compress(text, content_type, target_ratio)
    return result.compressed


def compress_with_stats(text: str, content_type: Optional[str] = None,
                        target_ratio: float = 0.80) -> V35Result:
    """压缩并返回完整统计"""
    master = TokenMasterV35()
    return master.compress(text, content_type, target_ratio)


def smart_compress(text: str) -> V35Result:
    """智能压缩 (自动选择策略)"""
    master = TokenMasterV35()
    return master.smart_compress(text)


# CLI 入口
def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Token经济大师 v3.5.0 - 超级压缩引擎'
    )
    
    parser.add_argument('text', help='要压缩的文本')
    parser.add_argument('--type', '-t', choices=['prompt', 'code', 'auto'],
                       default='auto', help='内容类型')
    parser.add_argument('--target', '-r', type=float, default=0.80,
                       help='目标压缩率 (0-1)')
    parser.add_argument('--smart', '-s', action='store_true',
                       help='使用智能模式 (自动选择策略)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🚀 Token经济大师 v3.5.0 - 超级压缩引擎")
    print("=" * 60)
    
    master = TokenMasterV35()
    
    if args.smart:
        result = master.smart_compress(args.text)
    else:
        result = master.compress(args.text, args.type, args.target)
    
    print(f"\n📊 压缩结果:")
    print(f"  原始长度: {len(result.original)} 字符")
    print(f"  压缩后: {len(result.compressed)} 字符")
    print(f"  节省: {result.savings_percentage:.1f}%")
    print(f"  使用策略: {result.strategy_used}")
    print(f"  迭代次数: {result.iterations}")
    print(f"  耗时: {result.time_ms:.2f}ms")
    
    print(f"\n📝 压缩后文本:")
    print(result.compressed)


if __name__ == '__main__':
    main()
