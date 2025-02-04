import streamlit as st
import requests
import os
import json
from datetime import datetime
import plotly.graph_objs as go
import numpy as np
import uuid
import subprocess
import io
from contextlib import redirect_stdout
import sys

class QuantumAIChat:
    def __init__(self):
        # Quantum AI Endpoint Configuration
        self.QUANTUM_AI_ENDPOINT = "http://142.117.62.233:3004/AI-QPU"
        
        # Conversation Storage Directory
        self.CONVERSATIONS_DIR = "quantum_conversations"
        os.makedirs(self.CONVERSATIONS_DIR, exist_ok=True)
        
        # Quantum Visualization Configurations
        self.QUANTUM_EMOJIS = ['🌌', '🔮', '⚛️', '🌠', '🛸', '🌈']

    def validate_api_key(self, api_key):
        """Validate API key format"""
        return api_key and api_key.startswith("oneness_")
    
    def quantum_ai_request(self, user_message):
        """Advanced Quantum AI Request"""
        # Get API key from session state
        api_key = st.session_state.get('api_key')
        if not api_key:
            return "Please enter your API key in the sidebar 🔑"
        
        if not self.validate_api_key(api_key):
            return "Invalid API key format. Key must start with 'oneness_' 🚫"

        try:
            payload = {
                "message": user_message,
                "api_key": api_key
            }
            response = requests.post(
                self.QUANTUM_AI_ENDPOINT,
                json=payload,
                headers={
                    "X-API-Key": api_key,
                    "Content-Type": "application/json"
                }
            )
            
            if response.status_code == 401:
                return "Invalid or expired API key 🔒"
            elif response.status_code == 429:
                return "Too many requests. Please wait a moment and try again ⏳"
            
            data = response.json()
            return data.get('response') or "No response from AI-QPU. Please try again 🤖"
        except Exception as e:
            return f"🚨 Quantum Transmission Error: {e}"

    def execute_command(self, command):
        """Execute system command safely"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout if result.stdout else result.stderr
        except Exception as e:
            return str(e)

    def execute_python_script(self, script):
        """Execute Python script safely"""
        try:
            output = io.StringIO()
            with redirect_stdout(output):
                exec(script)
            return output.getvalue()
        except Exception as e:
            return str(e)
    
    def save_conversation(self, conversation):
        """Save Conversation with Unique Quantum Identifier"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())
        filename = os.path.join(
            self.CONVERSATIONS_DIR, 
            f"quantum_conversation_{timestamp}_{unique_id}.json"
        )
        with open(filename, 'w') as f:
            json.dump(conversation, f, indent=4)
        return filename
    
    def generate_quantum_visualization(self, conversations):
        """Dynamic Quantum Visualization"""
        try:
            num_messages = len(conversations)
            x = np.linspace(0, num_messages, num_messages)
            y = np.random.rand(num_messages) * np.log(np.arange(1, num_messages+1))
            z = np.cumsum(np.random.rand(num_messages)) * 0.5
            
            fig = go.Figure(data=[go.Scatter3d(
                x=x, y=y, z=z,
                mode='markers+lines',
                marker=dict(
                    size=10,
                    color=z,
                    colorscale='Viridis',
                    opacity=0.8
                ),
                line=dict(color='cyan', width=3)
            )])
            
            fig.update_layout(
                title=f"🔮 Quantum Conversation Dynamics (Messages: {num_messages})",
                scene=dict(
                    xaxis_title="Conversation Flow",
                    yaxis_title="Semantic Complexity",
                    zaxis_title="Quantum Reasoning Depth"
                )
            )
            return fig
        except Exception as e:
            st.error(f"Visualization Error: {e}")
            return None

def main():
    st.set_page_config(
        page_title="🔮 AI-QPU Quantum Chat", 
        page_icon="⚛️", 
        layout="wide"
    )
    
    # Futuristic Styling with Better Readability
    st.markdown("""
    <style>
    .stApp { 
        background-color: #0a1128;
    }
    .stMarkdown {
        color: #ffffff !important;
    }
    /* Chat message styling */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        padding: 15px !important;
        margin: 5px 0 !important;
        border: 1px solid rgba(0, 255, 255, 0.2) !important;
    }
    .stChatMessage .stMarkdown p {
        color: #ffffff !important;
        font-size: 16px !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
    }
    /* User message */
    [data-testid="chat-message-user"] {
        background-color: rgba(0, 255, 255, 0.15) !important;
        border: 1px solid rgba(0, 255, 255, 0.3) !important;
    }
    /* Assistant message */
    [data-testid="chat-message-assistant"] {
        background-color: rgba(255, 255, 255, 0.25) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    /* Code blocks */
    .stCodeBlock {
        background-color: #1a1a1a !important;
        color: #00ff00 !important;
    }
    /* Buttons */
    .stButton button {
        background-color: #1a1a1a !important;
        color: #00ff00 !important;
        border: 1px solid #00ff00 !important;
    }
    /* Inputs */
    .stTextInput input {
        color: #ffffff !important;
        background-color: #1a1a1a !important;
        border: 1px solid #00ff00 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize Quantum AI Interface
    quantum_ai = QuantumAIChat()
    
    # Session State Management
    if 'conversations' not in st.session_state:
        st.session_state.conversations = []
    
    # Main Interface
    st.title("🌌 AI-QPU: AI Quantum Computing Reasoning LLM")
    st.subheader("Advanced (Artificial Intelligence - Quantum Processing Unit) Interface")
    
    # Sidebar Controls
    with st.sidebar:
        st.header("🛠️ Quantum Controls")

        # API Key Input
        api_key = st.text_input(
            "Enter API Key 🔑Visit www.QuantumIntelligence.ca to get your quantum access key! ⚛️",
            type="password",
            value=st.session_state.get('api_key', ''),
            help="Your API key should start with 'oneness_'"
        )
        
        if api_key:
            if quantum_ai.validate_api_key(api_key):
                st.session_state.api_key = api_key
                st.success("API key format valid ✅")
            else:
                st.error("Invalid API key format. Key must start with 'oneness_' ❌")

        enable_code_execution = st.checkbox("Enable Code Execution 💻", value=False)
        
        # Conversation Management
        if st.button("💾 Save Conversation"):
            saved_file = quantum_ai.save_conversation(
                st.session_state.conversations
            )
            st.success(f"Conversation Saved: {saved_file}")
    
    # Conversation Display
    for conversation in st.session_state.conversations:
        with st.chat_message(conversation['role']):
            content = conversation['content']
            
            # Handle command blocks
            if "```command" in content:
                command = content.split("```command")[1].split("```")[0].strip()
                st.code(command, language="bash")
                if enable_code_execution:
                    if st.button(f"Execute Command", key=f"cmd_{hash(command)}"):
                        result = quantum_ai.execute_command(command)
                        st.code(result, language="bash")
            
            # Handle script blocks
            elif "```script" in content:
                script = content.split("```script")[1].split("```")[0].strip()
                st.code(script, language="python")
                if enable_code_execution:
                    if st.button(f"Run Script", key=f"script_{hash(script)}"):
                        result = quantum_ai.execute_python_script(script)
                        st.code(result, language="python")
            
            # Handle regular text
            else:
                st.markdown(content)
    
    # 3D Visualization
    if st.session_state.conversations:
        fig = quantum_ai.generate_quantum_visualization(st.session_state.conversations)
        st.plotly_chart(fig, use_container_width=True)
    
    # User Input
    if prompt := st.chat_input("Enter Quantum Query 🤖"):
        # User Message
        st.session_state.conversations.append({
            'role': 'user', 
            'content': prompt
        })
        st.chat_message('user').write(prompt)
        
        # Quantum AI Response
        with st.spinner("🔮 Quantum Reasoning..."):
            response = quantum_ai.quantum_ai_request(prompt)
            st.session_state.conversations.append({
                'role': 'assistant', 
                'content': response
            })
            st.chat_message('assistant').write(response)

if __name__ == "__main__":
    main()

