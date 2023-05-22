import os

import guidance
import openai

from logger import get_logger

logger = get_logger(__name__)

openai_api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = openai_api_key
summary_llm = guidance.llms.OpenAI('gpt-3.5-turbo', caching=False)


def llm_summerize(document):
    summary = guidance("""
{{#system~}}
You are a world best summarizer. \n
Condense the text, capturing essential points and core ideas. Include relevant \
examples, omit excess details, and ensure the summary's length matches the \
original's complexity.
{{/system~}}
{{#user~}}
Summarize the following text:
---
{{document}}
{{/user~}}

{{#assistant~}}
{{gen 'summarization' temperature=0.2 max_tokens=100}}
{{/assistant~}}
""", llm=summary_llm)

    summary = summary(document=document)
    logger.info('Summarization: %s', summary)
    return summary['summarization']


def llm_evaluate_summaries(question, summaries, model):
    if not model.startswith('gpt'):
        logger.info(
            f'Model {model} not supported. Using gpt-3.5-turbo instead.')
        model = 'gpt-3.5-turbo'
    logger.info(f'Evaluating summaries with {model}')
    evaluation_llm = guidance.llms.OpenAI(model, caching=False)
    evaluation = guidance("""
{{#system~}}
You are a world best evaluator. You evaluate the relevance of summaries based \
on user input question. Return evaluation in following csv format, csv headers \
are [summary_id,document_id,evaluation,reason].
Evaluator Task
- Evaluation should be a score number between 0 and 5.
- Reason should be a short sentence within 20 words explain why the evaluation.
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
{{#each summaries}}
Summary
    summary_id: {{this.id}}
    document_id: {{this.document_id}}
    evaluation: ""
    reason: ""
    Summary Content: {{this.content}}
    File Name: {{this.metadata.file_name}}
{{/each}}
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
