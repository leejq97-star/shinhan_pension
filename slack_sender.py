import requests
from typing import Dict, List
from datetime import datetime

class SlackSender:
    """Slack Webhook을 통해 메시지를 전송하는 클래스"""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_news_alert(self, news_data: Dict[str, List[Dict]]) -> bool:
        """
        뉴스 알림을 Slack으로 전송

        Args:
            news_data: 키워드별 뉴스 리스트

        Returns:
            성공 여부
        """
        if not news_data:
            message = self._format_no_news_message()
        else:
            message = self._format_news_message(news_data)

        try:
            response = requests.post(
                self.webhook_url,
                json=message,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                print("✅ Slack 메시지 전송 성공")
                return True
            else:
                print(f"❌ Slack 메시지 전송 실패: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"❌ Slack 전송 오류: {e}")
            return False

    def _format_news_message(self, news_data: Dict[str, List[Dict]]) -> Dict:
        """뉴스 데이터를 Slack 메시지 형식으로 변환"""

        # 총 뉴스 개수 계산
        total_news = sum(len(news_list) for news_list in news_data.values())

        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📰 뉴스 알림",
                    "emoji": True
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"⏰ {datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분')} | 총 {total_news}개 뉴스"
                    }
                ]
            },
            {
                "type": "divider"
            }
        ]

        # 각 키워드별 뉴스 추가
        for keyword, news_list in news_data.items():
            # 키워드 섹션
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*🔍 {keyword}* ({len(news_list)}개)"
                }
            })

            # 뉴스 항목 (최대 5개만 표시)
            for i, news in enumerate(news_list[:5]):
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"• <{news['link']}|{news['title']}>\n   _{news['source']} | {news['published']}_"
                    }
                })

            if len(news_list) > 5:
                blocks.append({
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"_외 {len(news_list) - 5}개 더 있음 (이메일 확인)_"
                        }
                    ]
                })

            blocks.append({"type": "divider"})

        return {"blocks": blocks}

    def _format_no_news_message(self) -> Dict:
        """뉴스가 없을 때 메시지"""
        return {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "📰 뉴스 알림",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "최근 2시간 이내에 새로운 뉴스가 없습니다."
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"⏰ {datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분')}"
                        }
                    ]
                }
            ]
        }
