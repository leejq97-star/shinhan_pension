import schedule
import time
from main import main
from datetime import datetime

def job():
    """매시간 실행될 작업"""
    print("=" * 60)
    print(f"⏰ 스케줄 작업 실행: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    main()
    print()

# 매시간 정각에 실행
schedule.every().hour.at(":00").do(job)

print("🚀 뉴스 알림 스케줄러 시작")
print("📅 매시간 정각에 뉴스를 검색하고 이메일을 발송합니다")
print("⏹️  종료하려면 Ctrl+C를 누르세요")
print()

# 즉시 한 번 실행
print("📰 초기 실행 중...")
job()

# 무한 루프로 스케줄 유지
try:
    while True:
        schedule.run_pending()
        time.sleep(30)  # 30초마다 체크
except KeyboardInterrupt:
    print("\n👋 스케줄러 종료")
