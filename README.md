# Stock Market Analysis & Visualization Platform 📈

An interactive web application that helps users learn about stock market analysis through data visualization and AI-powered insights. This platform makes technical analysis accessible to everyone with intuitive visualizations and natural language interaction.

## Features ✨

- **Interactive Candlestick Charts** - Visualize stock price movements with various technical indicators
- **Multiple Technical Indicators** including:
  - Simple Moving Averages (SMA)
  - Exponential Moving Averages (EMA)
  - Moving Average Convergence Divergence (MACD)
  - Volatility metrics
- **AI-Powered Q&A** - Ask questions about stock data in plain English and get intelligent responses
- **User-Friendly Interface** - Clean, intuitive design built with Streamlit

## Installation 🛠️

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/stock-visualisation.git
   cd stock-visualisation
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage 🚀

1. Start the Streamlit application:
   ```bash
   streamlit run 1_Getting_👋_Started.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`

3. Explore the different sections using the sidebar navigation

## Project Structure 📂

```
stock-visualisation/
├── 1_Getting_👋_Started.py    # Main entry point and welcome page
├── pages/                     # Individual Streamlit pages
│   ├── 2_Candlesticks_💹.py
│   ├── 3_MACD_Indicator_💸.py
│   └── 4_Chat_🚀.py
├── src/
│   ├── components/           # Reusable chart components
│   │   └── charts.py
│   └── functions/            # Utility functions
│       └── generic_functions.py
└── requirements.txt          # Project dependencies
```

## Technologies Used 💻

- **Python** - Core programming language
- **Streamlit** - Web application framework
- **Plotly** - Interactive data visualization
- **Pandas** - Data manipulation and analysis
- **yfinance** - Financial market data

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- Built with ❤️ for educational purposes
- Special thanks to the Streamlit and Plotly communities for their amazing tools

---

Happy Trading! 📊🚀
