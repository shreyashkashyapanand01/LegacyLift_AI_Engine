# from parsing.rag.refactor_engine.cleaner.code_cleaner import CodeCleaner

# dirty_code = """
# ```java

# public int sum(int a, int b) {

#     return a + b;


# }
# """

# print(CodeCleaner.clean(dirty_code))


from parsing.rag.refactor_engine.utils.code_utils import CodeUtils

code = "private int sum(int a, int b) {return a+b;} "

lang = CodeUtils.detect_language(code)
formatted, applied = CodeUtils.format_code(code, lang)

print(lang)
print(formatted)
print(applied)

# from parsing.rag.refactor_engine.utils.code_utils import CodeUtils

# code = """
# def sum(a,b):
#  return a+b
# """

# # detect language
# lang = CodeUtils.detect_language(code)

# # format
# formatted, applied = CodeUtils.format_code(code, lang)

# print("Language:", lang)
# print("\nFormatted Code:\n")
# print(formatted)
# print("\nFormatting Applied:", applied)