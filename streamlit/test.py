import streamlit as st
import numpy as np
import pickle

st.set_page_config(page_title="ML API - Client Risky Prediction")

st.markdown("""
<style>
    .stApp {
        font-family: 'Arial', sans-serif;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    h1 {
        color: #2e6c80;
        text-align: center;
        padding: 20px;
        font-family: 'Pacifico', cursive;
    }
    .stButton > button {
        width: 100%;
        background-color: #1abc9c;
        padding: 10px;
        font-size: 18px;
        margin-top: 20px;
    }
    .prediction-result {
        text-align: center;
        margin-top: 20px;
        padding: 15px;
        background-color: #f0f0f0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Load model
#model = pickle.load(open("model.pkl", "rb"))

# Predefined mappings
predefined_mappings = {
    "usage": {
        "VP": 0, "u1": 1, "moto": 2, "taxi": 3, "U2": 4, "engin": 5, "autre": 6,
        "louage": 7, "transport_rural": 8, "taxi_collectif": 9
    },
    "civilite": {
        "Mr": 0, "Mme": 1, "Entreprise": 2, "mult_CT": 3, "Org": 4, "Couple": 5,
        "Etablissement": 6
    },
    "activite": {
        "EDUCATION_FORMATION": 0, "PROFESSIONS_MEDICALES": 1, "EMPLOYE": 2, "RETRAITE": 3,
        "ACTIVITES_COMMERCIALES": 4, "AGRICULTURE": 5, "RESIDENT_A_L'ETRANGER": 6, "ARTISAN": 7,
        "CORPS_ACTIFS": 8, "INGENIEUR": 9, "CHAUFFEUR": 10, "PARAMEDICAL": 11, "OUVRIER": 12,
        "TAXI_LOUAGE_TRASPORT_RURAL": 13, "ARCHITECTURE_BTP_IMMOBILIER": 14, "TECHNICIEN": 15,
        "GERANT_DIRIGEANT": 16, "PROFESSIONNEL_CONSULTANT_EXPERT": 17, "METIERS_LEGAUX": 18,
        "INFORMATIQUE": 19, "DIRECTEUR": 20, "TOURISME": 21, "AUTO_ECOLE": 22,
        "ACTIVITES_SPORTIVES": 23, "ACTIVITES_ARTISTIQUES": 24, "TRANSPORT_AEREEN": 25, "ETAT": 26,
        "TRANSPORT": 27, "ACTIVITES_FINACIAIRES_ET_BANCAIRES": 28, "JOURNALISME": 29, "DIPLOMATIE": 30,
        "ASSOCIATIONS_ONG": 31, "SANS_PROFESSION": 32, "ACTIVITES_INDUSTRIELLES": 33
    },
    "classe": {
        "1.0": 0, "3.0": 1, "4.0": 2, "2.0": 3, "8.0": 4, "5.0": 5, "6.0": 6,
        "9.0": 7, "7.0": 8, "10.0": 9, "11.0": 10, "0.0": 11
    },
    "age_objet_assuree": [
        {"min": 0, "max": 1, "level": 1},
        {"min": 1, "max": 4, "level": 2},
        {"min": 5, "max": 9, "level": 3},
        {"min": 10, "max": 14, "level": 4},
        {"min": 15, "max": 19, "level": 5},
        {"min": 20, "max": 50, "level": 6}
    ],
    "age_client": [
        {"min": 18, "max": 24, "level": 1},
        {"min": 25, "max": 29, "level": 2},
        {"min": 30, "max": 39, "level": 3},
        {"min": 40, "max": 49, "level": 4},
        {"min": 50, "max": 59, "level": 5},
        {"min": 60, "max": 69, "level": 6},
        {"min": 70, "max": 79, "level": 7},
        {"min": 80, "max": 120, "level": 8}
    ],
    "place": [
        {"min": 1, "max": 5, "level": 1},
        {"min": 6, "max": 9, "level": 2},
        {"min": 10, "max": 29, "level": 3},
        {"min": 30, "max": 59, "level": 4},
        {"min": 60, "max": 999, "level": 5}
    ],
    "anciennete": [
        {"min": 0, "max": 2, "level": 1},
        {"min": 3, "max": 6, "level": 2},
        {"min": 7, "max": 14, "level": 3},
        {"min": 15, "max": 19, "level": 4},
        {"min": 20, "max": 99, "level": 5},
        {"min": 100, "max": 999, "level": 6}
    ],
    "puissance": [
        {"min": 0, "max": 3, "level": 1},
        {"min": 4, "max": 4, "level": 2},
        {"min": 5, "max": 6, "level": 3},
        {"min": 7, "max": 9, "level": 4},
        {"min": 10, "max": 14, "level": 5},
        {"min": 15, "max": 49, "level": 6},
        {"min": 50, "max": 999, "level": 7}
    ],
    "valeur_ranges": [
        {"min": 0, "max": 9999, "level": 1},
        {"min": 10000, "max": 19999, "level": 2},
        {"min": 20000, "max": 29999, "level": 3},
        {"min": 30000, "max": 49999, "level": 4},
        {"min": 50000, "max": 99999, "level": 5},
        {"min": 100000, "max": 499999, "level": 6},
        {"min": 500000, "max": 999999, "level": 7},
        {"min": 1000000, "max": 9999999, "level": 8}
    ],

    "charge_utile": [
        {"min": 0, "max": 1, "level": 1},
        {"min": 1, "max": 1.6, "level": 2},
        {"min": 1.6, "max": 3, "level": 3},
        {"min": 3, "max": 10, "level": 4},
        {"min": 10, "max": 999, "level": 5}
    ],
    "marque": [
        "RENAULT", "VOLKSWAGEN", "PEUGEOT", "FIAT", "CITROEN", "KIA", "FORD", "OPEL", "ISUZU", "MERCEDES-BENZ", 
        "TOYOTA", "HYUNDAI", "NISSAN", "SEAT", "B.M.W.", "CHEVROLET", "AUDI", "MITSUBISHI", "DACIA", "SUZUKI", 
        "MAZDA", "IVECO", "CHERY", "MAHINDRA", "SSANGYONG", "SKODA", "GREATWALL", "MBK", "CHRYSLER", "PIAGGIO", 
        "MINI", "JEEP", "VOLVO", "YAMAHA", "JAGUAR_LAND_ROVER", "HONDA", "TATA", "PO", "ALFA_ROMEO", "MG", 
        "UNISCOOT", "DAEWOO", "JIALING", "LANCIA", "DAIMLER", "BERLIET", "SCANIA", "DONG_FENG_", "DFSK", "ROVER", 
        "APRILIA", "TUNICOM", "COMET", "LANDINI", "WALLYSCAR", "ZIMOTA", "MALAGUTI", "MAN", "SMART", "DAIHATSU", 
        "JEDAA", "MISTRAL", "AVIA", "MASSEY_FERGUSON", "PORSCHE", "FTM", "CATERPILLAR", "FOTON", "KYMCO", "BAIC", 
        "DEUTZ", "KUBOTA", "DAF", "HUARD-TUNISIE", "VESPA", "GILERA", "COMECAB", "SAME_DEUTZ_FAHR", "SAMSUNG", 
        "HIDROMEK", "KINGLONG", "AUTOBIANCHI", "DS", "BENTLEY", "MASERATI", "AIMA", "INFINITI", "BENZHOU", "BOBCAT", 
        "DOOSAN", "SIMATRA", "SYM", "CASE", "BAOLI", "DODGE", "HAVAL", "MAGIRUS", "LADA", "LAMBORGHINI", "GEELY"
    ],
    "delegation": [
        "Ariana Ville",
        "Sfax Ville",
        "Monastir",
        "El Menzah",
        "Le Bardo",
        "Mannouba",
        "El Mourouj",
        "Hammamet",
        "Sousse Ville",
        "Sakiet Ezzit",
        "Sousse Jaouhara",
        "La Marsa",
        "La Soukra",
        "Nabeul",
        "Ben Arous",
        "Msaken",
        "Raoued",
        "Sousse Riadh",
        "Kairouan Sud",
        "Moknine",
        "Bizerte Nord",
        "Sakiet Eddaier",
        "Rades",
        "El Omrane Superieur",
        "Ezzahra",
        "Hammam Sousse",
        "Le Kef Est",
        "Nouvelle Medina",
        "Sfax Sud",
        "El Kabbaria",
        "Megrine",
        "Bou Mhel El Bassatine",
        "Hammam Lif",
        "Mahdia",
        "El Ouerdia",
        "La Goulette",
        "Gafsa Sud",
        "Jendouba Nord",
        "Ksibet El Mediouni",
        "Beja Nord",
        "Carthage",
        "Houmet Essouk",
        "Korba",
        "Fouchana",
        "Hammam Chatt",
        "Bab Bhar",
        "Kalaa El Kebira",
        "Zarzis",
        "Ettahrir",
        "Ksar Helal",
        "Ezzouhour (Tunis)",
        "Siliana Sud",
        "Kalaa Essghira",
        "Kelibia",
        "Oued Ellil",
        "Akouda",
        "Dar Chaabane Elfehri",
        "Kasserine Nord",
        "El Hrairia",
        "Gabes Medina",
        "Mornag",
        "Mnihla",
        "Sayada Lamta Bou Hajar",
        "Midoun",
        "Sidi El Bechir",
        "Cite El Khadra",
        "Grombalia",
        "Mohamadia",
        "Zaghouan",
        "Sfax Est",
        "Beni Khiar",
        "Sidi Hassine",
        "Ettadhamen",
        "La Medina",
        "Teboulba",
        "Feriana",
        "Soliman",
        "Jemmal",
        "La Chebba",
        "Mejez El Bab",
        "Sidi Bouzid Ouest",
        "Sahline",
        "Bembla",
        "El Kram",
        "Gabes Sud",
        "Menzel Bourguiba",
        "Menzel Temime",
        "Medenine Sud",
        "El Omrane",
        "Bou Merdes",
        "El Ksar",
        "Ras Jebel",
        "Ajim",
        "Mornaguia",
        "Le Kef Ouest",
        "Tozeur",
        "Beni Khalled",
        "Kebili Sud",
        "Douar Hicher",
        "Menzel Jemil",
        "Testour",
        "Ghardimaou",
        "Tajerouine",
        "Enfidha",
        "Gabes Ouest",
        "Essijoumi",
        "Ksour Essaf",
        "Douz",
        "Menzel Bouzelfa",
        "Tataouine Sud",
        "Ouerdanine",
        "Jedaida",
        "Souassi",
        "El Hamma",
        "El Jem",
        "Bou Argoub",
        "Zeramdine",
        "Tinja",
        "Jebel Jelloud",
        "Sidi Thabet",
        "Dahmani",
        "Mahras",
        "Bekalta",
        "Jebeniana",
        "Kairouan Nord",
        "Makthar",
        "Ouled Chamakh",
        "Agareb",
        "Bou Salem",
        "Gaafour",
        "Bir Ali Ben Khelifa",
        "Jarzouna",
        "El Haouaria",
        "Sakiet Sidi Youssef",
        "Bou Hajla",
        "Teboursouk",
        "Ben Guerdane",
        "El Guettar",
        "Ain Draham",
        "Sned",
        "Chorbane",
        "Le Sers",
        "Ezzouhour (Kasserine)",
        "El Amra",
        "Nebeur",
        "Hammam El Ghezaz",
        "Sbikha",
        "Bou Ficha",
        "Fernana",
        "Beni Hassen",
        "El Ksour",
        "Foussana",
        "El Hencha",
        "Sidi Bou Ali",
        "Degueche",
        "Kalaat Sinane",
        "Sidi Alouene",
        "Hammam Zriba",
        "Kerkenah",
        "Metlaoui",
        "Oueslatia",
        "Borj El Amri",
        "Bou Arada",
        "Tebourba",
        "Bizerte Sud",
        "El Mida",
        "Hergla",
        "Thala",
        "El Mdhilla",
        "Sbeitla",
        "Tabarka",
        "Nasrallah",
        "El Fahs",
        "Bir Mcherga",
        "Souk El Ahad",
        "Jendouba",
        "Cherarda",
        "Mareth",
        "Mateur",
        "Hajeb El Ayoun",
        "Le Krib",
        "Ennadhour",
        "Moulares",
        "Nefza",
        "Mejel Bel Abbes",
        "El Metouia",
        "Haffouz",
        "Oued Mliz",
        "Chebika",
        "Ghar El Melh",
        "Bab Souika",
        "El Alia",
        "El Ala",
        "Tataouine Nord",
        "Menzel Chaker",
        "Kalaat Landlous",
        "Esskhira",
        "Rohia",
        "Regueb",
        "Bargou",
        "Sidi El Heni",
        "Redeyef",
        "Kesra",
        "Hassi El Frid",
        "Sidi Aich",
        "Nefta",
        "Beni Khedache",
        "Jerissa",
        "Nouvelle Matmata",
        "Kebili Nord",
        "Ghomrassen",
        "Melloulech",
        "Utique",
        "Kalaa El Khasba",
        "El Battan",
        "Thibar",
        "Maknassy",
        "Amdoun",
        "Takelsa",
        "Ghannouche",
        "Sidi Bouzid Est",
        "Goubellat",
        "El Aroussa",
        "Saouef",
        "Sidi Bou Rouis",
        "Sejnane",
        "Kasserine Sud",
        "Smar",
        "Bir El Haffey",
        "Ouled Haffouz",
        "Ben Oun",
        "Kondar",
        "Mezzouna",
        "Jilma",
        "Sbiba",
        "Ghraiba",
        "Bir Lahmar",
        "Beja Sud",
        "Joumine",
        "Dhehiba",
        "Haidra",
        "Hbira",
        "Menzel Bouzaiene",
        "Gafsa Nord",
        "Belkhir",
        "Cebbala",
        "Sidi Makhlouf",
        "Jediliane",
        "Touiref",
        "Balta Bou Aouene",
        "Menzel Habib",
        "Matmata",
        "Souk Jedid",
        "Tameghza",
        "Remada",
        "Medenine Nord",
        "Hezoua",
        "Ghezala",
        "El Faouar",
        "El Ayoun"
    ],
    
    "civilite": [
        "Mr",
        "Mme",
        "mult_CT",
        "Entreprise",
        "Couple",
        "Org",
        "Etablissement",
        "Gov"
    ]


}


def get_level(value, ranges):
    for range_ in ranges:
        if range_["min"] <= value < range_["max"]:
            return range_["level"]
    raise ValueError(f"Value {value} is out of the defined range!")

def main():
    st.title('Client Risky Prediction')

    with st.form('prediction_form'):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Object Info")
            puissance = st.number_input('Puissance', min_value=0)
            age_objet_assuree = st.number_input('Age de l\'objet assuré', min_value=0)
            valeur_venale = st.number_input('Valeur vénale', min_value=0)
            valeur_neuve = st.number_input('Valeur neuve', min_value=0)
            charge_utile = st.number_input('Charge utile', min_value=0.0)
            usage = st.selectbox('Usage', options=list(predefined_mappings["usage"].keys()))
            place = st.number_input('Nombre de places', min_value=1)


        with col2:
            st.subheader("Client Info") 
            age_client = st.number_input('Âge du client', min_value=18)
            sexe = st.selectbox('Sexe', ['M', 'F'])
            civilite = st.selectbox('Civilite',  options=list(predefined_mappings["civilite"]))
            delegation = st.selectbox('Délégation',  options=list(predefined_mappings["delegation"]))
            activite = st.selectbox('Activité', options=list(predefined_mappings["activite"].keys()))
            anciennete = st.number_input('Ancienneté', min_value=0)
            classe = st.selectbox('Classe', options=list(predefined_mappings["classe"].keys()))



        submitted = st.form_submit_button("Predict")

        if submitted:
            try:
                puissance = get_level(puissance, predefined_mappings["puissance"])
                age_objet_assuree = get_level(age_objet_assuree, predefined_mappings["age_objet_assuree"])
                valeur_venale = get_level(valeur_venale, predefined_mappings["valeur_ranges"])
                valeur_neuve = get_level(valeur_neuve, predefined_mappings["valeur_ranges"])
                Charge_utile = get_level(charge_utile, predefined_mappings["charge_utile"])
                anciennete = get_level(anciennete, predefined_mappings["anciennete"])
                place = get_level(place, predefined_mappings["place"])
                age_client = get_level(age_client, predefined_mappings["age_client"])

                usage = predefined_mappings["usage"][usage] # [usage] is the input value from the user
                activite = predefined_mappings["activite"][activite]
                classe = predefined_mappings["classe"][classe]
                sexe = 0 if sexe == 'M' else 1

                features = np.array([
                    puissance, age_objet_assuree, valeur_venale, valeur_neuve,
                    charge_utile, usage, anciennete, activite, classe,
                    age_client, delegation, sexe, place
                ]).reshape(1, -1)

                #prediction = model.predict(features)[0]

                #result_text = "Risque Élevé" if prediction == 1 else "Risque Faible"
                st.success(f"Résultat: {result_text}")
            except ValueError as e:
                st.error(f"Erreur: {e}")

if __name__ == "__main__":
    main()