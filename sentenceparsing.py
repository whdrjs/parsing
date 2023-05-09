import json

# JSON 데이터를 파이썬 딕셔너리로 변환
file_name = "SBRW1900014250.json"
with open(file_name, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 화자 정보를 저장하는 딕셔너리 생성
speaker_info = {}
for speaker in data['document'][0]['metadata']['speaker']:
    speaker_id = speaker['id']
    occupation = speaker['occupation']
    sex = speaker['sex']
    speaker_info[speaker_id] = f"{occupation}/{sex}"

# 각 화자별로 발화 내용을 저장하는 딕셔너리 생성
utterances = {}
for utterance in data['document'][0]['utterance']:
    speaker_id = utterance['speaker_id']
    form = utterance['form']

    if not form.strip():
        continue

    if speaker_id not in utterances:
        utterances[speaker_id] = []

    utterances[speaker_id].append(form)

# 결과 출력
for speaker_id, utterance_list in utterances.items():
    speaker = speaker_info[speaker_id]
    utterance_text = ' '.join(utterance_list)

    # 문장별로 분리하여 출력
    sentences = utterance_text.split('. ')
    for sentence in sentences:
        if sentence:
            print(f"{speaker}: {sentence.strip()}.")