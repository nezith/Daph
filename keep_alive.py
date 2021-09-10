from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    string = "This was a triumph\nI'm making a note here; 'Huge success'\nIt's hard to overstate\nMy satisfaction\nAperture Science:\nWe do what we must\nBecause we can\nFor the good of all of us\nExcept the ones who are dead\nBut there's no sense crying\nOver every mistake\nYou just keep on trying\nTill you run out of cake\nAnd the science gets done\nAnd you make a neat gun\nFor the people who are\nStill alive\nI'm not even angry\nI'm being so sincere right now\nEven though you broke my heart,\nAnd killed me\nAnd tore me to pieces\nAnd threw every piece into a fire\nAs they burned it hurt because\nI was so happy for you\nNow, these points of data\nMake a beautiful line\nAnd we're out of beta\nWe're releasing on time\nSo I'm GLaD I got burned\nThink of all the things we learned-\nFor the people who are\nStill alive\nGo ahead and leave me\nI think I'd prefer to stay inside\nMaybe you'll find someone else\nTo help you?\nMaybe Black Mesa?\nThat was a joke *Haha - Fat Chance*\nAnyway this cake is great\nIt's so delicious and moist\nLook at me: still talking\nWhen there's science to do\nWhen I look out there,\nIt makes me GLaD I'm not you\nI've experiments to run\nThere is research to be done\nOn the people who are\nStill alive\nAnd believe me I am\nStill alive\nI'm doing science and I'm\nStill alive\nI feel fantastic and I'm\nStill alive\nWhile you're dying I'll be\nStill alive\nAnd when you're dead I will be\nStill alive\nStill alive"

    still_alive = string.replace("\n", "<br />")

    return still_alive

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()