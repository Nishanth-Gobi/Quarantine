import random
import secrets
import matplotlib.pyplot as plt

'''
Glossary:
    
Vertex of graph -     
    
'trunc_gauss' - Normal distribution for a fixed range from bottom to top 
                i.e. in our case bottom = 0, top = n-1

line ( - ) - Input values
             effectiveness - actually 1-effectiveness

normal_community - An adjacency matrix that corresponds to a community
                   where there are no preventive measures against COVID
                 

cautious_community - An adjacency matrix that corresponds to a community
                   where there are preventive measures against COVID

people_labels - List of people, here each person is identified by an integer 
                (0 to population -1)

mask_list - List of people who wear mask (Randomised)
sanitize_list - List of people who use sanitiser (Randomised)
social_dist_list - List of people who follow social distancing (Randomised)

prioratise and randomise -  sort the 'individuals_at_risk' list in non-decresing order to 
                            ensure that those who don't take a lot of 
                            preventive measures are sooner to get infected
                            
                        -   randomise to ensure that the event of infection 
                            is a random event

'''

population = 100

percent_of_ppl_wear_mask = 0.55
no_of_ppl_wear_mask = int(percent_of_ppl_wear_mask * population)
effectiveness_of_mask = 0.7

percent_of_ppl_sanitizer = 0.2
no_of_ppl_sanitizer = int(percent_of_ppl_sanitizer * population)
effectiveness_of_sanitizer = 0.3

percent_of_ppl_social_dist = 0.80
no_of_ppl_social_dist = int(percent_of_ppl_social_dist * population)
effectiveness_of_social_dist = 0.1

def trunc_gauss(mu, sigma, bottom, top):
    a = random.gauss(mu,sigma)
    while (bottom <= a <= top) == False:
        a = random.gauss(mu,sigma)
    return a


people_labels = [i for i in range(0,population)] 

normal_community = [[0 for i in range(0,population)] for j in range(0,population)]
cautious_community = [[0 for i in range(0,population)] for j in range(0,population)]


for i in range(0,population):
    for j in range(i,population):
        cautious_community[i][j] = cautious_community[j][i] = normal_community[i][j] = normal_community[j][i] = secrets.randbelow(2)
        if(i==j):
            cautious_community[i][j] = cautious_community[j][i] = normal_community[i][j] = normal_community[j][i] = 0 #since you can't transmit disease to your self so matrix at i==j is zero


mask_list = random.sample(people_labels,no_of_ppl_wear_mask)
sanitize_list = random.sample(people_labels,no_of_ppl_sanitizer)
social_dist_list = random.sample(people_labels,no_of_ppl_social_dist)


for i in range(0,len(mask_list)):
    for j in range(0,population):
        cautious_community[mask_list[i]][j] = cautious_community[mask_list[i]][j]*effectiveness_of_mask
        cautious_community[j][mask_list[i]] = cautious_community[j][mask_list[i]]*effectiveness_of_mask

for i in range(0,len(sanitize_list)):
    for j in range(0,population):
        cautious_community[sanitize_list[i]][j] = cautious_community[sanitize_list[i]][j]*effectiveness_of_sanitizer
        cautious_community[j][sanitize_list[i]] = cautious_community[j][sanitize_list[i]]*effectiveness_of_sanitizer

for i in range(0,len(social_dist_list)):
    for j in range(0,population):
        cautious_community[social_dist_list[i]][j] = cautious_community[social_dist_list[i]][j]*effectiveness_of_social_dist
        cautious_community[j][social_dist_list[i]] = cautious_community[j][social_dist_list[i]]*effectiveness_of_social_dist
        

def prob(x):
    l1=[ i for i in range(0,int(10000*x))]
    y=secrets.randbelow(10000)
    if y in l1:
        return 1
    else:
        return 0

#Normal Community 

adj_list_normal=[]

for i in range(population):

    l1=[]

    for j in range(population):

        if(normal_community[i][j]==1):
            l1.append(j)

    adj_list_normal.append(l1)

rrand = trunc_gauss(2,0.3,0,population)

tot_infection = [i for i in range(0,population)] 

infected = []
infected.append(0) #infecting first person

carriers_on_day = []
carriers_on_day.append(0)

dummy = []
day_count = 0

ppl_inf={}

for k2 in range(10000):

    dummy=[]
    
    for i in carriers_on_day:
        rrand = int(trunc_gauss(2.7,0.3,0,population))
        count1 = min(rrand,len(adj_list_normal[i]))
        j = 0
        k3 = 0

        while j<count1 and k3<len(adj_list_normal[i]):
            
            if(adj_list_normal[i][k3] not in infected):
                infected.append(adj_list_normal[i][k3])
                dummy.append(adj_list_normal[i][k3])
                j+=1
            
            k3+=1
        
        carriers_on_day.remove(i)
    
    for k in dummy:
        carriers_on_day.append(k)

    day_count += 1
    
    if(sorted(infected)==tot_infection):
        break
    if(len(carriers_on_day)==0):
        break 

#    print("\nDay number : ",day_count)    
#    print("People infected : ",infected)
    ppl_inf[day_count]=len(infected)
    
print("\n\n\n\n")

dc=day_count

#Cautious community

adj_list_normal=[]

for i in range(population):

    l1=[]

    for j in range(population):

        if(cautious_community[i][j]!=0):
            l1.append(j)

    adj_list_normal.append(l1)

rrand = trunc_gauss(2,0.3,0,population)

tot_infection = [i for i in range(0,population)] 

infected = []
infected.append(0) #infecting first person

carriers_on_day = []
carriers_on_day.append(0)

dummy = []
day_count = 0

ppl_inf2={}

for k2 in range(10000):

    dummy=[]
    
    for i in carriers_on_day:
        rrand = int(trunc_gauss(2.7,0.3,0,population))
        count1 = min(rrand,len(adj_list_normal[i]))
        j = 0
        k3 = 0

        while j<count1 and k3<len(adj_list_normal[i]):
            
            if(adj_list_normal[i][k3] not in infected): 
                p = prob(cautious_community[i][adj_list_normal[i][k3]])
                if(p==1):
                    infected.append(adj_list_normal[i][k3])
                dummy.append(adj_list_normal[i][k3])
                j+=1
            
            k3+=1
        
        carriers_on_day.remove(i)
    
    for k in infected:
        carriers_on_day.append(k)

    day_count += 1
    
    if(sorted(infected)==tot_infection):
        break
    if(len(carriers_on_day)==0):
        break 

#    print("\nDay number : ",day_count)    
#    print("People infected : ",infected)
    ppl_inf2[day_count]=len(infected)

x=[]
y=[]

x1=[]
y1=[]

for k in ppl_inf.keys():
    y.append(ppl_inf[k])
    x.append(k)

for k in ppl_inf2.keys():
    y1.append(ppl_inf2[k])
    x1.append(k)

plt.plot(x, y)
plt.xlabel('no of days') 
plt.ylabel('no of people infected') 
plt.title('Virus sppread in a non-cautious community:') 
plt.show() 

print("No of days until total infection: ",dc)

plt.plot(x1, y1)
plt.xlabel('no of days') 
plt.ylabel('no of people infected') 
plt.title('Virus sppread in a cautious community:') 
plt.show()

print("No of days until total infection: ",day_count)
