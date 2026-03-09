class SkillsExtractorPrompt:
    def __init__(self):
        pass

    def get_prompt(self, text: str) -> str:
        prompt = [
            'You are extracting skills from professional resumes.',
            'Given the resume below, extract all relevant technical and soft skills.',
            text,
            'Respond with a valid JSON array of strings only. No explanation, no markdown, no code fences. Example: ["Python", "SQL", "Communication"]'
        ]

        return '\n'.join(prompt)