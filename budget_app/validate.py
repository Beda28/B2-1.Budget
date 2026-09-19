from datetime import datetime

def validate_date(date: str) -> str:
    try  : datetime.strptime(date, "%Y-%m-%d")
    except ValueError: raise ValueError("날짜는 YYYY-MM-DD 형식이어야 합니다.")
    return date

def validate_month(month: str) -> str:
    try  : datetime.strptime(month, "%Y-%m")
    except ValueError: raise ValueError("월은 YYYY-MM 형식이어야 합니다.")
    return month

def validate_amount(amount: int) -> int:
    if     amount <= 0: raise ValueError("금액은 0보다 커야 합니다.")
    return amount

def validate_type(type: str) -> str:
    if     type not in ("income", "expense"): raise ValueError("type은 income 또는 expense만 사용할 수 있습니다.")
    return type

def validate_category_name(name: str) -> str:
    name = name.strip()

    if not name      : raise ValueError("카테고리명은 비어 있을 수 없습니다.")
    if len(name) > 50: raise ValueError("카테고리명은 50자 이하로 입력해주세요.")
    return name

def validate_memo(memo: str | None) -> str:
    if     memo is None: return ""
    if len(memo) > 200 : raise ValueError("메모는 200자 이하로 입력해주세요.")
    return memo

def validate_tags(tags: list[str] | None) -> list[str]:
    if tags is None: return []
    if not isinstance(tags, list): raise ValueError("tags는 리스트 형식이어야 합니다.")
    if     len(tags) > 20        : raise ValueError("태그는 최대 20개까지 입력할 수 있습니다.")

    for tag in tags:
        if not isinstance(tag, str): raise ValueError("태그는 문자열이어야 합니다.")
        if not tag.strip()         : raise ValueError("빈 태그는 사용할 수 없습니다.")
        if len(tag) > 30           : raise ValueError("태그는 30자 이내로 입력해주세요.")

    return [tag.strip() for tag in tags]

def validate_limit(limit: int | None) -> int | None:
    if limit is None: return None
    if limit <= 0   : raise ValueError("limit은 1 이상의 숫자여야 합니다.")
    return limit

def validate_top(top: int | None) -> int:
    if top is None: return 3
    if top <= 0   : raise ValueError("top은 1 이상의 숫자여야 합니다.")
    return top

def validate_id(id: int) -> int:
    if id <= 0: raise ValueError("ID는 1 이상의 숫자여야 합니다.")
    return id

def validate_date_range(
        date_from: str | None = None,
        date_to  : str | None = None
        ) -> tuple[str | None, str | None]:
    
    if date_from is not None: validate_date(date_from)
    if date_to   is not None: validate_date(date_to)
    if date_from is not None and date_to is not None:
        if date_from > date_to: raise ValueError("시작 날짜는 종료 날짜보다 늦을 수 없습니다.")

    return date_from, date_to

def validate_csv_file(file_path: str) -> str:
    if not file_path.strip()                 : raise ValueError("CSV 파일 경로를 입력해주세요.")
    if not file_path.lower().endswith(".csv"): raise ValueError("CSV 파일만 사용할 수 있습니다.")
    return file_path

def validate_export_condition(
        month    : str | None = None,
        date_from: str | None = None,
        date_to  : str | None = None
        ) -> tuple[str | None, str | None, str | None]:

    print(month)
    
    if  month     is None and (\
        date_from is None and \
        date_to   is None):
        raise ValueError("month, from + to 중 하나 이상 입력해야 합니다.")
    
    if month is not None: validate_month(month)
    validate_date_range(date_from, date_to)

    return month, date_from, date_to