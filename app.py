"""
ChatReader API 服务
提供 RESTful API 接口用于处理聊天记录
"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from parser import ChatParser
from summarizer import SummaryGenerator
from analyzer import ChatAnalyzer
import os

app = Flask(__name__)
CORS(app)

# 初始化组件
parser = ChatParser()
summarizer = SummaryGenerator()
analyzer = ChatAnalyzer()


@app.route('/')
def index():
    """首页 - 返回 Web 界面"""
    return render_template('index.html')


@app.route('/api')
def api_info():
    """API 信息"""
    return jsonify({
        "name": "ChatReader API",
        "version": "1.0.0",
        "description": "微信群聊记录分析工具",
        "endpoints": {
            "/api/parse": "POST - 解析聊天记录",
            "/api/summarize": "POST - 生成聊天摘要",
            "/api/analyze_users": "POST - 分析用户画像",
            "/api/analyze_user": "POST - 分析单个用户",
            "/health": "GET - 健康检查"
        }
    })


@app.route('/health')
def health():
    """健康检查"""
    return jsonify({"status": "healthy"})


@app.route('/api/parse', methods=['POST'])
def parse_chat():
    """解析聊天记录
    
    Request Body:
        {
            "data": "聊天记录内容",
            "format": "text|json|wechat"
        }
    
    Returns:
        {
            "success": true,
            "messages": [...],
            "count": 100
        }
    """
    try:
        data = request.json
        chat_data = data.get('data', '')
        format_type = data.get('format', 'text')
        
        if not chat_data:
            return jsonify({
                "success": False,
                "error": "No chat data provided"
            }), 400
        
        # 根据格式解析
        if format_type == 'json':
            messages = parser.parse_json(chat_data)
        elif format_type == 'wechat':
            messages = parser.parse_wechat_export(chat_data)
        else:
            messages = parser.parse_text(chat_data)
        
        return jsonify({
            "success": True,
            "messages": [msg.to_dict() for msg in messages],
            "count": len(messages)
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/summarize', methods=['POST'])
def summarize_chat():
    """生成聊天摘要
    
    Request Body:
        {
            "data": "聊天记录内容",
            "format": "text|json|wechat",
            "group_name": "群组名称"
        }
    
    Returns:
        {
            "success": true,
            "summary": {...}
        }
    """
    try:
        data = request.json
        chat_data = data.get('data', '')
        format_type = data.get('format', 'text')
        group_name = data.get('group_name', '微信群')
        
        if not chat_data:
            return jsonify({
                "success": False,
                "error": "No chat data provided"
            }), 400
        
        # 解析聊天记录
        if format_type == 'json':
            messages = parser.parse_json(chat_data)
        elif format_type == 'wechat':
            messages = parser.parse_wechat_export(chat_data)
        else:
            messages = parser.parse_text(chat_data)
        
        # 生成摘要
        summary = summarizer.generate_summary(messages, group_name)
        
        return jsonify({
            "success": True,
            "summary": summary.to_dict()
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/analyze_users', methods=['POST'])
def analyze_users():
    """分析所有用户画像
    
    Request Body:
        {
            "data": "聊天记录内容",
            "format": "text|json|wechat"
        }
    
    Returns:
        {
            "success": true,
            "profiles": {...}
        }
    """
    try:
        data = request.json
        chat_data = data.get('data', '')
        format_type = data.get('format', 'text')
        
        if not chat_data:
            return jsonify({
                "success": False,
                "error": "No chat data provided"
            }), 400
        
        # 解析聊天记录
        if format_type == 'json':
            messages = parser.parse_json(chat_data)
        elif format_type == 'wechat':
            messages = parser.parse_wechat_export(chat_data)
        else:
            messages = parser.parse_text(chat_data)
        
        # 分析用户画像
        profiles = analyzer.analyze_all_users(messages)
        
        return jsonify({
            "success": True,
            "profiles": {uid: profile.to_dict() for uid, profile in profiles.items()},
            "count": len(profiles)
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/analyze_user', methods=['POST'])
def analyze_user():
    """分析单个用户
    
    Request Body:
        {
            "data": "聊天记录内容",
            "format": "text|json|wechat",
            "user_id": "用户ID"
        }
    
    Returns:
        {
            "success": true,
            "profile": {...},
            "summary": "..."
        }
    """
    try:
        data = request.json
        chat_data = data.get('data', '')
        format_type = data.get('format', 'text')
        user_id = data.get('user_id', '')
        
        if not chat_data or not user_id:
            return jsonify({
                "success": False,
                "error": "Missing chat data or user_id"
            }), 400
        
        # 解析聊天记录
        if format_type == 'json':
            messages = parser.parse_json(chat_data)
        elif format_type == 'wechat':
            messages = parser.parse_wechat_export(chat_data)
        else:
            messages = parser.parse_text(chat_data)
        
        # 分析用户画像
        profile = analyzer.analyze_user_profile(messages, user_id)
        
        if not profile:
            return jsonify({
                "success": False,
                "error": "User not found"
            }), 404
        
        # 生成用户总结
        user_summary = summarizer.generate_user_summary(messages, user_id)
        
        return jsonify({
            "success": True,
            "profile": profile.to_dict(),
            "summary": user_summary
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
