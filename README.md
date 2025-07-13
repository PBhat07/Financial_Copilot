# Financial Copilot 🤖📊

> AI-Powered Financial Analysis Platform with Multi-LLM Support

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-green.svg)](https://langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Financial Copilot is an advanced AI-powered financial analysis platform that combines multiple Large Language Models (Gemini & Claude) with real-time financial data APIs to provide comprehensive investment insights, market analysis, and portfolio recommendations.

## ✨ Features

- **🤖 Multi-LLM Support**: Switch between Google Gemini and Anthropic Claude
- **📊 Real-time Data**: Live stock prices, earnings, and financial news
- **🔍 RAG Pipeline**: Document search and analysis capabilities
- **💬 Interactive Interface**: User-friendly chat interface
- **⚡ Fast Performance**: Sub-5 second response times
- **🔧 Modular Architecture**: Easy to extend and customize

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- API keys for:
  - [Google Gemini](https://makersuite.google.com/app/apikey)
  - [Anthropic Claude](https://console.anthropic.com/)
  - [Twelve Data](https://twelvedata.com/) (stock data)
  - [Financial Modeling Prep](https://financialmodelingprep.com/) (financial data)
  - [News API](https://newsapi.org/) (news data)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/PBhat07/Financial_Copilot.git
   cd Financial_Copilot
   ```

2. **Set up the environment**
   ```bash
   # Copy example environment file
   cp env.example .env
   
   # Edit .env with your API keys
   nano .env  # or use your preferred editor
   ```

3. **Install dependencies**
   ```bash
   # Install PyTorch first (platform-specific)
   # Windows:
   pip install torch --index-url https://download.pytorch.org/whl/cpu
   
   # Linux/Mac:
   pip install torch
   
   # Install remaining dependencies
   pip install -r requirements.txt
   ```

4. **Add financial documents** (optional)
   ```bash
   # Option 1: Download sample documents
   python financial_downloader.py
   
   # Option 2: Manually add PDFs to data/financial_docs/
   ```

5. **Start the API server** (in one terminal)
   ```bash
   python launch_api.py
   ```

6. **Run the interactive launcher** (in another terminal)
   ```bash
   python interactive_launcher.py
   ```

## 📖 Usage

### Interactive Mode

The easiest way to use Financial Copilot is through the interactive launcher:

```bash
python interactive_launcher.py
```

This provides a menu-driven interface with options for:
- Quick testing
- Comprehensive testing
- Interactive chat
- Example queries
- Backend switching

### Example Queries

#### General Knowledge
```
"Explain the concept of market capitalization"
"What is the difference between fundamental and technical analysis?"
"How do I calculate the P/E ratio?"
```

#### Real-time Data
```
"Get the current stock price of AAPL"
"What are the latest earnings for TSLA?"
"Show me recent news about Microsoft"
```

#### Investment Analysis
```
"Compare Apple and Microsoft as investment opportunities"
"What are the key risks for AI companies?"
"How would you analyze a company's competitive moat?"
```

#### Portfolio Strategy
```
"If I have $10,000 to invest, what would be a good strategy?"
"How should I adjust my investment strategy for a recession?"
"What are the pros and cons of value vs growth investing?"
```

### Programmatic Usage

```python
from agent.agent_executor import FinancialAgentExecutor

# Initialize agent
agent = FinancialAgentExecutor()

# Process queries
result = agent.process_query("Get the current stock price of AAPL")
print(result['answer'])
```

## 🏗️ Architecture

```
┌──────────────────┐        ┌───────────────────────┐
│  User Interface  │───────►│  Interactive Launcher │
└──────────────────┘        └─────────┬─────────────┘
                                      ▼
                            ┌───────────────────────┐
                            │ FinancialAgentExecutor│
                            └─────────┬─────────────┘
          ┌────────────────────────────┼────────────────────────────┐
          │                            │                            │
          ▼                            ▼                            ▼
┌────────────────┐         ┌────────────────────────┐     ┌─────────────────┐
│ RAG Pipeline   │  JSON   │ FastAPI External Tools │     │ Direct LLM Call │
│ Document Search│◄───────►│ (stock, earnings, news)│     │ (Claude/Gemini)│
└────────────────┘         └────────────────────────┘     └─────────────────┘
```

### Core Components

- **`agent/agent_executor.py`**: Main agent orchestrator
- **`models/model_provider.py`**: LLM backend management
- **`rag/rag_pipeline.py`**: Document search and analysis
- **`api_server.py`**: External API server for real-time data
- **`interactive_launcher.py`**: User-friendly interface

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `LLM_BACKEND` | LLM backend: `gemini` or `claude` | Yes |
| `GOOGLE_API_KEY` | Google Gemini API key | For Gemini |
| `ANTHROPIC_API_KEY` | Anthropic Claude API key | For Claude |
| `EXTERNAL_API_URL` | External API server URL | Auto-detected |
| `TWELVE_DATA_API_KEY` | Twelve Data API key | Yes |
| `FMP_API_KEY` | Financial Modeling Prep API key | Yes |
| `NEWS_API_KEY` | News API key | Yes |
| `PDF_DIR` | Directory for financial documents | No |
| `VECTOR_DB_PATH` | Path for vector database | No |

### API Setup

1. **Start the API server**:
   ```bash
   python launch_api.py
   ```

2. **The system will automatically detect the API URL** (localhost or ngrok)

## 🧪 Testing

### Quick Test
```bash
python simple_launcher.py
```

### Comprehensive Test
```bash
python enhanced_test_suite.py
```

### Interactive Testing
```bash
python interactive_launcher.py
# Choose option 1 for quick test or 2 for comprehensive test
```

### System Test
```bash
python test_system.py
```

## 📊 Performance

Based on our testing with 15 complex queries:

| Metric | Gemini | Claude |
|--------|--------|--------|
| Success Rate | 100% | 100% |
| Avg Response Time | 4.70s | 4.97s |
| Query Types | All | All |

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure you're in the correct directory
   cd Financial_Copilot
   
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

2. **API Key Errors**
   ```bash
   # Check your .env file
   cat .env
   
   # Ensure all required keys are set
   ```

3. **PyTorch Installation Issues (Windows)**
   ```bash
   # Use CPU-only version
   pip install torch --index-url https://download.pytorch.org/whl/cpu
   ```

4. **FAISS Installation Issues**
   ```bash
   # Try installing without dependencies
   pip install faiss-cpu --no-deps
   ```

5. **API Server Not Found**
   ```bash
   # Start the API server first
   python launch_api.py
   
   # Then run the interactive launcher
   python interactive_launcher.py
   ```

### Platform-Specific Notes

- **Windows**: Use CPU-only PyTorch and check FAISS compatibility
- **Linux/Mac**: Standard installation should work
- **Google Colab**: Works out of the box

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues and pull requests.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Code Style

- Use Black for code formatting
- Follow PEP 8 guidelines
- Add type hints where appropriate
- Include docstrings for functions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the agent framework
- [Google Gemini](https://ai.google.dev/) for AI capabilities
- [Anthropic Claude](https://www.anthropic.com/) for AI capabilities
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/PBhat07/Financial_Copilot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/PBhat07/Financial_Copilot/discussions)

## 🗺️ Roadmap

See [ROADMAP.md](ROADMAP.md) for detailed development plans.

### Upcoming Features

- [ ] Web interface
- [ ] Portfolio management
- [ ] Advanced analytics
- [ ] Mobile app
- [ ] Enterprise features

---

**Made with ❤️ by the Financial Copilot Team**


