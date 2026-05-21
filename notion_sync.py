import requests
from datetime import datetime, timezone

NOTION_API = "https://api.notion.com/v1"
HEADERS_TEMPLATE = {
    "Authorization": "",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


def get_headers(token):
    h = HEADERS_TEMPLATE.copy()
    h["Authorization"] = f"Bearer {token}"
    return h


def get_existing_slugs(token, db_id):
    existing = set()
    cursor = None

    while True:
        body = {}
        if cursor:
            body["start_cursor"] = cursor

        res = requests.post(
            f"{NOTION_API}/databases/{db_id}/query",
            headers=get_headers(token),
            json=body
        )
        data = res.json()

        if "results" not in data:
            print(f"  ❌ Notion 오류: {data}")
            break

        for page in data["results"]:
            props = page["properties"]
            if "Slug" in props:
                rich = props["Slug"].get("rich_text", [])
                if rich:
                    existing.add(rich[0]["text"]["content"])

        if not data.get("has_more"):
            break
        cursor = data["next_cursor"]

    return existing


def add_problem(token, db_id, problem):
    body = {
        "parent": {"database_id": db_id},
        "properties": {
            "Problem": {
                "title": [{"text": {"content": f"✔️ {problem['name']}"}}]
            },
            "Slug": {
                "rich_text": [{"text": {"content": problem["slug"]}}]
            },
            "Solved At": {
                "date": {"start": datetime.now(timezone.utc).isoformat()}
            },
            "URL": {
                "url": problem["url"]
            },
            "Score": {
                "rich_text": [{"text": {"content": problem["score"]}}]
            }
        }
    }

    res = requests.post(
        f"{NOTION_API}/pages",
        headers=get_headers(token),
        json=body
    )

    if res.status_code == 200:
        print(f"  ✅ {problem['name']} ({problem['slug']}) → Notion 추가 완료")
    else:
        print(f"  ❌ 추가 실패: {res.json()}")


def sync(token, db_id, solved_list):
    print("\n📋 Notion DB 기존 데이터 조회 중...")
    existing = get_existing_slugs(token, db_id)
    print(f"  기존 등록: {len(existing)}문제")

    new_problems = [p for p in solved_list if p["slug"] not in existing]

    if not new_problems:
        print("  ✨ 새로 추가할 문제 없음 (이미 최신)")
        return 0

    print(f"  🆕 새로 추가: {[p['name'] for p in new_problems]}")
    for problem in new_problems:
        add_problem(token, db_id, problem)

    return len(new_problems)