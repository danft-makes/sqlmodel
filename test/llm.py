from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


class Agente:
    def __init__(self,MODEL_PATH):
        self.callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        self.MODEL_PATH = MODEL_PATH
        self.initialize_llm()

    def initialize_llm(self):
        self.llm = LlamaCpp(
            model_path=self.MODEL_PATH,
            callback_manager=self.callback_manager,
            verbose=True,
            temperature=0,
            max_tokens=750
        )

    def main(self):
        while True:
            QUERY = input('QUERY: ')
            response = self.llm(QUERY)
            print(response)


if __name__=='__main__':
    MODEL_PATH = '/home/shared/models/ggml/spider-skeleton-wizard-coder-ggml-q4_0.bin'
    agent = Agente(MODEL_PATH)
    agent.main()
