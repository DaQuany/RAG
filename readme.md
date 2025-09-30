# 🤖 RAG 질의응답 시스템

Supabase와 Google Gemini API를 사용한 문서 기반 질의응답 시스템입니다.

## 🚀 빠른 시작

### 1. 파일 구조 확인
```
rag-system/
├── main.py              # 백엔드 서버
├── index.html           # 프론트엔드
├── requirements.txt     # Python 패키지 목록
├── .env                # 환경 변수 (직접 설정 필요)
├── run.py              # 실행 스크립트
└── README.md           # 이 파일
```

### 2. 환경 변수 설정

`.env` 파일을 열고 다음 정보를 입력하세요:

```bash
# Supabase 설정
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key

# Google Gemini API 설정  
GEMINI_API_KEY=your_gemini_api_key
```

### 3. 실행

```bash
python run.py
```

또는 수동으로:

```bash
# 패키지 설치
pip install -r requirements.txt

# 서버 실행
python main.py

# 브라우저에서 index.html 파일 열기
```

## ⚙️ 사전 준비사항

### 1. Supabase 설정

1. [Supabase](https://supabase.com)에서 프로젝트 생성
2. SQL 에디터에서 다음 쿼리 실행:

```sql
-- 벡터 확장 활성화
CREATE EXTENSION IF NOT EXISTS vector;

-- 문서 테이블 생성
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(768),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

-- 벡터 검색용 인덱스 생성
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops);
```

3. 프로젝트 URL과 anon key를 `.env`에 입력

### 2. Google Gemini API 설정

1. [Google AI Studio](https://makersuite.google.com/)에서 API 키 생성
2. API 키를 `.env`에 입력

## 📱 사용법

1. **문서 추가**: 상단에 문서 내용을 입력하고 "문서 추가" 클릭
2. **질문하기**: 하단 채팅창에서 질문 입력
3. **답변 확인**: AI가 업로드된 문서를 바탕으로 답변 생성

## 🛠️ 기술 스택

- **백엔드**: FastAPI, Python
- **데이터베이스**: Supabase (PostgreSQL + pgvector)
- **임베딩**: SentenceTransformers (ko-sroberta-multitask)
- **LLM**: Google Gemini Pro
- **프론트엔드**: HTML, CSS, JavaScript

## 🔧 문제 해결

### 자주 발생하는 오류

1. **환경 변수 오류**
   ```
   ValueError: 환경 변수가 설정되지 않았습니다
   ```
   → `.env` 파일의 API 키들을 확인하세요

2. **Supabase 연결 오류**
   ```
   supabase connection failed
   ```
   → Supabase URL과 키가 정확한지, 테이블이 생성되었는지 확인하세요

3. **Gemini API 오류**
   ```
   google.generativeai.types.generation_types.BlockedPromptException
   ```
   → API 키가 유효한지, 요청이 정책에 맞는지 확인하세요

4. **CORS 오류**
   ```
   Access to fetch at 'http://localhost:8000' from origin 'file://' has been blocked
   ```
   → 백엔드 서버가 실행되고 있는지 확인하세요

## 📞 지원

문제가 발생하면:
1. 터미널의 오류 메시지를 확인
2. `.env` 파일 설정 재확인
3. Supabase 대시보드에서 테이블 생성 상태 확인
4. 브라우저 개발자 도구에서 네트워크 오류 확인

## 📈 확장 가능성

- 파일 업로드 기능 추가
- 사용자 인증 시스템
- 대화 기록 저장
- 다중 문서 컬렉션 관리
- PDF, Word 파일 지원