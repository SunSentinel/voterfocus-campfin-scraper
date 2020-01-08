import pathlib
import requests

class VoterFocusScraper(object):

    CURRENT_DIR = pathlib.Path(__file__).parent
    
    def __init__(self, county=None, election_id=None, data_dir=None, BASE_URL=None):

        if not county:
            raise NotImplementedError("County not specified. Pass in a lowercase county name with the 'county' parameter.")

        self.county = county

        
        if not election_id:
            self.BASE_URL = "https://www.voterfocus.com/CampaignFinance/candidate_pr.php?c=" + county
        else: 
            self.BASE_URL = "https://www.voterfocus.com/CampaignFinance/candidate_pr.php?c=" + county + "&el=" + election_id
            self.election_id = election_id


        # Make sure there's a place to save the data. If not, make it.
        if data_dir:
            self.data_dir = pathlib.Path(str(data_dir))
        else:
            self.data_dir = self.CURRENT_DIR.parent.joinpath("data")

        if not self.data_dir.exists():
            self.data_dir.mkdir()

    def request(self, url):

        r = requests.get(url,allow_redirects=True)
        if r.status_code == 200:
            page_data = r.text
            return page_data

        else:
            print("====\nERROR: {0} response from server\n====".format(
                                                                r.status_code
                                                                ))

