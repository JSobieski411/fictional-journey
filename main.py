import yaml
import os
from openai import OpenAI

# Load OpenAI API key
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable")

client = OpenAI(api_key=api_key)

# Load the YAML configurations
with open('src/see.yaml', 'r') as f:
    see_config = f.read()

with open('src/solve.yaml', 'r') as f:
    solve_config = f.read()

with open('src/unfold.yaml', 'r') as f:
    unfold_config = f.read()

# Conversation history
conversation = []

def analyze_with_unfold(content):
    # Use unfold.yaml as system prompt, content as user message
    response = client.chat.completions.create(
        model="gpt-4",  # or gpt-3.5-turbo
        messages=[
            {"role": "system", "content": unfold_config},
            {"role": "user", "content": f"Analyze the following conversation: {content}"}
        ],
        max_tokens=1000,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def solve_next(problem):
    # Use solve.yaml as system prompt
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": solve_config},
            {"role": "user", "content": f"Solve the following problem: {problem}"}
        ],
        max_tokens=1000,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def main():
    print("Welcome to fictional-journey interactive loop.")
    while True:
        user_input = input("User: ")
        if user_input.lower() == 'exit':
            break
        conversation.append(f"User: {user_input}")

        # Use unfold to present multi-perspective
        analysis = analyze_with_unfold(' '.join(conversation))
        print(f"AI Analysis: {analysis}")

        # Present options (placeholder)
        print("Options:")
        print("1. Accept analysis")
        print("2. Refine")
        print("3. Solve next")

        choice = input("Choose option: ")
        if choice == '3':
            next_problem = input("Enter next problem: ")
            solution = solve_next(next_problem)
            print(f"Solution: {solution}")
            conversation.append(f"AI: {solution}")

if __name__ == "__main__":
    main()