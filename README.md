# VoterFocus scraper

A python library to fetch campaign contribution data from government entities that use VoterFocus, an election management tool from VR Systems, Inc.

Here's an example: https://www.voterfocus.com/CampaignFinance/candidate_pr.php?c=palmbeach


## Usage


#### To get all candidates in an election
Election objects contain all of the candidates on the election webpage

```python
from voterfocus import Election

scraper = Election(county="palmbeach")
print(scraper.candidates)
```

This returns contribution totals for all candidates in each race in Palm Beach County as a JSON object.

```json
[    
    {
        "id": "333",
        "county": "palmbeach",
        "office": "Sheriff",
        "name": "Ric Bradshaw",
        "party": "DEM",
        "file_status": "Active-Filed",
        "monetary_contributions": 555805,
        "in-kind_contributions": 4042,
        "expenses": 34034.96
    },
    ... 
]
```


#### To download all campaign finance data for an election
This will download a spreadsheet of contributions and expenses in a separate file for each candidate in a `data/` directory.

```python
from voterfocus import Election

scraper = Election(county="palmbeach")
scraper.get_all_cash()
```