#!/usr/bin/env python3
"""
Token经济大师 v3.0 - 命令行入口

用法:
    python3 -m token_economy_master_v3 analyze <path>     # 分析
    python3 -m token_economy_master_v3 optimize <path>    # 优化
    python3 -m token_economy_master_v3 monitor <path>     # 监控
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from analyzer.unified_analyzer import TokenAnalyzer
from optimizer.smart_optimizer import SmartOptimizer
from learner.evolution_engine import EvolutionEngine
from monitor.intelligent_monitor import IntelligentMonitor

def analyze_command(args):
    """分析命令"""
    print(f"🔍 分析: {args.path}")
    
    path = Path(args.path)
    if not path.exists():
        print(f"❌ 路径不存在: {args.path}")
        return 1
    
    analyzer = TokenAnalyzer()
    
    if path.is_file():
        content = path.read_text(encoding='utf-8')
        result = analyzer.analyze(content)
        
        print(f"\n📊 分析结果:")
        print(f"  类型: {result['content_type']}")
        print(f"  字符数: {result['total_chars']}")
        print(f"  预估Token: {result['estimated_tokens']}")
        print(f"  问题数: {result.get('issue_count', 0)}")
        print(f"  优化潜力: {result.get('optimization_potential', 0)}%")
    else:
        # 分析目录
        total_files = 0
        total_tokens = 0
        
        for ext in ['*.py', '*.md', '*.json']:
            for file_path in path.rglob(ext):
                try:
                    content = file_path.read_text(encoding='utf-8')
                    result = analyzer.analyze(content)
                    total_files += 1
                    total_tokens += result['estimated_tokens']
                except Exception as e:
                    print(f"  ⚠️ 无法读取: {file_path} ({e})")
        
        print(f"\n📊 项目分析:")
        print(f"  文件数: {total_files}")
        print(f"  总Token: {total_tokens}")
    
    return 0

def optimize_command(args):
    """优化命令"""
    print(f"⚡ 优化: {args.path}")
    
    path = Path(args.path)
    if not path.exists():
        print(f"❌ 路径不存在: {args.path}")
        return 1
    
    optimizer = SmartOptimizer()
    learner = EvolutionEngine()
    
    if path.is_file():
        content = path.read_text(encoding='utf-8')
        result = optimizer.optimize(content)
        
        print(f"\n📊 优化结果:")
        print(f"  原Token: {result['original_tokens']}")
        print(f"  优化后: {result['optimized_tokens']}")
        print(f"  节省: {result['saving']} ({result['saving_percentage']}%)")
        
        # 记录学习
        learner.record_optimization(
            result['original'],
            result['optimized'],
            result['saving_percentage'],
            result['content_type']
        )
        
        # 保存优化结果
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(result['optimized'], encoding='utf-8')
            print(f"\n💾 已保存到: {output_path}")
    else:
        print("📁 目录优化模式（批量处理）")
        # 批量优化逻辑
    
    # 显示学习报告
    report = learner.get_learning_report()
    if report['status'] == 'active':
        print(f"\n🧠 学习进度: {report['total_usage']}/100 (下次进化还需{report['next_evolution_in']}次)")
    
    return 0

def monitor_command(args):
    """监控命令"""
    print(f"👁️ 监控: {args.path}")
    
    monitor = IntelligentMonitor(args.path)
    monitor.watch(interval=args.interval)
    
    return 0

def main():
    parser = argparse.ArgumentParser(
        description='Token经济大师 v3.0 - Token使用量优化工具'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # analyze 命令
    analyze_parser = subparsers.add_parser('analyze', help='分析Token使用情况')
    analyze_parser.add_argument('path', help='文件或目录路径')
    
    # optimize 命令
    optimize_parser = subparsers.add_parser('optimize', help='执行Token优化')
    optimize_parser.add_argument('path', help='文件或目录路径')
    optimize_parser.add_argument('--output', '-o', help='输出文件路径')
    
    # monitor 命令
    monitor_parser = subparsers.add_parser('monitor', help='实时监控Token变化')
    monitor_parser.add_argument('path', help='项目目录路径')
    monitor_parser.add_argument('--interval', '-i', type=int, default=60,
                               help='检查间隔(秒)，默认60')
    
    args = parser.parse_args()
    
    if args.command == 'analyze':
        return analyze_command(args)
    elif args.command == 'optimize':
        return optimize_command(args)
    elif args.command == 'monitor':
        return monitor_command(args)
    else:
        parser.print_help()
        return 1

if __name__ == '__main__':
    sys.exit(main())
