import hashlib
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import SupabaseVectorStore
import streamlit as st
import openai
from supabase import Client, create_client
import guidance
from streamlit.logger import get_logger
from langchain.schema import Document


logger = get_logger(__name__)

openai_api_key = st.secrets.openai_api_key
openai.api_key = openai_api_key
summary_llm = guidance.llms.OpenAI('gpt-3.5-turbo')
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
supabase_url = st.secrets.supabase_url
supabase_key = st.secrets.supabase_service_key
supabase_client: Client = create_client(supabase_url, supabase_key)
summaries_vector_store = SupabaseVectorStore(
    supabase_client, embeddings, table_name="summaries")


def llm_summerize(document):
    summary = guidance("""
{{#system~}}
You are a world best summarizer.
{{/system~}}
{{#user~}}
Summarize the following document 
{{document}}
{{/user~}}

{{#assistant~}}
{{gen 'summarization' temperature=0.2 max_tokens=200}}
{{/assistant~}}
""", llm=summary_llm)

    summary = summary(document=document)
    logger.info('Summarization: %s', summary)
    return summary['summarization']


def llm_evaluate_summaries(question, summaries):
    model = st.session_state['model']
    if not model.startswith('gpt'):
        logger.info(
            f'Model {model} not supported. Using gpt-3.5-turbo instead.')
        model = 'gpt-3.5-turbo'
    logger.info(f'Evaluating summaries with {model}')
    evaluation_llm = guidance.llms.OpenAI(model)
    evaluation = guidance("""
{{#system~}}
You are a world best evaluator. You evaluate the relevance of summaries based on user input question.
Return evaluation in following csv format, csv headers are [summary_id, evaluation, reason].
Evaluator Task
- Evaluation should be a number between 0 and 5.
- Reason should be a short sentence within 20 words explain why.
---
Example
summary_id,document_id,evaluation,reason
1,4,3,"not mentioned about topic A"
2,2,4,"It is not relevant to the question"
{{/system~}}
{{#user~}}
Based on the question, do Evaluator Task for each summary.
---
Question: {{question}}
```json
{
    "question": "{{question}}",
    "summaries": [
    {{#each summaries}}
        {
            "id": {{this.id}},
            "summary": "{{this.content}}",
            "evaluation": "",
            "reason": "",
            "meta": "{{this.metadata.file_name}}",
            "document_id": {{this.document_id}}
        },
    {{/each}}
    ]
}
{{/user~}}
{{#assistant~}}
{{gen 'evaluation' temperature=0.2 stop='<|im_end|>'}}
{{/assistant~}}
""", llm=evaluation_llm)
    result = evaluation(question=question, summaries=summaries)
    evaluations = {}
    for evaluation in result['evaluation'].split('\n'):
        if evaluation == '' or not evaluation[0].isdigit():
            continue
        logger.info('Evaluation Row: %s', evaluation)
        summary_id, document_id, score, *reason = evaluation.split(',')
        if not score.isdigit():
            continue
        score = int(score)
        if score < 3 or score > 5:
            continue
        evaluations[summary_id] = {
            'evaluation': score,
            'reason': ','.join(reason),
            'summary_id': summary_id,
            'document_id': document_id,
        }
    return [e for e in sorted(evaluations.values(), key=lambda x: x['evaluation'], reverse=True)]


def compute_sha1_from_file(file_path):
    with open(file_path, "rb") as file:
        bytes = file.read()
        readable_hash = compute_sha1_from_content(bytes)
    return readable_hash


def compute_sha1_from_content(content):
    readable_hash = hashlib.sha1(content).hexdigest()
    return readable_hash


def create_embedding(content):
    return embeddings.embed_query(content)


def similarity_search(query, table='match_summaries', top_k=5, threshold=0.5):
    query_embedding = create_embedding(query)
    summaries = supabase_client.rpc(
        table, {'query_embedding': query_embedding,
                'match_count': top_k, 'match_threshold': threshold}
    ).execute()
    return summaries.data


def create_summary(document_id, content, metadata):
    logger.info(f"Summarizing document {content[:100]}")
    summary = llm_summerize(content)
    logger.info(f"Summary: {summary}")
    metadata['document_id'] = document_id
    summary_doc_with_metadata = Document(
        page_content=summary, metadata=metadata)
    sids = summaries_vector_store.add_documents(
        [summary_doc_with_metadata])
    if sids and len(sids) > 0:
        logger.info(f"Added summary with id {sids}")
        supabase_client.table("summaries").update(
            {"document_id": document_id}).match({"id": sids[0]}).execute()
