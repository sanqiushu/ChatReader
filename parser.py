"""
聊天记录解析器
支持多种格式的聊天记录导入
"""
import json
import re
from typing import List, Dict
from datetime import datetime
from models import ChatMessage


class ChatParser:
    """聊天记录解析器"""
    
    def parse_json(self, json_data: str) -> List[ChatMessage]:
        """解析 JSON 格式的聊天记录
        
        Args:
            json_data: JSON 格式的聊天记录字符串
            
        Returns:
            List[ChatMessage]: 聊天消息列表
        """
        try:
            data = json.loads(json_data)
            messages = []
            
            for item in data:
                message = ChatMessage(
                    message_id=item.get('message_id', str(len(messages))),
                    user_id=item.get('user_id', ''),
                    user_name=item.get('user_name', '未知用户'),
                    content=item.get('content', ''),
                    timestamp=self._parse_timestamp(item.get('timestamp', '')),
                    message_type=item.get('message_type', 'text')
                )
                messages.append(message)
            
            return messages
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return []
    
    def parse_text(self, text_data: str) -> List[ChatMessage]:
        """解析文本格式的聊天记录
        
        文本格式示例：
        2023-12-24 10:30:45 张三: 大家好
        2023-12-24 10:31:12 李四: 你好啊
        
        Args:
            text_data: 文本格式的聊天记录
            
        Returns:
            List[ChatMessage]: 聊天消息列表
        """
        messages = []
        lines = text_data.strip().split('\n')
        
        # 正则表达式匹配时间、用户名和消息内容
        pattern = r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+([^:]+):\s*(.+)'
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            match = re.match(pattern, line)
            if match:
                timestamp_str, user_name, content = match.groups()
                
                message = ChatMessage(
                    message_id=str(i),
                    user_id=self._generate_user_id(user_name),
                    user_name=user_name.strip(),
                    content=content.strip(),
                    timestamp=self._parse_timestamp(timestamp_str),
                    message_type=self._detect_message_type(content)
                )
                messages.append(message)
        
        return messages
    
    def parse_wechat_export(self, text_data: str) -> List[ChatMessage]:
        """解析微信导出的聊天记录格式
        
        微信导出格式示例：
        张三 2023-12-24 10:30:45
        大家好
        
        李四 2023-12-24 10:31:12
        你好啊
        
        Args:
            text_data: 微信导出格式的聊天记录
            
        Returns:
            List[ChatMessage]: 聊天消息列表
        """
        messages = []
        lines = text_data.strip().split('\n')
        
        i = 0
        message_id = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if not line:
                i += 1
                continue
            
            # 尝试匹配用户名和时间戳行
            pattern = r'([^\d]+)\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})'
            match = re.match(pattern, line)
            
            if match and i + 1 < len(lines):
                user_name, timestamp_str = match.groups()
                content = lines[i + 1].strip()
                
                message = ChatMessage(
                    message_id=str(message_id),
                    user_id=self._generate_user_id(user_name),
                    user_name=user_name.strip(),
                    content=content,
                    timestamp=self._parse_timestamp(timestamp_str),
                    message_type=self._detect_message_type(content)
                )
                messages.append(message)
                message_id += 1
                i += 2
            else:
                i += 1
        
        return messages
    
    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """解析时间戳"""
        if isinstance(timestamp_str, datetime):
            return timestamp_str
        
        # 尝试多种时间格式
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y/%m/%d %H:%M:%S',
            '%Y-%m-%d %H:%M',
            '%Y/%m/%d %H:%M',
            '%Y-%m-%dT%H:%M:%S',
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue
        
        # 如果都失败了，返回当前时间
        print(f"Warning: Could not parse timestamp '{timestamp_str}', using current time")
        return datetime.now()
    
    def _generate_user_id(self, user_name: str) -> str:
        """根据用户名生成用户ID"""
        # 简单实现：使用用户名的 hash 值作为 ID
        return f"user_{hash(user_name) % 1000000}"
    
    def _detect_message_type(self, content: str) -> str:
        """检测消息类型"""
        if '[图片]' in content or '[Image]' in content:
            return 'image'
        elif '[语音]' in content or '[Voice]' in content:
            return 'voice'
        elif '[视频]' in content or '[Video]' in content:
            return 'video'
        elif '[文件]' in content or '[File]' in content:
            return 'file'
        else:
            return 'text'
    
    def export_to_json(self, messages: List[ChatMessage]) -> str:
        """将聊天记录导出为 JSON 格式"""
        data = [msg.to_dict() for msg in messages]
        return json.dumps(data, ensure_ascii=False, indent=2)
