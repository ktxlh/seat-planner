import os.path
BASE = os.path.dirname(os.path.abspath(__file__))
import json
import numpy as np
from sklearn.manifold import TSNE
import turtle
import random

from PIL import Image


def readkvp():
    data = {}
    ks = []
    vs = []
    with open(os.path.join(BASE, 'data.json'), 'r') as in_f:
        data = json.load(in_f)
    for user in data:
        ks.append( user["Name"] )
        values = []
        for _, key in enumerate(user["Preferences"]):
            values.append(user["Preferences"][key])
        vs.append(values)
    return ks, vs


def coor2color(ks, vs):
    tsne = TSNE(n_components=3, random_state=0, n_iter=10000, perplexity=2)
    np.set_printoptions(suppress=True)
    T = tsne.fit_transform(vs)
    
    # max & min
    maxs = [max( [t[i] for t in T] ) for i in range(3) ]
    mins = [min( [t[i] for t in T] ) for i in range(3) ]
        
    colors = [ ( [int(round((t[i]-mins[i]) * 255 / (maxs[i]-mins[i]))) for i in range(3)] ) for t in T ]

    return ks, colors


def visualize(hightlighted=200):
    ks, vs = readkvp()
    name_to_highlight = ks[hightlighted-1]
    highlight_neighbor = ''
    ks, colors = coor2color(ks, vs)

    jplan = {}
    with open(os.path.join(BASE, 'plan.json'), 'r') as in_f:
        jplan = json.load(in_f)
    
    plan = []
    for i, row in enumerate(jplan[0]):
        plan.append(
            (jplan[0][row]['Aisle'], jplan[0][row]['Window'])
        )
        if jplan[0][row]['Aisle']==name_to_highlight  or jplan[0][row]['Window']==name_to_highlight :
            draw = random.randint(0,max(0,min(i-1, 15)))
            temp = plan[draw]
            plan[draw] = plan[i]
            plan[i] = temp
            if jplan[0][row]['Aisle']==name_to_highlight:
                highlight_neighbor = jplan[0][row]['Window']
            else:
                highlight_neighbor = jplan[0][row]['Aisle']

    
    name2id = dict(zip(ks, (i for i in range(len(ks)))))

    # turtle!!!
    DISTANCE = 27
    WIDTH = 1080
    HEIGHT = 675
    BGPIC = os.path.join(BASE, 'background.png')

    turtle.setup( WIDTH, HEIGHT )
    turtle.bgpic(BGPIC)
    turtle.pencolor('grey')
    turtle.shape("square")
    turtle.colormode(255)
    turtle.shapesize(1.3)
    turtle.width(0)

    turtle.tracer(False)
    turtle.up()
    turtle.goto( -(WIDTH/2)+108, (HEIGHT/2)-100)
    
    for _, row in enumerate(jplan[0]):
        plan.append(
            (jplan[0][row]['Aisle'], jplan[0][row]['Window'])
        )


    for i in range(7):
        for j in range(2):
            p = name2id[plan[i][j]]
            
            turtle.fillcolor(colors[p][0], colors[p][1], colors[p][2])
            turtle.stamp() 
            
            if plan[i][j] == name_to_highlight:
                turtle.shape('circle')
                turtle.fillcolor(255, 255, 255)
                turtle.stamp()
                turtle.shape('square')
            
            turtle.right(90)
            turtle.forward( int(DISTANCE*1.07) )
            turtle.left(90)
        turtle.forward( int(DISTANCE*1.545) )
        turtle.left(90)
        turtle.forward( 2 * int(DISTANCE*1.07) )
        turtle.right(90)
    
    turtle.forward(215)

    for i2 in range(9):        
        i = i2+9
        for j in range(2):
            p = name2id[plan[i][j]]
            
            turtle.fillcolor(colors[p][0], colors[p][1], colors[p][2])
            turtle.stamp() 
            turtle.right(90)
            turtle.forward( int(DISTANCE*1.07) )
            turtle.left(90)
        turtle.forward( int(DISTANCE*1.6) )
        turtle.left(90)
        turtle.forward( 2 * int(DISTANCE*1.07) )
        turtle.right(90)

    turtle.hideturtle()
    ts = turtle.getscreen()
    ts.getcanvas().postscript(file=os.path.join(BASE, 'plan.eps'))
    im = Image.open(os.path.join(BASE, 'plan.eps'))
    im.save(os.path.join(BASE, 'plan.jpeg'), "JPEG")
    #ts = turtle.getscreen().getcanvas()
    #canvasvg.saveall(os.path.join(BASE, 'plan.svg'), ts)

    #return 0
    # return he's data, color, as well as his neighbor's
    # or visualize it and return the result?
    ret = json.dumps([
        {
            'Name': name_to_highlight,
            'Preferences':{
                'Window':vs[hightlighted-1][0],
                'Sleep':vs[hightlighted-1][1],
                'Networking':vs[hightlighted-1][2],
                'WindowShading':vs[hightlighted-1][3],
            },
            'Color': {
                'R':colors[hightlighted-1][0],
                'G':colors[hightlighted-1][1],
                'B':colors[hightlighted-1][2],
            }
        },
        {
            'Name': highlight_neighbor,
            'Preferences':{
                'Window':vs[name2id[highlight_neighbor]][0],
                'Sleep':vs[name2id[highlight_neighbor]][1],
                'Networking':vs[name2id[highlight_neighbor]][2],
                'WindowShading':vs[name2id[highlight_neighbor]][3],
            },
            'Color': {
                'R':colors[name2id[highlight_neighbor]][0],
                'G':colors[name2id[highlight_neighbor]][1],
                'B':colors[name2id[highlight_neighbor]][2],
            }
        }
    ])
    return ret

#if __name__ == '__main__':
    #visualize()