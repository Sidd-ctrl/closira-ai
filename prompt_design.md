# Prompt Design Documentation

## System Prompt Strategy

The AI assistant is designed to behave like a customer support assistant for Bloom Aesthetics Clinic.

The prompt clearly instructs the AI to:
- Answer only from the SOP data
- Never hallucinate information
- Escalate when information is unavailable
- Maintain a professional and polite tone

---

# Hallucination Prevention

The AI is explicitly instructed to:
- Use only the SOP content
- Avoid assumptions
- Inform the customer when information is unavailable
- Escalate instead of guessing

This improves reliability and customer trust.

---

# Escalation Logic

The system escalates when:
- Customer shows frustration
- Complaint-related keywords are detected
- User requests a human
- Medical or sensitive queries appear

Escalation reasons are logged in:
logs/escalation_logs.txt

---

# Lead Qualification

The workflow collects:
- Business Type
- Team Size
- Current Tools

These questions help qualify the customer before deeper engagement.

---

# Tone and Persona

The assistant tone is:
- Friendly
- Professional
- Clear
- Short and respectful

The assistant behaves like a real SMB customer support representative.