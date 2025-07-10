# Wasit market trends 🥕🍅

A real-time market price monitoring system for agricultural products, with Arabic/English bilingual support.

**Key Features:**
- Real-time price collection from multiple sources
- Arabic/English data processing
- PostgreSQL storage with historical tracking
- Chatbot interface for price queries

## Table of Contents
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Database Setup](#database-setup) 
- [Contribution Guidelines](#contribution-guidelines)
- [License](#license) 

## Installation

### Prerequisites
- Python 3.12+
- PostgreSQL 17+
- Redis (for caching, optional)

```bash
# Clone the repository
git clone https://github.com/rida-wasit/vegetable_price_tracker.git
cd vegetable-price-tracker

# Create virtual environment (Linux/macOS)
python3 -m venv .venv
source .venv/bin/activate

# Or Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
