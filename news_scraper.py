import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import urllib.parse

class NewsScraper:
    """네이버 뉴스 RSS를 통해 뉴스를 검색하는 클래스"""

    def __init__(self, keywords: List[str]):
        self.keywords = keywords
        self.base_url = "https://news.google.com/rss/search"

    def fetch_news(self, hours: int = 5) -> Dict[str, List[Dict]]:
        """
        키워드별로 최근 뉴스를 가져옴

        Args:
            hours: 몇 시간 이내의 뉴스를 가져올지 (기본: 5시간)

        Returns:
            키워드별 뉴스 리스트를 담은 딕셔너리
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        all_news = {}

        for keyword in self.keywords:
            try:
                news_list = self._search_keyword(keyword, cutoff_time)
                if news_list:
                    all_news[keyword] = news_list
            except Exception as e:
                print(f"키워드 '{keyword}' 검색 중 오류 발생: {e}")

        return all_news

    def _search_keyword(self, keyword: str, cutoff_time: datetime) -> List[Dict]:
        """특정 키워드로 뉴스 검색"""
        try:
            # Google News RSS 사용 (한국어)
            encoded_keyword = urllib.parse.quote(f"{keyword} when:5h")
            url = f"{self.base_url}?q={encoded_keyword}&hl=ko&gl=KR&ceid=KR:ko"

            feed = feedparser.parse(url)
            news_list = []

            for entry in feed.entries[:10]:  # 최대 10개
                news_item = {
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.get('published', ''),
                    'source': entry.get('source', {}).get('title', '알 수 없음')
                }
                news_list.append(news_item)

            return news_list

        except Exception as e:
            print(f"뉴스 검색 오류: {e}")
            return []

    def format_news_html(self, news_data: Dict[str, List[Dict]]) -> str:
        """뉴스 데이터를 HTML 형식으로 포맷팅"""
        if not news_data:
            return "<p>최근 5시간 이내에 새로운 뉴스가 없습니다.</p>"

        html = """
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {
                    font-family: 'Malgun Gothic', '맑은 고딕', Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }
                .header {
                    background-color: #0046ff;
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                }
                .keyword-section {
                    background-color: white;
                    padding: 20px;
                    margin-bottom: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .keyword-title {
                    color: #0046ff;
                    font-size: 20px;
                    font-weight: bold;
                    margin-bottom: 15px;
                    padding-bottom: 10px;
                    border-bottom: 2px solid #0046ff;
                }
                .news-item {
                    padding: 15px;
                    margin-bottom: 10px;
                    border-left: 3px solid #0046ff;
                    background-color: #f9f9f9;
                }
                .news-title {
                    font-size: 16px;
                    font-weight: bold;
                    margin-bottom: 8px;
                }
                .news-title a {
                    color: #333;
                    text-decoration: none;
                }
                .news-title a:hover {
                    color: #0046ff;
                    text-decoration: underline;
                }
                .news-meta {
                    font-size: 12px;
                    color: #666;
                }
                .footer {
                    margin-top: 30px;
                    padding: 20px;
                    text-align: center;
                    color: #666;
                    font-size: 12px;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📰 뉴스 알림</h1>
                <p>최근 5시간 이내 뉴스</p>
            </div>
        """

        for keyword, news_list in news_data.items():
            html += f'<div class="keyword-section">'
            html += f'<div class="keyword-title">🔍 {keyword}</div>'

            for news in news_list:
                html += '<div class="news-item">'
                html += f'<div class="news-title"><a href="{news["link"]}" target="_blank">{news["title"]}</a></div>'
                html += f'<div class="news-meta">출처: {news["source"]} | {news["published"]}</div>'
                html += '</div>'

            html += '</div>'

        html += f"""
            <div class="footer">
                <p>발송 시간: {datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분')}</p>
                <p>이 메일은 자동으로 발송되었습니다.</p>
            </div>
        </body>
        </html>
        """

        return html
