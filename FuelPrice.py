from bs4 import BeautifulSoup
from requests import get
import re

URL_BASE = "https://bensinpriser.nu/stationer/"
URL_LOCATION = "orebro-lan/hallsberg"

class FuelPrice:
    def get_data(self, fuel_type):
        url = f"{URL_BASE}{fuel_type}/{URL_LOCATION}"
        raw_html = get(url, stream=True).content
        soup = BeautifulSoup(raw_html, 'html.parser')
        table = soup.find("table", attrs={"class":"table"})
        head = ["Station", "City", "Adress", "Price", "Date"]

        # messy code to clean up the raw html data 
        rv = []
        for tr in table.find_all('tr'): # for all rows in table 
            # make list with only the useful data on the row 
            clean_list = [BeautifulSoup(data, features="html.parser").get_text() for data in re.split("</small></b><br/>| <small>|</b><br/><small>|</td>", str(tr).replace('\n', ''))] 
            clean_list.pop(-1) # I know this is ugly, it is to remove an empty place in the list caused by splitting on new line (</td>) which had to be done
            if clean_list: 
                rv.append(dict(zip(head, clean_list)))

        return rv

    def get_lowest_price(self, data):
        # Lowest price is always the first dict in the list, as the html-data is already sorted by price 
        return data[0]
            

    def main(self):
        switch = {"1":"diesel", "2":"95"}
        fuel_type = switch[input(f"Please input number associated with desired fuel type:\n1 for diesel\n2 for 95\n")]
    
        data = self.get_data(fuel_type)
        lowest_price = self.get_lowest_price(data)
        print(f'\nLowest price for {fuel_type}:\n{lowest_price["Station"]} @ {lowest_price["Price"]}\n{lowest_price["Adress"]}')


if __name__ == "__main__":
    FuelPrice().main()




""""
Example data for 1 row in table:

</tr>
<tr class="table-row" data-href="/station/orebro-lan/hallsberg/samzeliigatan" style="cursor: pointer;">
<td><b>Tanka <small>Hallsberg</small></b><br/>Samzeliigatan</td>
<td><b style="color: #84845C;">17,57kr</b><br/><small>7/9</small></td>
</tr>

""" 
