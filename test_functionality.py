"""
Test script for ChatReader functionality
"""
from parser import ChatParser
from summarizer import SummaryGenerator
from analyzer import ChatAnalyzer

# 测试数据
test_data = """
2023-12-24 10:30:45 张三: 大家好！今天天气真不错
2023-12-24 10:31:12 李四: 你好啊，确实很晴朗
2023-12-24 10:32:30 王五: 早上好，有人想去爬山吗？
2023-12-24 10:33:15 张三: 我可以去！什么时候出发？
2023-12-24 10:34:20 李四: 我也想去，周末怎么样？
2023-12-24 10:35:45 赵六: 周末好啊，我也报名
2023-12-24 10:36:30 王五: 那就定周六上午9点吧
2023-12-24 10:37:10 张三: 没问题，记得带水和零食
2023-12-24 10:38:25 李四: 好的，我会准备的
2023-12-24 10:39:40 赵六: 天气预报说周六晴天，完美
"""

print("=" * 60)
print("ChatReader 功能测试")
print("=" * 60)

# 测试解析器
print("\n1. 测试聊天记录解析...")
parser = ChatParser()
messages = parser.parse_text(test_data)
print(f"✓ 成功解析 {len(messages)} 条消息")
for msg in messages[:3]:
    print(f"  - {msg.user_name}: {msg.content}")

# 测试分析器
print("\n2. 测试用户画像分析...")
analyzer = ChatAnalyzer()
profiles = analyzer.analyze_all_users(messages)
print(f"✓ 成功分析 {len(profiles)} 位用户")
for user_id, profile in list(profiles.items())[:2]:
    print(f"  - {profile.user_name}: {profile.message_count}条消息, 常见话题: {', '.join(profile.common_topics[:3])}")

# 测试主题提取
print("\n3. 测试主题提取...")
main_topics = analyzer.extract_main_topics(messages, top_k=5)
print(f"✓ 提取主题: {', '.join(main_topics)}")

# 测试摘要生成器
print("\n4. 测试摘要生成...")
summarizer = SummaryGenerator()
summary = summarizer.generate_summary(messages, "测试群")
print(f"✓ 群组: {summary.group_name}")
print(f"  时间段: {summary.time_period}")
print(f"  消息总数: {summary.total_messages}")
print(f"  参与人数: {summary.participant_count}")
print(f"  主要话题: {', '.join(summary.main_topics)}")
print(f"  摘要: {summary.summary_text}")

# 测试用户总结
print("\n5. 测试单个用户总结...")
first_user_id = list(profiles.keys())[0]
user_summary = summarizer.generate_user_summary(messages, first_user_id)
print(f"✓ {user_summary}")

# 测试 JSON 导出
print("\n6. 测试 JSON 导出...")
json_output = parser.export_to_json(messages[:3])
print(f"✓ JSON 导出成功 (前3条消息)")

# 测试文件读取
print("\n7. 测试示例文件读取...")
try:
    with open('examples/sample_chat.txt', 'r', encoding='utf-8') as f:
        sample_data = f.read()
    sample_messages = parser.parse_text(sample_data)
    print(f"✓ 成功读取示例文件，包含 {len(sample_messages)} 条消息")
except Exception as e:
    print(f"✗ 读取示例文件失败: {e}")

print("\n" + "=" * 60)
print("所有测试完成！")
print("=" * 60)
