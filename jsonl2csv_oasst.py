import json
import csv
from datetime import datetime

# 현재 시각을 문자열로 변환
current_time = datetime.now().strftime('%m-%d-%H%M')

# JSONL 파일 경로와 출력할 CSV 파일 경로를 지정하세요
input_file_path = '.jsonl'
output_file_path = f'/Users/.../t_{current_time}.csv'

# JSONL 파일을 읽어들이는 함수
def read_jsonl_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            yield json.loads(line)

# JSONL 데이터를 CSV로 변환하는 함수
def convert_jsonl_to_csv(input_file_path, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['대화 번호', '번호', '질문', '답변'])  # 헤더 작성

        conversation_idx = 1
        line_idx = 1
        question = ''
        answer = ''
        last_speaker = None
        for item in read_jsonl_file(input_file_path):
            # 새로운 대화에 대해 빈 행을 추가하고 대화 번호를 증가시킵니다.
            if line_idx != 1:
                csv_writer.writerow([])
                conversation_idx += 1

            text = item['text']
            lines = text.split('\n')
            for line in lines:
                if ': ' not in line:
                    if last_speaker == '질문' or last_speaker =='P':
                        question += ' ' + line
                    elif last_speaker == 'A':
                        answer += ' ' + line
                    continue

                speaker, content = line.split(': ', 1)
                if speaker == 'P' or speaker == '질문':
                    speaker = '질문'
                    question = content
                elif speaker == 'A':
                    speaker = 'A'
                    answer = content
                else:
                    print(f"Error: Invalid speaker name '{speaker}' at line {line_idx}. Skipping this line.")
                    continue

                last_speaker = speaker
                csv_writer.writerow([conversation_idx, line_idx, question, answer])
                line_idx += 1
                question = ''
                answer = ''


# 변환 실행
convert_jsonl_to_csv(input_file_path, output_file_path)