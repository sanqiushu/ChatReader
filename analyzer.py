"""
聊天记录分析器
用于分析聊天记录并生成用户画像
"""
from typing import List, Dict
from collections import Counter, defaultdict
from datetime import datetime
import jieba
import jieba.analyse
from models import ChatMessage, UserProfile


class ChatAnalyzer:
    """聊天记录分析器"""
    
    def __init__(self):
        # 初始化中文分词
        jieba.setLogLevel(jieba.logging.INFO)
        # 停用词列表
        self.stop_words = set([
            '的', '了', '是', '我', '你', '他', '她', '它', '们',
            '在', '有', '和', '就', '不', '人', '都', '一', '个',
            '这', '那', '要', '会', '好', '吗', '啊', '呢', '吧'
        ])
    
    def analyze_user_profile(self, messages: List[ChatMessage], user_id: str) -> UserProfile:
        """分析单个用户的画像"""
        user_messages = [msg for msg in messages if msg.user_id == user_id]
        
        if not user_messages:
            return None
        
        user_name = user_messages[0].user_name
        message_count = len(user_messages)
        
        # 分析活跃时间分布
        active_time_distribution = defaultdict(int)
        for msg in user_messages:
            hour = msg.timestamp.hour
            active_time_distribution[hour] += 1
        
        # 提取常见话题（关键词）
        all_content = " ".join([msg.content for msg in user_messages if msg.message_type == "text"])
        keywords = jieba.analyse.extract_tags(all_content, topK=10, withWeight=False)
        common_topics = [kw for kw in keywords if kw not in self.stop_words]
        
        # 分析互动用户（@ 或回复）
        interaction_users = defaultdict(int)
        for msg in user_messages:
            # 简单分析：检查消息中是否提到其他用户
            for other_msg in messages:
                if other_msg.user_id != user_id and other_msg.user_name in msg.content:
                    interaction_users[other_msg.user_name] += 1
        
        # 情感得分（简化版本：基于积极词汇占比）
        positive_words = ['好', '棒', '赞', '开心', '哈哈', '喜欢', '感谢', '谢谢', '厉害']
        positive_count = sum(1 for msg in user_messages for word in positive_words if word in msg.content)
        sentiment_score = min(1.0, positive_count / max(1, message_count))
        
        return UserProfile(
            user_id=user_id,
            user_name=user_name,
            message_count=message_count,
            active_time_distribution=dict(active_time_distribution),
            common_topics=common_topics,
            sentiment_score=sentiment_score,
            interaction_users=dict(interaction_users)
        )
    
    def analyze_all_users(self, messages: List[ChatMessage]) -> Dict[str, UserProfile]:
        """分析所有用户的画像"""
        user_ids = set(msg.user_id for msg in messages)
        profiles = {}
        
        for user_id in user_ids:
            profile = self.analyze_user_profile(messages, user_id)
            if profile:
                profiles[user_id] = profile
        
        return profiles
    
    def extract_main_topics(self, messages: List[ChatMessage], top_k: int = 10) -> List[str]:
        """提取聊天记录的主要话题"""
        all_content = " ".join([msg.content for msg in messages if msg.message_type == "text"])
        
        if not all_content:
            return []
        
        keywords = jieba.analyse.extract_tags(all_content, topK=top_k, withWeight=False)
        return [kw for kw in keywords if kw not in self.stop_words]
    
    def get_time_period_summary(self, messages: List[ChatMessage]) -> str:
        """获取时间段摘要"""
        if not messages:
            return "无消息"
        
        timestamps = [msg.timestamp for msg in messages]
        start_time = min(timestamps)
        end_time = max(timestamps)
        
        return f"{start_time.strftime('%Y-%m-%d %H:%M')} 至 {end_time.strftime('%Y-%m-%d %H:%M')}"
    
    def get_highlights(self, messages: List[ChatMessage], max_highlights: int = 5) -> List[str]:
        """提取聊天记录中的亮点/关键消息"""
        # 简单策略：选择较长的消息作为亮点
        text_messages = [msg for msg in messages if msg.message_type == "text" and len(msg.content) > 20]
        
        # 按长度排序
        text_messages.sort(key=lambda x: len(x.content), reverse=True)
        
        highlights = []
        for msg in text_messages[:max_highlights]:
            highlight = f"{msg.user_name}: {msg.content[:100]}" + ("..." if len(msg.content) > 100 else "")
            highlights.append(highlight)
        
        return highlights
