import csv
import functools
import json
import sys

def handel_error(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try: return function(*args, **kwargs)

        except ValueError as error:
            print(f"입력값 오류: {error}")
            print("입력값을 다시 확인해주세요.")
            sys.exit(1)

        except FileNotFoundError as error:
            print(f"파일을 찾을 수 없습니다: {error.filename}")
            print("파일 경로를 확인해주세요.")
            sys.exit(1)

        except PermissionError:
            print("파일 접근 권한이 없습니다.")
            print("파일 권한을 확인해주세요.")
            sys.exit(1)

        except UnicodeDecodeError:
            print("파일 인코딩을 읽을 수 없습니다.")
            print("UTF-8 형식의 파일인지 확인해주세요.")
            sys.exit(1)

        except csv.Error as error:
            print(f"CSV 파일 오류: {error}")
            print("CSV 형식과 컬럼을 확인해주세요.")
            sys.exit(1)

        except json.JSONDecodeError:
            print("JSONL 파일 형식이 올바르지 않습니다.")
            print("데이터 파일이 손상되었는지 확인해주세요.")
            sys.exit(1)

        except KeyError as error:
            print(f"필수 데이터가 없습니다: {error}")
            print("데이터 컬럼을 확인해주세요.")
            sys.exit(1)

        except OSError as error:
            print(f"파일 처리 오류: {error}")
            print("파일 경로와 권한을 확인해주세요.")
            sys.exit(1)

        except Exception as error:
            print(f"예상하지 못한 오류가 발생했습니다: {error}")
            sys.exit(1)

    return wrapper