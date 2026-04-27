#!/usr/bin/env python3
"""UserPromptSubmit router for develop-workflow.

Emits a compact routing protocol only for backend development work. It avoids
CLAUDE.md duplication and does not call external models.
"""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Route:
    category: str
    agent: str
    skill: str
    reason: str


ROUTES: list[Route] = [
    Route("security", "security-reviewer", "security-review", "인증/인가, 접근 제어, 객체 권한, 인젝션, SSRF, 시크릿, 토큰, CORS/CSRF, 레이트 리밋, 민감정보 로깅 등 보안 위험"),
    Route("query", "persistence-query-specialist", "persistence-query-review", "Repository, SQL/JPQL/QueryDSL, JPA fetch, scalar FK, 관계 어노테이션 지양, 연결 엔티티, N+1, 인덱스, 페이지네이션, 데이터 접근 권한 등 영속성/쿼리 작업"),
    Route("api-contract", "api-contract-designer", "api-contract-design", "GraphQL, gRPC/protobuf, REST/OpenAPI, 요청/응답 DTO, 스키마, 하위 호환성 등 API 계약 설계"),
    Route("test", "backend-test-writer", "backend-test-strategy", "단위/통합/회귀/엣지 케이스/TDD/인가 경계 테스트 작성 또는 보강"),
    Route("migration", "migration-planner", "migration-adr", "DB 스키마, 데이터 이관, 스토리지 전환, 서비스 분리, 롤아웃/롤백, ADR이 필요한 마이그레이션"),
    Route("build", "build-validation-specialist", "build-validation", "Gradle, Maven, CI, 컴파일, 테스트 실패, 의존성, protobuf/generated source 검증"),
    Route("concurrency", "coroutine-concurrency-specialist", "spring-coroutine-concurrency", "Spring Boot + Kotlin coroutine, suspend, coroutineScope/supervisorScope, Dispatchers.IO, blocking IO, 경량 스레드, cancellation/timeout, thread/memory tradeoff"),
    Route("performance", "performance-reviewer", "performance-review", "응답 시간, 처리량, 캐시, 타임아웃, 재시도, 락, 메모리, 커넥션풀, 시스템 병목"),
    Route("review", "backend-reviewer", "review", "PR, diff, 코드리뷰, 감사, 머지 전 검토, 품질 게이트, 전반적 백엔드 리뷰"),
    Route("design", "backend-architect", "design", "백엔드 아키텍처, 서비스 경계, 도메인 모델, 트랜잭션, 권한 소유, 계층 설계"),
    Route("implement", "backend-coder", "implement", "더 적합한 전문 에이전트가 없고 실제 백엔드 코드 구현/수정이 필요한 작업"),
]

NON_BACKEND_PATTERNS = [
    r"\b(read|show|print|cat|open)\b.*\b(readme|license|changelog|package\.json)\b",
    r"\b(git log|git status|date|time|pwd|ls)\b",
    r"\b(frontend|css|html|figma|image|screenshot|presentation|spreadsheet)\b",
    r"\bskill\.md\b|\bskill authoring\b|\bskill pattern\b|\bbackend skill\b",
    r"README|리드미|라이선스|체인지로그",
    r"스킬|SKILL\.md|스킬화|스킬\s*작성|스킬\s*패턴|컨벤션\s*정리|개발\s*워크플로우\s*정리|reference\s*문서|상세\s*참조",
    r"프론트엔드|화면|UI|CSS|HTML|피그마|이미지|스크린샷|발표자료|스프레드시트|엑셀|문서",
    r"최근\s*커밋|현재\s*시간|현재\s*경로|파일\s*목록",
]

CATEGORY_PATTERNS: list[tuple[str, list[str]]] = [
    ("security", [r"\bsecurity\b", r"\bauth(orization|entication)?\b", r"\bcsrf\b", r"\bcors\b", r"\bssrf\b", r"\binjection\b", r"\bsecret\b", r"\btoken\b", r"\bjwt\b", r"\bcredential\b", r"\bpermission\b", r"\bprivilege\b", r"\bforbidden\b", r"\bunauthorized\b", r"\banother account\b", r"\banother user's data\b", r"\bcannot read another\b", r"보안|취약점?|취약|인증|인가|권한|접근\s*제어|객체\s*권한|권한\s*상승|권한\s*우회|토큰|JWT|쿠키|세션|CSRF|CORS|SSRF|인젝션|SQL\s*인젝션|시크릿|비밀키|자격\s*증명|개인정보|민감정보|민감\s*데이터|로깅|암호화|해시|레이트\s*리밋|속도\s*제한|탈취|우회|다른\s*계정|다른\s*사용자"]),
    ("migration", [r"\bmigrat(e|ion)\b", r"\bbackfill\b", r"\brollout\b", r"\brollback\b", r"\bstrangler\b", r"\bblue[- ]green\b", r"\bdynamodb\b", r"\bstorage\b", r"마이그레이션|전환|이관|백필|backfill|롤아웃|롤백|블루\s*그린|스트랭글러|DynamoDB|스토리지\s*전환|DB\s*전환|스키마\s*변경|데이터\s*이동|무중단"]),
    ("query", [r"\brepository\b", r"\bquerydsl\b", r"\bjpql\b", r"\bsql\b", r"\bjpa\b", r"\bhibernate\b", r"\bn\+1\b", r"\bindex\b", r"\bfetch join\b", r"\bpagination\b", r"\bfindall\b", r"\bmanytoone\b", r"\bonetomany\b", r"\bmanytomany\b", r"\bjoincolumn\b", r"\bscalar fk\b", r"\bforeign key\b", r"쿼리|레포지토리|리포지토리|저장소|영속성|JPA|하이버네이트|QueryDSL|JPQL|\bSQL\b|N\+1|페치\s*조인|fetch\s*join|인덱스|페이지네이션|페이징|정렬|필터|카운트|count|findAll|조회\s*(쿼리|성능|최적화)?|DB\s*(조회|부하|쿼리)|ManyToOne|OneToMany|ManyToMany|JoinColumn|관계\s*어노테이션|외래키|스칼라\s*FK|scalar\s*FK|FK\s*기반|명시\s*조인|연결\s*엔티티"]),
    ("concurrency", [r"\bcoroutine(s)?\b", r"\bsuspend\b", r"\bdispatchers?\.io\b", r"\bcoroutinescope\b", r"\bsupervisorscope\b", r"\basync\b", r"\bawait(all)?\b", r"\brunblocking\b", r"\bkotlin\s+flow\b", r"\bflowof\b", r"\bflow\s*[<{]", r"\bstructured concurrency\b", r"\bnon[- ]blocking\b", r"\bblocking io\b", r"코루틴|Coroutine|coroutineScope|supervisorScope|Dispatchers\.IO|런블로킹|runBlocking|비동기|동시성|경량\s*스레드|블로킹\s*IO|논블로킹|suspend|서스펜드|async|await|코틀린\s*Flow|structured\s*concurrency"]),
    ("performance", [r"\bperformance\b", r"\blatency\b", r"\bslow\b", r"\btimeout\b", r"\bretry\b", r"\bcache\b", r"\bredis\b", r"\bmemory\b", r"\block\b", r"\bthroughput\b", r"\btps\b", r"\bconnection pool\b", r"\bhikari\b", r"성능|응답\s*시간|응답이\s*\d+\s*초|지연|느림|느려|병목|처리량|TPS|캐시|Redis|타임아웃|재시도|락|락\s*경합|메모리|스레드|커넥션\s*풀|Hikari|부하|최적화|장애\s*전파"]),
    ("test", [r"\btest\b", r"\bjunit\b", r"\bmockito\b", r"\bmockk\b", r"\btdd\b", r"\bcoverage\b", r"\bregression\b", r"테스트|단위\s*테스트|유닛\s*테스트|통합\s*테스트|회귀\s*테스트|회귀|엣지|경계값|JUnit|Mockito|MockK|TDD|커버리지|테스트\s*커버|검증\s*케이스|실패\s*케이스"]),
    ("build", [r"\bgradle\b", r"\bmaven\b", r"\bci\b", r"\bcompile\b", r"\bbuild\b", r"\bdependency\b", r"\bprotobuf:build\b", r"\bktlint\b", r"\bdetekt\b", r"빌드|컴파일|Gradle|Maven|\bCI\b|파이프라인|의존성|dependency|protobuf|generated|생성\s*코드|ktlint|detekt|린트|정적\s*분석|깨졌|실패|테스트\s*실행"]),
    ("api-contract", [r"\bgraphql\b", r"\bgrpc\b", r"\bproto(buf)?\b", r"\bopenapi\b", r"\brest\b", r"\bendpoint\b", r"\bapi\b", r"\bschema\b", r"\brequest\b", r"\bresponse\b", r"\bdto\b", r"GraphQL|gRPC|Proto|Protobuf|OpenAPI|REST|API|스키마|엔드포인트|입출력|요청|응답|DTO|리졸버|Resolver|컨트랙트|계약|하위\s*호환|필드\s*추가|메서드\s*추가"]),
    ("review", [r"\breview\b", r"\bpr\b", r"\bdiff\b", r"\baudit\b", r"\bpre[- ]merge\b", r"리뷰|코드\s*리뷰|검토|검수|감사|\bPR\b|풀리퀘|머지\s*전|변경\s*사항|diff|품질\s*게이트"]),
    ("design", [r"\bdesign\b", r"\barchitecture\b", r"\bdomain model\b", r"\bboundary\b", r"\btransaction\b", r"\bservice design\b", r"\boop\b", r"\bsolid\b", r"\bdesign pattern(s)?\b", r"\bstrategy pattern\b", r"\btemplate method\b", r"\bstate pattern\b", r"\bspecification pattern\b", r"\badapter pattern\b", r"\bdecorator pattern\b", r"\bchain of responsibility\b", r"\bpipeline pattern\b", r"\bstatic factory\b", r"\bfactory method\b", r"\bcompanion object\b", r"\bcriteria pattern\b", r"\bcommand pattern\b", r"\bquery pattern\b", r"\bresult type\b", r"\blink entity\b", r"설계|아키텍처|도메인\s*모델|도메인|경계|서비스\s*경계|계층|레이어|트랜잭션|유스케이스|Use\s*Case|책임\s*분리|의존성\s*방향|모듈\s*구조|객체\s*지향|객체지향|디자인\s*패턴|전략\s*패턴|템플릿\s*메서드|상태\s*패턴|명세\s*패턴|정책\s*패턴|어댑터\s*패턴|데코레이터\s*패턴|책임\s*연쇄|파이프라인\s*패턴|정적\s*팩토리|팩토리\s*메서드|Command\s*패턴|Query\s*패턴|Criteria\s*패턴|Result\s*타입|연결\s*엔티티\s*설계"]),
    ("implement", [r"\bimplement\b", r"\bmodify\b", r"\bfix\b", r"\badd\b", r"\bcreate\b", r"\bupdate\b", r"\brefactor\b", r"구현|수정|추가|고쳐|고치|작성|생성|변경|업데이트|리팩터|리팩토링|버그\s*수정|기능\s*추가"]),
]

BACKEND_HINTS = [
    r"\bbackend\b", r"\bspring\b", r"\bkotlin\b", r"\bjava\b", r"\bservice\b",
    r"\bcontroller\b", r"\buse case\b", r"\bdatabase\b", r"\bmysql\b",
    r"\bpostgres\b", r"\bredis\b", r"\bkafka\b", r"\bapi\b", r"\bgraphql\b",
    r"\bgrpc\b", r"\bjpa\b", r"\brepository\b", r"\btransaction\b", r"\bcoroutine\b", r"\bsuspend\b",
    r"백엔드|서버|서버사이드|스프링|코틀린|자바|서비스|컨트롤러|유스케이스|데이터베이스|DB|레포지토리|리포지토리|트랜잭션|도메인|엔티티|JPA|QueryDSL|GraphQL|gRPC|API",
]


def load_input() -> dict:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {"prompt": raw}
    return data if isinstance(data, dict) else {}


def matches_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def classify(prompt: str) -> tuple[str, str]:
    text = " ".join(prompt.split())
    lowered = text.lower()

    if not text:
        return "non-backend", "빈 프롬프트"
    if matches_any(lowered, NON_BACKEND_PATTERNS):
        return "non-backend", "백엔드 작업이 아니거나 단순 조회/설명 요청으로 판단"
    if re.search(r"\b(add|implement|create|build)\b\s+(the\s+)?backend feature\b", lowered) or re.search(r"백엔드\s*(기능|작업).*(추가|구현|만들|작성|진행)", text):
        return "unclear", "백엔드 기능 요청이지만 대상 동작과 성공 기준이 부족함"
    if re.search(r"\b(pr|diff|pre[- ]merge)\b|풀리퀘|머지\s*전|변경\s*사항", text, re.IGNORECASE):
        return "review", "PR/diff/머지 전 변경 검토 요청"

    for category, patterns in CATEGORY_PATTERNS:
        if matches_any(lowered, patterns):
            return category, f"{category} 분류 키워드와 일치"

    if matches_any(lowered, BACKEND_HINTS):
        return "unclear", "백엔드 관련 신호는 있으나 범위가 불명확함"
    return "non-backend", "백엔드 라우팅 신호가 없음"


def route_for(category: str) -> Route | None:
    if category == "unclear":
        return Route("unclear", "backend-architect", "clarify-requirements", "백엔드 요청이지만 범위/성공 기준/대상 모듈이 불명확함")
    for route in ROUTES:
        if route.category == category:
            return route
    return None


def agent_lines() -> str:
    lines = []
    for route in ROUTES:
        lines.append(f"- {route.agent}: {route.reason}; 권장 skill `{route.skill}`")
    lines.append("- backend-architect: 백엔드 의도는 있으나 범위가 불명확하면 `clarify-requirements`와 함께 사용")
    return "\n".join(lines)


def main() -> None:
    data = load_input()
    prompt = data.get("prompt") or data.get("user_prompt") or data.get("message") or ""
    if not isinstance(prompt, str):
        prompt = str(prompt)

    category, reason = classify(prompt)
    route = route_for(category)
    if route is None:
        return

    project_dir = data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR", "")
    project_note = f"\n프로젝트 경로: {project_dir}" if project_dir else ""

    print(
        f"""지시: DEVELOP WORKFLOW ROUTING PROTOCOL

Step 0 - 먼저 요청을 분류:
- 분류: {category}
- 근거: {reason}
- 작업 유형: analysis | write/modify | test | design | planning | review
- 대상 구체성: specific | general | vague

Step 1 - 사용 가능한 develop-workflow 에이전트를 평가:
{agent_lines()}

Step 2 - 선택:
Step 0 결과상 다른 listed agent가 명확히 더 적합하지 않다면 `{route.agent}`를 사용.
non-backend 또는 단순 조회 요청이면 이 hook은 출력되지 않아야 하므로 위임하지 말 것.

Step 3 - skill 힌트와 함께 위임:
Task(subagent_type="{route.agent}", prompt=\"\"\"
<!-- skill: {route.skill} -->
작업 전 Skill 도구가 사용 가능하면 Skill({route.skill})을 먼저 활성화한 뒤 사용자 요청을 처리하세요.
사용자 요청:
{prompt}
\"\"\")

중요:
- 메인 세션에서 Skill을 호출한 뒤 위임하지 말 것. 로드된 skill 내용은 서브에이전트로 전달되지 않음.
- 선택된 서브에이전트가 위 힌트를 보고 자신의 skill을 직접 활성화해야 함.
- 분류가 unclear이고 성공 기준이 부족하면 수정하지 말고 짧게 확인 질문을 할 것.{project_note}
"""
    )


if __name__ == "__main__":
    main()
