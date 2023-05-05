# encoding=utf-8
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys


# input="本文转自"
# text_summary = pipeline(Tasks.text_generation, model='damo/nlp_palm2.0_text-generation_chinese-base')
# result = text_summary(input)
#
# print('输入文本:\n' + input + '\n')
# print('文本摘要结果:\n' + result[OutputKeys.TEXT])

def generate(input):
    text_summary = pipeline(Tasks.text_generation, model='damo/nlp_palm2.0_text-generation_chinese-base')
    result = text_summary(input)
    return result[OutputKeys.TEXT]
