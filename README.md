# 1. 문서 개요
> 본 프로젝트는 용돈 기입장 프로그램입니다.

# 2. 실행 방법
```bash
python -m budget_app [명령어] [옵션]
```

# 3. 명령어 목록
```bash
add                      - 거래 기록을 추가합니다. [ 대화형 ]
list                     - 거래 기록을 모두 출력합니다.
detail [-id]             - id에 해당하는 거래내역을 가져옵니다.
update [-id]             - id에 해당하는 거래내역을 수정합니다. [ 대화형 ]
category [list]          - 카테고리 리스트를 출력합니다.
category [add] [name]    - name에 해당하는 카테고리를 추가합니다.
category [remove] [name] - name에 해당하는 카테고리를 삭제합니다.
```