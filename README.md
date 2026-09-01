# 뉴스 알림 시스템

매시간 정각에 지정된 키워드의 최신 뉴스를 이메일로 받는 자동화 시스템

## 주요 기능

- 🔍 키워드 기반 뉴스 검색 (퇴직연금, 신한지주, 신한은행, 사모펀드)
- ⏰ 매시간 최근 2시간 이내 뉴스만 수집
- 📧 Gmail을 통한 자동 이메일 발송
- 📱 HTML 형식의 보기 좋은 뉴스 레이아웃

## 설치 방법

1. Python 패키지 설치
```bash
pip install -r requirements.txt
```

2. 환경 변수 설정
`.env.example` 파일을 `.env`로 복사하고 내용을 수정합니다.

```bash
copy .env.example .env
```

`.env` 파일 내용:
```
SENDER_EMAIL=leejq97@gmail.com
SENDER_PASSWORD=your_app_password_here
RECEIVER_EMAIL=leejq97@gmail.com
NEWS_KEYWORDS=퇴직연금,신한지주,신한은행,사모펀드
```

## Gmail 앱 비밀번호 설정

Gmail SMTP를 사용하려면 앱 비밀번호가 필요합니다:

1. Google 계정 설정 (https://myaccount.google.com/)
2. 보안 > 2단계 인증 활성화
3. 보안 > 앱 비밀번호 생성
4. 생성된 16자리 비밀번호를 `.env` 파일의 `SENDER_PASSWORD`에 입력

## 실행 방법

### 수동 실행
```bash
python main.py
```

### Windows 작업 스케줄러로 매시간 실행

1. 작업 스케줄러 열기 (Win + R → `taskschd.msc`)
2. "기본 작업 만들기" 클릭
3. 설정:
   - 이름: "뉴스 알림"
   - 트리거: 매일, 되풀이 간격 1시간
   - 동작: 프로그램 시작
   - 프로그램: `python.exe`의 전체 경로
   - 인수: `main.py`의 전체 경로
   - 시작 위치: 프로젝트 폴더 경로

### Python schedule 라이브러리 사용

`scheduler.py` 파일을 실행:
```bash
python scheduler.py
```

## 프로젝트 구조

```
.
├── main.py              # 메인 실행 파일
├── news_scraper.py      # 뉴스 검색 로직
├── email_sender.py      # 이메일 전송 로직
├── scheduler.py         # 스케줄러 (선택사항)
├── requirements.txt     # 필요한 패키지 목록
├── .env                 # 환경 변수 (직접 생성)
├── .env.example         # 환경 변수 예시
└── README.md           # 이 파일
```

## GitHub 연동

```bash
git init
git remote add origin https://github.com/leejq97-star/shinhan_pension.git
git add .
git commit -m "Initial commit: 뉴스 알림 시스템"
git push -u origin main
```

## 문제 해결

### 이메일 전송 실패
- Gmail 앱 비밀번호가 올바른지 확인
- 2단계 인증이 활성화되어 있는지 확인
- 방화벽에서 포트 587이 열려있는지 확인

### 뉴스가 검색되지 않음
- 인터넷 연결 확인
- 키워드가 올바른지 확인
- Google News RSS 접근 가능 여부 확인

## 라이선스

MIT License
