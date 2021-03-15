import pandas as pd
from collections import Counter


def map_star_categories(data_table):
    """Codes mit Sternchen in die ohne Sternchen überführen"""

    coders = ["annotator1", "annotator2", "annotator3", "annotator4"]

    mapping_dict = {
        "Verfasser-Ich*": "Verfasser-Ich",
        "Forscher-Ich*": "Forscher-Ich",
        "Erzähler-Ich*": "Erzähler-Ich",
    }
    for coder in coders:
        data_table["Code-{}".format(coder)] = data_table["Code-{}".format(coder)].replace(
            mapping_dict
        )

    return data_table


def add_agreement_info(data_table):

    max_agreement_freqs = []
    max_agreement_labels = []

    for a, b, c, d in zip(
        data_table["Code-annotator1"],
        data_table["Code-annotator2"],
        data_table["Code-annotator3"],
        data_table["Code-annotator4"],
    ):
        counts = Counter([a, b, c, d])
        max_agreement_label = counts.most_common(1)[0][0]
        max_agreement_freq = counts[max_agreement_label]
        max_agreement_freqs.append(max_agreement_freq)
        max_agreement_labels.append(max_agreement_label)

    data_table["max_agreement_freq"] = max_agreement_freqs
    data_table["max_agreement_label"] = max_agreement_labels

    return data_table


def fix_data_set(data):

    data = data[data["Text"] != "MA-Expose_12-01-18_19-23-29_SB14"]
    data = data[data["Text"] != "HA-Inklusion_14-12-29_22-14-33_SB02"]
    data = data[data["Text"] != "BA-Experteninterview-Theorie-Methode_13-07-29_28-17-44"]
    data = data[data["Text"] != "Expose_15-10-01_03-11-18_WB06"]
    data = data[data["Text"] != "BA-Arbeit_13-06-03_28-17-44_SB01"]
    data = data[data["Text"] != "HA-Scaffolding-Bildungssprache_13-09-16_10-07-01_SB01"]
    data = data[data["Text"] != "HA-Scaffolding-Einleitung_13-09-02_10-07-01_SB01"]
    data = data[data["Text"] != "HA-Scaffolding-Scaffolding_13-09-22_10-07-01_SB01"]
    data = data[data["Text"] != "Hausarbeit-Scaffolding_13-10-06_10-07-01_SB12"]
    data = data[data["Text"] != "MA-Gliederung_15-07-15_23-21-75_SB02"]
    data = data.drop("MA-Ergebnisse-Interpretation_16-07-05_23-21-27_SB02+8912")  # ich ist Wortteil
    data = data.drop("HA-Linguistik-des-Russischen_12-06-15_14-03-93_SB16+34501")  # viel Russisch
    data = data.drop("Uebergangssystem-freigeschrieben_13-06-07_24-29-07+20796")  # ich ist Wortteil
    data = data.drop("BA-Kunst_15-12-17_10-07-01_SB01+6239")  # Autorenkommentar
    data = data.drop("BA-Kunst_15-12-17_10-07-01_SB01+6271")  # Autorenkommentar
    data = data.drop(
        "HA-Gleichberechtignung-in-der-Schule_12-03-21_06-07-80_SB13+522"
    )  # Autorenkommentar
    data = data.drop("Aufgaben-Portofolio_15-01-29_21-02-74_SB01+1178")
    data = data.drop("BA-Kindergarten_15-05-11_15-23-51_SB20+4441")
    data = data.drop("HA-Lesemotivation_15-06-02_21-02-74_SB01+10785")
    data = data.drop("HA-Lesemotivation_15-06-02_21-02-74_SB01+14733")
    data = data.drop("HA-Lesemotivation_15-06-02_21-02-74_SB01+3004")
    data = data.drop("HA-Motivation_15-12-07_24-05-64_SB02+9886")
    data = data.drop("HA-der-Gebrauch-juedischer-Stereotypen-in-deutschen-Medien_12-0+3513")
    data = data.drop("MA-Prozessdatei_15-07-07_11-24-33_SB02+100907")
    data = data.drop("MA-Prozessdatei_15-07-07_11-24-33_SB02+112899")
    data = data.drop("MA-Prozessdatei_15-07-07_11-24-33_SB02+115275")
    data = data.drop("MA-Prozessdatei_15-07-07_11-24-33_SB02+116027")
    data = data.drop("MA-Prozessdatei_15-07-07_11-24-33_SB02+130178")
    data = data.drop("MA-Prozessdatei_15-07-07_11-24-33_SB02+133683")
    data = data.drop("MA-Prozessdatei_15-07-07_11-24-33_SB02+142118")
    data = data.drop("MA-Prozessdatei_15-07-07_11-24-33_SB02+154012")
    data = data.drop("MA-Prozessdatei_15-07-07_11-24-33_SB02+172377")
    data = data.drop("MA-Prozessdatei_15-07-07_11-24-33_SB02+19778")
    data = data.drop("MA-Prozessdatei_15-07-07_11-24-33_SB02+23371")
    data = data.drop("MA-Prozessdatei_15-07-07_11-24-33_SB02+8118")
    data = data.drop("Magisterarbeit-Fragebogenauswertung_13-05-10_09-19-81_SB13+4121")
    data = data.drop("Magisterarbeit-Fragebogenauswertung_13-05-10_09-19-81_SB13+6707")

    # fix spelling:
    data.index = data.index.str.replace("Bildungsstandarts", "Bildungsstandards", regex=True)

    return data


data_table = pd.read_csv("results/02_context.txt", sep="\t", index_col=0)
print("{} Zeilen vor weiterer Bereinigung".format(data_table.shape[0]))

# Instanzen ohne erfolgreiche Kontextextraktion aussschließen
data_table = data_table[data_table["status"] != "no_match"]
print("{} Zeilen nach Ausschluss von Zeilen ohne Treffer im Text".format(data_table.shape[0]))

# Instanzen aus PDF-Dateien ausschließen
data_table = data_table[data_table["status"] != "PDF"]
print("{} Zeilen nach Löschung von PDFs".format(data_table.shape[0]))

# Duplikate aussschließen
data_table = data_table.drop_duplicates(subset=["context_before"], keep="first")
data_table = data_table.drop_duplicates(subset=["context_after"], keep="first")
print("{} Zeilen nach Löschung von Duplikaten".format(data_table.shape[0]))

# Weitere Instanzen manuell ausschließen (Beinahe-Duplikate, überwiegend fremdsprachliche Belege, …)
data_table = fix_data_set(data_table)
print(
    "{} Zeilen nach Löschung von fehlerhaften Dateien und Einzelsätzen".format(data_table.shape[0])
)

# Minimales Agreement von zwei Annotator:innen
min_agreement = 2
data_table = map_star_categories(data_table)
data_table = add_agreement_info(data_table)
data_table = data_table[data_table["max_agreement_freq"] >= min_agreement]
print(
    "{} Zeilen nach Reduktion auf minimales Agreement von {}".format(
        data_table.shape[0], min_agreement
    )
)

# Reduktion auf die drei Kernkategorien
categories_of_interest = ["Verfasser-Ich", "Forscher-Ich", "Erzähler-Ich"]
data_table = data_table[data_table["max_agreement_label"].isin(categories_of_interest)]
print("{} Zeilen für die drei relevanten Kategorien".format(data_table.shape[0]))

data_table.to_csv("results/03_filter.txt".format(min_agreement), sep="\t")
