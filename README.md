# Aufbereitung von Annotationsdaten zur *Ich*-Verwendung in wissenschaftlichen Texten Studierender

In Knorr (2021) wurden *Ich*-Instanzen in wissenschaftlichen Texten Studierender annotiert und qualitativ ausgewertet.
In Andresen & Knorr (2021) wurden diese Annotationen für eine quantitative Auswertung nachgenutzt. Dazu sind eine
Reihe von Aufbereitungsschritten notwendig, die in Andresen (2021) ausführlich beschrieben werden. Dieses Repository
stellt die zu diesem Zweck verwendeten Pythonskripte zur Verfügung. Die Beschreibung der Schritte erfolgt hier nur 
überblicksartig, für Details zur Datenaufbereitung, der Motivation und dem dazugehörigen Forschungskontext 
siehe Andresen (2021).

## Voraussetzungen
Für Schritt 2 wird das Korpus KoLaS (Andresen & Knorr 2017) in einer in txt-Dateien konvertierten Version im 
Verzeichnis `data/corpus` benötigt. Das Korpus kann aus datenschutzrechtlichen Gründen nicht hier zur Verfügung 
gestellt werden. Nach einer kostenlosen Registrierung können die Daten aber hier bezogen werden: 
http://doi.org/10.25592/uhhfdm.8326.

## 1 Mapping
Die *Ich*-Instanzen wurden von vier Personen in MAXQDA annotiert. Aus einer Datenbank-Version (.mex) der MAXQDA-Projekte
wurden die csv-Dateien im Verzeichnis `data/annotation-data` gewonnen. Im ersten Schritt werden die vier Versionen der
Annotator:innen aufeinander abgebildet. Dieser Schritt ist vergleichsweise aufwendig, weil nicht alle vier Personen
die gleichen *Ich*-Instanzen annotiert haben.

## 2 Kontextextraktion
Für jede *Ich*-Instanz wurde anschließend aus dem Korpus der unmittelbare sprachliche Kontext extrahiert. Dies war aus
verschiedenen Gründen, die in Andresen (2021) beschrieben werden, nicht für alle Instanzen möglich.

## 3 Filtern
Anschließend wird der Datensatz in mehrfacher Hinsicht gefiltert. Ausgeschlossen werden dabei:
- Instanzen ohne erfolgreiche Kontextextraktion,
- Instanzen aus PDF-Dateien,
- (Beinahe-)Duplikate,
- weitere fehlerhafte oder für die Auswertung problematische Instanzen wie überwiegend fremdsprachliche Belege
- Instanzen, bei denen sich nicht mindestens zwei Annotator:innen einig waren,
- Instanzen, die nicht einer der Kernkategorien (Verfasser-Ich, Forscher-Ich und Erzähler-Ich nach Steinhoff, 2007) 
zugeordnet wurden.

## Weiterführende Analyse der Daten
Der resultierende Datensatz (`results/03_filter.txt`) ist identisch mit 
[dieser bei Zenodo veröffentlichten Version](https://doi.org/10.5281/zenodo.3999304). Eine quantitative Auswertung der 
Daten erfolgt in Andresen & Knorr (2021).

## Literatur

Andresen, Melanie. 2021. Nachnutzen und nachnutzen lassen: Datenaufbereitung im Rampenlicht. 
In Carmen Heine & Dagmar Knorr (eds.), Schreibwissenschaft methodisch (Forum Angewandte Linguistik). Berlin: Lang.

Andresen, Melanie & Dagmar Knorr. 2017. KoLaS – Ein Lernendenkorpus in der Schreibberatungsausbildung einsetzen. 
Zeitschrift Schreiben 10–17. https://zeitschrift-schreiben.ch/2017/#andresen.

Andresen, Melanie & Dagmar Knorr. 2021. 
Exploring the Use of the Pronoun I in German Academic Texts with Machine Learning. 
In Ralf H. Reussner, Anne Koziolek & Robert Heinrich (eds.), 
INFORMATIK 2020: Back to the Future (Lecture Notes in Informatics), 1327–1333. 
Bonn: Gesellschaft für Informatik. https://doi.org/10.18420/inf2020_124.

Knorr, Dagmar. 2021. Zwischen Forscher-, Verfasser- und Erzähler-Ich. 
Eine korpuslinguistische Studie zur Konstruktion von Selbstreferenz und zu ihrer Einsatzmöglichkeit in der 
Schreibberatungsausbildung. Zeitschrift für interkulturellen Fremdsprachenunterricht 26(1).

Steinhoff, Torsten. 2007. Zum ich-Gebrauch in Wissenschaftstexten. Zeitschrift für germanistische Linguistik 35(1–2). 
1–26. https://doi.org/10.1515/ZGL.2007.002.
