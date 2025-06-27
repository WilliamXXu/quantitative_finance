from google.genai import types
from google import genai
from dashscope import Generation
def gemini(question,client):
    response = client.models.generate_content(
    model="gemini-2.0-flash", contents=question,config=types.GenerateContentConfig(
        tools=[types.Tool(
            google_search=types.GoogleSearchRetrieval
        )]
    )
)
    return response.text

def writeOut(li,name):
    file = open(name+'.txt','w')
    for item in li:
        file.write(item+"\n")
    file.close()
   


def alicloud_llm(question,background,api,model="deepseek-r1-distill-llama-70b"):

    messages = [
        {'role': 'system', 'content': background}, #Python programmer 'You are a financial analyst'
        {'role': 'user', 'content': question}
        ]
    response = Generation.call(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx",
        api_key=api,#os.getenv("DASHSCOPE_API_KEY"), 
        model=model,   # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=messages,
        result_format="message"
    )

    if response.status_code == 200:
        return response.output.choices[0].message.content
    else:
        print(f"HTTP返回码：{response.status_code}")
        print(f"错误码：{response.code}")
        print(f"错误信息：{response.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        return None
        
def gamma_param(mean, std):
    """
    Creates a gamma distribution with a specified mean (μ) and standard deviation (σ).

    Parameters:
        mean (float): Desired mean of the distribution (must be > 0).
        std (float): Desired standard deviation of the distribution (must be > 0).

    Returns:
        scipy.stats._distn_infrastructure.rv_frozen: A frozen gamma distribution object.

    Raises:
        ValueError: If mean or std is non-positive.
    """
    if mean <= 0 or std <= 0:
        raise ValueError("Mean and standard deviation must be positive.")

    # Calculate shape (alpha) and scale (theta) parameters
    alpha = (mean ** 2) / (std ** 2)  # Shape parameter (k or a)
    theta = (std ** 2) / mean          # Scale parameter

    # Create and return the gamma distribution
    return alpha,theta
def beta_param(mu,sigma2):
    a=mu*(mu*(1-mu)/sigma2 - 1)
    b = a*(1-mu)/mu
    return a,b 