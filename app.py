from gradio_client import Client

client = Client("cvachet/pdf-chatbot")
result = client.predict(
		message="what is the document about?",
		history=[],
		api_name="/conversation"
)
print(result)

# text='what is the office of Mgasa Lucas?'

# client = Client("freddyaboulton/gradiopdf")
# result = client.predict(
#     question=text,
#     # doc="https://gradio-builds.s3.amazonaws.com/assets/pdf-guide/fw9.pdf",
#     doc="staff.pdf",
#     api_name="/predict"
#             )

# print(result)


# from gradio_client import Client

# client = Client("cvachet/pdf-chatbot")
# result = client.predict(
# 		llm_option="Mistral-7B-Instruct-v0.2",
# 		llm_temperature=0.7,
# 		max_tokens=1024,
# 		top_k=3,
# 		api_name="/initialize_LLM"
# )
# print(result)


# from gradio_client import Client

# client = Client("MuntasirHossain/RAG-PDF-Chatbot")
# result = client.predict(
# 		message="Hello!!",
# 		history=[],
# 		api_name="/conversation"
# )
# print(result)

# from gradio_client import Client

# client = Client("bishmoy/Arxiv-CS-RAG")
# result = client.predict(
# 		"Hello!!",	# str  in 'parameter_13' Textbox component
# 		"mistralai/Mixtral-8x7B-Instruct-v0.1",	# Literal['mistralai/Mixtral-8x7B-Instruct-v0.1', 'mistralai/Mistral-7B-Instruct-v0.2', 'google/gemma-7b-it', 'None']  in 'LLM Model' Dropdown component
# 		True,	# bool  in 'Stream output' Checkbox component
# 		api_name="/ask_llm"
# )
# print(result)