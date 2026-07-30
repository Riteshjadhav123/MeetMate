import sys
from pathlib import Path
import google.generativeai as genai
import os
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def generate_local_summary(text):
    """Generates a structured summary directly from the transcript when Gemini API is unavailable."""
    import re
    # Clean text into sentences
    cleaned_text = re.sub(r'\s+', ' ', text).strip()
    raw_sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', cleaned_text) if len(s.strip()) > 15]
    
    # Executive Summary (First 3 significant sentences)
    exec_sentences = raw_sentences[:3] if raw_sentences else ["Meeting transcript processed successfully."]
    exec_summary = " ".join(exec_sentences)
    
    # Key Decisions / Key Points
    key_points = []
    keywords = ["model", "process", "setup", "discuss", "explain", "present", "agree", "decide", "important", "first", "second"]
    for s in raw_sentences:
        if any(w in s.lower() for w in keywords):
            if s not in key_points and len(key_points) < 4:
                key_points.append(f"- {s}")
    if not key_points and raw_sentences:
        key_points = [f"- {s}" for s in raw_sentences[:3]]
    if not key_points:
        key_points = ["- No key decisions were finalized in this meeting."]
        
    # Open Questions
    questions = []
    for s in raw_sentences:
        if "?" in s or s.lower().startswith(("why", "how", "what", "where", "who")):
            if s not in questions and len(questions) < 3:
                questions.append(f"{len(questions)+1}. {s}")
    if not questions:
        questions = ["1. All topics were resolved."]

    return f"""📌 **EXECUTIVE SUMMARY**
{exec_summary}

✅ **KEY DECISIONS**
{chr(10).join(key_points)}

📝 **ACTION ITEMS**
- ☑️ Meeting Participants → Review transcript notes and action items (Due: TBD)

❓ **OPEN QUESTIONS**
{chr(10).join(questions)}"""

def summarize_transcript(transcript_file, output_file="outputs/meeting_summary.txt"):
    """
    Reads a meeting transcript, generates a professional, structured summary using the Gemini API (or local fallback),
    and saves it to a file.
    """
    try:
        text = Path(transcript_file).read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: The transcript file was not found at {transcript_file}")
        return

    if not text.strip():
        print(f"Warning: Transcript file {transcript_file} is empty.")
        text = "No speech detected in meeting audio."

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    result = None

    if api_key and api_key != "YOUR_FALLBACK_API_KEY_HERE":
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""
            **Objective:** Analyze the following meeting transcript and produce a professional, structured summary suitable for executive review.
            **Role:** You are an expert executive assistant. Distill the conversation into its most critical components.

            **Transcript to Analyze:**
            ---
            {text}
            ---

            **Required Output Format:**
            📌 **EXECUTIVE SUMMARY**
            A concise summary of the meeting's core purpose and key outcomes.

            ✅ **KEY DECISIONS**
            A bulleted list of all concrete decisions that were finalized.

            📝 **ACTION ITEMS**
            A checklist of tasks assigned. Format: ☑️ Name → Task (Due: Deadline)

            ❓ **OPEN QUESTIONS**
            A numbered list of unresolved questions.
            """
            response = model.generate_content(prompt)
            result = response.text.strip()
            print("✅ Generated summary via Gemini AI API")
        except Exception as e:
            print(f"Gemini API error: {e}. Falling back to local summarizer.")

    if not result:
        print("ℹ️ Using local transcript summarizer...")
        result = generate_local_summary(text)

    # Ensure the output directory exists and save summary
    Path("outputs").mkdir(exist_ok=True)
    Path(output_file).write_text(result, encoding="utf-8")
    print(f"✅ Summary saved to {output_file}")
    print("\n--- Summary Preview ---\n")
    print(result)


if __name__ == "__main__":
    summarize_transcript("outputs/meeting_transcript.txt")

