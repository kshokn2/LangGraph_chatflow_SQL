# LangGraph_chatflow_SQL
LangGraph를 이용해서 SQL 쿼리 기반의 Workflow를 구현합니다.


### 프로젝트 설정하기

python에 대해서
- python libraries 설정은 requirements.txt를 참고해서 설치. (`pip freeze > requirements.txt`)

api key들의 설정에 대해서
- 프로젝트 최상위 레벨에 .env 파일을 생성
    ```GOOGLE_API_KEY="my_gemini_api_key"
    LANGSMITH_TRACING="true"
    LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
    LANGSMITH_API_KEY="my_langsmith_api_key"
    LANGSMITH_PROJECT="my_langsmith_project_name"
    ```

### Workflow 테스트

planner 하기 전 supervisor까지 테스트 파일: my_agent_test.ipynb   
planner된 테스트 파일: my_agent_test_0714.ipynb

### streamlit 테스트
streamlit run streamlit_app.py
