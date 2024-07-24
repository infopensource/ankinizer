from openai import OpenAI
import concurrent.futures
import os
import argparse

class Translator:
    def __init__(self, api_key='czywCRTzhPEky', base_url='https://ai.liaobots.work/v1'):
        self.client = OpenAI(
            api_key=api_key,  # 使用传入的api_key，如果没有则使用默认值
            base_url=base_url
        )
        self.file_lines = []
        self.output_lines = []
        self.translated_words = set()

    def read_file(self, file_path, output_file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            self.file_lines = content.splitlines()
        # Read existing translations to avoid redundant translations
        if os.path.exists(output_file_path):
            with open(output_file_path, 'r') as file:
                for line in file:
                    word = line.split(';')[0]
                    self.translated_words.add(word)
    
    def translate_line(self, line):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f'''
                        我会给你一个德语单词，这个单词是{line}，请你将它制作抽认卡，要求包括简单的例句展示用法，中文含义，以及用构词法助记。
                        格式要求：单词+半角分号(注意！一定不要全角符号)+词性(名词一律分为阴性阳性中性三种)和释义(如果这个词经过了变位则同时输出原型，这个词已经是原型则不再次输出；如果这个单词没有经过变位但是这个单词的变位不规则，输出变位置表，要求变位表用html的表格标签输出。同理，名词复数有特殊变形的也按照如上方法处理，形容词亦然)+<br>+例句（例句的中文翻译）+<br>+构词法或词源助记（不要凭空捏造牵强附会的解释）。
                        按照格式输出，不要有多余的内容。
                    '''
                }
            ],
            stream=True,
        )
        
        reply = ""
        for res in response:
            content = res.choices[0].delta.content
            if content:
                reply += content
        reply = reply.replace("\n", "").replace("  ", "")
        return reply

    def translate(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_line = {executor.submit(self.translate_line, line): line for line in self.file_lines if line not in self.translated_words}
            for future in concurrent.futures.as_completed(future_to_line):
                line = future_to_line[future]
                try:
                    result = future.result()
                    print(result)
                    self.output_lines.append(result)
                except Exception as exc:
                    print(f'Line {line} generated an exception: {exc}')
            
    def write_file(self, file_path):
        with open(file_path, 'a') as file:
            file.write("\n".join(self.output_lines))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translate words from a file using OpenAI API.')
    parser.add_argument('-i', '--input', help='Input file path.')
    parser.add_argument('-o', '--output', help='Output file path.')
    parser.add_argument('-k', '--apikey', help='Custom API key for OpenAI.')
    parser.add_argument('-u', '--baseurl', help='Custom base URL for OpenAI.')
    
    args = parser.parse_args()
    
    api_key = args.apikey if args.apikey != None else 'yKUxbcpmj8mtR'
    input_file = args.input if args.input != None else 'input.txt'
    output_file = args.output if args.output != None else 'output.txt'
    base_url='https://ai.liaobots.work/v1'

    
    t = Translator(api_key=api_key, base_url=base_url)
    t.read_file(input_file, output_file)
    t.translate()
    t.write_file(output_file)