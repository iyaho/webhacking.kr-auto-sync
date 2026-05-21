# webhacking.kr → Notion 자동 동기화

webhacking.kr에서 풀린 문제를 자동으로 Notion 데이터베이스에 기록해주는 도구입니다.

---

## 📁 파일 구조

```
webhackingkr/
├── .env              # 개인 설정 (ID, 비밀번호, Notion 토큰)
├── main.py           # 실행 진입점
├── scraper.py        # webhacking.kr 로그인 및 풀린 문제 수집
├── notion_sync.py    # Notion DB 동기화
```

---

## ✅ 사전 준비

### 1. Python 설치 확인

터미널을 열고 아래 명령어를 실행하세요.

```bash
python3 --version
```

버전이 출력되면 설치된 것입니다. 출력되지 않으면 [python.org](https://www.python.org/downloads/)에서 설치하세요.

---

### 2. 필요한 패키지 설치

```bash
pip3 install requests beautifulsoup4 python-dotenv
```

---

### 3. Notion Integration 생성

1. [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations) 접속
2. **`+ 새 Integration 만들기`** 클릭
3. 이름 입력 후 저장
4. 생성된 **`시크릿 키 (Secret Key)`** 복사 → `.env`에 저장

---

### 4. Notion 데이터베이스 생성

Notion에서 새 페이지를 만들고, 아래 컬럼 구성으로 **데이터베이스**를 추가합니다.

| 컬럼명 | 타입 |
|--------|------|
| Problem | 제목 (Title) |
| Slug | 텍스트 (Text) |
| Solved At | 날짜 (Date) |
| URL | URL |
| Score | 텍스트 (Text) |

> ⚠️ 컬럼명 대소문자를 정확히 맞춰야 합니다.

---

### 5. Notion DB에 Integration 연결

1. 데이터베이스가 있는 Notion 페이지 열기
2. 우상단 **`···`** 클릭
3. **`연결 (Connections)`** 클릭
4. 3단계에서 만든 Integration 이름 검색 후 연결

---

### 6. Notion DB ID 확인

브라우저에서 Notion DB 페이지 URL을 확인합니다.

```
https://www.notion.so/유저명/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx?v=...
                            ↑ 이 32자리가 DB ID
```

---

### 7. .env 파일 설정

프로젝트 폴더 안에 `.env` 파일을 만들고 아래 내용을 채웁니다.

```env
WEBHACKING_ID=여기에_webhacking.kr_아이디
WEBHACKING_PW=여기에_webhacking.kr_비밀번호
NOTION_TOKEN=secret_여기에_노션_시크릿키
NOTION_DB_ID=여기에_노션_DB_아이디
```

---

## 🚀 실행 방법

### 방법 A: 바탕화면 더블클릭

바탕화면의 **`wh-sync.command`** 파일을 더블클릭합니다.

> 처음 실행 시 "확인되지 않은 개발자" 경고가 뜰 수 있습니다.
> **시스템 설정 → 개인 정보 보호 및 보안 → 아래쪽에서 `허용`** 클릭 후 다시 실행하세요.

---

### 방법 B: 터미널에서 실행

```bash
cd ~/Desktop/projects/webhackingkr
python3 main.py
```

---

### 방법 C: 터미널 단축어로 실행

아래 명령어로 단축어를 등록하면 어디서든 `wh-sync`로 실행할 수 있습니다.

```bash
echo 'alias wh-sync="python3 ~/Desktop/projects/webhackingkr/main.py"' >> ~/.zshrc
source ~/.zshrc
```

이후:
```bash
wh-sync
```

---

## 📋 실행 결과 예시

```
🔄 webhacking.kr → Notion 동기화 시작

✅ 로그인 성공
📡 풀린 문제 목록 수집 중...
  총 8문제 풀었음

📋 Notion DB 기존 데이터 조회 중...
  기존 등록: 6문제
  🆕 새로 추가: ['old-15', 'old-06']
  ✅ old-15 (js-2) → Notion 추가 완료
  ✅ old-06 (web-06) → Notion 추가 완료

✅ 완료! 2개 문제 새로 추가됨
```

---

## ❓ 자주 발생하는 오류

| 오류 메시지 | 해결 방법 |
|------------|----------|
| `로그인 실패` | `.env`의 ID/PW 확인 |
| `object_not_found` | Notion DB에 Integration 연결 확인 |
| `Slug is not a property` | Notion DB 컬럼명 대소문자 확인 |
| `pip: command not found` | `pip3` 또는 `python3 -m pip` 사용 |

---

## 🔒 보안 주의사항

- `.env` 파일은 절대 GitHub 등에 업로드하지 마세요.
- 프로젝트 폴더에 `.gitignore` 파일을 만들고 아래 내용을 추가하세요.

```
.env
```
