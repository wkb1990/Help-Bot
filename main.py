import json
from difflib import get_close_matches


def load_knowledge_base(file_path: str):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error loading knowledge base. Please check the file format or existence.")
        return None

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question.lower(), [q.lower() for q in questions], n=1, cutoff=0.65)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"].lower() == question:
            return q["answer"]

def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    if knowledge_base is None:
        return

    while True:
        print('PDX Support: How can I help with your Xplan query? Please try to provide me clear details, including relevant modules :)')
        user_input: str = input('You: ')

        if user_input.lower() == 'quit bot':
            break

        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'PDX Support: {answer}')
        else:
            alternative_matches = get_close_matches(user_input, [q["question"] for q in knowledge_base["questions"]], n=5, cutoff=0.15)
            if alternative_matches:
                print(f'Did you mean one of these?')
                for i, alt_match in enumerate(alternative_matches):
                    print(f'{i + 1}. {alt_match}')

                try:
                    selected_option = int(input(f'Select an option (1-{len(alternative_matches)}): '))

                    # Check if selected option is within a valid range
                    if 1 <= selected_option <= len(alternative_matches):
                        selected_question = alternative_matches[selected_option - 1]
                        best_match = find_best_match(selected_question, [q["question"] for q in knowledge_base["questions"]])

                        if best_match:
                            answer = get_answer_for_question(best_match, knowledge_base)
                            print(f'PDX Support: {answer}')
                        else:
                            print("Sorry, I couldn't find a match for your input. Please contact support@practicedynamix.com.au ")
                    else:
                        print(f"Invalid selection. Please enter a number between 1 and {len(alternative_matches)}.")
                except ValueError:
                    print("Invalid selection. Please enter a number.")
            else:
                print("Sorry, I couldn't find a match for your input. Please contact support@practicedynamix.com.au ")

if __name__ == '__main__':
    chat_bot()
