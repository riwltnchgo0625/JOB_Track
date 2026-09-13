from pathlib import Path
import re, json

index=Path('app/src/main/assets/index.html')
html=index.read_text(encoding='utf-8')

defaults=[
{"id":"knotz-automation-test-engineer-2026","company":"노츠","position":"자동화 테스트 엔지니어 (판교)","industry":"Software QA · Test Outsourcing · QA Automation","status":"지원 검토","interest":5,"fitScore":87,"website":"https://www.knotz.co.kr/","careersUrl":"https://m.saramin.co.kr/job-search/view?rec_idx=54965497","summary":"소프트웨어 테스트 전문기업. 자동화 테스트 직무는 현재 SQA 경험을 유지하면서 QA Automation 방향으로 확장하기 좋은 포지션.","business":"SW 테스트 아웃소싱·품질 컨설팅. Web/App, 임베디드, 영상보안, 전장, 의료 SW 등 다양한 도메인 프로젝트 수행.","finance":"2023 매출 약 98.7억, 2024 약 88.2억, 2025 약 93.9억. 2025년 흑자 전환.","competitors":"와이즈와이어즈, 인피닉, 와이즈스톤, 어니컴 등. 다양한 도메인 수행 경험이 강점이나 고객사 프로젝트 의존성은 확인 필요.","issues":"자동화 테스트 직군 지속 채용. Python 및 과거 공고의 Playwright·TypeScript·Docker·Node.js 기술 태그 확인.","jd":"경력 1년 이상 · Python · 자동화 테스트. 실제 자동화 코드 작성 비중, 프레임워크, CI/CD 연동 여부 확인 필요.","motivation":"1. AI/서비스 QA의 예외 검증 경험을 자동화 회귀 시나리오로 전환\n2. Python/Playwright/API 자동화 역량 확대\n3. 다양한 도메인에서 Technical QA 경험 확보","memo":"지원 추천 4.5/5. 자동화 코드 작성 비중과 고객사 상주 여부, 프로젝트 종료 후 재배치 방식 반드시 확인."},
{"id":"whitecube-challengers-qa-manager-2026","company":"화이트큐브","position":"QA Manager","industry":"IT Platform · Commerce · AdTech · B2C/B2B","status":"관심","interest":5,"fitScore":89,"website":"https://recruit.whitecube.co.kr/ko","careersUrl":"https://whitecube.ninehire.site/job_posting/wjkwZNoK","summary":"챌린저스 운영사 Product QA 포지션. 앱/웹·어드민·결제 플로우, Edge Case 발굴, QA 자동화 구축까지 포함.","business":"챌린저스 중심 B2C 제품 경험·커머스와 B2B 성과형 마케팅 사업. 일본 등 글로벌 확장.","finance":"2023 매출 약 57.1억, 2024 약 146.9억, 2025 약 273.5억. 고성장 중이나 2025 영업이익률은 하락.","competitors":"화해, 올리브영, 레뷰코퍼레이션 등과 일부 영역 경쟁. 행동·매출 성과를 연결하는 구조가 차별점.","issues":"카테고리 확장, 일본 진출, 성과형 마케팅 고도화, 신규 사업 실험. 높은 실행 속도와 DRI 문화.","jd":"Product QA · Test Plan · JIRA · Edge Case · QA DRI · QA 자동화 프로세스 구축/고도화.","motivation":"1. AI Agent 예외·실패조건 검증 경험\n2. 품질 판단 기준 정의 경험\n3. Manual QA에서 Automation까지 확장","memo":"지원 추천 4.5/5. 경력 연차와 실무 자동화 구축 경험이 주요 갭. 재공고 시 우선지원 후보."},
{"id":"winstechnet-qa-career-2026","company":"윈스테크넷","position":"품질보증(QA) - 경력","industry":"Cyber Security · Network Security · B2B/B2G","status":"지원 검토","interest":5,"fitScore":83,"website":"https://www.wins21.com/kor/main/main.html","careersUrl":"https://wins21.recruiter.co.kr/","summary":"네트워크 보안 솔루션 QA. TC 설계·유지보수, 개발 설계 리뷰, 테스트 전략 수립이 포함된 Technical QA.","business":"IPS, Anti-DDoS, 방화벽, APT, 보안관제, 클라우드 보안 사업.","finance":"재무 안정성은 비교적 높은 편이나 최근 성장 정체와 수익성 변동은 최신 공시 재확인 필요.","competitors":"안랩, 시큐아이, 이글루코퍼레이션 등. 네트워크 보안 제품과 공공·금융 레퍼런스가 강점.","issues":"AI 보안, 제로트러스트, 클라우드 보안, N2SF 대응 확대.","jd":"Security QA · Network · Linux · Test Design · Test Strategy. 네트워크/Linux 실무 역량 필요.","motivation":"1. 비정형 실패 검증을 보안 예외상황 검증으로 확장\n2. 품질 기준 정의 경험을 테스트 전략과 연결\n3. Technical QA/SDET 방향 강화","memo":"지원 추천 4/5. TCP/IP, Linux, Wireshark, Python/Shell 자동화 보강 필요."},
{"id":"winstechnet-qa-2026","company":"윈스테크넷","position":"품질보증(QA/QC) - 신입","industry":"Cyber Security · Network Security · B2B/B2G","status":"지원 검토","interest":5,"fitScore":88,"website":"https://www.wins21.com/kor/main/main.html","careersUrl":"https://wins21.recruiter.co.kr/","summary":"코스닥 상장 사이버보안 기업의 신입 QA/QC. 기존 QA 실무 경험을 강점으로 활용하기 좋은 Technical QA 포지션.","business":"유지관리·보안관제·컨설팅, 보안제품, 클라우드 보안/MSP가 주요 사업.","finance":"2023 매출 1,069억/영업이익 231억, 2024 1,015억/204억, 2025 986억/212억.","competitors":"안랩, 시큐아이, 이글루코퍼레이션 등. IPS·DDoS 네트워크 보안 기술과 고객 레퍼런스 강점.","issues":"SNIPER AIVAX, N2SF, 제로트러스트, AI 보안관제, 클라우드 MSP 확대.","jd":"OS/네트워크 기본지식 · SW 테스팅 · TC 설계/수행 · 개발 설계 리뷰 · 테스트 전략 · Shift-Left.","motivation":"1. 복잡한 실패조건 구조화 경험\n2. 품질 판단 기준 정의 경험\n3. 서비스 QA를 네트워크/보안 Technical QA로 확장","memo":"지원 추천 4.5/5. 네트워크/Linux 기본기와 패킷 분석 실습 우선 보강."},
{"id":"toss-securities-qa-manager-2026","company":"토스증권","position":"QA Manager","industry":"FinTech · 증권 · B2C","status":"지원 검토","interest":5,"fitScore":82,"website":"https://www.tossinvest.com/","careersUrl":"https://toss.im/career","summary":"사일로와 함께 제품 A to Z 품질을 책임지는 Product QA. 빠른 이터레이션 환경에서 Risk Based Testing과 품질문화 개선이 핵심.","business":"모바일 중심 B2C 증권 서비스. 주문·체결·잔고·환전·실시간 상태 등 높은 신뢰성 요구.","finance":"서비스 규모와 거래 복잡도가 빠르게 커지는 성장 기업. 지원 전 최신 공시 재확인 필요.","competitors":"키움증권, 미래에셋증권, 삼성증권, 카카오페이증권 등. 모바일 UX와 빠른 제품 개선이 차별점.","issues":"QA를 개발 후 검수 단계가 아니라 사일로 초기부터 참여시키고 품질 문화를 내재화하는 방향.","jd":"Product QA · Agile · Silo · B2C · Risk Based Testing · Quality Improvement. 소프트웨어 QA 2년 이상 요건.","motivation":"1. B2C 사용자 관점 QA\n2. 비정형 실패 구조화 경험\n3. 품질 기준과 Metric 정의 경험","memo":"지원 추천 4/5의 Stretch Application. 2년 이상 경력 요건이 가장 큰 리스크."},
{"id":"codit","company":"코딧 (CODIT)","position":"QA / SQA","industry":"AI SaaS · RegTech","status":"지원 검토","interest":4,"fitScore":90,"website":"https://thecodit.com/","careersUrl":"https://codit.career.rivers.co.kr/","summary":"AI 기반 법률·규제·정책 데이터를 분석하는 B2B SaaS 기업.","business":"B2B SaaS · ChatCODIT · B2G 규제 서비스 · 글로벌 정책 데이터","finance":"2023 매출 약 6억 원\n2024 매출 약 7.2억 / 영업손실 약 9.2억\n2025 매출 약 20.4억 / 영업이익 약 2억","competitors":"FiscalNote, Quorum 대비 국내 정책 데이터와 RegTech 초기 선점이 강점","issues":"ChatCODIT 출시 · AI Policy Agent 강화 · B2G 확대 · 글로벌 데이터 확대","jd":"Frontend/Backend QA · 요구사항 분석 · Test Plan · TC · Jira · QA 프로세스 개선 · Python · 생성형 AI","motivation":"1. AI 챗봇 검증 경험 연결\n2. 품질 기준 정의 경험 강조\n3. 법·규제 AI의 정확성과 신뢰성 관점","memo":"지원 전 QA팀 인원, 자동화 수준, 연봉, 업무강도 확인"}
]

# version label
html=html.replace('기업 분석과 지원 현황</div>','기업 분석과 지원 현황 · v1.9</div>',1)

# replace initial sample/default storage block
pattern=r"const K='jobtrack-v1'; const sample=\{.*?\}; let a=JSON\.parse\(localStorage\.getItem\(K\)\|\|'null'\)\|\|\[sample\]; for\(const c of a\)\{if\(c\.id==='codit'\)\{c\.website=c\.website\|\|sample\.website;c\.careersUrl=c\.careersUrl\|\|sample\.careersUrl\}\}"
replacement="const K='jobtrack-v1'; const defaults="+json.dumps(defaults,ensure_ascii=False,separators=(',',':'))+"; let a=JSON.parse(localStorage.getItem(K)||'null')||defaults.map(x=>({...x}));"
html,n=re.subn(pattern,lambda _m: replacement,html,count=1,flags=re.S)
if n!=1:
    raise SystemExit('v1.9 default data patch target not found')

# add direct paste button alongside clipboard/file import
html=html.replace('<button class="secondary" onclick="importClipboard()">클립보드에서 가져오기</button><button class="secondary" onclick="document.getElementById(\'jsonFileInput\').click()">JSON 파일 선택</button>',
                  '<button class="secondary" onclick="importJ()">JSON 직접 붙여넣기</button><button class="secondary" onclick="importClipboard()">클립보드에서 가져오기</button><button class="secondary" onclick="document.getElementById(\'jsonFileInput\').click()">JSON 파일 선택</button>',1)

index.write_text(html,encoding='utf-8')

# version
gradle=Path('app/build.gradle')
g=gradle.read_text(encoding='utf-8')
g=re.sub(r'versionCode\s+\d+','versionCode 9',g,count=1)
g=re.sub(r"versionName\s+'[^']+'","versionName '1.9'",g,count=1)
gradle.write_text(g,encoding='utf-8')

# custom centered vector icon
drawable=Path('app/src/main/res/drawable')
drawable.mkdir(parents=True,exist_ok=True)
(drawable/'ic_jobtrack.xml').write_text('''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">
<path android:fillColor="#0B0F17" android:pathData="M0,0h108v108h-108z"/>
<path android:fillColor="#91BAFF" android:pathData="M30,22h48a8,8 0,0 1,8 8v56a8,8 0,0 1,-8 8h-48a8,8 0,0 1,-8 -8v-56a8,8 0,0 1,8 -8z"/>
<path android:fillColor="#0B0F17" android:pathData="M39,37h30v6h-30zM39,51h30v6h-30zM39,65h18v6h-18z"/>
<path android:fillColor="#0B0F17" android:pathData="M61,69l6,6 12,-14 4,4 -16,19 -10,-10z"/>
</vector>''',encoding='utf-8')

manifest=Path('app/src/main/AndroidManifest.xml')
m=manifest.read_text(encoding='utf-8')
m=m.replace('<application android:allowBackup="true" android:label="이직로그" android:theme="@style/Theme.JobTrack">',
            '<application android:allowBackup="true" android:label="이직로그" android:icon="@drawable/ic_jobtrack" android:roundIcon="@drawable/ic_jobtrack" android:theme="@style/Theme.JobTrack">',1)
manifest.write_text(m,encoding='utf-8')

print('Applied JOB_Track v1.9 patch')
