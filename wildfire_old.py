from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import string
app = Flask(__name__)
@app.route("/")
def main():
    return render_template('main.html')

@app.route("/counter/<pet>")
def counter(pet):    
    counters = {"flying":"magic", "beast":"mechanical", "humanoid":"undead", "critter":"beast", \
                "magic":"dragonkin", "aquatic":"flying", "mechanical":"elemental", "elemental":"aquatic", \
                "undead":"critter", "dragonkin":"humanoid"}
    use_against = {}
    for k in counters:
        use_against[counters[k]] = k
    defends_against = {"flying":"beast", "beast":"humanoid", "humanoid":"critter", "critter":"elemental", \
                       "magic":"aquatic", "aquatic":"undead", "mechanical":"magic", "elemental":"mechanical",\
                       "undead":"dragonkin", "dragonkin":"flying"}
    dont_bother = {}
    for k in defends_against:
        dont_bother[defends_against[k]] = k
        
    details = ("Details: "+str(pet).title()+" Pets")
    weak = ("Weak Against: "+str(counters[pet]).title())
    use = ("Use Against: "+str(use_against[pet]).title())
    defend = ("Defends Against: "+str(defends_against[pet]).title())
    eww = ("Don't Bother Using Against: "+str(dont_bother[pet]).title())

    return render_template('counters.html', details=details,
                           weak=weak, use=use, defend=defend, eww=eww)



@app.route("/dreamteam/<trainer>")

def dreamteam(trainer):

    trainer_pets = {}
    pet1 = {"Tiun":"Flying", "Lucky Yi":"Roach", "Dos-Ryga":"Roach", "Kawi":"Runt", "Gorespine":"Fox", "Greyhoof":"Wild Jade Hatchling", \
            "No-No":"Flying (Lift-Off/Cocoon Strike)", "Kafi":"Gryphon (Flock)", "Nitun":"Fox", "Skitterer":"Gryphon", "Hyuna":"Celestial Dragon", \
            "Nishi":"Leveler", "Moruk":"Clockwork Gnome", "Yon":"Idol", "Zusshi":"Crab", \
            "Shu":"Moth", "Aki":"Runt", "Flowing":"Idol", "Whispering":"Emmy",\
            "Burning":"Idol", "Thundering":""}
    pet2 = {"Tiun":"Flying", "Lucky Yi":"Crab", "Dos-Ryga":"Gryphon", "Kawi":"Rabbit (Stampede)", "Gorespine":"Runt", "Greyhoof":"Mechanical", \
            "No-No":"Flying (Lift-Off/Cocoon)", \
            "Kafi":"Idol (Demolish)", "Nitun":"Runt", "Skitterer":"Idol", "Hyuna":"Flyer", "Nishi":"Strider", "Moruk":"Tara", "Yon":"Leveler", "Zusshi":["Turtle", "Crab"], \
            "Shu":"Snail", "Aki":"Pandaren Monk", "Flowing":"Crab", "Whispering":"Leveler", \
            "Burning":"Emerald Turtle", "Thundering":""}
    pet3 = {"Tiun":"Flying", "Lucky Yi":"Crab", "Dos-Ryga":"Idol", "Kawi":"Anything", "Gorespine":"Clockwork Gnome", "Greyhoof":"Mechanical", \
            "No-No":"Flying (Lift-Off/Cocoon Strike)", \
            "Kafi":"Clockwork Gnome", "Nitun":"Idol", "Skitterer":"Runt", "Hyuna":"Leveler", "Nishi":"Snail", "Moruk":"Flying", "Yon":"Leveler", "Zusshi":["Turtle", "Crab"], \
            "Shu":"High-level carry pet", "Aki":"Moth or Gryphon", "Flowing":"High-level carry pet", "Whispering":"Leveler", "Burning":"Leveler", "Thundering":""}
    strats = {"No-No":"Don't attack while the beaver dam is up, and avoid Dive.", \
              "Gorespine":"Dazzling Dance > Bite > Howl when about to die.  Rampage, finish with Gnome rockets.",\
              "Flowing":"NO ELEMENTAL CARRY PETS, start with Sandstorm against the fish.","Greyhoof":"Call Lightning, Turret on the Gnome", "Skitterer":"Flock > Sandstorm/Crush",\
              "Moruk":"Fuck this guy.  Either turret/repair/turret/fist/fist/repeat with the Gnome and Demolish/block Headbutt with the Idol, or bite/presence/dream him to death"\
              " with Emmy. Idol/Tara can do it as well but I haven't had much luck.  Don't bother with a leveling pet.", "Tiun":"Make sure the flyers don't have multihit up.  Alternately, Apocalyse + healytanks.",\
              "Burning":"Crush > Sandstorm > Deflection > Crushcrushcrushcrush > Def on first turn > use def when sandstorm comes off cooldown.",\
              "Hyuna":"Bring in carry pet on Dor's second turn.", "Kawi":"Mangle > Stampede > Rampage"}
    tpet = {"Hyuna":["Skyshaper", "Fangor", "Dor"], "Nishi":["Siren", "Toothbreaker", "Brood of Mothallus"], "Moruk":["Woodcarver", "Lightstalker", "Needleback"], "Yon":["Piqua", "Lapin", "Bleat"], "Zusshi":["Diamond",
              "Mollus", "Skimmer"], "Shu":["Crusher", "Pounder", "Mutilator"], "Aki":["Whiskers", "Stormlash", "Chirrup"], "Thundering":["Darnak the Tunneler", "Pandaren Earth Spirit", "Sludgy"], "Burning":["Crimson",
              "Glowy", "Pandaren Fire Spirit"], "Whispering":["Dusty", "Pandaren Air Spirit", "Whispertail"], "Flowing":["Marley", "Tiptoe", "Pandaren Water Spirit"]}
    ptype = {"flying":[], "aquatic":[], "mechanical":[], "magic":[], "dragonkin":[], "elemental":[], "critter":[], "beast":[], "undead":[], "humanoid":[]}
    rtype = {}
    def reverse_ptype(pet):
            for t in ptype:
                if pet in ptype[t]:
                    rtype[pet] = t
            return rtype[pet]
                    
    tpet1 = tpet[trainer][0]
    tpet2 = tpet[trainer][1]
    tpet3 = tpet[trainer][2]
    
    ttype1 = reverse_ptype(tpet1).title()
    ttype2 = reverse_ptype(tpet2).title()
    ttype3 = reverse_ptype(tpet3).title()
    
    title = "Lineup: "+trainer
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
    return render_template('trainers.html', title=title, islist1=islist1, pet_one=pet_one,
                           pet_one_a=pet_one_a, pet_two=pet_two, pet_three=pet_three,
                           strat=strat, islist2=islist2, islist3=islist3, pet_two_a=pet_two_a,
                           pet_three_a=pet_three_a)

if __name__ == '__main__':
    app.run(debug='True',host='0.0.0.0')
