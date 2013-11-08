from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import string
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect('dbname=wildfire user=Marava password=mickey69')
cur = conn.cursor()

def get_pet(pet):
    data = "select * from pet_type pt join counters c on c.id=pt.id where pt.type=%s"
    ptype = (str(pet),)
    cur.execute(data, ptype)
    pet_data = cur.fetchall()
    return pet_data

def get_id(pet):
    data = "select pt.id from pet_type pt where pt.type=%s;"
    ptype = (str(pet),)
    cur.execute(data, ptype)
    base_id = cur.fetchall()
    final_id = base_id[0][0]
    return str(final_id)

def get_name(num):
    data = "select pt.type from pet_type pt where pt.id=%s;"
    pid = (str(num),)
    cur.execute(data, pid)
    base_type = cur.fetchall()
    final_type = base_type[0][0]
    return str(final_type.title())

def wowhead(name):
    data = "select npc_id from petnames where name=%s;"
    info = (str(name),)
    cur.execute(data, info)
    wh_id = cur.fetchall()
    wh_id = str(wh_id[0][0])
    return wh_id

def twowhead(name):
    data = "select id from trainer_ids where name=%s;"
    info = (str(name),)
    cur.execute(data, info)
    wh_id = cur.fetchall()
    wh_id = str(wh_id[0][0])
    return wh_id

def wh_convert(num):
    data = "select w_id from wowhead_id where id=%s;"
    info = (str(num),)
    cur.execute(data, info)
    temp = cur.fetchall()
    c_id = str(temp[0][0])
    return c_id
    
def rec_pets(fam):
    data = "select name from petnames where type=%s and trainer='n';"
    info = (str(get_id(fam)),)
    cur.execute(data, info)
    petlist = cur.fetchall()
    return petlist

def rec_list(petlist):
    r_list = []
    for pet in petlist:
	    r_list.append(pet[0])
    return r_list

def get_tpets(trainer):
    data = "select name from petnames where t_name=%s;"
    info = (str(longform[trainer]),)
    cur.execute(data, info)
    tpetlist = cur.fetchall()
    return tpetlist
    
def tpets(tpetlist):
    t_list = []
    for pet in tpetlist:
        t_list.append(pet[0])
    return t_list

def ptype(pet):
    data = "select pt.type from petnames p join pet_type pt on pt.id=p.type where name=%s;"
    info = (str(pet),)
    cur.execute(data, info)
    pet_type = (cur.fetchall())[0][0]
    return pet_type

trainer_pets = {}
pet1 = {"Tiun":"Flying (No multi-hit)", "Lucky Yi":"Roach (Apocalypse)", "Dos-Ryga":"Roach (Apocalypse)", "Kawi":"Kun-Lai Runt", "Gorespine":"Fox(Bite/Howl/Dazzling Dance)",
            "Greyhoof":"Wild Jade Hatchling (Call Lightning)", "No-No":"Flying (Lift-Off/Cocoon Strike)", "Kafi":"Gryphon (Flock)", "Nitun":"Fox (Bite/Howl/Dazzling Dance)",
            "Skitterer":"Gryphon", "Hyuna":"Celestial Dragon", "Nishi":"Carry Pet", "Moruk":"Clockwork Gnome", "Yon":"Idol", "Zusshi":"Crab", 
            "Shu":"Moth", "Aki":["Runt", "Crab"], "Flowing":"Anubisath Idol", "Whispering":"Emmy", "Burning":"Anubisath Idol", "Thundering":""}
pet2 = {"Tiun":"Flying (No multi-hit)", "Lucky Yi":"Crab", "Dos-Ryga":"Gryphon (Lift-Off)", "Kawi":"Rabbit (Stampede)", "Gorespine":"Kun-Lai Runt", "Greyhoof":"Mechanical", 
            "No-No":"Flying (Lift-Off/Cocoon)", "Kafi":"Anubisath Idol (Demolish)", "Nitun":"Kun-Lai Runt", "Skitterer":"Anubisath Idol", "Hyuna":"Flyer",
            "Nishi":"Eternal or Mirror Strider", "Moruk":"Li'l Tarecgosa", "Yon":"Carry Pet", "Zusshi":["Turtle", "Crab"], "Shu":"Snail", "Aki":["Pandaren Monk", "Anubisath Idol"], "Flowing":"Crab",
            "Whispering":"Carry Pet", "Burning":"Emerald Turtle", "Thundering":""}
pet3 = {"Tiun":"Flying (No multi-hit)", "Lucky Yi":"Crab", "Dos-Ryga":"Anubisath Idol", "Kawi":"Anything", "Gorespine":"Clockwork Gnome", "Greyhoof":"Mechanical", 
            "No-No":"Flying (Lift-Off/Cocoon Strike)", "Kafi":"Clockwork Gnome", "Nitun":"Anubisath Idol", "Skitterer":"Kun-Lai Runt", "Hyuna":"Carry Pet", "Nishi":"Snail",
            "Moruk":"Flying", "Yon":"Carry Pet", "Zusshi":["Turtle", "Crab"], "Shu":"High-level carry pet", "Aki":["Moth or Gryphon", "Carry pet"], "Flowing":"High-level carry pet",
            "Whispering":"Carry Pet", "Burning":"Carry Pet", "Thundering":""}
strats = {"No-No":"Don't attack while the beaver dam is up, and avoid Dive.", "Dos-Ryga":"Apocalypse, then tank out the next 14 rounds.  Swap the roach back in for the final round to ensure Apocalypse goes off.  Don't let the roach die!",
              "Gorespine":"Dazzling Dance > Bite > Howl when about to die.  Rampage, finish with Gnome rockets.",
              "Flowing":"NO ELEMENTAL CARRY PETS, start with Sandstorm against the fish.","Greyhoof":"Call Lightning, Turret on the Gnome", "Skitterer":"Flock > Sandstorm/Crush",
              "Moruk":"Fuck this guy.  Either turret/repair/turret/fist/fist/repeat with the Gnome and Demolish/block Headbutt with the Idol, or bite/presence/dream him to death with Emmy. Idol/Tara can do it as well but I haven't had much luck.  Don't bother with a leveling pet.",
              "Tiun":"Make sure the flyers don't have multihit up.  Alternately, Apocalyse + healytanks.",
              "Burning":"Crush > Sandstorm > Deflection > Crushcrushcrushcrush > Def on first turn > use def when sandstorm comes off cooldown. Use the turtle to finish the fight if the Idol manages to die.",
              "Hyuna":"Bring in carry pet on Dor's second turn.", "Kawi":"Mangle > Stampede > Rampage"}
"""tpet = {"Hyuna":["Skyshaper", "Fangor", "Dor"], "Nishi":["Siren", "Toothbreaker", "Brood of Mothallus"], "Moruk":["Woodcarver", "Lightstalker", "Needleback"], "Yon":["Piqua", "Lapin", "Bleat"], "Zusshi":["Diamond",
              "Mollus", "Skimmer"], "Shu":["Crusher", "Pounder", "Mutilator"], "Aki":["Whiskers", "Stormlash", "Chirrup"], "Thundering":["Darnak the Tunneler", "Pandaren Earth Spirit", "Sludgy"], "Burning":["Crimson",
              "Glowy", "Pandaren Fire Spirit"], "Whispering":["Dusty", "Pandaren Air Spirit", "Whispertail"], "Flowing":["Marley", "Tiptoe", "Pandaren Water Spirit"]}
"""
"""ptype = {"flying":["Skyshaper", "Lightstalker", "Dusty", "Piqua", "Glowy"], "aquatic":["Marley", "Tiptoe", "Skimmer", "Whiskers", "Crusher", "Dor", "Needleback"],
        "mechanical":[], "magic":["Sludgy"], "dragonkin":["Crimson", "Whispertail", "Stormlash"], "elemental":["Siren", "Toothbreaker", "Diamond", "Pounder", "Pandaren Fire Spirit", "Pandaren Water Spirit", "Pandaren Earth Spirit",
        "Pandaren Air Spirit"],"critter":["Lapin", "Mollus", "Chirrup"], "beast":["Fangor", "Brood of Mothallus", "Woodcarver", "Bleat", "Mutilator", "Darnak the Tunneler"], "undead":[], "humanoid":[]}
rtype = {}
"""

longform = {"Hyuna":"Hyuna of the Shrines", "Nishi":"Farmer Nishi", "Yon":"Courageous Yon", "Moruk":"Mo'ruk", "Zusshi":"Seeker Zusshi", "Shu":"Wastewalker Shu", "Aki":"Aki the Chosen",
            "Burning":"Burning Pandaren Spirit", "Whispering":"Whispering Pandaren Spirit", "Thundering":"Thundering Pandaren Spirit", "Flowing":"Flowing Pandaren Spirit"}
blongform = {"Kawi":"Kawi the Gorger", "Kafi":"Kafi", "Dos-Ryga":"Dos-Ryga", "Nitun":"Nitun", "Greyhoof":"Greyhoof", "Lucky Yi":"Lucky Yi",
             "Skitterer":"Skitterer Xi'a", "Gorespine":"Gorespine", "No-No":"No-No", "Tiun":"Ti'un the Wanderer"}

bgimage = {'Aki':'http://i.imgur.com/qMY1QRH.jpg'}


def reverse_ptype(pet):
    for t in ptype:
        if pet in ptype[t]:
            rtype[pet] = t
    return rtype[pet]    

def searchsplit(trainer):
    return "+".join(longform[trainer].split())
def bsearchsplit(trainer):
    return "+".join(blongform[trainer].split())



@app.route("/")
def main():
    return render_template('main.html')

@app.route("/counter/<pet>")
def counter(pet):
    
    details = ("Details: "+str(pet).title()+" Pets")
    weak = get_name(str(get_pet(pet)[0][3]))
    defend = get_name(str(get_pet(pet)[0][4]))
    pplist = rec_list(rec_pets(pet))
    pp1 = pplist[0]
    pp2 = pplist[1]
    pp3 = pplist[2]
    pp4 = pplist[3]
    pp5 = pplist[4]
    wh_link = wh_convert(get_id(pet))
    
    return render_template('counters.html', details=details,
                           weak=weak, defend=defend, pplist=pplist, pp1=pp1, pp2=pp2,
                           pp3=pp3, pp4=pp4, pp5=pp5, link1=wowhead(pp1), link2=wowhead(pp2),
                           link3=wowhead(pp3), link4=wowhead(pp4), link5=wowhead(pp5), wh_link=wh_link,
                           pet_type=str(pet).title())



@app.route("/dreamteam/<trainer>")



def dreamteam(trainer):
    
    
    islist1 = isinstance(pet1[trainer], list)
    islist2 = isinstance(pet2[trainer], list)
    islist3 = isinstance(pet3[trainer], list)
    if islist1==True:
        pet_one = pet1[trainer][0]
        pet_one_a = pet1[trainer][1]
    else:
        pet_one = pet1[trainer]
        pet_one_a = ''

    if islist2==True:
        pet_two = "Option 1: "+pet2[trainer][0]
        pet_two_a = "Option 2: "+pet2[trainer][1]
    else:
        pet_two = pet2[trainer]
        pet_two_a = ''

    if islist3==True:
        pet_three = "Option 1: "+pet3[trainer][0]
        pet_three_a = "Option 2: "+pet3[trainer][1]
    else:
        pet_three = pet3[trainer]
        pet_three_a = ''
    
    if trainer in strats:
        strat = strats[trainer]
    else:
        strat = "No particular strategy is required for this trainer."
    if trainer in longform:
        title = twowhead(longform[trainer])
        tplist = tpets(get_tpets(trainer))
        tpet1 = tplist[0]
        tpet2 = tplist[1]
        tpet3 = tplist[2]

        ttype1 = (ptype(tpet1)).title()
        ttype2 = (ptype(tpet2)).title()
        ttype3 = (ptype(tpet3)).title()

        return render_template('trainers.html', trainer=longform[trainer], trainersplit=searchsplit(trainer), title=title, islist1=islist1, pet_one=pet_one,
                           pet_one_a=pet_one_a, pet_two=pet_two, pet_three=pet_three,
                           strat=strat, islist2=islist2, islist3=islist3, pet_two_a=pet_two_a,
                           pet_three_a=pet_three_a, ttype1=ttype1, ttype2=ttype2, ttype3=ttype3,
                           tpet1=tpet1, tpet2=tpet2, tpet3=tpet3, link1=wowhead(tpet1), link2=wowhead(tpet2), link3=wowhead(tpet3))
    else:
        title = blongform[trainer]
        return render_template('beastsoffable.html', trainer=blongform[trainer], trainersplit=bsearchsplit(trainer), title=title, islist1=islist1, pet_one=pet_one,
                           pet_one_a=pet_one_a, pet_two=pet_two, pet_three=pet_three,
                           strat=strat, islist2=islist2, islist3=islist3, pet_two_a=pet_two_a,
                           pet_three_a=pet_three_a)

if __name__ == '__main__':
    app.run(debug='True',host='0.0.0.0')
