from llama_index import SimpleDirectoryReader, GPTListIndex, readers, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
import os
os.environ["OPENAI_API_KEY"] = "Your API KEY HERE"

def construct_index(directory_path):
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_outputs = 2000
    # set maximum chunk overlap
    max_chunk_overlap = 20
    # set chunk size limit
    chunk_size_limit = 600 

    # define LLM
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo", max_tokens=2000))

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
 
    documents = SimpleDirectoryReader(directory_path).load_data()
    
    index = GPTSimpleVectorIndex(
        documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper
    )

    index.save_to_disk('grugg.json')

    return index

def ask_ai():
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="text-davinci-003", max_tokens=2000))

    index = GPTSimpleVectorIndex.load_from_disk('grugg.json')
    while True: 
        user_input = input("What learns do you want from GruggBot? ")
        query = "You are pretending to be a senior developer Grugg.  Grugg has a funny way of speaking (sort of like a cave man) I want all your answers to resemblel Gruggs natural speaking patterns. Pretend you are a senior Grugg, giving younger gruggs advice. The following will be the junior grugg's question: " 
        response = index.query(query + user_input, llm_predictor=llm_predictor, response_mode="compact")
        print(response)

#construct_index("d:\\AI\\git\\langchain\\grugg")
ask_ai()