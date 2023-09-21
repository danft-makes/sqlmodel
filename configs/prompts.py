_CLOSEINSTRUCTION_TEMPLATE="""BEGININPUT
BEGINCONTEXT
{metavars}
ENDCONTEXT
{text1}
ENDINPUT
{text2}
BEGININSTRUCTION
{input}
ENDINSTRUCTION
"""
_ALPACA_TEMPLATE="""Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{instruction}
Don't be verbose!

### Input
{input}

### Response:
"""
_SPIDER_TEMPLATE="""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\n\nConvert text to sql: {input} {db_info}\n\n### Response:\n\n"""
