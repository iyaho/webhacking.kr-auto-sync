import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://webhacking.kr"

def login(session, user_id, password):
    import json
    
    login_url = f"{BASE_URL}/login.php?login"
    payload = {"id": user_id, "pw": password}
    
    res = session.post(
        login_url,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
        allow_redirects=True
    )
    
    print(f"  🔍 응답: {res.text[:100]}")  # 디버그용

    try:
        result = res.json()
        if result.get("stat") == True:
            print("✅ 로그인 성공")
            return True
        else:
            print(f"❌ 로그인 실패: {result}")
            return False
    except:
        print(f"❌ JSON 파싱 실패: {res.text[:200]}")
        return False

def get_solved_problems(session):
    chall_url = f"{BASE_URL}/chall.php"
    res = session.get(chall_url)
    soup = BeautifulSoup(res.text, "html.parser")

    solved = []

    for row in soup.select("tr.table-success"):
        a_tag = row.select_one("td a")
        tds = row.select("td")

        if not a_tag:
            continue

        # 이름에서 ✔️ 제거
        name = a_tag.get_text(strip=True).replace("✔️", "").strip()

        # URL 정리
        href = a_tag.get("href", "")
        if href.startswith("./"):
            full_url = BASE_URL + "/" + href[2:]
        elif href.startswith("http"):
            full_url = href
        else:
            full_url = BASE_URL + href

        # slug 추출 (ex: web-06, js-2, bonus-14)
        slug_match = re.search(r"challenge/(.+?)/?$", href)
        slug = slug_match.group(1) if slug_match else name

        # 점수
        score = tds[1].get_text(strip=True) if len(tds) > 1 else "-"

        solved.append({
            "name": name,
            "slug": slug,
            "url": full_url,
            "score": score
        })

    return solved