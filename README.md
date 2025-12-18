## AI Portfolio with Flowise Chatbot

This is a simple web portfolio that includes:

- **Portfolio sections**: Home, About, Projects, and Contact.
- **Chatbot section**: A panel where visitors can chat with your AI assistant.
- **Flowise integration**: Calls Flowise from a **Python (Flask) backend**, plus an optional iframe for embedding Flowise’s own UI.

### Files

- **index.html**: Main page layout and content (no JavaScript required).
- **styles.css**: Styling and responsive layout.
- **app.py**: Flask app that receives chat messages and calls Flowise.
- **requirements.txt**: Python dependencies (`flask`, `requests`).

### How to run (Python / Flask)

1. **Install dependencies** (once):

   ```bash
   pip install -r requirements.txt
   ```

2. **Set your Flowise API URL** (example commands):

   - Windows PowerShell:

     ```bash
     $env:FLOWISE_API_URL="http://localhost:3000/api/v1/prediction/your-flow-id"
     ```

   - macOS / Linux:

     ```bash
     export FLOWISE_API_URL="http://localhost:3000/api/v1/prediction/your-flow-id"
     ```

3. **Run the Flask server**:

   ```bash
   python app.py
   ```

4. Open `http://localhost:5000` in your browser.

### How the chatbot works now

- In the **Chatbot** section of `index.html`, the input form sends a `POST` to `/chat` on the Flask server.
- `app.py` forwards the question to `FLOWISE_API_URL` with JSON:

  ```json
  { "question": "user message here" }
  ```

- The server then renders a simple response page showing **your question** and the **AI answer**.

### Optional: embed Flowise UI

- In `index.html`, the iframe in the chatbot section has an empty `src`.
- Set it directly in the HTML if you want to show Flowise’s own chat interface, for example:

  ```html
  <iframe
    id="flowise-iframe"
    src="https://your-flowise-chat-url"
    title="Flowise Chatbot"
    loading="lazy"
  ></iframe>
  ```

### Customization

- **Text & content**: Edit headings, paragraphs, and project descriptions in `index.html`.
_- **Colors & layout**: Tweak gradients, fonts, and layout in `styles.css`.
- **Flowise payload/response**: If your Flowise flow expects different fields, adjust the JSON body and response parsing in `app.py`.


