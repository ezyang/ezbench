from evaluator import *

DESCRIPTION = "Without prompting, model should provide a correct and efficient implementation"

question = '''
Write a function called `unescape_attr_value` which unescapes this function:

def escape_attr_value(value: str) -> str:
    """
    Escape the attribute value by replacing backslashes and newline characters
    (plus other common whitespace, if desired) with their escaped forms.
    Order is important: first escape backslashes to avoid double conversion.
    """
    # Escape backslashes.
    value = value.replace('\\', '\\\\')
    # Escape newline, carriage return, and tab characters.
    value = value.replace('\n', '\\n')
    value = value.replace('\r', '\\r')
    value = value.replace('\t', '\\t')
    return value
'''

# Prompt engineering:
# - Write it with an explicit character by character for loop
# - Write it efficiently without for/while loop, using regex and a substitution function

test_case, answer = make_python_test([(r"unescape_attr_value(r'\\\n\r\t')", r'"\\\n\r\t"'),
                                      (r"unescape_attr_value(r'\\n\n')", r'"\\n\n"')])

TestUnescape = StringNode(question) >> LLMRun() >> ExtractCode(keep_main=False) >> (
    NotNode(RegexEvaluator(r'(for |while )')) &
    (PythonRun(test_case) >> SubstringEvaluator(answer))
)

if __name__ == "__main__":
    print(run_test(TestUnescape))
