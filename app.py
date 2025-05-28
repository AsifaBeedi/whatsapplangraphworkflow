# app.py
from flask import Flask, request, jsonify, render_template_string
from workflow import process_message_node
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from marketing_helper import create_marketing_message, create_ab_test_variations, generate_marketing_text_groq  # Already imported

# Load environment variables
load_dotenv()

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=5)

# Function to process messages synchronously
def sync_process(message):
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(process_message_node(message))
    loop.close()
    return result

@app.route('/process_message', methods=['POST'])
def process_message():
    """API endpoint to process chat messages using Groq LLM"""
    try:
        data = request.json
        message = data.get('message', '')
        # You can add chat history/context here if you want
        prompt = f"You are a helpful WhatsApp assistant. User says: {message}\nAssistant:"
        response = generate_marketing_text_groq(prompt, model="llama3-8b-8192", max_tokens=120)
        return jsonify({
            'status': 'success',
            'response': response
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/generate_marketing', methods=['POST'])
def generate_marketing():
    """API endpoint to generate marketing content"""
    try:
        data = request.json
        product_info = data.get('product_info', '')
        campaign_type = data.get('campaign_type', 'promotion')
        
        # Generate marketing message
        marketing_message = create_marketing_message(product_info, campaign_type)
        
        # Generate A/B variations
        variations = create_ab_test_variations(product_info, campaign_type, 2)
        
        # Format response
        formatted_response = f"Generated Marketing Message:\n{marketing_message}\n\n"
        formatted_response += "A/B Test Variations:\n"
        for i, var in enumerate(variations, 1):
            formatted_response += f"Variation {i}:\n{var}\n\n"
        
        return jsonify({
            'status': 'success',
            'marketing_message': marketing_message,
            'ab_variations': variations,
            'formatted_response': formatted_response
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/', methods=['GET'])
def index():
    """Serve the index page"""
    html_template = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>WhatsApp Marketing Assistant</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }
                h1 {
                    color: #128C7E; /* WhatsApp green */
                    text-align: center;
                }
                .container {
                    background-color: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                .tab {
                    overflow: hidden;
                    border: 1px solid #ccc;
                    background-color: #f1f1f1;
                    border-radius: 5px 5px 0 0;
                }
                .tab button {
                    background-color: inherit;
                    float: left;
                    border: none;
                    outline: none;
                    cursor: pointer;
                    padding: 14px 16px;
                    transition: 0.3s;
                    font-size: 16px;
                }
                .tab button:hover {
                    background-color: #ddd;
                }
                .tab button.active {
                    background-color: #128C7E;
                    color: white;
                }
                .tabcontent {
                    display: none;
                    padding: 20px;
                    border: 1px solid #ccc;
                    border-top: none;
                    border-radius: 0 0 5px 5px;
                    animation: fadeEffect 1s;
                }
                @keyframes fadeEffect {
                    from {opacity: 0;}
                    to {opacity: 1;}
                }
                textarea, select {
                    width: 100%;
                    padding: 12px;
                    margin: 8px 0;
                    display: inline-block;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    box-sizing: border-box;
                }
                textarea {
                    height: 100px;
                    resize: vertical;
                }
                button {
                    background-color: #128C7E;
                    color: white;
                    padding: 14px 20px;
                    margin: 8px 0;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    width: 100%;
                    font-size: 16px;
                }
                button:hover {
                    background-color: #075E54;
                }
                .result {
                    margin-top: 20px;
                    padding: 15px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    background-color: #f9f9f9;
                    white-space: pre-wrap;
                }
                .hidden {
                    display: none;
                }
                .loader {
                    border: 5px solid #f3f3f3;
                    border-radius: 50%;
                    border-top: 5px solid #128C7E;
                    width: 40px;
                    height: 40px;
                    margin: 20px auto;
                    animation: spin 2s linear infinite;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        </head>
        <body>
            <h1>WhatsApp Marketing Assistant</h1>
            
            <div class="container">
                <div class="tab">
                    <button class="tablinks active" onclick="openTab(event, 'Marketing')">Marketing Generator</button>
                    <button class="tablinks" onclick="openTab(event, 'Chat')">Chat Assistant</button>
                </div>
                
                <div id="Marketing" class="tabcontent" style="display: block;">
                    <h2>Generate Marketing Content</h2>
                    <p>Enter product information or campaign details below:</p>
                    
                    <select id="campaignType">
                        <option value="promotion">Promotion/Discount</option>
                        <option value="announcement">New Product/Announcement</option>
                        <option value="reminder">Reminder</option>
                    </select>
                    
                    <textarea id="productInfo" placeholder="Example: We are launching a new eco-friendly water bottle next week with a 20% discount for early buyers."></textarea>
                    
                    <button onclick="generateMarketing()">Generate Marketing Content</button>
                    
                    <div id="marketingLoading" class="loader hidden"></div>
                    <div id="marketingResult" class="result hidden"></div>
                </div>
                
                <div id="Chat" class="tabcontent">
                    <h2>Chat Assistant</h2>
                    <p>Send a message to the assistant:</p>
                    
                    <textarea id="chatMessage" placeholder="Enter your message here..."></textarea>
                    
                    <button onclick="sendMessage()">Send Message</button>
                    
                    <div id="chatLoading" class="loader hidden"></div>
                    <div id="chatResult" class="result hidden"></div>
                </div>
                
                <a id="whatsappSendBtn" href="#" target="_blank" style="display:none;">
                    <button style="background-color:#25D366;">Send to WhatsApp</button>
                </a>
            </div>
            
            <script>
                function openTab(evt, tabName) {
                    var i, tabcontent, tablinks;
                    
                    tabcontent = document.getElementsByClassName("tabcontent");
                    for (i = 0; i < tabcontent.length; i++) {
                        tabcontent[i].style.display = "none";
                    }
                    
                    tablinks = document.getElementsByClassName("tablinks");
                    for (i = 0; i < tablinks.length; i++) {
                        tablinks[i].className = tablinks[i].className.replace(" active", "");
                    }
                    
                    document.getElementById(tabName).style.display = "block";
                    evt.currentTarget.className += " active";
                }
                
                async function generateMarketing() {
                    const productInfo = document.getElementById('productInfo').value;
                    const campaignType = document.getElementById('campaignType').value;
                    
                    if (!productInfo) {
                        alert('Please enter product information');
                        return;
                    }
                    
                    // Show loading
                    document.getElementById('marketingLoading').classList.remove('hidden');
                    document.getElementById('marketingResult').classList.add('hidden');
                    
                    try {
                        const response = await fetch('/generate_marketing', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ 
                                product_info: productInfo,
                                campaign_type: campaignType
                            })
                        });
                        
                        const data = await response.json();
                        
                        // Hide loading
                        document.getElementById('marketingLoading').classList.add('hidden');
                        document.getElementById('marketingResult').classList.remove('hidden');
                        
                        if (data.status === 'success') {
                            document.getElementById('marketingResult').textContent = data.formatted_response;

                            // WhatsApp integration
                            const phone = ""; // Optionally, set a default phone number with country code (e.g., "919999999999")
                            const text = encodeURIComponent(data.marketing_message);
                            const waBtn = document.getElementById('whatsappSendBtn');
                            waBtn.href = `https://wa.me/${phone}?text=${text}`;
                            waBtn.style.display = "inline-block";
                        } else {
                            document.getElementById('marketingResult').textContent = 'Error: ' + data.message;
                            document.getElementById('whatsappSendBtn').style.display = "none";
                        }
                    } catch (error) {
                        document.getElementById('marketingLoading').classList.add('hidden');
                        document.getElementById('marketingResult').classList.remove('hidden');
                        document.getElementById('marketingResult').textContent = 'Error: ' + error.message;
                    }
                }
                
                async function sendMessage() {
                    const message = document.getElementById('chatMessage').value;
                    
                    if (!message) {
                        alert('Please enter a message');
                        return;
                    }
                    
                    // Show loading
                    document.getElementById('chatLoading').classList.remove('hidden');
                    document.getElementById('chatResult').classList.add('hidden');
                    
                    try {
                        const response = await fetch('/process_message', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ message })
                        });
                        
                        const data = await response.json();
                        
                        // Hide loading
                        document.getElementById('chatLoading').classList.add('hidden');
                        document.getElementById('chatResult').classList.remove('hidden');
                        
                        if (data.status === 'success') {
                            document.getElementById('chatResult').textContent = data.response;
                        } else {
                            document.getElementById('chatResult').textContent = 'Error: ' + data.message;
                        }
                    } catch (error) {
                        document.getElementById('chatLoading').classList.add('hidden');
                        document.getElementById('chatResult').classList.remove('hidden');
                        document.getElementById('chatResult').textContent = 'Error: ' + error.message;
                    }
                }
            </script>
        </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)