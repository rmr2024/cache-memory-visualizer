# Cache Memory Visualizer

An interactive learning tool for understanding cache memory mapping techniques in Computer Organization and Architecture.

## Features

- **Three Mapping Techniques**: Direct Mapping, Fully Associative, Set Associative
- **Replacement Policies**: FIFO and LRU
- **Step-by-step Animation**: Visual simulation with configurable speed
- **Real-time Statistics**: Hit/Miss ratios and performance metrics
- **Educational Explanations**: Formula display and step-by-step reasoning
- **Interactive Controls**: Manual stepping or auto-run mode

## Installation

```bash
pip install -r requirements.txt
```

## Run Locally

```bash
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy!

## Usage

1. Select mapping type from sidebar
2. Configure cache size and parameters
3. Enter memory access sequence (or use examples)
4. Click "Start" to begin simulation
5. Watch the step-by-step visualization
6. Analyze hit/miss statistics

## Tech Stack

- Python 3
- Streamlit
- Clean modular architecture

## License

MIT
