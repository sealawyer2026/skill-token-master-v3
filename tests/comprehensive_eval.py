#!/usr/bin/env python3
"""
Token经济大师 v3.0 - 多轮迭代评测脚本
自动进行多轮迭代并记录效果
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/skill-token-master-v3')

from optimizer.smart_optimizer import SmartOptimizer

def run_comprehensive_test():
    """运行综合评测"""
    opt = SmartOptimizer()
    
    test_cases = [
        # 提示词测试
        ('简单冗余', '请你非常仔细地帮我分析一下', 'agent'),
        ('客套话', '麻烦您帮我处理一下这个任务，谢谢', 'agent'),
        ('综合长句', '如果用户提出了一个比较复杂的问题，请你认真地分析一下，然后给出详细的回答', 'agent'),
        ('列表任务', '请你帮我完成以下任务：1. 分析数据 2. 检查结果 3. 整理结果', 'agent'),
        ('复杂场景', '虽然这个问题非常复杂，但是只要你仔细地分析，就一定能找到解决方法', 'agent'),
        
        # 代码测试
        ('简单函数', '''def test(x):\n    # 检查\n    if x is not None:\n        return True\n    else:\n        return False''', 'skill'),
        ('列表处理', '''def process(items):\n    result = []\n    for item in items:\n        if item is not None and len(item) > 0:\n            result.append(item)\n    return result''', 'skill'),
        ('统计函数', '''def stats(data):\n    total = 0\n    for d in data:\n        total += d\n    return {"total": total}''', 'skill'),
        
        # 工作流测试
        ('简单配置', '{"name": "test", "steps": [{"name": "step1", "type": "load"}]}', 'workflow'),
    ]
    
    results = []
    print("=" * 70)
    print("🔬 综合评测报告")
    print("=" * 70)
    
    for name, content, ctype in test_cases:
        result = opt.optimize(content, ctype)
        results.append({
            'name': name,
            'type': ctype,
            'saving': result['saving_percentage']
        })
        
        icon = '📝' if ctype == 'agent' else '💻' if ctype == 'skill' else '⚙️'
        print(f"{icon} {name:12s} | {ctype:8s} | 节省: {result['saving_percentage']:5.1f}%")
    
    # 分类统计
    agent_results = [r['saving'] for r in results if r['type'] == 'agent']
    skill_results = [r['saving'] for r in results if r['type'] == 'skill']
    workflow_results = [r['saving'] for r in results if r['type'] == 'workflow']
    
    print("-" * 70)
    print(f"📊 分类统计:")
    print(f"   提示词优化: 平均 {sum(agent_results)/len(agent_results):.1f}%")
    print(f"   代码优化:   平均 {sum(skill_results)/len(skill_results):.1f}%")
    print(f"   工作流优化: 平均 {sum(workflow_results)/len(workflow_results):.1f}%" if workflow_results else "   工作流优化: 无数据")
    print("=" * 70)
    
    return results

if __name__ == '__main__':
    run_comprehensive_test()
