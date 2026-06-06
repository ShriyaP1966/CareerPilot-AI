import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_resume_report(resume_text, desired_role):

    prompt = f"""
You are an expert recruiter, ATS evaluator, career coach, and hiring manager.

TARGET ROLE:
{desired_role}

RESUME:
{resume_text}

Analyze the resume ONLY with respect to the target role.

SCORING RULES:

ROLE MATCH SCORE:
- Must be between 0 and 100
- 90-100 = Excellent Match
- 75-89 = Strong Match
- 60-74 = Moderate Match
- Below 60 = Weak Match

ATS SCORE:
- Must be between 0 and 100
- Consider:
  * Skills
  * Projects
  * Education
  * Resume completeness
  * Role relevance
  * Technical depth
- Never give extremely low scores unless the resume is nearly empty

INTERVIEW READINESS:
- Must be between 0 and 100
- Estimate how prepared the candidate appears

IMPORTANT:
- Keep the report concise
- Avoid long paragraphs
- Give actionable insights
- Be realistic with scoring

Return EXACTLY in this format:

ROLE_MATCH_SCORE: <score>/100

ATS_SCORE: <score>/100

INTERVIEW_READINESS: <score>/100

VERDICT: <Strong Candidate / Moderate Candidate / Needs Improvement>

TOP_STRENGTHS:
- point
- point
- point
- point
- point

CRITICAL_SKILL_GAPS:
- point
- point
- point
- point
- point

TOP_5_INTERVIEW_QUESTIONS:
1. question
2. question
3. question
4. question
5. question

NEXT_3_ACTIONS:
1. action
2. action
3. action

"""
    response = model.generate_content(prompt)

    return response.text
