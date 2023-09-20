import os
from langchain.llms import LlamaCpp, OpenAI
from langchain.utilities import SQLDatabase
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from prompts import _CLOSEINSTRUCTION_TEMPLATE
from constants import *
from utils import ModelChooser, DatabaseManager

def main():
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])  # Initialize the callback manager
    MODEL_PATH = ModelChooser.choose_model()
    if MODEL_PATH=="gpt4":
        print("\nUsing OpenAI api key...\n")
        llm = OpenAI(temperature=0.0)
    elif MODEL_PATH=="ALL":
        #TODO rodar todos os modelos, precisamos quebrar a main
        pass
    else:
        llm = LlamaCpp(
            model_path=MODEL_PATH,
            callback_manager=callback_manager,
            verbose=True,
            temperature=0,
        )

    prompt = PromptTemplate(
            input_variables=["input","text1","text2","metavars"], template=_CLOSEINSTRUCTION_TEMPLATE # vars in string format 'key0:value0\nkey1:value1\n...\nkeyn:valuen
    )
    chain = LLMChain(llm=llm, prompt=prompt)

    conn_query, c_query = DatabaseManager.connect_to_db('db/queries.db')
    conn_analysis, c_analysis = DatabaseManager.connect_to_db('db/analysis.db')
    queries = DatabaseManager.execute_query(c_query)
    for id, query in queries:
        QUERY = {'input': query, 'metavars':metavars, 'text1':text1, 'text2':text2}
        response = chain.run(QUERY)
        DatabaseManager.update_analysis(c_analysis, id, response)
    conn_query.commit()
    conn_analysis.commit()
    c_query.close()
    c_analysis.close()

if __name__=='__main__':
    main()

if __name__=='__main__':
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])  # Initialize the callback manager
    MODEL_PATH = choose_model()
    if MODEL_PATH=="gpt4":
        print("\nUsing OpenAI api key...\n")
        llm = OpenAI(temperature=0.0)
    elif MODEL_PATH=="ALL":
        #TODO rodar todos os modelos, precisamos quebrar a main
    else:
        llm = LlamaCpp(
            model_path=MODEL_PATH,
            callback_manager=callback_manager,
            verbose=True,
            temperature=0,
        )

    prompt = PromptTemplate(
            input_variables=["input","text1","text2","metavars"], template=_CLOSEINSTRUCTION_TEMPLATE # vars in string format 'key0:value0\nkey1:value1\n...\nkeyn:valuen
    )
    chain = LLMChain(llm=llm, prompt=prompt)

    conn_query, c_query = connect_to_db('db/queries.db')
    conn_analysis, c_analysis = connect_to_db('db/analysis.db')
    queries = execute_query(c_query)
    for id, query in queries:
        QUERY = {'input': query, 'metavars':metavars, 'text1':text1, 'text2':text2}
        response = chain.run(QUERY)
        update_analysis(c_analysis, id, response)
    conn_query.commit()
    conn_analysis.commit()
    c_query.close()
    c_analysis.close()
