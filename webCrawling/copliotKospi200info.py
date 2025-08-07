import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_kospi200_data(page=1):
    url = f"https://finance.naver.com/sise/entryJongmok.naver?&page={page}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    
    # 데이터를 저장할 리스트
    stock_data = []
    
    # 종목 테이블 찾기
    table = soup.find("table", class_="type_1")
    if table:
        rows = table.find_all("tr")[2:]  # 헤더와 빈 줄 제외
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 7:  # 유효한 데이터 행인 경우
                # 종목 코드 추출
                code = cols[0].find('a')['href'].split('=')[-1]
                
                # 데이터 추출
                name = cols[0].get_text(strip=True)
                price = cols[1].get_text(strip=True)
                change = cols[2].find("span").get_text(strip=True)
                rate = cols[3].find("span").get_text(strip=True)
                volume = cols[4].get_text(strip=True)
                trading_value = cols[5].get_text(strip=True)
                market_cap = cols[6].get_text(strip=True)
                
                # 상승/하락 여부 확인
                is_up = "상승" in cols[2].find("em")["class"][1]
                change_direction = "+" if is_up else "-"
                
                stock_data.append({
                    '종목코드': code,
                    '종목명': name,
                    '현재가': price,
                    '전일비': f"{change_direction}{change}",
                    '등락률': rate,
                    '거래량': volume,
                    '거래대금': trading_value,
                    '시가총액': market_cap
                })
                
    return stock_data

# 첫 페이지 데이터 수집
stocks = get_kospi200_data()

# 데이터프레임으로 변환
df = pd.DataFrame(stocks)
if not df.empty:
    print("\n=== 코스피200 편입종목 상위 데이터 ===")
    print(df.to_string(index=False))
    
    # CSV 파일로 저장
    df.to_csv('kospi200_top_stocks.csv', index=False, encoding='utf-8-sig')
    print("\n데이터가 kospi200_top_stocks.csv 파일로 저장되었습니다.")
else:
    print("데이터를 가져오는데 실패했습니다.")