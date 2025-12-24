# ChatReader 使用指南 📖

## 快速开始

### 准备聊天记录

在使用 ChatReader 之前，你需要准备好微信群聊的聊天记录。以下是几种获取方式：

#### 方法 1：手动复制
1. 打开微信群聊
2. 长按消息，选择"更多"
3. 选择需要分析的消息
4. 点击分享图标，选择"复制"
5. 将内容粘贴到 ChatReader 中

#### 方法 2：使用微信PC版导出
1. 在微信PC版中打开群聊
2. 点击右上角的"..."
3. 选择"聊天记录备份"
4. 导出为文本文件

### 使用 Web 界面

1. **启动应用**
   ```bash
   python app.py
   ```

2. **打开浏览器**
   - 在电脑上访问：`http://localhost:5000`
   - 在手机上访问：`http://你的电脑IP:5000`

3. **输入信息**
   - 群组名称：输入你的群聊名称（可选）
   - 选择格式：根据你的聊天记录格式选择
   - 粘贴记录：将复制的聊天记录粘贴到文本框

4. **查看结果**
   - 点击"开始分析"按钮
   - 等待几秒钟处理
   - 查看生成的摘要和用户画像

## 使用 API

### Python 示例

```python
import requests

# 准备聊天记录
chat_data = """
2023-12-24 10:30:45 张三: 大家好！
2023-12-24 10:31:12 李四: 你好啊
"""

# 生成摘要
response = requests.post(
    'http://localhost:5000/api/summarize',
    json={
        'data': chat_data,
        'format': 'text',
        'group_name': '朋友圈'
    }
)

summary = response.json()
print(summary['summary']['summary_text'])

# 分析用户画像
response = requests.post(
    'http://localhost:5000/api/analyze_users',
    json={
        'data': chat_data,
        'format': 'text'
    }
)

profiles = response.json()
for user_id, profile in profiles['profiles'].items():
    print(f"{profile['user_name']}: {profile['message_count']}条消息")
```

### JavaScript 示例

```javascript
// 生成摘要
async function analyzeChatHistory() {
    const chatData = `
2023-12-24 10:30:45 张三: 大家好！
2023-12-24 10:31:12 李四: 你好啊
    `;

    const response = await fetch('http://localhost:5000/api/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            data: chatData,
            format: 'text',
            group_name: '朋友圈'
        })
    });

    const result = await response.json();
    console.log(result.summary.summary_text);
}
```

### cURL 示例

```bash
# 生成摘要
curl -X POST http://localhost:5000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "data": "2023-12-24 10:30:45 张三: 大家好！\n2023-12-24 10:31:12 李四: 你好啊",
    "format": "text",
    "group_name": "朋友圈"
  }'
```

## 高级功能

### 使用 AI 智能摘要

如果想使用更智能的摘要功能，需要配置 OpenAI API：

1. **获取 API Key**
   - 访问 https://platform.openai.com/
   - 注册账号并获取 API Key

2. **配置环境变量**
   ```bash
   cp .env.example .env
   ```
   
   编辑 `.env` 文件：
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   OPENAI_API_BASE=https://api.openai.com/v1
   ```

3. **重启应用**
   ```bash
   python app.py
   ```

### 批量处理多个群聊

```python
import os
import glob
from parser import ChatParser
from summarizer import SummaryGenerator

parser = ChatParser()
summarizer = SummaryGenerator()

# 读取所有聊天记录文件
chat_files = glob.glob('chats/*.txt')

results = []
for file_path in chat_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        chat_data = f.read()
    
    # 解析和分析
    messages = parser.parse_text(chat_data)
    summary = summarizer.generate_summary(messages, 
                                         os.path.basename(file_path))
    results.append(summary)

# 输出结果
for summary in results:
    print(f"\n{summary.group_name}")
    print(f"摘要：{summary.summary_text}")
    print(f"主要话题：{', '.join(summary.main_topics)}")
```

### 导出分析结果

```python
import json
from parser import ChatParser
from summarizer import SummaryGenerator
from analyzer import ChatAnalyzer

# 解析聊天记录
with open('chat.txt', 'r', encoding='utf-8') as f:
    chat_data = f.read()

parser = ChatParser()
messages = parser.parse_text(chat_data)

# 生成分析结果
summarizer = SummaryGenerator()
analyzer = ChatAnalyzer()

summary = summarizer.generate_summary(messages, "测试群")
profiles = analyzer.analyze_all_users(messages)

# 导出为 JSON
result = {
    'summary': summary.to_dict(),
    'profiles': {uid: p.to_dict() for uid, p in profiles.items()}
}

with open('analysis_result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("分析结果已保存到 analysis_result.json")
```

## 最佳实践

### 1. 数据清洗
在分析前，建议：
- 移除系统消息（如"XXX加入群聊"）
- 保持时间戳格式一致
- 确保用户名的一致性

### 2. 分段分析
对于大量聊天记录：
- 按时间段分批分析
- 每批建议不超过 1000 条消息
- 可以按日、周、月进行聚合分析

### 3. 隐私保护
- 分析敏感群聊时注意数据安全
- 不要将分析结果公开分享
- 使用完毕后清理聊天记录文件

## 故障排除

### 问题：无法启动应用

**解决方法：**
```bash
# 检查 Python 版本（需要 3.7+）
python --version

# 重新安装依赖
pip install -r requirements.txt

# 检查端口占用
lsof -i :5000  # Mac/Linux
netstat -ano | findstr :5000  # Windows
```

### 问题：分析结果不准确

**可能原因：**
1. 聊天记录格式不正确
2. 时间戳解析失败
3. 用户名包含特殊字符

**解决方法：**
- 使用标准格式重新整理聊天记录
- 查看控制台错误信息
- 尝试不同的格式选项

### 问题：AI 摘要失败

**可能原因：**
1. API Key 未配置或无效
2. 网络连接问题
3. API 额度用完

**解决方法：**
- 检查 `.env` 文件配置
- 验证 API Key 有效性
- 使用规则摘要功能（不需要 API）

## 更多帮助

如果遇到其他问题，请：
1. 查看 [README.md](README.md) 文档
2. 在 GitHub 上提交 Issue
3. 查看示例代码和数据

## 反馈建议

我们欢迎你的反馈和建议：
- 提交 Issue：描述问题或功能请求
- 提交 PR：贡献代码或文档改进
- 分享使用经验：帮助其他用户
