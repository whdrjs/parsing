import json
import os
from datetime import datetime

# 감탄사 걸러내기
def filter_exclamations(text):
    words = text.split()
    filtered_words = [word for word in words if not (len(word) == 1 or (len(word) <= 3 and ('~' in word or '.' in word)))]
    return ' '.join(filtered_words)

# JSON 데이터를 파이썬 딕셔너리로 변환
file_name = "SBRW1900009199.json"
with open(file_name, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 화자 정보를 저장하는 딕셔너리 생성
speaker_info = {}
speaker_count = {}
for speaker in data['document'][0]['metadata']['speaker']:
    speaker_id = speaker['id']
    occupation = speaker['occupation']
    sex = speaker['sex']

    key = f"{occupation}/{sex}"

    # 동일한 occupation과 sex를 가진 화자 수를 계산하고 저장
    if key not in speaker_count:
        speaker_count[key] = 1
    else:
        speaker_count[key] += 1

    # 발화자 정보에 고유한 표시 추가
    speaker_info[speaker_id] = f"{key} {speaker_count[key]}"

# 결과를 output 폴더에 txt 파일로 저장
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

current_time = datetime.now().strftime("%m-%d-%H-%M")
output_file = os.path.join(output_dir, f"{file_name}_{current_time}.txt")

with open(output_file, 'w', encoding='utf-8') as f:
    for utterance in data['document'][0]['utterance']:
        speaker_id = utterance['speaker_id']
        form = utterance['form']

        if not form.strip():
            continue

        # 미리 알 수 없는 화자 정보 처리
        if speaker_id not in speaker_info:
            speaker_info[speaker_id] = "unknown/unknown"

        speaker = speaker_info[speaker_id]

        # 감탄사 걸러내기
        filtered_form = filter_exclamations(form)

        # 출력 줄 작성
        output_line = f"{speaker}: {filtered_form.strip()}"

        # 빈 줄이 아닌 경우에만 출력
        if filtered_form.strip():
            f.write(output_line + "\n")