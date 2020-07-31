######## PLOTTING USING 39000+ TILES DICTIONAIRY #############################################
import rasterio as rio
import plotly.graph_objects as go
from rasterio.mask import mask
import requests
import re


################################################################################################

# find coordinates of address you are searching

address = "Sint-Pietersvliet 7, 2000 Antwerpen"
#address = "Francis Wellesplein 1, 2018 Antwerpen"
#address = "Eigenaarsstraat 13, 2350 Vosselaar"
#address = "De Keyserlei 50, 2000 Antwerpen"
#address = "Narcislaan 13, 2900 Schoten"
#address = "Werverbos 78, 2930 Brasschaat"
#address = "Pareloesterlaan 15, 8400 Oostende"
#address = "De Tomermaat 25, 2930 Brasschaat"
#address = "Huidevetterslaan 10, 3500 Hasselt"
#address = "Serafijnstraat 8, 9000 Gent"
#address = "Veldstraat 45, 9630 Zwalm"


def get_coordinates(address: str) -> (int, int):
    req = requests.get(f"http://loc.geopunt.be/geolocation/location?q={address}&c=1")
    return (req.json()["LocationResult"][0]["Location"]["X_Lambert72"],
            req.json()["LocationResult"][0]["Location"]["Y_Lambert72"])


coordinaten = get_coordinates(address)
x = coordinaten[0]
y = coordinaten[1]
print("x coordinaat = ", coordinaten[0])  # X
print("y coordinaat = ", coordinaten[1])  # Y

########################################################################################################

# compare coordinate values to values of pandaframe

path = "./tile_12040.tif"


#################### PROJECT HOUSE #################################################""

data = rio.open(path)
address_regx = re.compile("^([A-z- ]+)\s(\d+),\s(\d+)\s([A-z]+)")
result = address_regx.search(address)
street = result.group(1)
print(street)
nb = result.group(2)
print(nb)
pc = result.group(3)
print(pc)
city = result.group(4)
print(city)

req = requests.get(
            f"https://api.basisregisters.dev-vlaanderen.be/v1/adresmatch?gemeentenaam={city}&straatnaam={street}&huisnummer={nb}&postcode={pc}").json()
objectId = req["adresMatches"][0]["adresseerbareObjecten"][0]["objectId"]

req = requests.get(f"https://api.basisregisters.dev-vlaanderen.be/v1/gebouweenheden/{objectId}").json()
objectId = req["gebouw"]["objectId"]

req = requests.get(f"https://api.basisregisters.dev-vlaanderen.be/v1/gebouwen/{objectId}").json()
polygon = [req["geometriePolygoon"]["polygon"]]
print("polygon -> ", polygon)

crop_img, crop_transform = mask(dataset=data, shapes=polygon, crop=True, indexes=1, nodata=0, filled=True)
print("crop image -> ", crop_img)

fig = go.Figure(data=go.Surface(z=crop_img, colorscale='YlOrRd'))
fig.show()


#################### PLOT HOUSE ####################w

data = rio.open(path)
address_regx = re.compile("^([A-z- ]+)\s(\d+),\s(\d+)\s([A-z]+)")
result = address_regx.search(address)
street = result.group(1)
print(street)
nb = result.group(2)
print(nb)
pc = result.group(3)
print(pc)
city = result.group(4)
print(city)

req = requests.get(
    f"https://api.basisregisters.dev-vlaanderen.be/v1/adresmatch?gemeentenaam={city}&straatnaam={street}&huisnummer={nb}&postcode={pc}").json()
objectId = req["adresMatches"][0]["adresseerbareObjecten"][0]["objectId"]

req = requests.get(f"https://api.basisregisters.dev-vlaanderen.be/v1/gebouweenheden/{objectId}").json()
objectId = req["gebouw"]["objectId"]

req = requests.get(f"https://api.basisregisters.dev-vlaanderen.be/v1/gebouwen/{objectId}").json()
polygon = [req["geometriePolygoon"]["polygon"]]
print("polygon -> ", polygon)

crop_img, crop_transform = mask(dataset=data, shapes=polygon, crop=True, indexes=1, nodata=0, filled=True)
print("crop image -> ", crop_img)

fig = go.Figure(data=go.Surface(z=crop_img, colorscale='YlOrRd'))
fig.show()








