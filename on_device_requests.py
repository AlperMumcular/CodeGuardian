from openai import OpenAI
import time

def get_response_on_device(prompt):
    """
    Get response from local LLM using LM Studio
    Args:
        prompt (str): Input prompt for the model
    Returns:
        str: Generated response
    """
    try:
        client = OpenAI(
            base_url="http://127.0.0.1:1234/v1",
            api_key="not-needed"  # can be any string for local LLM
        )
        
        response = client.chat.completions.create(
            model="qwen2.5-coder-7b-instruct",  # your local model name
            messages=[
                {"role": "system", "content": "DO AS REQUESTED"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=-1,
            stream=True
        )
        
        # Handle streaming response
        full_response = ""
        print("Generating response...")
        for chunk in response:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content
                print(content, end='', flush=True)  # Print response as it streams
                
        return full_response
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

def test_llm():
    """
    Test function to verify LLM responses
    """
    test_prompts = [
        "Tell me a short story about a cat",
        "What is Python programming?",
        "Write a haiku about summer"
    ]
    
    print("Starting LLM test...\n")
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\nTest {i}: '{prompt}'\n")
        print("=" * 50)
        
        start_time = time.time()
        response = get_response_on_device(prompt)
        end_time = time.time()
        
        if response:
            print("\n" + "=" * 50)
            print(f"\nResponse time: {end_time - start_time:.2f} seconds")
        else:
            print("\nFailed to get response")
        
        print("\n" + "-" * 50)

# if __name__ == "__main__":
#     # Make sure LM Studio is running locally before executing
#     print("Ensure LM Studio is running locally on port 1234")
#     print("Press Enter to continue...")
#     input()
    
#     test_llm()