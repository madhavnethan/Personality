from flask import Flask, render_template, request, url_for, redirect
import avengers
import math
import os



app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    print("yo, index")
    if request.method == "POST":
        name = request.form.get("name")
        print(name)

        # Getting answers from the form
        skill = request.form.get("skill")
        car = request.form.get("car")
        live = request.form.get("live")
        house = request.form.get("house")
        traits = request.form.getlist("traits")
        music = request.form.getlist("music")
        color = request.form.get("color")
        team = request.form.get("team")

        # Color data is coming to server as a hexadecimal code
        # We need to change that to RGB
        h = color.lstrip('#')
        ct = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

        # Based on color value, we need to approximate the colors
        # Anything closer to red we consider red, same for blue and green
        # Anything grey or black color is considered as black
        # If user selects color that is not any of this, we consider it as an unkown color and wouldn't give points to any characters
        color_value = 'Unkown'

        if ct[0] > ct[1] + ct[2]:
            color_value = 'Red'

        elif ct[1] > ct[0] + ct[2]:
            color_value = 'Green'

        elif ct[2] > ct[1] + ct[0]:
            color_value = 'Blue'

        elif abs(ct[0] - ct[1]) < 20 and abs(ct[1] - ct[2]) < 20 and abs(ct[0] - ct[2]) < 20 and sum(list(ct))/3 < 150:
            color_value = 'Black'

        # Translate the slider value into numbers from 1-4
        team = int(math.ceil(int(team)/5))

        # Built Question + Answer dictionary, questions name as key and answer as value
        qa = {
        'skill' : skill,
        'car' : car,
        'live' : live,
        'house' : house,
        'traits' : traits,
        'music' : music,
        'color' : color_value,
        'team' : team

        }

        # Define avenger character image dictionary
        avg_images = {
        avengers.CA : "https://pm1.narvii.com/6816/2eba7922a72d48a40b1f9bec9d6cb0d10fb190d6v2_hq.jpg",
        avengers.IM : "https://mocah.org/thumbs/330528-Iron-Man-Avengers-Endgame-4K-iphone-wallpaper.jpg",
        avengers.BW : "https://www.nme.com/wp-content/uploads/2018/02/Black-Widow-Avengers-696x442.jpg",
        avengers.HK : "https://www.pluggedin.com/wp-content/uploads/2019/12/the-hulk-1024x640.jpg",
        avengers.HE : "https://images.hindustantimes.com/rf/image_size_630x354/HT/p2/2019/04/14/Pictures/_b928d83c-5ea1-11e9-93dc-bd285d0e4b85.jpg",
        avengers.BP : "https://cdn.mos.cms.futurecdn.net/NtnzY6kWuhqqSWkBXEbbSP-1024-80.jpg.webp",
        avengers.TH : "https://ichef.bbci.co.uk/images/ic/640x360/p09t1hg0.jpg",
        avengers.SM : "https://stylecaster.com/wp-content/uploads/2021/11/Spider-Man-No-Way-Home-2.jpg"

        }

        # Finding out the avenger character from user's answers
        avg_name = get_avenger(qa)

        avg_image = avg_images[avg_name]

        # Send the response back to the user with the appropriate avenger character
        return render_template("submit.html", avg_name = avg_name, qa = qa, avg_image = avg_image)

    else:
        return render_template("index.html")


@app.route("/page2", methods=["GET", "POST"])
def page2():
    
    # Get the values from page 1 and pass it on to page 2
    skill = request.form.get("skill")
    car = request.form.get("car")
    live = request.form.get("live")
    house = request.form.get("house")
    
     
    return render_template("page2.html", skill = skill, car = car, live = live, house = house)
    

def get_avenger(qa):

    # Construct character dictionary, key is character and value is points.
    # Initialize character dictionary with 0 points
    characters = {
    avengers.CA : 0,
    avengers.IM : 0,
    avengers.BW : 0,
    avengers.HK : 0,
    avengers.HE : 0,
    avengers.BP : 0,
    avengers.TH : 0,
    avengers.SM : 0}

    # Question + Answers mapping to avengers list
    #If the key matches we would add one point to the corresponding avenger
    qa_avengers_map = {
    'skill-SS' : [avengers.CA, avengers.TH, avengers.HK],
    'skill-MA' : [avengers.BW, avengers.BP],
    'skill-F' : [avengers.IM],
    'skill-S' : [avengers.HE, avengers.SM],

    'car-Lambo' : [avengers.IM, avengers.TH, avengers.SM],
    'car-Jeep' : [avengers.CA, avengers.HK],
    'car-Cadillac' : [avengers.BW, avengers.HE],
    'car-Lexus' : [avengers.BP],

    'live-NY' : [avengers.IM, avengers.CA, avengers.SM],
    'live-LA' : [avengers.BP, avengers.HK],
    'live-BA' : [avengers.TH],
    'live-BU' : [avengers.BW, avengers.HE],

    'house-mansion' : [avengers.IM],
    'house-reg' : [avengers.HE, avengers.HK, avengers.CA],
    'house-apart' : [avengers.BW, avengers.SM],
    'house-kingdom' : [avengers.BP, avengers.TH],

    'traits-Funny' : [avengers.SM, avengers.TH],
    'traits-Serious' : [avengers.BW, avengers.IM, avengers.BP, avengers.HE],
    'traits-Angry' : [avengers.HK],
    'traits-Kind' : [avengers.CA],

    'music-Pop' : [avengers.SM, avengers.BW],
    'music-Jazz' : [avengers.CA, avengers.HK, avengers.HE],
    'music-Rock' : [avengers.TH, avengers.IM],
    'music-H-H' : [avengers.BP],

    'team-1' : [avengers.BP, avengers.IM],
    'team-2' : [avengers.TH, avengers.HE],
    'team-3' : [avengers.HK, avengers.SM],
    'team-4' : [avengers.CA, avengers.BW],

    'color-Red' : [avengers.SM, avengers.IM],
    'color-Green' : [avengers.HK],
    'color-Blue' : [avengers.TH, avengers.CA],
    'color-Black' : [avengers.BP, avengers.BW, avengers.HE],
    'color-Unkown' : []


    }

    # Based on the key and value, we incriment points to teh corresponding avengers
    for k, v in qa.items():
        key = str(k) + '-' + str(v)
        if key in qa_avengers_map:
            av_list = qa_avengers_map[key]
            for avenger in av_list:
                characters[avenger] += 1

   # Finding out the avenger with the max points
    maxpoints = 0
    avg_name = ''


    for k, v in characters.items():
        if v > maxpoints:
            maxpoints = v
            avg_name = k

    return avg_name

