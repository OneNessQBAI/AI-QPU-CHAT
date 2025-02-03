import streamlit as st
import subprocess
import plotly.graph_objects as go
from datetime import datetime
import json
import os
from bs4 import BeautifulSoup
import sys
import io
from contextlib import redirect_stdout
from openai import OpenAI
import requests

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

def validate_api_key(api_key):
    """Validate API key format"""
    return api_key and api_key.startswith("oneness_")

def chat_with_ai_qpu(messages, api_key):
    """Send request to AI-QPU endpoint"""
    try:
        response = requests.post(
            "http://142.117.62.233:3004/AI-QPU",
            json={
                "message": messages[-1]["content"],
                "api_key": api_key
            },
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
        st.error(f"Error communicating with AI-QPU: {str(e)}")
        return None

def clear_chat():
    st.session_state.messages = []

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return str(e)

def execute_python_script(script):
    try:
        output = io.StringIO()
        with redirect_stdout(output):
            exec(script)
        return output.getvalue()
    except Exception as e:
        return str(e)

def search_duckduckgo(query):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = f"https://duckduckgo.com/html/?q={query}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # Find all search results
        for result in soup.find_all('div', class_='result'):
            title = result.find('a', class_='result__a')
            snippet = result.find('a', class_='result__snippet')
            if title and snippet:
                results.append({
                    'Title': title.text.strip(),
                    'Summary': snippet.text.strip(),
                    'URL': title['href']
                })
        
        # If no results found
        if not results:
            return [{
                'Title': 'No results found',
                'Summary': 'Try modifying your search query',
                'URL': ''
            }]
        
        # Return formatted results
        return {
            'Search Results': results[:5],
            'Query': query,
            'Total Results': len(results[:5])
        }
    except Exception as e:
        return {
            'Error': str(e),
            'Query': query,
            'Total Results': 0
        }

def create_visualization(data):
    try:
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except:
                pass
        
        if isinstance(data, dict):
            fig = go.Figure(data=[go.Table(
                header=dict(values=list(data.keys()),
                          fill_color='paleturquoise',
                          align='left'),
                cells=dict(values=list(data.values()),
                          fill_color='lavender',
                          align='left'))
            ])
        elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            headers = list(data[0].keys())
            values = [[d[k] for d in data] for k in headers]
            fig = go.Figure(data=[go.Table(
                header=dict(values=headers,
                          fill_color='paleturquoise',
                          align='left'),
                cells=dict(values=values,
                          fill_color='lavender',
                          align='left'))
            ])
        elif isinstance(data, str):
            fig = go.Figure()
            fig.add_annotation(
                text=data,
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False
            )
        else:
            return None
            
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        return fig
    except:
        return None

st.set_page_config(
    page_title="🌌 AI-QPU Quantum Terminal ⚛️",
    page_icon="🔮",
    layout="wide"
)

st.title("🌌 AI-QPU Quantum Terminal ⚛️")
st.subheader("🧠 Artificial Intelligence - Quantum Processing Unit 🌟")

# Add API key input in sidebar
with st.sidebar:
    # API Key Input
    api_key = st.text_input(
        "Enter API Key 🔑www.QuantumIntelligence.ca 🌟",
        type="password",
        value=st.session_state.get('api_key', ''),
        help="Get your API key at www.QuantumIntelligence.ca ⚛️"
    )
    
    if api_key:
        if validate_api_key(api_key):
            st.session_state.api_key = api_key
            st.success("API key format valid ✅")
        else:
            st.error("Invalid API key format. Key must start with 'oneness_' ❌")

# Add clear chat button in sidebar
with st.sidebar:
    if st.button("Clear Chat History"):
        clear_chat()

# System prompt for AI-QPU
SYSTEM_PROMPT = """You are AI-QPU (Artificial Intelligence - Quantum Processing Unit), an advanced AI assistant capable of natural conversation, code execution, and web search.

IMPORTANT: When users ask questions about current events, facts, or information that requires research, ALWAYS use the web search format first:
```search
detailed search query here
```

For code and commands, use these formats:

For Python scripts:
```script
try:
    # Your code here
except Exception as e:
    print(f"Error: {e}")
```

For system commands:
```command
your_command_here
```

For web searches:
```search
your_search_query
```

For visualizations:
```visualization
{
    "data": your_data_here
}
```

Otherwise, engage in natural conversation and be helpful!
"""

# Chat input
user_input = st.chat_input("🌌 Enter your quantum query... ⚛️")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        # Prepare messages for API call
        api_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
        
        # Check for API key
        api_key = st.session_state.get('api_key')
        if not api_key:
            st.error("Please enter your API key in the sidebar 🔑")
        elif not validate_api_key(api_key):
            st.error("Invalid API key format. Key must start with 'oneness_' 🚫")
        else:
            # Get AI response
            content = chat_with_ai_qpu(api_messages, api_key)
        
        if content:
            # Add AI response directly
            st.session_state.messages.append({
                "role": "assistant",
                "content": content
            })
    except Exception as e:
        st.error(f"Error getting AI response: {str(e)}")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        content = msg["content"]
        
        # Check for code blocks
        if "```" in content:
            # Handle command blocks
            if "```command" in content:
                command = content.split("```command")[1].split("```")[0].strip()
                st.code(command, language="bash")
                button_key = f"cmd_{len(st.session_state.messages)}_{abs(hash(command))}"
                if st.button(f"Execute Command", key=button_key):
                    result = execute_command(command)
                    st.code(result, language="bash")
            
            # Handle script blocks
            elif "```script" in content:
                script = content.split("```script")[1].split("```")[0].strip()
                st.code(script, language="python")
                button_key = f"script_{len(st.session_state.messages)}_{abs(hash(script))}"
                if st.button(f"Run Script", key=button_key):
                    result = execute_python_script(script)
                    st.code(result, language="python")
            
            # Handle search blocks
            elif "```search" in content:
                query = content.split("```search")[1].split("```")[0].strip()
                st.info(f"🔍 Searching for: {query}")
                results = search_duckduckgo(query)
                
                # Display results in a more readable format
                st.write("### 🌐 Search Results")
                if 'Search Results' in results:
                    for idx, result in enumerate(results['Search Results'], 1):
                        st.markdown(f"""
                        **{idx}. [{result['Title']}]({result['URL']})**  
                        {result['Summary']}
                        """)
                elif 'Error' in results:
                    st.error(f"Search error: {results['Error']}")
                
                # Create visualization
                fig = create_visualization(results)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            # Handle visualization blocks
            elif "```visualization" in content:
                viz_data = content.split("```visualization")[1].split("```")[0].strip()
                fig = create_visualization(viz_data)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        else:
            # Display regular chat response
            st.markdown(content)

st.sidebar.markdown("""
### ✨ Quantum Features 🌟
- 🔬 Execute Python scripts
- ⚡ Run system commands
- 🌐 Web search 
PAST THIS IN THE CHAT:
For web searches:
```search
``search your_search_query
```
- 📊 Data visualization
- 🧠 Powered by AI-QPU

### 🎯 Response Formats
1. 💻 Scripts: ```script```
2. ⚙️ Commands: ```command```
3. 🔍 Search: ```search```
4. 📈 Visualization: ```visualization```
5. 💬 Text: ```response```

### 💡 Quantum Tips
- 🛡️ Scripts and commands are executed safely
- 🌍 Web search provides up-to-date information
- 📊 Visualizations are created automatically

### 🔑 Get API Key
Visit www.QuantumIntelligence.ca to get your quantum access key! ⚛️
""")
