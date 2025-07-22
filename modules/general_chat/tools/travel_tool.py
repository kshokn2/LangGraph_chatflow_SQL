from langchain_core.tools import tool

@tool
def get_city_activities(city: str) -> str:
    """주어진 도시에서 할 수 있는 추천 활동 목록을 반환합니다."""
    if not city:
        return "도시 이름을 알려주세요."
    # 실제 API 대신 더미 데이터 사용
    if city.lower() == "paris":
        return f"{city}에서는 에펠탑 방문, 루브르 박물관 관람, 세느강 유람선 타기를 추천합니다."
    elif city.lower() == "london":
        return f"{city}에서는 런던 아이 탑승, 대영 박물관 방문, 버킹엄 궁전 근위병 교대식 보기를 추천합니다."
    else:
        return f"{city}에서는 맛집 탐방과 현지 문화 체험을 즐겨보세요!"