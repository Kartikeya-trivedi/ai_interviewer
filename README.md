# AI Interviewer System

A cross-platform AI interviewer application designed to work seamlessly on Windows and Linux systems.

## Features

- ✅ Cross-platform support (Windows & Linux)
- 🤖 AI-powered interview management
- 📝 Question and response tracking
- ⚙️ Configurable interview settings
- 🖥️ Command-line interface

## Platform Support

This application has been designed to run on:
- **Windows** (Windows 10/11 and Server)
- **Linux** (Ubuntu, Debian, Fedora, and other distributions)

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Kartikeya-trivedi/ai_interviewer.git
cd ai_interviewer
```

2. (Optional) Create a virtual environment:

**On Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the application in demo mode:

```bash
python main.py --demo
```

### Check Platform Information

To verify your platform is supported:

```bash
python main.py --info
```

### Help

For all available options:

```bash
python main.py --help
```

## Project Structure

```
ai_interviewer/
├── src/                    # Source code
│   ├── __init__.py
│   └── interviewer.py     # Core interviewer logic
├── tests/                 # Test files
├── docs/                  # Documentation
├── main.py               # Application entry point
├── config.yaml           # Configuration file
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Configuration

Edit `config.yaml` to customize interview settings:

- Maximum number of questions
- Timeout settings
- Platform-specific options
- Output format and location

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

See LICENSE file for details.

## Author

Kartikeya Trivedi

## Version

Current version: 0.1.0