import os
import requests
from dotenv import load_dotenv

from scraper import login, get_solved_problems
from notion_sync import sync

load_dotenv()

def run():
    print("🔄 webhacking.kr → Notion 동기화 시작\n")

    wh_id   = os.getenv("WEBHACKING_ID")
    wh_pw   = os.getenv("WEBHACKING_PW")
    n_token = os.getenv("NOTION_TOKEN")
    n_db_id = os.getenv("NOTION_DB_ID")

    if not all([wh_id, wh_pw, n_token, n_db_id]):
        print("❌ .env 설정을 확인하세요")
        return

    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})

    if not login(session, wh_id, wh_pw):
        return

    print("📡 풀린 문제 목록 수집 중...")
    solved = get_solved_problems(session)
    print(f"  총 {len(solved)}문제 풀었음: {solved}")

    added = sync(n_token, n_db_id, solved)
    print(f"\n✅ 완료! {added}개 문제 새로 추가됨")

if __name__ == "__main__":
    run()