import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def all_bar_obj(obj:list,pre_obj:list, calc_bool:list, names:list):
    labels = [[],[],[]]

    for i in range(len(obj)):
        if calc_bool[i]:
            it = str(i+1)
            labels[0].append("b"+str(i+1))
            labels[0].append("a"+str(i+1))

        else:
            it = "x"+str(i+1)
            labels[0].append("xb"+str(i+1))
            labels[0].append("xa"+str(i+1))
        
        labels[1].append(it)
        labels[2].append(it)
            
    xs = [[],[],[]]
    xn = [[],[],[]]
    On = [[],[],[]]
    
    for i in range(len(obj)):
        xs[0].append(pre_obj[i][0])
        xn[0].append(pre_obj[i][1])
        On[0].append(pre_obj[i][2])
        xs[0].append(obj[i][0])
        xn[0].append(obj[i][1])
        On[0].append(obj[i][2])
        
        xs[1].append(pre_obj[i][0])
        xn[1].append(pre_obj[i][1])
        On[1].append(pre_obj[i][2])
        xs[2].append(obj[i][0])
        xn[2].append(obj[i][1])
        On[2].append(obj[i][2])

    titles = ["z pré/post recherche locale","z pré recherche locale","z post recherche locale"]
    
    for i in range(3):
        bar_obj([On[i],xn[i],xs[i]], labels[i], titles[i],names[i])
    
    
def bar_obj(costs:list, labels:list, title:str,name:str):
    names = ["Coûts plateformes","Tournées propres", "Tournées sales"]
    colors = ["red","green","blue"]
    fig,ax = plt.subplots()
    bottom = np.zeros(len(costs[0]))
    width = 0.5

    print(labels)
    print(costs)
    print(title)
    for i in range(3):
        p = ax.bar(labels,costs[i], width, bottom = bottom, edgecolor = "black",color = colors[i])
        bottom += costs[i]
        ax.bar_label(p, label_type = 'center')
    
    ax.set_title(title)
    ax.tick_params(axis='x', labelrotation=90)
    fig.savefig(name+".png")
    #fig.show()

def plot_obj(obj:list,pre_obj:list, calc_bool:list, name:str):
    
    fig= plt.figure()
    ax = fig.add_axes([0,0,1,1])
    best_obj = []
    i_best_obj = []
    not_finished = [[],[]]
    finished = [[],[]]

    for i in range(len(obj)):
        if best_obj == []:
            best_obj.append(obj[i])
            i_best_obj.append(i)

        elif best_obj[-1] > obj[i]:
            best_obj.append(obj[i])
            i_best_obj.append(i)

        ax.plot([i,i],[pre_obj[i],obj[i]], color ="green")
        if calc_bool[i]:
            finished[0].append(obj[i])
            finished[1].append(i)
        else:
            not_finished[0].append(obj[i])
            not_finished[1].append(i)

    best_obj.append(best_obj[-1])
    i_best_obj.append(i)
    ax.scatter(list(range(len(pre_obj))),pre_obj, marker = '^', color = "green", label = "z pré-recherche locale")
    ax.scatter(finished[1],finished[0], marker = 'o', color = "red", label = "z post-recherche locale")
    ax.scatter(not_finished[1],not_finished[0], marker = 'x', color = "black", label = "z post-recherche locale (inachevée)")
    ax.plot(i_best_obj,best_obj, color = "red", label = "Meilleure valeur z connue")
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    
    ax.set_xlabel("Iteration VNS")
    ax.set_xlim([-0.1,len(obj)-0.9])
    ax.tick_params(left = False, bottom = False) 
    ax.set_ylabel("Valeur de z")
    ax.set_ylim(math.floor(min(obj)*0.9), math.ceil(max(pre_obj)*1.1))
    
    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=1))  # x-axis ticks at multiples of 2
    
    fig.savefig(name+".png")

    #fig.show()

def plot_time(time:list,calc_bool:list):
    print(time)
    best_time = []
    fig= plt.figure()
    ax = fig.add_axes([0,0,1,1])
    avg_time = 0

    for i in range(len(time)):
        if best_time == []:
            best_time.append(time[i])
        elif best_time[i-1] > time[i]:
            best_time.append(time[i])
        else:
            best_time.append(best_time[i-1])
        if calc_bool[i]:
            ax.plot(i,time[i], marker = 'o', color = "red")
        else:
            ax.plot(i,time[i], marker = 'x', color = "black")
    print(best_time)
    ax.plot(list(range(len(time))),time, color = "blue")
    ax.plot(list(range(len(time))),best_time, color = "red")
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    
    fig.savefig(name+".png")

    #fig.show()