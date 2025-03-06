import requests
from openai import OpenAI
import torch
def get_aliyun_deepseek(instruction,inputs):
    client = OpenAI(
        api_key="sk-b24dd900bf1a43f9823ed32f2df3d49f", 
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    completion = client.chat.completions.create(
        model="deepseek-v3",  
        messages = [
            {"role": "system", "content": instruction},
            {"role": "user", "content": inputs},
        ]
    )
    print(completion)
    response = completion.choices[0].message.content
    return response

def get_deepseek_response(instruction, input):
    # Please install OpenAI SDK first: `pip3 install openai`
    print("get_deepseek_response_siliconflow")

    # siliconflow
    # 188
    # sk-eotrzevibhyamnthslaxmuzqvuemgsgwkiudtauwmfgwspyd
    # 150
    # sk-edhwfyoisrugijmmswudoogbcuslhfticskakzamwinlrftl
    client = OpenAI(api_key="sk-eotrzevibhyamnthslaxmuzqvuemgsgwkiudtauwmfgwspyd", base_url="https://api.siliconflow.cn/v1")
    response = client.chat.completions.create(
        model='deepseek-ai/DeepSeek-V3',
        messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": input},
            ],
        stream=False
    )



    # 正版deepseek

    # print("get_deepseek_response")
    # 19213150768
    # sk-ccf153b465d444219d808fd7e94acde4

    # 18812055801
    # sk-1ab8d8ce6fea4ec4aeb9009246e9e0ea


    # 13503259974
    # sk-f0fd919e450c44489143affa9ba7ed1e
    # client = OpenAI(api_key="sk-ccf153b465d444219d808fd7e94acde4", base_url="https://api.deepseek.com")

    # response = client.chat.completions.create(
    #     model="deepseek-chat",
    #     messages=[
    #         {"role": "system", "content": instruction},
    #         {"role": "user", "content": input},
    #     ],
    #     stream=False
    # )

    
    print(response)
    return response.choices[0].message.content

import json
def get_hauweiyun_deepseek(instruction,inputs):
    print("get_hauweiyun_deepseek")
    url = "https://infer-modelarts-cn-southwest-2.modelarts-infer.com/v1/infers/fd53915b-8935-48fe-be70-449d76c0fc87/v1/chat/completions"

    # Send request.
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer x0vWDS2P8Fiynwl4MvQKFQr8Yq_8d9Eg8Bg_QHphp9QTiHJD4xaJ37eM3L18f303s2ctMKjwlRNQWs94m9tREQ' 
    }
    data = {
        "model": "DeepSeek-V3",
        "messages": [
            {"role": "system", "content": instruction},
            {"role": "user", "content": inputs}
        ],
        "stream": False,
        "temperature": 1.0
    }
    resp = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

    # Print result.
    print(resp.status_code)
    return resp.json()['choices'][0]['message']['content']

def get_baidu_response(instruction,inputs):
    print("get_baidu_response")
    client = OpenAI(
        base_url='https://qianfan.baidubce.com/v2',
        api_key='bce-v3/ALTAK-SPe902TWvXSgJMYpQWUbE/fe4669407f40ff9ab691be12ca6c159d35fa8b09'
    )
    chat_completion = client.chat.completions.create(
        model="deepseek-v3", 
        messages = [
            {"role": "system", "content": instruction},
            {"role": "user", "content": inputs},
        ]
    )
    print(chat_completion)
    response = chat_completion.choices[0].message.content 
    return response
    



def get_gpt_response(instruction, input): 
    print("get_gpt_response")
    url = "https://hyjingsong.cognitiveservices.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"  
    headers = {  
        "api-key": "86ESER78K7vIqpxYEXsrlzGbKA9wGX35DszkMb85l6AyeTmxDr5DJQQJ99ALACHYHv6XJ3w3AAAAACOGMbuD",  
        "Content-Type": "application/json"  
    }  
    data = {  
        "messages": [  
            {  
                "role": "system",  
                "content": instruction
            },  
            {  
                "role": "user",  
                "content": input
            }  
        ],  
        "stream": False  
    }  

    response = requests.post(url, headers=headers, json=data)  

    print(f"Status Code: {response.status_code}")  

    # 检查响应内容是否为 JSON  
    try:  
        response_json = response.json()  
        print(response_json)
    except requests.JSONDecodeError:  
        print("Failed to decode JSON.")  
        print("Response content:", response.text)  
        return None  


    response = response_json['choices'][0]['message']['content']  
    return response
  

def get_llm_response(instruction, input, pipeline):
    print("LLM")
    messages = [
        {"role": "system", "content": instruction},
        {"role": "user", "content": input},
    ]

    prompt = pipeline.tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    print("prompt:",prompt)

    terminators = [
        pipeline.tokenizer.eos_token_id,
        pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = pipeline(
        prompt,
        max_new_tokens=2560,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.1,
        top_p=0.9,
    )
    res=outputs[0]["generated_text"][len(prompt):]
    return res


def get_codes_response(model, inputs, tokenizer, max_new_tokens):
    input_length = inputs["input_ids"].shape[1]
    
    with torch.no_grad():
        generate_ids = model.generate(
            **inputs,
            max_new_tokens = max_new_tokens,
            num_beams = 1,
            num_return_sequences = 1
        )

    # print(tokenizer.decode(generate_ids[0]))
    generated_sqls = tokenizer.batch_decode(generate_ids[:, input_length:], skip_special_tokens = True, clean_up_tokenization_spaces = False)
    print("codes")
    print(generated_sqls)

    return generated_sqls

# question_sort_instruction = (
#     "You are a Text-to-SQL expert. Your task is to classify text-based queries."
#     "The types are defined as follows: 1. Set operations, which require complex logical connections between multiple conditions and often involve the use of INTERSECT, EXCEPT, UNION, and other operations; 2. Combination operations, which group specific objects, usually achieved using GROUP BY; 3. Extremum operations, which do not group specific objects but need to take extreme values or sort; 4. Filtering operations, which select targets based on specific judgment conditions, generally completed using WHERE statements."
#     "Your task is to determine the operations required for the query and output them in the order of [Set, Combination, Extremum, Filtering]. For operations not involved, output them as None."
# )


# question_sort_input = "Query: Which of these players performs the best in crossing actions, Alexis, Ariel Borysiuk or Arouna Kone? player who perform best in crossing actions refers to MAX(crossing);"
# print(get_gpt_response(question_sort_instruction,question_sort_input))