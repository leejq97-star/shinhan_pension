import os
from datetime import datetime
from dotenv import load_dotenv
from news_scraper import NewsScraper
from email_sender import EmailSender
from slack_sender import SlackSender

def main():
    """메인 실행 함수"""
    # 환경 변수 로드
    load_dotenv()

    # 설정 값 가져오기
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    keywords_str = os.getenv('NEWS_KEYWORDS', '퇴직연금,신한지주,신한은행,사모펀드')

    # 키워드 리스트로 변환
    keywords = [k.strip() for k in keywords_str.split(',')]

    print(f"🚀 뉴스 알림 시스템 시작 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📋 키워드: {', '.join(keywords)}")
    print(f"📧 받는 사람: {receiver_email}")
    print()

    # 뉴스 스크래핑
    print("📰 뉴스 검색 중...")
    scraper = NewsScraper(keywords)
    news_data = scraper.fetch_news(hours=2)

    if news_data:
        print(f"✅ 총 {len(news_data)}개 키워드에서 뉴스 발견")
        for keyword, news_list in news_data.items():
            print(f"  - {keyword}: {len(news_list)}개")
    else:
        print("ℹ️  새로운 뉴스가 없습니다")

    # HTML 형식으로 변환
    html_content = scraper.format_news_html(news_data)

    # 이메일 전송
    print()
    print("📤 이메일 전송 중...")

    if not sender_email or not sender_password:
        print("❌ 오류: .env 파일에 이메일 설정이 필요합니다")
        print("   SENDER_EMAIL과 SENDER_PASSWORD를 설정해주세요")
        return

    email_sender = EmailSender(sender_email, sender_password)

    subject = f"📰 뉴스 알림 - {datetime.now().strftime('%Y-%m-%d %H시')}"

    success = email_sender.send_email(
        receiver_email=receiver_email,
        subject=subject,
        html_content=html_content
    )

    # Slack 전송
    if slack_webhook_url:
        print()
        print("📤 Slack 메시지 전송 중...")
        slack_sender = SlackSender(slack_webhook_url)
        slack_sender.send_news_alert(news_data)

    if success:
        print()
        print("✅ 작업 완료!")
    else:
        print()
        print("❌ 이메일 전송 실패했지만 Slack은 전송됨" if slack_webhook_url else "❌ 작업 실패")

if __name__ == "__main__":
    main()
