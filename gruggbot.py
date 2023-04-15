import asyncio
from dataclasses import dataclass
import os

from llama_index import SimpleDirectoryReader, GPTListIndex, readers, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI


# "text-ada-001" is significantly less costly than davinci
MODEL = os.environ.get("OPENAI_MODEL", "text-davinci-003")
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", 2000))


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


@dataclass
class Grugg:
    Thinking = object()
    llm_predictor: LLMPredictor
    index: GPTSimpleVectorIndex
    prompt: str = "You are pretending to be a senior developer Grugg.  Grugg has a funny way of speaking (sort of like a cave man) I want all your answers to resemblel Gruggs natural speaking patterns. Pretend you are a senior Grugg, giving younger gruggs advice. The following will be the junior grugg's question: " 
    brain = {}

    async def is_asked_with_brain(self, user_query: str) -> str:
        thought = self.brain.get(user_query)
        if thought is None:
            self.brain[user_query] = Grugg.Thinking
            try:
                thought = self.brain[user_query] = self.is_asked(user_query=user_query)
            except Exception as e:
                # let grug think about it later
                del self.brain[user_query]
                raise
        elif thought is Grugg.Thinking:
            await asyncio.sleep(1.0)
            return await self.is_asked_with_brain(user_query=user_query)
        return thought

    def is_asked(self, user_query: str) -> str:
        return self.index.query(self.prompt + user_query, llm_predictor=self.llm_predictor, response_mode="compact")

    @classmethod
    def load_from_disk(cls, filename: str = "grugg.json", **llm_predictor_args):
        if llm_predictor_args.get("llm") is None:
            llm_predictor_args["llm"] = OpenAI(temperature=0.5, model_name=MODEL, max_tokens=MAX_TOKENS)
        return cls(
            llm_predictor=LLMPredictor(**llm_predictor_args),
            index = GPTSimpleVectorIndex.load_from_disk(filename),
        )


def ask_ai():
    grugg = Grugg.load_from_disk("grugg.json")
    while True: 
        try:
            user_input = input("What learns do you want from GruggBot? ")
            response = grugg.is_asked(user_input)
            print(response)
        except (KeyboardInterrupt, EOFError):
            print()
            break


if __name__ == "__main__":
    #construct_index("d:\\AI\\git\\langchain\\grugg")
    ask_ai()
