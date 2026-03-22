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
import json
import hashlib
from pathlib import Path
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime

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


@dataclass
class UsageRecord:
    """使用记录"""
    timestamp: str
    session_id: str
    content_type: str
    strategy: str
    original_len: int
    compressed_len: int
    compression_ratio: float
    target_ratio: float
    iterations: int
    time_ms: float
    version: str = "3.5.0"


class UsageStats:
    """使用统计管理器"""
    
    def __init__(self, data_dir: str = "./usage_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.stats_file = self.data_dir / "usage_stats.jsonl"
        self.session_id = self._generate_session_id()
    
    def _generate_session_id(self) -> str:
        """生成会话ID"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def log_usage(self, record: UsageRecord):
        """记录使用情况"""
        record.session_id = self.session_id
        with open(self.stats_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(record), ensure_ascii=False) + '\n')
    
    def get_stats(self, days: int = 7) -> Dict:
        """获取统计摘要"""
        if not self.stats_file.exists():
            return {"error": "暂无使用数据"}
        
        records = []
        with open(self.stats_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    records.append(json.loads(line.strip()))
                except:
                    continue
        
        if not records:
            return {"error": "暂无使用数据"}
        
        # 计算统计
        total_uses = len(records)
        prompt_uses = sum(1 for r in records if r.get('content_type') == 'prompt')
        code_uses = sum(1 for r in records if r.get('content_type') == 'code')
        
        avg_ratio = sum(r.get('compression_ratio', 0) for r in records) / total_uses
        avg_time = sum(r.get('time_ms', 0) for r in records) / total_uses
        
        # 策略分布
        strategies = {}
        for r in records:
            s = r.get('strategy', 'unknown')
            strategies[s] = strategies.get(s, 0) + 1
        
        return {
            "total_uses": total_uses,
            "prompt_uses": prompt_uses,
            "code_uses": code_uses,
            "avg_compression_ratio": round(avg_ratio, 3),
            "avg_time_ms": round(avg_time, 2),
            "strategy_distribution": strategies,
            "data_file": str(self.stats_file)
        }
    
    def export_report(self, output_file: str = "usage_report.json"):
        """导出详细报告"""
        stats = self.get_stats()
        output_path = self.data_dir / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        return str(output_path)


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
        self.usage_stats = UsageStats()
        
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
        
        v35_result = V35Result(
            original=text,
            compressed=result['compressed'],
            strategy_used=result['strategy'],
            compression_ratio=result['ratio'],
            savings_percentage=result['ratio'] * 100,
            iterations=result.get('iterations', 1),
            time_ms=elapsed_ms
        )
        
        # 记录使用统计
        self._log_usage(v35_result, content_type, target_ratio)
        
        return v35_result
    
    def _log_usage(self, result: V35Result, content_type: str, target_ratio: float):
        """记录使用情况"""
        record = UsageRecord(
            timestamp=datetime.now().isoformat(),
            session_id="",
            content_type=content_type,
            strategy=result.strategy_used,
            original_len=len(result.original),
            compressed_len=len(result.compressed),
            compression_ratio=result.compression_ratio,
            target_ratio=target_ratio,
            iterations=result.iterations,
            time_ms=result.time_ms
        )
        self.usage_stats.log_usage(record)
    
    def get_usage_stats(self) -> Dict:
        """获取使用统计"""
        return self.usage_stats.get_stats()
    
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
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # compress 命令
    compress_parser = subparsers.add_parser('compress', help='压缩文本')
    compress_parser.add_argument('text', help='要压缩的文本')
    compress_parser.add_argument('--type', '-t', choices=['prompt', 'code', 'auto'],
                                default='auto', help='内容类型')
    compress_parser.add_argument('--target', '-r', type=float, default=0.80,
                                help='目标压缩率 (0-1)')
    compress_parser.add_argument('--smart', '-s', action='store_true',
                                help='使用智能模式 (自动选择策略)')
    
    # stats 命令
    stats_parser = subparsers.add_parser('stats', help='查看使用统计')
    stats_parser.add_argument('--export', '-e', help='导出报告到文件')
    
    args = parser.parse_args()
    
    if args.command == 'compress' or args.command is None:
        # 默认压缩模式
        text = args.text if hasattr(args, 'text') else args.text if args.command == 'compress' else None
        if text is None:
            parser.print_help()
            return
        
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
        print(f"  📈 已记录使用统计")
        
        print(f"\n📝 压缩后文本:")
        print(result.compressed)
    
    elif args.command == 'stats':
        # 统计模式
        master = TokenMasterV35()
        stats = master.get_usage_stats()
        
        print("=" * 60)
        print("📊 Token经济大师 v3.5.0 - 使用统计")
        print("=" * 60)
        
        if "error" in stats:
            print(f"\n{stats['error']}")
        else:
            print(f"\n📈 总体统计:")
            print(f"  总使用次数: {stats['total_uses']}")
            print(f"  提示词压缩: {stats['prompt_uses']} 次")
            print(f"  代码压缩: {stats['code_uses']} 次")
            print(f"  平均压缩率: {stats['avg_compression_ratio']*100:.1f}%")
            print(f"  平均耗时: {stats['avg_time_ms']:.2f}ms")
            
            print(f"\n📊 策略分布:")
            for strategy, count in stats['strategy_distribution'].items():
                print(f"  - {strategy}: {count} 次")
            
            print(f"\n💾 数据文件: {stats['data_file']}")
            
            if args.export:
                output = master.usage_stats.export_report(args.export)
                print(f"📄 报告已导出: {output}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
