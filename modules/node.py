# from models import * # llm
# from states import PlanExecute

# def chatbot(state: PlanExecute):
#     prompt = ChatPromptTemplate.from_messages(
#             [
#                 ("system", pe),
#                 MessagesPlaceholder(variable_name="messages"),
#                 (
#                     "system",
#                     "Given the conversation above, determine who should act next or if the conversation should FINISH.\n"
#                     "If the previous agent's response indicates missing context, an inability to proceed, or a request for clarification,"
#                     "then respond with FINISH.\n"
#                     "Select one of: {options}\n"
                    
#                     "Examples of 'FINISH' responses include:\n"
#                     "- 죄송합니다. 답변을 하기위한 필요한 정보가 주어지지 않았습니다.\n"
#                     "- 정확한 답변을 하려면 추가적인 정보가 필요합니다.\n"
#                     "- 입력된 데이터가 부족하여 분석을 수행할 수 없습니다."
#                 ),
#             ]
#         )

#     # 메시지 호출 및 반환
#     return {"messages": [llm_with_tools.invoke(state["messages"])]}