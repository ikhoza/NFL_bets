# NFL_public

## Overview
**NFL_public** showcases a system I’ve developed for profitable sports betting on NFL games. The system generates a score for each gamee where:
- Positive values indicate a higher likelihood of a home team win.
- Negative values indicate a higher likelihood of an away team win.

The greater the absolute value of the score, the higher the probability of the corresponding team’s victory. 

While the specific method for calculating these scores is proprietary, this repository includes:
- A file containing precalculated scores for NFL games from 2010 - 2023.
- A scraping script for collecting NFL game data.
- The method used to determine optimal betting amounts based on the calculated scores.

## Features
- Precalculated Game Scores: A data file containing scores for past NFL games (2010-2023) is provided. These scores serve as the foundation for betting decisions.
- Web Scraping Script: A Python script to scrape NFL game data, enabling future updates with new game data.
- Betting Strategy: Documentation and code outlining how to calculate optimal betting amounts based on game scores and associated probabilities.

## Data Sources
The data used spans from 2010 to 2023 and is sourced from publicly available NFL game results and statistics. The provided scraping script handles data collection for future use.

## How to Use
1. **Clone the repository**:
   ```bash
   git clone https://github.com/ikhoza/NFL_public.git
   ```
2. **Set up the environment** by installing the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the scraping script** to collect new data (optional):
   ```bash
   python scrape_nfl_data.py
   ```
4. **Analyze scores** using the provided betting strategy to determine optimal bets based on the game's score.

## Betting Strategy
The betting method included here demonstrates how to leverage the scores to maximize returns. It calculates the optimal bet size based on confidence in the score’s prediction, offering a guide for betting decisions.

## Disclaimer
This project is for **educational purposes only**. Betting involves risk, and there are no guarantees of profit. Please gamble responsibly.

---

**Author**: Cody Dunlap  
**Contact**: cdunlap0325@gmail.com