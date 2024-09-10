from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

load_dotenv()
llm = ChatGroq(model='llama-3.1-8b-instant')

# Verification for article
def seed_related(title):
    prompt_template = """
        You are an expert news segregator.
        Your job is to look at a news article title and decide if it is related to new funding to a company.
        Acquisition is not considered to be related.
        If the title is related, say 'yes' else say 'no'.
        Only give 'yes' or 'no' as the answer.

        Example:
        Title-Odigos Raises $13M in Funding.
        Output-yes

        Title-Execupay Acquires Professional Payroll.
        Output-no

        Title-Superluminal Medicines Closes $120M Series A Funding.
        Output-yes

        Now, give output for the following title,
        Title-{title}
        Output-
    """
    prompt = PromptTemplate(
        input_variables=['title'],
        template=prompt_template
    )

    chain = prompt | llm
    response = chain.invoke(title).content
    print(f"{title}:{response}")
    return True if response=='yes' else False

# Class to define the output structure
class Data(BaseModel):
    company_name: str = Field("Name of the Company that recieved the funding.")
    sector: str = Field("The broad sector that the company provides their services in.")
    summary: str = Field("A one line summary about what the company does")
    amount: str = Field("The amount of money the company recieved in funding")

# Data extraction function
def extractor(data):
    prompt_template = """
        You are a data extractor bot.
        Your job is to extract the following details from the data provided to you:
            - Company Name
            - Sector
            - Summary
            - Amount
        If you are unsure of the value in a particular field, just generate a <None> token.
        {format_instructions}
        Extract the fields from the following data: {data}
    """
    parser = JsonOutputParser(pydantic_object=Data)

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=['data'],
        partial_variables={'format_instructions': parser.get_format_instructions()}
    )
    chain = prompt | llm | parser
    response = chain.invoke({'data': data})
    return response

if __name__ == '__main__':
    with open('content.txt') as f:
        data = f.read()
    print(extractor(data))