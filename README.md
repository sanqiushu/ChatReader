# ChatReader - 微信群聊记录分析工具 📱

ChatReader 是一个强大的微信群聊记录分析工具，能够帮助你快速读取、总结微信群聊记录，并生成智能摘要和用户画像。

## ✨ 主要功能

- 📊 **智能摘要生成**：自动分析聊天记录，生成简洁的摘要
- 👥 **用户画像分析**：深入分析每位群成员的聊天习惯和特征
- 🔍 **关键话题提取**：自动识别聊天中的主要讨论话题
- 💡 **亮点提炼**：提取聊天记录中的重要信息和有趣内容
- 📱 **移动端优化**：提供移动友好的 Web 界面
- 🚀 **API 接口**：完整的 RESTful API 支持集成

## 🎯 核心特性

### 聊天记录摘要
- 统计消息总数和参与人数
- 识别聊天时间段
- 提取主要话题关键词
- 生成智能文本摘要
- 展示聊天亮点

### 用户画像分析
- 消息数量统计
- 活跃时间分布分析
- 常见话题识别
- 情感倾向评分
- 用户互动关系分析

## 📦 安装与使用

### 1. 克隆项目

```bash
git clone https://github.com/sanqiushu/ChatReader.git
cd ChatReader
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量（可选）

如果需要使用 AI 智能摘要功能，需要配置 OpenAI API：

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 API key
```

### 4. 启动应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动。

### 5. 使用 Web 界面

在浏览器中打开 `http://localhost:5000`，你将看到一个移动端优化的界面：

1. 输入群组名称
2. 选择聊天记录格式
3. 粘贴聊天记录
4. 点击"开始分析"按钮
5. 查看生成的摘要和用户画像

## 📝 支持的聊天记录格式

### 1. 标准文本格式

```
2023-12-24 10:30:45 张三: 大家好！今天天气真不错
2023-12-24 10:31:12 李四: 你好啊，确实很晴朗
2023-12-24 10:32:30 王五: 早上好，有人想去爬山吗？
```

### 2. 微信导出格式

```
张三 2023-12-24 10:30:45
大家好！今天天气真不错

李四 2023-12-24 10:31:12
你好啊，确实很晴朗
```

### 3. JSON 格式

```json
[
  {
    "message_id": "1",
    "user_id": "user_001",
    "user_name": "张三",
    "content": "大家好！今天天气真不错",
    "timestamp": "2023-12-24 10:30:45",
    "message_type": "text"
  }
]
```

## 🔌 API 使用

### 生成聊天摘要

```bash
curl -X POST http://localhost:5000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "data": "聊天记录内容",
    "format": "text",
    "group_name": "测试群"
  }'
```

### 分析用户画像

```bash
curl -X POST http://localhost:5000/api/analyze_users \
  -H "Content-Type: application/json" \
  -d '{
    "data": "聊天记录内容",
    "format": "text"
  }'
```

### 分析单个用户

```bash
curl -X POST http://localhost:5000/api/analyze_user \
  -H "Content-Type: application/json" \
  -d '{
    "data": "聊天记录内容",
    "format": "text",
    "user_id": "user_001"
  }'
```

## 📚 示例数据

项目提供了示例聊天记录供测试使用：

- `examples/sample_chat.txt` - 标准文本格式示例
- `examples/sample_chat.json` - JSON 格式示例

## 🛠️ 技术栈

- **后端框架**：Flask
- **数据处理**：Python 3.7+
- **中文分词**：jieba
- **AI 能力**：OpenAI API（可选）
- **前端**：HTML5 + CSS3 + JavaScript

## 📱 移动端支持

ChatReader 提供了移动端优化的 Web 界面，可以在手机浏览器中直接使用。界面特性：

- 响应式设计，自适应各种屏幕尺寸
- 简洁直观的操作流程
- 美观的渐变色设计
- 实时加载提示
- 友好的错误处理

## 🔒 隐私说明

- 所有聊天记录处理在本地完成
- 数据不会被存储或上传到服务器
- 如果使用 AI 摘要功能，聊天内容会发送到 OpenAI API（可选）

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙋 常见问题

**Q: 可以离线使用吗？**  
A: 可以。基础的摘要和分析功能完全离线。AI 智能摘要功能需要网络连接（可选）。

**Q: 支持哪些语言？**  
A: 目前主要支持中文聊天记录分析。

**Q: 可以分析多大的聊天记录？**  
A: 建议单次分析不超过 1000 条消息，以获得最佳性能。

**Q: 如何获取微信聊天记录？**  
A: 可以通过微信自带的导出功能，或使用第三方工具导出聊天记录。

## 📞 联系方式

如有问题或建议，请提交 Issue 或联系项目维护者。