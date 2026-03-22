#!/usr/bin/env python3
"""
Token经济大师 CLI - v3.5.0
命令行工具入口
"""

import sys
import os
import argparse
import json
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from optimizer.smart_optimizer import SmartOptimizer
from optimizer.extreme_compressor import ExtremeCompressor
from analyzer.unified_analyzer import TokenAnalyzer
from billing import UsageTracker

class TokenMasterCLI:
    """Token经济大师 CLI"""
    
    def __init__(self):
        self.optimizer = SmartOptimizer()
        self.analyzer = TokenAnalyzer()
        self.tracker = UsageTracker()
    
    def main(self):
        """主入口"""
        parser = argparse.ArgumentParser(
            prog='token-master',
            description='Token经济大师 - 智能Token优化工具 v3.3.0',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''
示例:
  token-master optimize file.py              # 优化单个文件
  token-master optimize ./src --recursive    # 递归优化目录
  token-master analyze file.txt              # 分析Token使用
  token-master batch ./project               # 批量优化项目
  token-master stats                         # 查看使用统计
            '''
        )
        
        parser.add_argument('--version', action='version', version='%(prog)s 3.5.0')
        
        subparsers = parser.add_subparsers(dest='command', help='可用命令')
        
        # optimize 命令
        optimize_parser = subparsers.add_parser('optimize', help='优化文件或目录')
        optimize_parser.add_argument('path', help='文件或目录路径')
        optimize_parser.add_argument('-r', '--recursive', action='store_true', help='递归处理目录')
        optimize_parser.add_argument('-e', '--extreme', action='store_true', help='使用极致压缩')
        optimize_parser.add_argument('-o', '--output', help='输出路径')
        optimize_parser.add_argument('-f', '--format', choices=['text', 'json'], default='text', help='输出格式')
        optimize_parser.add_argument('--dry-run', action='store_true', help='试运行，不写入文件')
        
        # analyze 命令
        analyze_parser = subparsers.add_parser('analyze', help='分析Token使用情况')
        analyze_parser.add_argument('path', help='文件路径')
        analyze_parser.add_argument('-f', '--format', choices=['text', 'json'], default='text', help='输出格式')
        
        # batch 命令
        batch_parser = subparsers.add_parser('batch', help='批量优化项目')
        batch_parser.add_argument('path', help='项目目录')
        batch_parser.add_argument('--include', default='*.py,*.js,*.md', help='包含的文件类型')
        batch_parser.add_argument('--exclude', default='node_modules,venv,__pycache__', help='排除的目录')
        batch_parser.add_argument('-o', '--output', help='输出报告路径')
        
        # stats 命令
        stats_parser = subparsers.add_parser('stats', help='查看使用统计')
        stats_parser.add_argument('-d', '--days', type=int, default=30, help='统计天数')
        
        # config 命令
        config_parser = subparsers.add_parser('config', help='配置管理')
        config_parser.add_argument('--init', action='store_true', help='初始化配置文件')
        config_parser.add_argument('--show', action='store_true', help='显示当前配置')
        
        args = parser.parse_args()
        
        if not args.command:
            parser.print_help()
            return 0
        
        # 执行命令
        commands = {
            'optimize': self.cmd_optimize,
            'analyze': self.cmd_analyze,
            'batch': self.cmd_batch,
            'stats': self.cmd_stats,
            'config': self.cmd_config,
        }
        
        return commands[args.command](args)
    
    def cmd_optimize(self, args):
        """优化命令"""
        path = Path(args.path)
        
        if path.is_file():
            return self._optimize_file(path, args)
        elif path.is_dir():
            if args.recursive:
                return self._optimize_directory(path, args)
            else:
                print(f"错误: {path} 是目录，请使用 -r 递归处理")
                return 1
        else:
            print(f"错误: 路径不存在 {path}")
            return 1
    
    def _optimize_file(self, path: Path, args):
        """优化单个文件"""
        try:
            content = path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"错误: 无法读取文件 {path}: {e}")
            return 1
        
        orig_size = len(content)
        
        # 选择优化器
        if args.extreme:
            compressor = ExtremeCompressor()
            optimized = compressor.compress(content)
            method = 'extreme'
        else:
            # 自动检测类型并优化
            content_type = self.analyzer._detect_type(content)
            
            if content_type == 'agent':
                optimized = self.optimizer.optimize_extreme(content)
                method = 'extreme'
            elif content_type == 'skill':
                optimized = self.optimizer.optimize_code_ast(content)
                method = 'ast'
            elif content_type == 'markdown':
                optimized = self.optimizer.optimize_markdown(content)
                method = 'markdown'
            elif content_type == 'mcp':
                optimized = self.optimizer.optimize_mcp(content)
                method = 'mcp'
            elif content_type == 'sql':
                optimized = self.optimizer.optimize_sql(content)
                method = 'sql'
            else:
                # 默认使用prompt优化
                optimized = self.optimizer.optimize_prompt(content) if hasattr(self.optimizer, 'optimize_prompt') else content
                method = 'prompt'
        
        opt_size = len(optimized)
        saved = orig_size - opt_size
        savings_rate = (saved / orig_size * 100) if orig_size > 0 else 0
        
        # 输出结果
        if args.format == 'json':
            result = {
                'file': str(path),
                'original_size': orig_size,
                'optimized_size': opt_size,
                'saved': saved,
                'savings_rate': round(savings_rate, 2),
                'method': method
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"文件: {path}")
            print(f"原始大小: {orig_size} 字节")
            print(f"优化后: {opt_size} 字节")
            print(f"节省: {saved} 字节 ({savings_rate:.1f}%)")
            print(f"方法: {method}")
        
        # 写入文件
        if not args.dry_run:
            if args.output:
                output_path = Path(args.output)
            else:
                output_path = path.with_suffix(path.suffix + '.optimized')
            
            try:
                output_path.write_text(optimized, encoding='utf-8')
                if args.format != 'json':
                    print(f"已保存到: {output_path}")
            except Exception as e:
                print(f"错误: 无法写入文件 {output_path}: {e}")
                return 1
        
        # 记录使用
        self.tracker.record('optimize', orig_size, opt_size, path.suffix, True)
        
        return 0
    
    def _optimize_directory(self, path: Path, args):
        """递归优化目录"""
        results = []
        
        for file_path in path.rglob('*'):
            if file_path.is_file() and file_path.suffix in ['.py', '.js', '.md', '.txt', '.json']:
                result = self._optimize_file(file_path, args)
                results.append(result)
        
        success_count = sum(1 for r in results if r == 0)
        print(f"\n完成: {success_count}/{len(results)} 个文件优化成功")
        return 0 if success_count == len(results) else 1
    
    def cmd_analyze(self, args):
        """分析命令"""
        path = Path(args.path)
        
        if not path.is_file():
            print(f"错误: 文件不存在 {path}")
            return 1
        
        try:
            content = path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"错误: 无法读取文件 {path}: {e}")
            return 1
        
        result = self.analyzer.analyze(content, 'auto')
        
        if args.format == 'json':
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"文件: {path}")
            print(f"类型: {result.get('content_type', 'unknown')}")
            print(f"字符数: {result.get('total_chars', 0)}")
            print(f"估算Token: {result.get('estimated_tokens', 0)}")
            if 'optimization_potential' in result:
                print(f"优化潜力: {result['optimization_potential']}%")
        
        return 0
    
    def cmd_batch(self, args):
        """批量优化命令"""
        path = Path(args.path)
        
        if not path.is_dir():
            print(f"错误: 目录不存在 {path}")
            return 1
        
        include_patterns = args.include.split(',')
        exclude_dirs = args.exclude.split(',')
        
        files = []
        for pattern in include_patterns:
            for file_path in path.rglob(pattern.strip()):
                if any(excluded in str(file_path) for excluded in exclude_dirs):
                    continue
                if file_path.is_file():
                    files.append(file_path)
        
        print(f"找到 {len(files)} 个文件待优化")
        
        results = []
        total_orig = 0
        total_opt = 0
        
        for file_path in files:
            try:
                content = file_path.read_text(encoding='utf-8')
                orig_size = len(content)
                
                result_type = self.analyzer._detect_type(content)
                
                if result_type == 'agent':
                    optimized = self.optimizer.optimize_extreme(content)
                elif result_type == 'skill':
                    optimized = self.optimizer.optimize_code_ast(content)
                elif result_type == 'markdown':
                    optimized = self.optimizer.optimize_markdown(content)
                elif result_type == 'mcp':
                    optimized = self.optimizer.optimize_mcp(content)
                elif result_type == 'sql':
                    optimized = self.optimizer.optimize_sql(content)
                else:
                    optimized = content
                
                opt_size = len(optimized)
                
                total_orig += orig_size
                total_opt += opt_size
                
                results.append({
                    'file': str(file_path),
                    'original': orig_size,
                    'optimized': opt_size,
                    'saved': orig_size - opt_size,
                    'method': result_type
                })
                
                print(f"✓ {file_path} ({orig_size} -> {opt_size})")
                
            except Exception as e:
                print(f"✗ {file_path}: {e}")
                results.append({
                    'file': str(file_path),
                    'error': str(e)
                })
        
        # 生成报告
        report = {
            'total_files': len(files),
            'successful': len([r for r in results if 'error' not in r]),
            'failed': len([r for r in results if 'error' in r]),
            'total_original': total_orig,
            'total_optimized': total_opt,
            'total_saved': total_orig - total_opt,
            'savings_rate': ((total_orig - total_opt) / total_orig * 100) if total_orig > 0 else 0,
            'files': results
        }
        
        # 输出报告
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
            print(f"\n报告已保存: {output_path}")
        
        print(f"\n批量优化完成:")
        print(f"  总文件: {report['total_files']}")
        print(f"  成功: {report['successful']}")
        print(f"  失败: {report['failed']}")
        print(f"  原始大小: {report['total_original']} 字节")
        print(f"  优化后: {report['total_optimized']} 字节")
        print(f"  节省: {report['total_saved']} 字节 ({report['savings_rate']:.1f}%)")
        
        return 0
    
    def cmd_stats(self, args):
        """统计命令"""
        stats = self.tracker.get_stats(args.days)
        
        print(f"\n{'='*60}")
        print(f"📊 Token经济大师 - 使用统计 (过去{args.days}天)")
        print(f"{'='*60}")
        print(f"总调用次数: {stats['total_calls']}")
        print(f"输入Token: {stats['total_input_tokens']:,}")
        print(f"输出Token: {stats['total_output_tokens']:,}")
        print(f"节省Token: {stats['total_saved_tokens']:,}")
        print(f"节省比例: {stats['savings_rate']:.1f}%")
        print(f"成功率: {stats['success_rate']:.1f}%")
        print(f"{'='*60}")
        
        return 0
    
    def cmd_config(self, args):
        """配置命令"""
        config_path = Path.home() / '.token_master' / 'config.json'
        
        if args.init:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            default_config = {
                'version': '3.3.0',
                'default_optimizer': 'smart',
                'extreme_mode': False,
                'auto_save': True,
                'output_format': 'text'
            }
            config_path.write_text(json.dumps(default_config, indent=2), encoding='utf-8')
            print(f"配置文件已创建: {config_path}")
            return 0
        
        if args.show:
            if config_path.exists():
                config = json.loads(config_path.read_text(encoding='utf-8'))
                print(json.dumps(config, ensure_ascii=False, indent=2))
            else:
                print("配置文件不存在，请运行: token-master config --init")
            return 0
        
        return 0

def main():
    cli = TokenMasterCLI()
    return cli.main()

if __name__ == '__main__':
    sys.exit(main())
