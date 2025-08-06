import re

# 요청: 정규표현식의 패턴을 5살 아이도 이해할수 있도록 설명해주고 자세하게 한글로 주석도 추가해줘.

def is_valid_email(email):
    # 이메일이 맞는지 확인하는 아주 간단한 규칙(정규표현식)
    # 패턴 설명:
    # 1. 이메일의 앞부분에는 영어, 숫자, 점(.), 밑줄(_), 퍼센트(%), 더하기(+), 빼기(-)가 올 수 있어요.
    # 2. 그 다음에는 꼭 @가 있어야 해요.
    # 3. @ 뒤에는 영어, 숫자, 점(.), 빼기(-)가 올 수 있어요.
    # 4. 마지막에는 점(.)이 나오고, 그 뒤에 영어가 두 글자 이상 나와야 해요.
    # 예시: abcd@efg.com
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    # 이메일이 위 규칙에 맞으면 True, 아니면 False를 반환해요
    return re.match(pattern, email) is not None

# 테스트용 이메일 주소 10개
test_emails = [
    "test@example.com",           # 올바른 이메일
    "user.name@domain.co.kr",     # 올바른 이메일
    "invalid-email@",             # @ 뒤가 없어서 잘못된 이메일
    "another.user@domain.com",    # 올바른 이메일
    "user@domain",                # .com 같은 점(.)과 글자가 없어서 잘못된 이메일
    "user@domain.c",              # 마지막 글자가 한 글자라서 잘못된 이메일
    "user@domain.company",        # 올바른 이메일
    "user123@sub.domain.com",     # 올바른 이메일
    "user+tag@domain.org",        # 올바른 이메일
    "user@domain..com"            # 점(.)이 두 번 연속 나와서 잘못된 이메일
]

# 이메일 주소를 하나씩 검사해서 결과를 출력해요
for email in test_emails:
    result = "유효함" if is_valid_email(email) else "유효하지 않음"
    print(f"{email}: {result}")