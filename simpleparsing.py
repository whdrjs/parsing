import json

file_name = "SARW1800000001.json"

with open(file_name, "r", encoding="utf-8") as file:
    parsed_data = json.load(file)

utterances = parsed_data["document"][0]["utterance"]
speakers = {}

for utterance in utterances:
    speaker_id = utterance["speaker_id"]
    form = utterance["form"]

    if speaker_id not in speakers:
        speakers[speaker_id] = []
    speakers[speaker_id].append(form)

for speaker_id, forms in speakers.items():
    print(f"{speaker_id}: {' '.join(forms)}")