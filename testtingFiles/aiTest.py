import gpt4all


gptj = gpt4all.GPT4All("ggml-gpt4all-j-v1.3-groovy")

while True:
	message = input(">")
	messages = [{"role": "user", "content": message}]
	gptj.chat_completion(messages)