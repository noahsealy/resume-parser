class NameExtractorPrompt:
    def __init__(self):
        pass

    def get_prompt(self, text: str) -> str:
        prompt = [
            'You are assessing the skills of professional candidates from their resumes',
            'Given a resume, please extract the candidates name',
            text,
            'Provide an output that is exactly one string of the candidates name.'
        ]

        return '\n'.join(prompt)