import googlemaps
from flask import Flask, render_template, request
import http.client
import requests
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('finalPage.html',dialogue=list())

@app.route("/dialogue", methods = ["POST","GET"])
@app.route("/<dialogue>/<dialogue2>", methods = ["POST","GET"])
def dialogue():
    print("salut")
    lat = request.form["lat"]
    long = request.form["long"]
    print("salut")
    print(lat,long,type(lat),float(lat),float(long))
    name = googleApi((float(lat), float(long)) )
    info = extractText(name)
    tr_info = translate_text("ro",info)
    return render_template('finalPage.html',dialogue=[(name,info,tr_info)])

def extractText(topic):
    conn = http.client.HTTPSConnection("en.wikipedia.org")

    headers = {
        'cache-control': "no-cache",
        'postman-token': "11291106-6c83-deb8-41ff-7d54140c90da"
    }
    topic.replace(" ", "%20")
    conn.request("GET",
                 "/w/api.php?action=query&titles=" + topic + "&prop=revisions&rvprop=content&format=json&formatversion=2",
                 headers=headers)

    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    print(data)
    data= data.split("{")
    max_now = 0
    for d in data:
        if len(d) > max_now:
            max_now = len(d)
            maxim = d
    return maxim

def translate_text(target, text):
    # TODO: If you have your own Client ID and secret, put down their values here:
    clientId = "FREE_TRIAL_ACCOUNT"
    clientSecret = "PUBLIC_SECRET"

    # TODO: Specify your translation requirements here:
    fromLang = "en"
    toLang = target
    text = text[:500]
    jsonBody = {
        'fromLang': fromLang,
        'toLang': toLang,
        'text': text
    }

    headers = {
        'X-WM-CLIENT-ID': clientId,
        'X-WM-CLIENT-SECRET': clientSecret
    }

    r = requests.post('http://api.whatsmate.net/v1/translation/translate',
                      headers=headers,
                      json=jsonBody)

    print("Status code: " + str(r.status_code))
    print("Translated Text: " + r.content.decode("utf-8"))
    return str(r.content)

def googleApi(t):
    gmaps = googlemaps.Client(key="AIzaSyBHfcD4fUVauqK5D3vQ7FcH9T0SGH6ja1A")
    # myschool-196618 id
    # AIzaSyCeih_XkR0ePd54CvueWLVJ63iMYjaQYJY
    reverse_geocode_result = gmaps.reverse_geocode(t)
    st = reverse_geocode_result[2]
    name_of_loc = st["address_components"][0]["short_name"]
    return name_of_loc


def tema2():
    gmaps = googlemaps.Client(key="AIzaSyBHfcD4fUVauqK5D3vQ7FcH9T0SGH6ja1A")
    # myschool-196618 id
    # AIzaSyCeih_XkR0ePd54CvueWLVJ63iMYjaQYJY
    #reverse_geocode_result = gmaps.reverse_geocode((47.1584549, 27.601441799999975))#46.7667,23.6
    reverse_geocode_result = gmaps.reverse_geocode((46.7667,23.6))
    st = reverse_geocode_result[2]
    name_of_loc = st["address_components"][0]["short_name"]
    print(name_of_loc)
    infoAboutlocation = extractText(name_of_loc)
    translate_text("ro", infoAboutlocation)


#tema2()
if __name__ == "__main__":
       app.run(debug=True)
