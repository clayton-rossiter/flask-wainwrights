from src.api import app
from src.scraper import Scraper


def scrape():
    """uses Scraper class to retrieve Wainwright fell and outlying fell data"""
    scraper = Scraper()
    scraper.scrape_wikipedia()
    scraper.convert_grid_references()
    df = scraper.append_df()
    return df


if __name__ == '__main__':
    app.run(debug=True)