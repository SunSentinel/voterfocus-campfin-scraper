import re
import csv
import json
import requests
from slugify import slugify
from datetime import datetime

from bs4 import BeautifulSoup
from collections import OrderedDict
from .base import VoterFocusScraper

from .utils import *


class Election(VoterFocusScraper):

    def __init__(self, election_id=None, *args, **kwargs):
        super(Election, self).__init__(*args, **kwargs)
        self.election_id = election_id
        self.candidates = self._get_candidates()


    def _get_candidates(self):

        page_data = self.request(self.BASE_URL)

        # List of candidates
        candidate_list = []

        soup = BeautifulSoup(page_data, "html.parser")
        office_groups = soup.find_all("div", attrs={"class": "officegroup"})

        for contest in office_groups:

            # Race name row
            contest_name = contest.find("div", attrs={"class": "officename"}).text.replace("Office: ", "")

            # Candidate rows
            candidates = contest.find_all("div", attrs={"class": "candidate"})

            for candidate in candidates:
                row_link = candidate.find("a", attrs={"class": "rowlink"})

                link_href = row_link["href"]
                cand_id = re.findall(r'&ca=(.+?)&', link_href)[0]

                row_cells = candidate.find_all("div", attrs={"role": "gridcell"})

                # Remove screenreader label tag
                row_cells[2].span.decompose()
                row_cells[3].span.decompose()
                row_cells[4].span.decompose()
                
                candidate_obj = {
                    "id": cand_id,
                    "county": self.county,
                    "office": contest_name, 
                    "name": get_name(row_cells[0].text),
                    "party": get_in_parenthesis(row_cells[0].text),
                    "file_status": get_in_parenthesis(row_cells[1].text),
                    "monetary_contributions": CashtoFloat(row_cells[2].text),
                    "in-kind_contributions": CashtoFloat(row_cells[3].text),
                    "expenses": CashtoFloat(row_cells[4].text)
                }

                candidate_list.append(candidate_obj)

        return candidate_list



    def get_all_cash(self):
        """
        Downloads all campaign finance data for each candidate in the election and saves them locally.
        """

        if self.CURRENT_DIR.parent.joinpath("data", self.county).exists():
            pass
        else:
            self.CURRENT_DIR.parent.joinpath("data", self.county).mkdir()


        for candidate in self.candidates:

            race_slug = slugify(candidate["office"])

            if self.CURRENT_DIR.parent.joinpath("data", self.county, race_slug).exists():
                pass
            else:
                self.CURRENT_DIR.parent.joinpath("data", self.county, race_slug).mkdir()
            
            # Build download url
            dl_link = "https://www.voterfocus.com/CampaignFinance/export.php?op=CFINANCE&cand_id={0}&dhc=0&county={1}".format(candidate["id"], self.county)

            # Download file
            dl_file = requests.get(dl_link)

            save_file = self.data_dir.joinpath(
                self.county,
                race_slug, 
                "{0}.csv".format(slugify(candidate["name"])
                )
            )

            with open(save_file, 'wb') as f:
                f.write(dl_file.content)


    def download_summaries(self):
        save_file = self.data_dir.joinpath("{0}_summaries.csv".format(self.county))

        keys = self.candidates[0].keys()
        with open(save_file, 'w') as outf:
            dw = csv.DictWriter(outf, keys)
            dw.writeheader()
            dw.writerows(self.candidates)