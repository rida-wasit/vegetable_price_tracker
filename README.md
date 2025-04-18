# Vegetable Price Tracker 🥕🍅

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
- Python 3.9+
- PostgreSQL 14+
- Redis (for caching, optional)

```bash
# Clone the repository
git clone https://github.com/yourrepo/vegetable-price-tracker.git
cd vegetable-price-tracker

# Create virtual environment (Linux/macOS)
python3 -m venv .venv
source .venv/bin/activate

# Or Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt