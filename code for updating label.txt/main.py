import json
from fuzzywuzzy import fuzz

def fix_text(wrong_text, correct_text):
    # Save text before fixing
    # with open('wrong_text', 'w', encoding='utf-8') as f:
    #     for s in wrong_text:
    #         f.write(s + '\n')

    i = -1
    for index in range(len(wrong_text)):
        #Exception
        if (len(wrong_text[index]) < 15): continue

        i += 1
        attempts = -5
        while (i + attempts < len(correct_text) 
               and fuzz.ratio(wrong_text[index], correct_text[max(0, i + attempts)]) < 50
               and attempts < 50):
            attempts += 1
        if (attempts >= 50): 
            print("Ignore: ", index + 1, i + 1)
            continue

        i += attempts
        if (i >= len(correct_text)): break

        # if (index > 1990 and index < 2000):
        #     print(index + 1, i + 1) 
        #     print(index, wrong_text[index])
        #     print(i, correct_text[i])
        #     print('---------------\n')
        
        wrong_text[index] = correct_text[i]   
    
    return wrong_text

def create_new_label_txt(label_txt='Label.txt', new_jsons=None):
    page = new_jsons[0]["page"]
    page_jsons = []
    index = 0
    while (True):
        cur_page_json = []
        while(index < len(new_jsons)):
            j = new_jsons[index]
            if j["page"] == page:
                del j["page"]
                cur_page_json.append(j)
                index += 1
            else:
                page += 1
                break
        page_jsons.append(cur_page_json)
        if (index >= len(new_jsons)): break

    #Write Label.txt
    filenames = []
    with open(label_txt, "r", encoding="utf-8") as f:
        for line in f:
            filename, _ = line.split('[', 1)
            filenames.append(filename)

    with open('NewLabel.txt', "w", encoding="utf-8") as f:
        for i in range(len(filenames)):
            f.write(filenames[i] + json.dumps(page_jsons[i], ensure_ascii=False) + "\n")
        
    print(f"Generated NewLabel.txt with {len(filenames)} pages!")

def main_func(label_txt='Label.txt', correct_txt='correct_text.txt', start_page=5, end_page=147):
    # Read Label.txt --> json_data ------------------------
    json_data = []
    with open(label_txt, "r", encoding="utf-8") as f:
        page = start_page - 1
        for line in f:
            page += 1
            line = line.strip()
            filename, json_text = line.split('[', 1)
            page_json = json.loads('[' + json_text)
            for j in page_json:
                j["page"] = page
            json_data.extend(page_json)

    # Read correct text file .txt --------------------------
    correct_text = []
    with open(correct_txt, "r", encoding="utf-8") as f:
        correct_text = [line.strip() for line in f]

    # Match wrong text with correct text -------------------
    json_text = [j["transcription"] for j in json_data] 
    fixed_text = fix_text(json_text, correct_text)
    
    # Update Label.txt -------------------------------------
    for i in range(len(json_data)):
        json_data[i]["transcription"] = json_text[i]
    
    # with open('new_jsons.json', 'w', encoding='utf-8') as g:
    #     json.dump(json_data, g, ensure_ascii=False, indent=4)
    
    create_new_label_txt(label_txt=label_txt, new_jsons=json_data)

if __name__ == "__main__":
    # Hàm này sẽ tạo một file NewLabel.txt (đã chỉnh sửa)
    main_func(label_txt='Label.txt', correct_txt='correct_text.txt')  
