# 1. 문서 개요
> 본 프로젝트는 용돈 기입장 프로그램입니다.

# 2. 실행 방법
```bash
python -m budget_app [명령어] [옵션]
```

# 3. 명령어 목록
```bash
add                      - 거래 내역 추가
list                     - 거래 내역 조회
detail [id]              - 거래 내역 상세 조회
update [id]              - 거래 내역 수정
delete [id]              - 거래 내역 삭제
category list            - 카테고리 조회
category add [name]      - 카테고리 추가
category remove [name]   - 카테고리 삭제
budget set               - 월별 예산 설정
summary                  - 월별 거래 요약
search                   - 거래 내역 검색
import                   - CSV 파일 가져오기
export                   - CSV 파일 내보내기
```

# 4. 테스트 명령어

```bash
# transaction 추가 (카테고리로 인해 추가 x)
python -m budget_app add

# category list 확인
python -m budget_app category list

# category food, test 추가
python -m budget_app category add food
python -m budget_app category add test

# category 추가 확인
python -m budget_app category list

# transaction 추가
python -m budget_app add

# transaction 추가 확인
python -m budget_app list
python -m budget_app list --limit 5

# transaction 미리 생성된 6 종류 더 추가 (import)
python -m budget_app import --from test.py    # csv 파일 X
python -m budget_app import --from test.csv   # 경로를 찾을 수 없는 파일
python -m budget_app import --from result.csv # 없는 카테고리
python -m budget_app import --from result.csv # 정상 추가

# transaction 추가 확인
python -m budget_app list

# 추가된 transaction까지 포함해서 csv 파일로 export
python -m budget_app export --out result.csv --month 2026-09   # 26년 9월의 거래내역 export
python -m budget_app export --out result.csv --from 2026-09-15 # 26년 9월 15일 부터의 거래내역 export
python -m budget_app export --out result.csv --to 2026-09-15   # 26년 9월 15일 까지의 거래내역 export

# transaction 수정
python -m budget_app update 1

# transaction 수정 확인
python -m budget_app list
python -m budget_app detail 1

# transaction 삭제
python -m budget_app delete 1

# transaction 삭제 확인
python -m budget_app list

# 월별 예산 설정
python -m budget_app budget set --month 2026-09 --amount 100000

# 월별 거래 요약
python -m budget_app summary --month 2026-09         
python -m budget_app summary --month 2026-09 --top 5 

# 거래 내역 검색
python -m budget_app search --category food   # 카테고리 검색
python -m budget_app search --type expense    # 거래 유형 검색
python -m budget_app search --q haha          # 메모 검색
python -m budget_app search --tag morning     # 태그 검색
python -m budget_app search --from 2026-09-19 # 2026-09-15 부터의 거래내역 검색
python -m budget_app search --to 2026-09-19   # 2026-09-15 까지의 거래내역 검색
```

# 5. 파일 경로
```bash
B2-2. Budget

|- budget_app
|-- __main__.py
|-- bridge.py
|-- cli.py
|-- decorator.py
|-- model.py
|-- repository.py
|-- service.py
|-- validate.py

|- data
|-- budgets.jsonl
|-- categories.jsonl
|-- transactions.jsonl

|- README.md
|- .gitignore

|- (import / export csv)
```

# 6. csv 스키마
```bash
# id는 충돌방지를 위해 사용 x
date,type,category,amount,memo,tags
```