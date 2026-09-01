import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

class EmailSender:
    """Gmail SMTP를 통해 이메일을 전송하는 클래스"""

    def __init__(self, sender_email: str, sender_password: str):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_email(self,
                   receiver_email: str,
                   subject: str,
                   html_content: str) -> bool:
        """
        HTML 이메일 전송

        Args:
            receiver_email: 받는 사람 이메일
            subject: 이메일 제목
            html_content: HTML 형식의 이메일 내용

        Returns:
            성공 여부
        """
        try:
            # 이메일 메시지 생성
            message = MIMEMultipart('alternative')
            message['From'] = self.sender_email
            message['To'] = receiver_email
            message['Subject'] = subject

            # HTML 파트 추가
            html_part = MIMEText(html_content, 'html', 'utf-8')
            message.attach(html_part)

            # SMTP 서버 연결 및 전송
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # TLS 암호화
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)

            print(f"✅ 이메일 전송 성공: {receiver_email}")
            return True

        except Exception as e:
            print(f"❌ 이메일 전송 실패: {e}")
            return False
