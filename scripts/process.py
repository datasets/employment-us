import os
import requests
from bs4 import BeautifulSoup

class Regular:
    def __init__(self):
        self.url = 'https://www.bls.gov/cps/cpsaat01.htm'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1'
        }
        self.data = []

    def parse_bls(self):
        try:
            response = requests.get(self.url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'id':'cps_eeann_year'})
            
            if table is None:
                print("Available table IDs:")
                for t in soup.find_all('table'):
                    print(f"- {t.get('id', 'no-id')}")
                raise ValueError(f"Could not find table with id 'cps_eeann_year' at {self.url}")
            
            tbody = table.find('tbody') or table
            
            for row in tbody.find_all('tr')[1:]:
                # skip first row since it's a header
                cells = row.find_all(['th', 'td'])
                # check if first row's year is more than 2010
                if len(cells) > 0 and int(cells[0].text.strip()) > 2010:
                    # Parse from 0 to -1 because we want all columns including the last one
                    # Remove commas and clean the numbers
                    cleaned_cells = [cell.text.strip().replace(',', '') for cell in cells[:]]
                    self.data.append(cleaned_cells)
            
            if not self.data:
                raise ValueError("No data was extracted from the table")
            
            return self.data
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            print(f"Response status code: {getattr(e.response, 'status_code', 'N/A')}")
            print(f"Response headers: {getattr(e.response, 'headers', {})}")
            raise

    def merge_data(self):
        # Read aat1.csv as a list of lists
        with open(os.path.join('archive', 'aat1.csv'), 'r') as f:
            aat1_data = [line.strip().split(',') for line in f.readlines()]
        
        header = aat1_data[0]
        aat1_data = aat1_data[1:]

        # Merge aat1_data and self.data
        merged_data = [header] + aat1_data + self.data
        
        # Write the data into the data folder
        with open(os.path.join('data', 'aat1.csv'), 'w') as f:
            for row in merged_data:
                f.write(','.join(row) + '\n')


if __name__ == '__main__':
    regular = Regular()
    regular.parse_bls()
    regular.merge_data()
