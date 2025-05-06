from bs4 import BeautifulSoup
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

#interestingDatas = ['comments', 'likes', 'saved', 'media', 'story_interactions']

interestingDatas = ['comments', 'likes', 'saved', 'story_interactions']

DifferentPlots = [] # [fichier, X, Y]
def determineSousDossier(dossier, fichier):
    thepath = os.path.join(dossier, fichier)[44:]
    print(thepath)
    SousDossiers = ""
    for c in thepath:
        if c =="/":
            return SousDossiers
        SousDossiers+=c
    return SousDossiers

def data_counter(soup):
    Data={}
    A = [p.text for p in soup.find_all('div', class_="_3-95 _2pim _a6-h _a6-i")]
    for account in A:
        if account in Data.keys():
            Data[account]+=1
        else:
            Data[account]=1
    res= [(key,val) for (key,val) in Data.items()]
    res.sort(key=lambda x: x[1], reverse=True)
    return res
def EnleveUnderScoreNomFichier(fichier):
    file = ""
    for c in fichier:
        if c == "_":
            continue
        file+=c
    return file
def traitement_data(dossier_html, fichier, soup):
    SousDossier = determineSousDossier(dossier_html, fichier)
    if SousDossier=="comments":
        X = np.array([2016+i for i in range(10)])
        Y = np.array([0 for i in range(10)])
        contenu = " ".join([p.text for p in soup.find_all(["td"])])
        L = contenu[7:].split("Comment")
        for comment in L:
            a = comment.split("Time")
            #print(a)
            yearDet = a[1][-14:]
            year=""
            for i in range(len(yearDet)):
                if yearDet[i] not in [str(i) for i in range(10)]:
                    continue
                else:
                    for c in range(4):
                        year+=yearDet[i+c]
                    Y[int(year)-2016]+=1
                    break
            data.append({"file": fichier, "type":SousDossier, "content": year})
        DifferentPlots.append([EnleveUnderScoreNomFichier(fichier), X, Y])
    if SousDossier=="likes":
        #L = [p.text for p in soup.find_all(['div'])]
        #print(L)
        if fichier == "liked_posts.html":
            res= data_counter(soup)
            X = np.array([res[i][0] for i in range(len(res))])
            Y = np.array([res[i][1] for i in range(len(res))])
            DifferentPlots.append([EnleveUnderScoreNomFichier(fichier), X, Y])
            for i in range(len(res)):
                data.append({"file": fichier, "type": SousDossier, "content": res[i][0]+ " " + str(res[i][1])})
        #L = contenu[66:].split("👍")
        else:
            res= data_counter(soup)
            X = np.array([res[i][0] for i in range(len(res))])
            Y = np.array([res[i][1] for i in range(len(res))])
            DifferentPlots.append([EnleveUnderScoreNomFichier(fichier), X, Y])
            for i in range(len(res)):
                data.append({"file": fichier, "type": SousDossier, "content": res[i][0]+ " " + str(res[i][1])})
    if SousDossier=="story_interactions":
        res= data_counter(soup)
        X = np.array([res[i][0] for i in range(len(res))])
        Y = np.array([res[i][1] for i in range(len(res))])
        DifferentPlots.append([EnleveUnderScoreNomFichier(fichier), X, Y])
        for i in range(len(res)):
            data.append({"file": fichier, "type": fichier[:-5], "content": res[i][0]+ " " + str(res[i][1])})
    if SousDossier=="saved":
        if fichier == "saved_posts.html":
            return
        contenu = [p.text for p in soup.find_all("tr")]
        D = {}
        collection=""
        for i in range(3,len(contenu)):
            if contenu[i][:4]=="Name" and contenu[i+1][:8]=="Creation":
                collection = contenu[i][4:]
                if collection in D.keys():
                    collection = collection+"2"
                    D[collection]=0
                else:D[collection]=0
            elif contenu[i][:4]=="Name":
                D[collection]+=1
        res= [(key,val) for (key,val) in D.items()]
        res.sort(key=lambda x: x[1], reverse=True)
        X= np.array([res[i][0] for i in range(len(res))])
        Y = np.array([res[i][1] for i in range(len(res))])
        DifferentPlots.append([EnleveUnderScoreNomFichier(fichier), X,Y])
        sum = 0
        for key in range(len(res)):
            sum+=res[key][1]
        data.append({"file":"saved_posts.html", "type":SousDossier, "content": sum})
        for key in range(len(res)):
            data.append({"file": fichier, "type":SousDossier, "content": res[key][0] + ", " + str(res[key][1])})
    return

def parcourir_fichier_dossier(dossier_html):
    for fichier in os.listdir(dossier_html):
        filePath=os.path.join(dossier_html, fichier)
        SousDossier = determineSousDossier(dossier_html, fichier)
        #print(fichier + " filepath: " + filePath)
        if fichier.endswith(".html"):
            #print(fichier)
            with open(filePath, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
            
            # Extraire le texte des paragraphes et autres éléments
            
            #L = contenu.split("Comment")
            #print(L)
            traitement_data(dossier_html, fichier, soup)
            # Ajouter aux données
            
            #data.append({"file": fichier, "type": SousDossier, "content": contenu})
        elif os.path.isdir(filePath) and SousDossier in interestingDatas:
            parcourir_fichier_dossier(filePath)
        
def tracerCourbe():
    for L in DifferentPlots:
        if L[0][:-5] in ["likedposts", "savedcollections", "emojisliders", "polls", "questions", "quizzes", "storylikes"]:
            if L[0][:-5]=="emojisliders":
                plt.plot(L[1][:4], L[2][:4])
            else:plt.plot(L[1][:5], L[2][:5])
        else:plt.plot(L[1],L[2])
        print(L[0][:-5])
        plt.legend(f"{L[0][:-5]}")
        plt.show()
    print(DifferentPlots)
# Dossier contenant les fichiers HTML
dossier_html = "./Instagram_Account/your_instagram_activity"

# Liste pour stocker les données
data = []
# Parcourir tous les fichiers HTML
parcourir_fichier_dossier(dossier_html)
tracerCourbe()

# Convertir en DataFrame Pandas
df = pd.DataFrame(data)

# Sauvegarder en CSV
df.to_csv("activity_extraites.csv", index=False, encoding="utf-8")

print("Extraction terminée ! Fichier CSV généré.")