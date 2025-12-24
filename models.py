"""
ChatReader - 微信群聊记录分析工具
用于读取、总结微信群聊记录，并生成用户画像
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
import json


@dataclass
class ChatMessage:
    """聊天消息数据模型"""
    message_id: str
    user_id: str
    user_name: str
    content: str
    timestamp: datetime
    message_type: str = "text"  # text, image, voice, video, etc.
    
    def to_dict(self) -> Dict:
        return {
            "message_id": self.message_id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "message_type": self.message_type
        }


@dataclass
class UserProfile:
    """用户画像数据模型"""
    user_id: str
    user_name: str
    message_count: int = 0
    active_time_distribution: Dict[int, int] = None  # 活跃时间分布（小时）
    common_topics: List[str] = None  # 常见话题
    sentiment_score: float = 0.0  # 情感得分
    interaction_users: Dict[str, int] = None  # 互动用户及次数
    
    def __post_init__(self):
        if self.active_time_distribution is None:
            self.active_time_distribution = {}
        if self.common_topics is None:
            self.common_topics = []
        if self.interaction_users is None:
            self.interaction_users = {}
    
    def to_dict(self) -> Dict:
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "message_count": self.message_count,
            "active_time_distribution": self.active_time_distribution,
            "common_topics": self.common_topics,
            "sentiment_score": self.sentiment_score,
            "interaction_users": self.interaction_users
        }


@dataclass
class ChatSummary:
    """聊天记录摘要数据模型"""
    group_name: str
    time_period: str
    total_messages: int
    participant_count: int
    main_topics: List[str]
    summary_text: str
    highlights: List[str]
    
    def to_dict(self) -> Dict:
        return {
            "group_name": self.group_name,
            "time_period": self.time_period,
            "total_messages": self.total_messages,
            "participant_count": self.participant_count,
            "main_topics": self.main_topics,
            "summary_text": self.summary_text,
            "highlights": self.highlights
        }
