"""
Token经济大师 v3.0 - 自迭代引擎

实现技能的自我优化能力：
1. 自动分析评测失败案例
2. 生成新优化规则
3. 自动测试验证
4. 发布新版本
"""

import re
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any

class SelfIteratingEngine:
    """自迭代引擎 - 让技能自己优化自己"""
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.optimizer_path = self.skill_path / "optimizer" / "smart_optimizer.py"
        self.iteration_log = []
    
    def run_iteration(self) -> Dict[str, Any]:
        """运行一次完整迭代"""
        print("🔄 启动自迭代流程...")
        
        # 1. 运行评测
        print("\n1️⃣ 运行深度评测...")
        test_results = self._run_tests()
        
        # 2. 分析失败案例
        print("\n2️⃣ 分析优化机会...")
        improvements = self._analyze_failures(test_results)
        
        if not improvements:
            print("✅ 无需优化，当前效果已达标")
            return {'status': 'no_improvement_needed'}
        
        # 3. 生成新规则
        print("\n3️⃣ 生成新优化规则...")
        new_rules = self._generate_rules(improvements)
        
        # 4. 应用规则
        print("\n4️⃣ 应用新规则...")
        self._apply_rules(new_rules)
        
        # 5. 验证效果
        print("\n5️⃣ 验证优化效果...")
        verification = self._verify_improvement(test_results)
        
        if verification['improved']:
            # 6. 发布更新
            print("\n6️⃣ 发布新版本...")
            self._publish_update(new_rules, verification)
            
            return {
                'status': 'success',
                'rules_added': len(new_rules),
                'improvement': verification['improvement'],
                'new_version': verification['new_version']
            }
        else:
            # 回滚
            print("\n⚠️ 优化效果不佳，回滚更改")
            self._rollback()
            return {'status': 'rolled_back'}
    
    def _run_tests(self) -> List[Dict]:
        """运行测试收集结果"""
        test_cases = [
            {
                'name': '综合压缩测试',
                'input': '如果用户提出了一个比较复杂的问题，请你认真地分析一下，然后给出详细的回答。',
                'type': 'agent',
                'target_saving': 40
            },
            {
                'name': '长文本测试',
                'input': '请你帮我完成以下任务：\n1. 仔细地分析输入的数据\n2. 认真地检查每一个细节',
                'type': 'agent',
                'target_saving': 45
            },
            {
                'name': '代码优化测试',
                'input': 'def test():\n    # 注释\n    x = 1\n    return x',
                'type': 'skill',
                'target_saving': 30
            }
        ]
        
        # 动态导入当前的optimizer
        import sys
        sys.path.insert(0, str(self.skill_path))
        from optimizer.smart_optimizer import SmartOptimizer
        
        optimizer = SmartOptimizer()
        results = []
        
        for case in test_cases:
            result = optimizer.optimize(case['input'], case['type'])
            case['actual_saving'] = result['saving_percentage']
            case['optimized'] = result['optimized']
            case['needs_improvement'] = result['saving_percentage'] < case['target_saving']
            results.append(case)
            
            status = '❌' if case['needs_improvement'] else '✅'
            print(f"  {status} {case['name']}: {result['saving_percentage']}% / 目标{case['target_saving']}%")
        
        return results
    
    def _analyze_failures(self, results: List[Dict]) -> List[Dict]:
        """分析需要改进的地方"""
        failures = [r for r in results if r['needs_improvement']]
        
        improvements = []
        for fail in failures:
            # 分析原文和优化后的差异
            original = fail['input']
            optimized = fail['optimized']
            
            # 找出原文中未被压缩的模式
            remaining_patterns = self._extract_patterns(original, optimized)
            
            improvements.append({
                'test_name': fail['name'],
                'type': fail['type'],
                'remaining_patterns': remaining_patterns,
                'gap': fail['target_saving'] - fail['actual_saving']
            })
        
        return improvements
    
    def _extract_patterns(self, original: str, optimized: str) -> List[str]:
        """提取未被压缩的模式"""
        patterns = []
        
        # 常见可压缩模式
        common_patterns = [
            r'一个', r'然后', r'接着', r'详细地', r'复杂的',
            r'每个', r'所有', r'结果', r'数据', r'信息',
            r'仔细地', r'认真地', r'分析一下', r'处理一下'
        ]
        
        for pattern in common_patterns:
            if re.search(pattern, original) and re.search(pattern, optimized):
                patterns.append(pattern)
        
        return patterns
    
    def _generate_rules(self, improvements: List[Dict]) -> List[tuple]:
        """基于分析生成新规则"""
        new_rules = []
        
        # 规则模板库
        rule_templates = {
            '一个': (r'一个', ''),
            '然后': (r'然后', ''),
            '接着': (r'接着', ''),
            '详细地': (r'详细地?', '详'),
            '复杂的': (r'复杂的?', '繁'),
            '每个': (r'每个', '各'),
            '所有': (r'所有', '全'),
            '结果': (r'结果', '果'),
            '数据': (r'数据', '数'),
            '信息': (r'信息', '息'),
            '仔细地': (r'仔细地?', ''),
            '认真地': (r'认真地?', ''),
            '分析一下': (r'分析一下', '析'),
            '处理一下': (r'处理一下', '处'),
        }
        
        # 收集所有需要改进的模式
        all_patterns = set()
        for imp in improvements:
            all_patterns.update(imp['remaining_patterns'])
        
        # 生成规则
        for pattern in all_patterns:
            if pattern in rule_templates:
                new_rules.append(rule_templates[pattern])
                print(f"  + 新规则: '{pattern}' → '{rule_templates[pattern][1]}'")
        
        return new_rules
    
    def _apply_rules(self, new_rules: List[tuple]):
        """将新规则应用到代码"""
        # 读取当前规则文件
        content = self.optimizer_path.read_text(encoding='utf-8')
        
        # 找到规则列表的位置
        rules_start = content.find('self.prompt_rules = [')
        rules_end = content.find(']', rules_start)
        
        # 生成新规则代码
        new_rules_code = '\n'.join([
            f"            (r'{pattern}', '{replacement}'),  # 自迭代生成"
            for pattern, replacement in new_rules
        ])
        
        # 插入新规则
        updated_content = (
            content[:rules_end] + 
            '\n            # 自迭代生成规则\n' + 
            new_rules_code + 
            '\n' + 
            content[rules_end:]
        )
        
        # 备份原文件
        backup_path = self.optimizer_path.with_suffix('.py.bak')
        backup_path.write_text(content, encoding='utf-8')
        
        # 写入更新
        self.optimizer_path.write_text(updated_content, encoding='utf-8')
        print(f"  ✅ 已应用 {len(new_rules)} 条新规则")
    
    def _verify_improvement(self, original_results: List[Dict]) -> Dict:
        """验证优化效果"""
        # 重新运行测试
        new_results = self._run_tests()
        
        # 计算整体提升
        original_avg = sum(r['actual_saving'] for r in original_results) / len(original_results)
        new_avg = sum(r['actual_saving'] for r in new_results) / len(new_results)
        
        improvement = new_avg - original_avg
        
        return {
            'improved': improvement > 0,
            'improvement': round(improvement, 1),
            'original_avg': round(original_avg, 1),
            'new_avg': round(new_avg, 1),
            'new_version': self._bump_version()
        }
    
    def _bump_version(self) -> str:
        """版本号+1"""
        init_file = self.skill_path / '__init__.py'
        content = init_file.read_text(encoding='utf-8')
        
        # 提取当前版本
        match = re.search(r"__version__ = '(\d+)\.(\d+)\.(\d+)'", content)
        if match:
            major, minor, patch = map(int, match.groups())
            new_version = f"{major}.{minor}.{patch + 1}"
            
            # 更新版本号
            new_content = re.sub(
                r"__version__ = '[\d.]+'",
                f"__version__ = '{new_version}'",
                content
            )
            init_file.write_text(new_content, encoding='utf-8')
            
            return new_version
        
        return "unknown"
    
    def _publish_update(self, new_rules: List[tuple], verification: Dict):
        """发布更新"""
        print(f"\n📦 发布 v{verification['new_version']}")
        print(f"   新增规则: {len(new_rules)}条")
        print(f"   效果提升: {verification['improvement']}%")
        
        # 这里可以添加git提交和push的逻辑
        print("   (git提交和ClawHub上传可由外部调用完成)")
    
    def _rollback(self):
        """回滚更改"""
        backup_path = self.optimizer_path.with_suffix('.py.bak')
        if backup_path.exists():
            content = backup_path.read_text(encoding='utf-8')
            self.optimizer_path.write_text(content, encoding='utf-8')
            backup_path.unlink()
            print("   ✅ 已回滚到原版本")


def main():
    """演示自迭代"""
    import sys
    
    skill_path = Path(__file__).parent
    engine = SelfIteratingEngine(skill_path)
    
    result = engine.run_iteration()
    
    print("\n" + "=" * 60)
    print(f"🎉 自迭代结果: {result['status']}")
    if result['status'] == 'success':
        print(f"   新增规则: {result['rules_added']}条")
        print(f"   效果提升: {result['improvement']}%")
        print(f"   新版本: {result['new_version']}")
    print("=" * 60)


if __name__ == '__main__':
    main()
