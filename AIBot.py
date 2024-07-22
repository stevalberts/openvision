
import getpass
import os

from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv



#Load the details about bot Document
file_path = "openvission-from-kaggle.pdf"
loader = PyPDFLoader(file_path)

docs = loader.load()


### OpenAI ####
#Load the AIPKEY and the model 

load_dotenv()
api_key= os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o")

####ToagetheAI ####


#Load API_KEYS
# load_dotenv()
# TOGETHER_API_KEY= os.getenv("TOGETHER_API_KEY")

# from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(
#     base_url="https://api.together.xyz/v1",
#     api_key=TOGETHER_API_KEY,
#     model="mistralai/Mixtral-8x7B-Instruct-v0.1",
# )


#Load the text into vector store. 
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

retriever = vectorstore.as_retriever()

#Builld the rag_chain
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "Where possibele show the code that was used and also comment on its functionality"
    "When someone ask about the bot give a summarry of how the bot works"
    "When ask about the bot's creators, always mention about the creaters and share their github links as given in the document"
    "For thing that are outside the topic answer that you offer assisntance for the openvision bot and it usability"
    "Answer the quation related to the code snipest used in the documents"
    "the question. If you don't know the answer, say that you "
    "I dont have that information about the openvision bot. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)


question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

#results = rag_chain.invoke({"input": "what did nike make in 2012?"})
def get_ansewr(query):
    results = rag_chain.invoke({"input": f"{query}"})
    return results['answer']



#print(get_ansewr('what did nike make in 2023?'))
