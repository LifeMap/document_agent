# AI 에이전트 학습 프로젝트

## 개인 문서 검색 + 웹검색 에이전트

---

## 프로젝트 개요

| 항목 | 내용 |
|------|------|
| 목표 | 문서에서 답변 찾고, 없으면 웹 검색하는 에이전트 |
| 난이도 | 중 (RAG + Tool 사용 + 분기처리) |
| 예상 기간 | 2~3주 |
| 목적 | AI 에이전트 핵심 개념 실습 및 포트폴리오 |

---

## 핵심 기능

| 기능 | 설명 | 학습 포인트 |
|------|------|------------|
| 문서 업로드 | PDF/텍스트 → 벡터 저장 | 청킹, 임베딩, 벡터DB |
| 문서 검색 | 질문 → 유사 문서 찾기 → 답변 | RAG 파이프라인 |
| 웹 검색 | 문서에 없으면 웹 검색 | Tool 정의/호출 |
| 출처 표시 | 답변 근거 표시 | 메타데이터 활용 |

---

## 사용자 시나리오

### 시나리오 1: 문서에서 답변 찾기

```
사용자: "RAG에서 청킹 크기는 어떻게 정해?"

[에이전트 판단]
→ 내 문서에서 검색      ← Tool 1: search_documents()
→ 관련 내용 발견        ← 결과 있음
→ 답변 생성            ← LLM
```

### 시나리오 2: 웹 검색 필요

```
사용자: "2025년 LangChain 최신 업데이트 뭐야?"

[에이전트 판단]
→ 내 문서에서 검색      ← Tool 1: search_documents()
→ 관련 내용 없음        ← 결과 없음
→ 웹 검색              ← Tool 2: web_search()
→ 답변 생성            ← LLM
```

---

## 기술 스택

| 영역 | 기술 | 용도 |
|------|------|------|
| 프레임워크 | LangChain + LangGraph | 에이전트 구조, Tool 연결 |
| LLM | OpenAI 또는 Claude | 판단, 답변 생성 |
| 벡터DB | Chroma (로컬) | 문서 임베딩 저장/검색 |
| 웹검색 | Tavily 또는 DuckDuckGo | 외부 정보 검색 |
| UI | Streamlit | 간단한 웹 인터페이스 |

---

## 개발 순서

| 단계 | 할 일 | 산출물 | 예상 시간 |
|------|------|--------|----------|
| 1 | 문서 로딩 → 청킹 → 임베딩 → Chroma 저장 | RAG 파이프라인 | 3~4일 |
| 2 | 질문 → 벡터 검색 → 답변 | 기본 Q&A | 2~3일 |
| 3 | 웹검색 Tool 정의 | Tool 구현 | 2일 |
| 4 | 문서에 없으면 웹검색 분기 | 라우팅 로직 | 2~3일 |
| 5 | Streamlit UI | 사용 가능한 앱 | 2~3일 |

---

## Tool 설계

| Tool 이름 | 기능 | 입력 | 출력 |
|----------|------|------|------|
| `search_documents` | 벡터DB에서 유사 문서 검색 | query (str) | 관련 문서 리스트 |
| `web_search` | 웹에서 정보 검색 | query (str) | 검색 결과 리스트 |

---

## 에이전트 흐름 (ReAct 패턴)

```
[입력] 사용자 질문
    ↓
[Thought] "이 질문에 답하려면 먼저 내 문서를 검색해야겠다"
    ↓
[Action] search_documents(query)
    ↓
[Observation] 검색 결과 확인
    ↓
[Thought] "결과가 충분한가? / 부족한가?"
    ↓
  ┌─────────────────┐
  │ 충분함          │ 부족함
  ↓                 ↓
[답변 생성]      [Action] web_search(query)
                    ↓
                [Observation] 웹 검색 결과
                    ↓
                [답변 생성]
```

---

## 학습 효과 → 고객응대 에이전트 연결

| 학습 프로젝트 | 고객응대 에이전트 |
|-------------|-----------------|
| 문서 청킹/임베딩 | FAQ 데이터 임베딩 |
| Chroma 벡터 검색 | pgvector 검색 |
| 웹검색 Tool | 주문조회/환불처리 Tool |
| 검색결과 분기 | 의도분류 분기 |
| 출처 표시 | 답변 근거 제시 |

---

## 학습 리소스

### 필수 자료

| 자료 | URL | 용도 |
|------|-----|------|
| Anthropic - Building Effective Agents | https://www.anthropic.com/engineering/building-effective-agents | 에이전트 개념, 패턴 |
| LangGraph 공식 문서 | https://docs.langchain.com/oss/python/langgraph/workflows-agents | 구현 가이드 |
| Anthropic Cookbook | https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents | 코드 예제 |

### 참고 자료

| 자료 | URL | 용도 |
|------|-----|------|
| Prompt Engineering Guide | https://www.promptingguide.ai/techniques/react | ReAct 패턴 상세 |
| LangChain RAG Tutorial | https://python.langchain.com/docs/tutorials/rag/ | RAG 구현 |
| Chroma 공식 문서 | https://docs.trychroma.com/ | 벡터DB 사용법 |

---

## 확장 가능성

| 확장 기능 | 설명 | 추가 학습 |
|----------|------|----------|
| 멀티 문서 소스 | PDF, Notion, 웹페이지 동시 지원 | 문서 로더 확장 |
| 대화 기록 | 이전 대화 맥락 유지 | Memory 구현 |
| 자체 평가 | 답변 품질 스스로 검증 | Reflexion 패턴 |
| 복잡한 질문 처리 | 질문을 하위 질문으로 분해 | Plan-and-Execute |

---

## 완료 기준

- [ ] PDF/텍스트 파일 업로드 및 벡터 저장
- [ ] 문서 기반 Q&A 동작
- [ ] 웹 검색 Tool 동작
- [ ] 문서 검색 → 웹 검색 분기 처리
- [ ] 출처 표시 기능
- [ ] Streamlit UI 완성
- [ ] GitHub 저장소 정리 및 README 작성

---

## 메모

_학습 중 발생한 이슈나 인사이트를 여기에 기록_

