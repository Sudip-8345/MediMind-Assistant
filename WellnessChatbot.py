import streamlit as st
import json
from AI_assistant import generate_wellness_plan

st.set_page_config(page_title="AI Wellness Assistant", page_icon="🩺")

st.title("🩺 AI Wellness Assistant")
st.write("Describe your symptoms, ask health queries, and chat with the assistant.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_text := st.chat_input("Type your symptoms or health question..."):

    st.session_state.messages.append({"role": "user", "content": user_text})

    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        with st.spinner("Generating your wellness plan..."):
            plan = generate_wellness_plan(user_text)

            parsed_output = None
            if isinstance(plan, str):
                try:
                    if '```json' in plan:
                        json_str = plan.split('```json')[1].split('```')[0].strip()
                        parsed_output = json.loads(json_str)
                    elif plan.strip().startswith("{"):
                        parsed_output = json.loads(plan.strip())
                except:
                    parsed_output = None
            elif isinstance(plan, dict):
                parsed_output = plan

            if parsed_output:
                intent = parsed_output.get("Intent", parsed_output.get("intent", "Symptom Check"))

                response_text = f"**Intent:** {intent}\n\n"

                if intent == "Symptom Check":
                    if "condition_summary" in parsed_output:
                        response_text += f"📋 **Condition Summary:** {parsed_output['condition_summary']}\n\n"
                    
                    if precautions := parsed_output.get("precautions"):
                        response_text += "🚫 **Precautions:**\n"
                        for p in precautions if isinstance(precautions, list) else [precautions]:
                            response_text += f"- {p}\n"

                    if yoga_plan := parsed_output.get("yoga_plan"):
                        response_text += "\n🧘 **Yoga Plan:**\n"
                        for y in yoga_plan if isinstance(yoga_plan, list) else [yoga_plan]:
                            response_text += f"- {y}\n"

                    if diet_plan := parsed_output.get("diet_plan"):
                        response_text += "\n🍎 **Diet Plan:**\n"
                        for d in diet_plan if isinstance(diet_plan, list) else [diet_plan]:
                            response_text += f"- {d}\n"

                    if medication := parsed_output.get("medication_advice"):
                        response_text += f"\n💊 **Medical Advice:** {medication}\n"

                else:
                    advice = parsed_output.get("advice", "No specific advice available.")
                    response_text += f"💡 **Advice:**\n"
                    for a in advice if isinstance(advice, list) else [advice]:
                        response_text += f"- {a}\n"

            else:
                response_text = plan if isinstance(plan, str) else str(plan)

            st.markdown(response_text)

            st.session_state.messages.append({"role": "assistant", "content": response_text})

st.markdown("---")
st.caption("⚠️ This is not medical diagnosis. Please consult a healthcare professional for any medical concerns.")
