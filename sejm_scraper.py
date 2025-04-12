import requests
import pandas as pd
import time
import random
from tqdm import tqdm

BASE_API_URL = "https://api.sejm.gov.pl/sejm/term{term}/votings/{session}/{vote}"
BASE_VOTE_LIST_URL = "https://api.sejm.gov.pl/sejm/term{term}/votings/{session}"

def get_votes_for_session(term, session):
    """
    Get all votes from a specific session in a given term.
    """
    url = BASE_VOTE_LIST_URL.format(term=term, session=session)
    try:
        res = requests.get(url)
        if res.status_code != 200:
            return []
        return res.json()
    except Exception as e:
        print(f"Error getting votes for term {term} session {session}: {e}")
        return []

def get_vote_details(term, session, vote):
    """
    Get detailed results for a single vote.
    """
    url = BASE_API_URL.format(term=term, session=session, vote=vote)
    try:
        res = requests.get(url)
        if res.status_code != 200:
            return None
        return res.json()
    except Exception as e:
        print(f"Error getting vote detail for term {term} session {session} vote {vote}: {e}")
        return None

def summarize_party_votes(vote_json):
    """
    Count how each party voted: Yes, No, Abstain, or Not Voting.
    """
    vote_data = []
    votes = vote_json.get('votes', [])
    title = vote_json.get('title')
    date = vote_json.get('date')
    term = vote_json.get('term')
    session = vote_json.get('sitting')
    vote_number = vote_json.get('votingNumber')

    party_counts = {}
    for v in votes:
        party = v.get('club', 'UNKNOWN')
        decision = v.get('vote')
        if party not in party_counts:
            party_counts[party] = {'Yes': 0, 'No': 0, 'Abstain': 0, 'Not Voting': 0}

        if decision == 'YES':
            party_counts[party]['Yes'] += 1
        elif decision == 'NO':
            party_counts[party]['No'] += 1
        elif decision == 'ABSTAIN':
            party_counts[party]['Abstain'] += 1
        else:
            party_counts[party]['Not Voting'] += 1

    for party, counts in party_counts.items():
        vote_data.append({
            'Term': term,
            'Session': session,
            'Vote Number': vote_number,
            'Date': date,
            'Policy Title': title,
            'Party': party,
            'Yes': counts['Yes'],
            'No': counts['No'],
            'Abstain': counts['Abstain'],
            'Not Voting': counts['Not Voting']
        })
    return vote_data

def scrape_sejm_votes():
    """
    Go through all terms and sessions collecting votes.
    """
    all_data = []
    for term in range(7, 11):
        print(f"Processing term {term}...")
        session = 1
        while True:
            votes_list = get_votes_for_session(term, session)
            if not votes_list:
                break  # assume no more sessions
            print(f"  Session {session}: {len(votes_list)} votes")
            for vote in tqdm(votes_list, desc=f"Term {term} Session {session}", leave=False):
                vote_number = vote.get('votingNumber')
                details = get_vote_details(term, session, vote_number)
                if details:
                    summary = summarize_party_votes(details)
                    all_data.extend(summary)
                    time.sleep(random.uniform(0.3, 0.8))
            session += 1
    return all_data

if __name__ == "__main__":
    data = scrape_sejm_votes()
    df = pd.DataFrame(data)
    df.to_csv("sejm_votes_by_party.csv", index=False, encoding='utf-8')
    print("Saved to sejm_votes_by_party.csv")
