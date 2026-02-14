# HBDB Banking Bot

An AI-powered banking assistant chatbot built with Mistral Large, Streamlit, and Python. This bot answers banking questions based on HBDB's FAQ database.

## Features

- 🤖 **AI-Powered Responses** using Mistral Large model
- 📱 **User-Friendly Interface** built with Streamlit
- 📚 **FAQ Database Integration** for accurate banking information
- 🔐 **Secure API Key Management** using environment variables
- 💬 **Real-time Chat Interface**

## Prerequisites

- Python 3.8+
- Mistral AI API Key (get it from [https://console.mistral.ai/](https://console.mistral.ai/))

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/hirani60-ops/Banking-Bot.git
   cd Banking-Bot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your Mistral API key:
   ```
   MISTRAL_API_KEY=your_api_key_here
   ```

## Running Locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Deployment to Streamlit Cloud

1. **Push to GitHub** (already done)

2. **Deploy to Streamlit Cloud**:
   - Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
   - Click "New app"
   - Select your GitHub repository: `hirani60-ops/Banking-Bot`
   - Select branch: `main`
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Add Secrets**:
   - In Streamlit Cloud dashboard, go to your app settings
   - Click "Secrets"
   - Add your Mistral API key:
     ```
     MISTRAL_API_KEY = "your_api_key_here"
     ```

## Project Structure

```
Banking-Bot/
├── app.py                           # Main Streamlit application
├── requirements.txt                 # Python dependencies
├── .env.example                     # Example environment variables
├── .gitignore                       # Git ignore file
├── README.md                        # This file
└── hbdb_banking_faqs (2) (1).csv   # FAQ database
```

## How It Works

1. **Load FAQ Data**: The app reads the Banking FAQ CSV file
2. **User Input**: User asks a banking question
3. **AI Processing**: The question is sent to Mistral Large with FAQ context
4. **Response Generation**: The model generates an answer based on FAQs and general banking knowledge
5. **Display**: The response is displayed in the Streamlit interface

## Environment Variables

- `MISTRAL_API_KEY`: Your Mistral AI API key (required)

## Technologies Used

- **Mistral Large**: Large language model for generating responses
- **Streamlit**: Web framework for building the UI
- **Pandas**: Data processing for FAQ database
- **Python-dotenv**: Environment variable management

## Security Notes

- Never commit `.env` file to GitHub
- Always use environment variables for sensitive data
- Regularly rotate your API keys

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the FAQ section in the app
2. Contact HBDB customer service through the app
3. Open an issue on GitHub: [https://github.com/hirani60-ops/Banking-Bot/issues](https://github.com/hirani60-ops/Banking-Bot/issues)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Built with ❤️ using Mistral AI**
