
# 🇵🇱 Sejm Vote Scraper

This Python script scrapes and summarizes voting data from the **Polish Sejm** (parliament) using the official [Sejm API](https://api.sejm.gov.pl/). It gathers voting records by term and session, then outputs a clean CSV showing how each political party voted.

---

## 🧠 Features

- ✅ Fetches detailed vote data by term and session
- ✅ Summarizes how each party voted: Yes / No / Abstain / Not Voting
- ✅ Saves the output to a CSV (`sejm_votes_by_party.csv`)
- ✅ Handles API errors and adds delay between requests to avoid rate limits
- ✅ Uses `tqdm` for progress bars

---

## 📦 Requirements

Python 3.7 or higher

Install required libraries with:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

To run the scraper:

```bash
python sejm_scraper.py
```

The script will:
- Loop through all available terms
- Fetch vote lists by session
- Retrieve detailed vote data
- Summarize the votes by party
- Save everything into `sejm_votes_by_party.csv`

---

## 🗃️ Output Example

Here’s what the CSV will look like:

| Term | Session | Vote Number | Date       | Policy Title          | Party    | Yes | No | Abstain | Not Voting |
|------|---------|-------------|------------|------------------------|----------|-----|----|---------|------------|
| 9    | 2       | 15          | 2023-05-12 | Act on Something       | KO       | 98  | 3  | 1       | 0          |
| 9    | 2       | 15          | 2023-05-12 | Act on Something       | PiS      | 230 | 0  | 0       | 5          |

---

## 📁 Files

| File | Description |
|------|-------------|
| `sejm_scraper.py` | The main scraping script |
| `requirements.txt` | Lists required Python libraries |
| `README.md` | This file |
| `sejm_votes_by_party.csv` | Output |

---

## 📚 License

This project is licensed under the **MIT License**.

---

## 💬 Credits

Built using open data from the [Sejm API](https://api.sejm.gov.pl/).  
