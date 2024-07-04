import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def all_bar_obj(obj:list,pre_obj:list, calc_bool:list, names:list):
    labels = [[],[],[]]

    for i in range(len(obj)):
        if calc_bool[i]:
            it = "x"+str(i+1)
            labels[0].append("b"+str(i+1))
            labels[0].append("a"+str(i+1))

        else:
            it = str(i+1)
            labels[0].append("xb"+str(i+1))
            labels[0].append("xa"+str(i+1))
        
        labels[1].append(it)
        labels[2].append(it)

    xs = [[],[],[]]
    xn = [[],[],[]]
    On = [[],[],[]]
    sum_obj = []
    sum_pre_obj = []
    max_z = 0
    for i in range(len(obj)):
        if max_z < sum(pre_obj[i]):
            max_z = sum(pre_obj[i])
        xs[0].append(pre_obj[i][0])
        xn[0].append(pre_obj[i][1])
        On[0].append(pre_obj[i][2])
        xs[0].append(obj[i][0])
        xn[0].append(obj[i][1])
        On[0].append(obj[i][2])
        sum_obj.append(obj[i][0]+obj[i][1]+obj[i][2])
        sum_pre_obj.append(pre_obj[i][0]+pre_obj[i][1]+pre_obj[i][2])

        xs[1].append(pre_obj[i][0])
        xn[1].append(pre_obj[i][1])
        On[1].append(pre_obj[i][2])
        xs[2].append(obj[i][0])
        xn[2].append(obj[i][1])
        On[2].append(obj[i][2])

    titles = ["z pré/post RL","z pré RL","z post RL"]
    #print(On)
    #print(xn)
    for i in range(3):
        bar_obj([On[i],xn[i],xs[i]], labels[i], names[i], max_z)
    plot_obj(sum_obj,sum_pre_obj,calc_bool,names[3])
    
def bar_obj(costs:list, labels:list, name:str,top_scale:int):
    names = ["Coûts plateformes","Coûts Tournées propres", "Coûts Tournées sales"]
    colors = ["red","green","blue"]
    fig,ax = plt.subplots()
    bottom = np.zeros(len(costs[0]))
    width = 0.5

    for i in range(3):
        p = ax.bar(labels,costs[i], width, bottom = bottom, edgecolor = "black",color = colors[i], label = names[i])
        bottom += costs[i]
        #ax.bar_label(p, label_type = 'center')
    
    ax.set_ylim(0, math.ceil(top_scale)*1.1)
    ax.set_xlabel("Iteration VNS")
    ax.set_ylabel("Valeur de z")
    ax.tick_params(axis='x', labelrotation=90)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels,loc='upper center', bbox_to_anchor=(0.5, 1.05),ncol=2)
    fig.savefig(name+".png")
    #fig.show()

def plot_obj(obj:list,pre_obj:list, calc_bool:list, name:str):
    
    fig,ax = plt.subplots()
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
        if not calc_bool[i]:
            finished[0].append(obj[i])
            finished[1].append(i)
        else:
            not_finished[0].append(obj[i])
            not_finished[1].append(i)

    best_obj.append(best_obj[-1])
    i_best_obj.append(i)
    ax.scatter(list(range(len(pre_obj))),pre_obj, marker = '^', color = "green", label = "z pré-RL")
    ax.scatter(finished[1],finished[0], marker = 'o', color = "red", label = "z post-RL")
    ax.scatter(not_finished[1],not_finished[0], marker = 'x', color = "black", label = "z post-RL (inachevée)")
    ax.plot(i_best_obj,best_obj, color = "red", label = "Meilleure valeur z connue")
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels,loc='upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=2)
    ax.set_xlim([-0.1,len(obj)-0.9])
    ax.tick_params(left = False, bottom = False) 
    ax.set_xlabel("Iteration VNS")
    ax.set_ylabel("Valeur de z")
    ax.set_ylim(math.floor(min(obj)*0.9), math.ceil(max(pre_obj)*1.1))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=1)) 
    
    fig.savefig(name+".png")

def plot_time(time:list,calc_bool:list, name:str):
    print(time)
    best_time = []
    fig,ax = plt.subplots()
    not_finished = [[],[]]
    finished = [[],[]]

    avg_time = 0

    for i in range(len(time)):
        if best_time == []:
            best_time.append(time[i])
        elif best_time[i-1] > time[i]:
            best_time.append(time[i])
        else:
            best_time.append(best_time[i-1])
        if not calc_bool[i]:
            finished[0].append(time[i])
            finished[1].append(i)
        else:
            not_finished[0].append(time[i])
            not_finished[1].append(i)
    #print(best_time)
    ax.scatter(finished[1],finished[0], marker = 'o', color = "red", label = "RL terminée")
    ax.scatter(not_finished[1],not_finished[0], marker = 'x', color = "black", label = "RL inachevée")
    ax.plot(list(range(len(time))),time, color = "blue")
    ax.plot(list(range(len(time))),best_time, color = "red")
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels,loc='upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=2)
    ax.set_xlabel("Iteration VNS")
    ax.set_ylabel("Temps (en secondes)")
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=1)) 

    
    fig.show()
    fig.savefig(name+".png")