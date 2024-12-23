import streamlit as st # type: ignore
import joblib
import numpy as np
import pandas as pd

st.title("Prédiction de risque de crédit ")
st.subheader(" APP")

# Chargement du modele
modele = joblib.load('KN_model.pkl')

def inference(Age,Sex,Emploi,Logement,Duree,Epargne,Courant,Montant,Obj):
    new_data = np.array([
        Age,Sex,Emploi,Logement,Duree,
        Epargne,Courant,Montant,Obj
    ])
    pred = modele.predict(new_data.reshape(1,-1))
    proba = modele.predict_proba(new_data)[0][1]
    return [pred,proba]

# Tableau DF pour plus d'infos

dico = {
    "Sexe"          : ["Femme","Homme","Rien","Rien" ,"Rien","Rien","Rien","Rien"],
    "Emploi"        : ["Non qualifié et non résident","Non qualifié et résident","Qualifié","Hautement qualifié","Rien","Rien","Rien","Rien"],
    "Logement"      :["Gratuit","Propriétaire","Locataire","Rien","Rien","Rien","Rien","Rien"],
    "Compte courant":["Peu","Modéré","Assez riche","Riche","Rien","Rien","Rien","Rien"],
    "Compte épargne":["Peu","Modéré","Assez riche","Riche","Rien","Rien","Rien","Rien"],
    "Objectif"      :["Affaire","Voiture","Appareils ménagers","Education","Meubles/équipements","Radio/Télé","Réparations","Vacances/Autres"]
}

df = pd.DataFrame(dico)
st.write(df)

st.write("Pour remplir le formulaire, veuillez suivre l'exemple suivant :  Au niveau du sexe mettez  0 à si vous êtes femme,2, si vous êtes locataire(au niveau de logement)")

# ENtrée utilisateur ( Saisie de données)
nom = st.text_input(label="Nom")
sex = st.selectbox('Sexe',[0,1],index = 1)
age = st.number_input(label="Age (18 ans ou plus)",min_value=18,step = 1,value= 30)
duree = st.number_input(label="Durée de crédit (en mois)",min_value=1,step = 1, value = 12)
emploi = st.selectbox("Emploi",[0,1,2,3],index = 2)
montant = st.number_input(label="Montant du crédit",min_value=0,step = 1,value = 52)
logement = st.selectbox("Logement",[0,1,2],index = 1)
courant = st.selectbox("Compte courant",[0,1,2],index= 1)
epargne = st.selectbox("Compte épargne",[0,1,2,3],index = 1)
objectif = st.selectbox("Objectif",[0,1,2,3,4,5,6,7],index = 1)

# Création du bouton "Prédict" qui retourne la prédiction
if st.button("Predire"):
    prediction = inference(
        sex,age,duree,emploi,montant,logement,courant,epargne,objectif
    )
    if prediction[0] == 1:
        st.success("Crédit accordé")
        st.info(f"Probablité de risque :{prediction[1]}")
    else:
        st.error("Crédit refusé")