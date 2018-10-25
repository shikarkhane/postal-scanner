# coding=utf-8
from bs4 import BeautifulSoup

html = ''' <div id="resultsPanel">
					<hr><p>Item summary</p><table><tbody><tr><th>Tracking number</th><th>Origin</th><th>Destination</th><th>Status</th></tr><tr><td>RE165006654SE</td><td>SWEDEN</td><td>SRI LANKA</td><td bgcolor="#80FF80">Delivered</td></tr></tbody></table><p>Activity summary</p><table><tbody><tr><th>Local date/time</th><th>Activity</th><th>Location</th><th>Remarks</th></tr><tr><td>10/8/2018 9:41 PM</td><td>Final delivery</td><td>ND10250</td><td></td></tr></tbody></table><p class="warning">No tracking information is available from SWEDEN</p>
					<br>
					<input type="submit" name="btnNewSearch" value="New search" id="btnNewSearch" class="btn">
				</div>'''

soup = BeautifulSoup(html, 'html.parser')

delivery = soup.find_all('table')[1]
print ( 'nikhil')