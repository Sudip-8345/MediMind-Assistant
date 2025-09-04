import streamlit as st
import json
from AI_assistant import generate_wellness_plan

st.set_page_config(page_title="AI Wellness Assistant", page_icon="🩺")

st.title("🩺 AI Wellness Assistant")
st.write("Describe your symptoms and get a personalized wellness plan.")

user_text = st.text_area("Enter your symptoms:", height=100)

if st.button("Generate Wellness Plan"):
    if user_text.strip():
        with st.spinner("Generating your wellness plan..."):
            plan = generate_wellness_plan(user_text)
            # check if plan is a JSON string and parse it
            if isinstance(plan, str):
                try:
                    if '```json' in plan:
                        json_str = plan.split('```json')[1].split('```')[0].strip()
                        plan = json.loads(json_str)
                    elif '```' in plan:
                        json_str = plan.split('```')[1].split('```')[0].strip()
                        if json_str.startswith('{'):
                            plan = json.loads(json_str)
                    else:
                        st.write(plan)
                        st.stop()
                except:
                    st.write(plan)
                    st.stop()
            
            # main display logic
            if isinstance(plan, dict):
                intent = plan.get("Intent", "Symptom Check")
                
                st.markdown(f"### 🤔 Intent: {intent}")
                
                if intent == "Symptom Check":
                    if "condition_summary" in plan:
                        st.markdown("### 📋 Condition Summary")
                        st.info(plan["condition_summary"])
                    
                    precautions = plan.get("precautions", [])
                    if precautions:
                        st.markdown("### 🚫 Precautions")
                        if isinstance(precautions, list):
                            for precaution in precautions:
                                st.write(f"• {precaution}")
                        else:
                            st.write(f"• {precautions}")
                    
                    yoga_plan = plan.get("yoga_plan", [])
                    if yoga_plan:
                        st.markdown("### 🧘 Yoga Plan")
                        if isinstance(yoga_plan, list):
                            for yoga in yoga_plan:
                                st.write(f"• {yoga}")
                        else:
                            st.write(f"• {yoga_plan}")
                    
                    diet_plan = plan.get("diet_plan", [])
                    if diet_plan:
                        st.markdown("### 🍎 Diet Plan")
                        if isinstance(diet_plan, list):
                            for food in diet_plan:
                                st.write(f"• {food}")
                        else:
                            st.write(f"• {diet_plan}")
                    
                    medication_advice = plan.get("medication_advice")
                    if medication_advice:
                        st.markdown("### 💊 Medical Advice")
                        st.write(medication_advice)
                
                else:
                    advice = plan.get("advice", plan.get("response", "No specific advice available."))
                    st.markdown("### 💡 Advice")
                    if isinstance(advice, list):
                        for item in advice:
                            st.write(f"• {item}")
                    else:
                        st.write(advice)
            
            else:
                st.write("Unexpected response format:", plan)
                
        st.markdown("---")
        st.caption("⚠️ This is not medical diagnosis. Please consult a healthcare professional for any medical concerns.")
    
    else:
        st.warning("Please enter your symptoms to get a plan.")