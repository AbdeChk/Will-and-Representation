# Will-and-Representation

### 📖 About This Repository
This project collects and analyzes the works of **Arthur Schopenhauer**. It provides simple metrics on his texts, including:

- **Network similarity** between books  
- **Sentiment analysis** of key writings  
- **Word counts** and **bar charts** for easy visualization  

> **Note:** Some books have not been processed properly and may not appear correctly in the analyses.

---
![Alt text](assets/gif.gif)

---

## Prerequisites

Before running the project, ensure you have the following installed:

- [Python 3.x](https://www.python.org/downloads/)  
- [pip](https://pip.pypa.io/en/stable/)  
- [Git](https://git-scm.com/)  

---

## Installation

Follow these steps to set up and run the app on your local machine:

1. Clone the repository:
```bash
git clone https://github.com/AbdeChk/Will-and-Representation.git
```

2. Navigate to the project directory:
```bash
cd Will-and-Representation
```

3. Create and activate a virtual environment (recommended):
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

4. Install required dependencies:
```bash
pip install -r requirements.txt
```

5. Run the application:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.
