class SkillsExtractorPrompt:
    def __init__(self):
        pass

    def get_prompt(self, text: str) -> str:
        prompt = [
            'You are assessing the skills of professional candidates from their resumes'
            'Given a resume, please extract all relevant skills: ',
            text,
            'Provide an output that is exactly one array of strings, of the skills you find.'
        ]

        return '\n'.join(prompt)