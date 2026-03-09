class NameExtractorPrompt:
    def __init__(self):
        pass

    def get_prompt(self, text: str) -> str:
        prompt = [
            'You are extracting information from professional resumes.',
            'Given the resume below, extract the full name of the candidate.',
            text,
            'Respond with the candidate\'s full name only. No explanation, no punctuation, no extra text.'
        ]

        return '\n'.join(prompt)