"""
聊天记录摘要生成器
使用 OpenAI API 生成智能摘要
"""
import os
from typing import List, Optional
from openai import OpenAI
from dotenv import load_dotenv
from models import ChatMessage, ChatSummary
from analyzer import ChatAnalyzer

# 加载环境变量
load_dotenv()


class SummaryGenerator:
    """摘要生成器"""
    
    def __init__(self, api_key: Optional[str] = None, api_base: Optional[str] = None):
        """初始化摘要生成器
        
        Args:
            api_key: OpenAI API key，如果不提供则从环境变量读取
            api_base: OpenAI API base URL，如果不提供则从环境变量读取
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.api_base = api_base or os.getenv("OPENAI_API_BASE")
        
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.api_base if self.api_base else None
            )
            self.use_ai = True
        else:
            self.client = None
            self.use_ai = False
            print("Warning: OpenAI API key not found. Using rule-based summarization.")
        
        self.analyzer = ChatAnalyzer()
    
    def generate_summary(self, messages: List[ChatMessage], group_name: str = "微信群") -> ChatSummary:
        """生成聊天记录摘要
        
        Args:
            messages: 聊天消息列表
            group_name: 群组名称
            
        Returns:
            ChatSummary: 聊天摘要对象
        """
        if not messages:
            return ChatSummary(
                group_name=group_name,
                time_period="无消息",
                total_messages=0,
                participant_count=0,
                main_topics=[],
                summary_text="暂无聊天记录",
                highlights=[]
            )
        
        # 基本统计信息
        total_messages = len(messages)
        participant_count = len(set(msg.user_id for msg in messages))
        time_period = self.analyzer.get_time_period_summary(messages)
        main_topics = self.analyzer.extract_main_topics(messages, top_k=5)
        highlights = self.analyzer.get_highlights(messages, max_highlights=5)
        
        # 生成摘要文本
        if self.use_ai and self.client:
            summary_text = self._generate_ai_summary(messages, main_topics)
        else:
            summary_text = self._generate_rule_based_summary(messages, main_topics)
        
        return ChatSummary(
            group_name=group_name,
            time_period=time_period,
            total_messages=total_messages,
            participant_count=participant_count,
            main_topics=main_topics,
            summary_text=summary_text,
            highlights=highlights
        )
    
    def _generate_ai_summary(self, messages: List[ChatMessage], main_topics: List[str]) -> str:
        """使用 AI 生成摘要"""
        # 准备聊天内容（限制长度以避免超出 token 限制）
        chat_content = []
        for msg in messages[:100]:  # 限制最多100条消息
            if msg.message_type == "text":
                chat_content.append(f"{msg.user_name}: {msg.content}")
        
        chat_text = "\n".join(chat_content)
        
        # 构建提示词
        prompt = f"""请分析以下微信群聊记录，生成一段简洁的摘要（200字以内）：

主要话题：{', '.join(main_topics)}

聊天记录：
{chat_text}

请用中文生成摘要，包括：
1. 群聊的主要讨论内容
2. 参与者的互动情况
3. 重要信息或决定
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的聊天记录分析助手，擅长总结和提炼信息。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"AI summarization failed: {e}")
            return self._generate_rule_based_summary(messages, main_topics)
    
    def _generate_rule_based_summary(self, messages: List[ChatMessage], main_topics: List[str]) -> str:
        """使用规则生成摘要（备用方案）"""
        participant_count = len(set(msg.user_id for msg in messages))
        total_messages = len(messages)
        
        # 统计消息类型
        type_counter = {}
        for msg in messages:
            type_counter[msg.message_type] = type_counter.get(msg.message_type, 0) + 1
        
        summary_parts = [
            f"本次群聊共有 {participant_count} 位成员参与，产生了 {total_messages} 条消息。"
        ]
        
        if main_topics:
            summary_parts.append(f"主要讨论话题包括：{', '.join(main_topics[:3])}。")
        
        # 消息类型统计
        if type_counter.get('text', 0) > 0:
            summary_parts.append(f"文字消息 {type_counter['text']} 条")
        if type_counter.get('image', 0) > 0:
            summary_parts.append(f"图片 {type_counter['image']} 张")
        if type_counter.get('voice', 0) > 0:
            summary_parts.append(f"语音 {type_counter['voice']} 条")
        
        return "，".join(summary_parts) + "。"
    
    def generate_user_summary(self, messages: List[ChatMessage], user_id: str) -> str:
        """生成单个用户的总结
        
        Args:
            messages: 聊天消息列表
            user_id: 用户ID
            
        Returns:
            str: 用户总结文本
        """
        profile = self.analyzer.analyze_user_profile(messages, user_id)
        
        if not profile:
            return "该用户没有发送消息"
        
        # 找出最活跃的时间段
        if profile.active_time_distribution:
            most_active_hour = max(profile.active_time_distribution.items(), key=lambda x: x[1])[0]
            active_time_str = f"{most_active_hour}:00-{most_active_hour+1}:00"
        else:
            active_time_str = "未知"
        
        summary_parts = [
            f"{profile.user_name} 共发送了 {profile.message_count} 条消息。",
            f"最活跃时段：{active_time_str}。"
        ]
        
        if profile.common_topics:
            summary_parts.append(f"常讨论的话题：{', '.join(profile.common_topics[:3])}。")
        
        if profile.interaction_users:
            top_interaction = sorted(profile.interaction_users.items(), key=lambda x: x[1], reverse=True)[:3]
            interaction_names = [name for name, _ in top_interaction]
            summary_parts.append(f"经常互动的用户：{', '.join(interaction_names)}。")
        
        sentiment_desc = "积极" if profile.sentiment_score > 0.3 else "中性"
        summary_parts.append(f"整体情绪：{sentiment_desc}。")
        
        return " ".join(summary_parts)
