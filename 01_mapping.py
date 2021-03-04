import re
import pandas as pd
import numpy as np


def fix_annotator1(data_table):

    data_table.loc[data_table.Text == 'BA-Twi-in-Kirchen_15-01-19_10-08-86_SB11', 'StartChar'] \
        = data_table['StartChar'] + 89
    data_table.loc[data_table.Text == 'HA-Fachdidaktik-Teil2_13-03-14_26-06-32_SB02', 'StartChar'] \
        = data_table['StartChar'] + 1
    data_table.loc[(data_table.Text == 'HA-Texthabitualisierung_15-08-26_10-19-88_SB20')
                   & (data_table.StartChar > 10000), 'StartChar'] = data_table['StartChar'] + 7
    data_table.loc[data_table.Text == 'HA-Fachdidaktik_13-03-14_26-06-32_SB02', 'StartChar'] \
        = data_table['StartChar'] + 1
    data_table.loc[data_table.Text == 'Examensarbeit-Ergebnisse-Diskussion_12-06-12_27-23-27_SB15', 'StartChar'] \
        = data_table['StartChar'] + 4
    data_table.loc[(data_table.Text == 'Text-Beobachten_11-12-11_25-11-18_SB03')
                   & (data_table.StartChar > 1000), 'StartChar'] = data_table['StartChar'] + 1
    data_table.loc[data_table.Text == 'MA-Sprachkurse_15-12-17_07-16-13_WB06', 'StartChar'] \
        = data_table['StartChar'] + 47
    data_table.loc[(data_table.Text == 'BA-2011-Edition_15-03-09_24-24-59_SB02')
                   & (data_table.StartChar > 30000), 'StartChar'] = data_table['StartChar'] + 1

    return data_table


def fix_annotator2(data_table):

    data_table.loc[(data_table.Text == 'HA-Texthabitualisierung_15-08-26_10-19-88_SB20')
                   & (data_table.StartChar > 10000), 'StartChar'] = data_table['StartChar'] + 23
    data_table.loc[(data_table.Text == 'HA-Texthabitualisierung_15-08-26_10-19-88_SB20')
                   & (data_table.StartChar < 10000), 'StartChar'] = data_table['StartChar'] + 4

    return data_table


def invert_filename_order(filename):

    if re.fullmatch('.*?_([0-9]{2}-[0-9]{2}-[0-9]{2}_).*', filename):
        filename_new = re.sub('(.*?_)([0-9]{2}-[0-9]{2}-[0-9]{2}_)(.*)', r'\2\1\3.txt', filename)
        return filename_new
    else:
        print('Fehlerhaft benannte Datei: {}'.format(filename))
        return 'Fehlerhaft benannte Datei'


def correct_file_names(text_name_series):

    shortend_filenames = {'Modulabschlusspruefung-Genderansaetze-in-der-Jugendarbeit_13-04':
                              'Modulabschlusspruefung-Genderansaetze-in-der-Jugendarbeit_13-04-17_31-10-43',
                          'HA-der-Gebrauch-juedischer-Stereotypen-in-deutschen-Medien_12-0':
                          'HA-der-Gebrauch-juedischer-Stereotypen-in-deutschen-Medien_12-03-10_26-24-82_SB16',
                          'Abstract-Zusammenhang-Einleitung-Forschungsstand_15-06-10_52-14':
                          'Abstract-Zusammenhang-Einleitung-Forschungsstand_15-06-10_52-14-99_WB06',
                          'HA-Bildungstheorie-und-qualitative-Bildungsforschung_13-03-07_2':
                          'HA-Bildungstheorie-und-qualitative-Bildungsforschung_13-03-07_21-02-26_SB16',
                          'HA-Scaffolding-Bildungssprache-Ergaenzung_13-09-16_10-07-01_SB0':
                          'HA-Scaffolding-Bildungssprache-Ergaenzung_13-09-16_10-07-01_SB01'}

    filenames_mapping = {}

    for filename in text_name_series:
        if filename in shortend_filenames:
            filename_full = shortend_filenames[filename]
            filenames_mapping[filename] = invert_filename_order(filename_full)
        else:
            filenames_mapping[filename] = invert_filename_order(filename)

    corrected_file_names = text_name_series.map(filenames_mapping)

    return corrected_file_names


def get_coder_data(annotation_directory, coders):

    coder_data = {}

    for coder in coders:
        codings = pd.read_csv('{}{}_Codings.csv'.format(annotation_directory, coder), sep='\t')
        codings = codings[
            ['ID', 'TextID', 'WordID', 'SegPos1X', 'SegPos2X', 'SegPos1StdUnit', 'SegPos2StdUnit', 'Preview']]
        codings = codings.rename(columns={'WordID': 'CodeID',
                                          'SegPos1X': 'StartChar',
                                          'SegPos2X': 'EndChar',
                                          'Preview': 'Span',
                                          'SegPos1StdUnit': 'StartChar-PDF',
                                          'SegPos2StdUnit': 'EndChar-PDF'})

        # Code-IDs auf Code-Namen abbilden:
        codes = pd.read_csv('{}{}_Codewords.csv'.format(annotation_directory, coder), sep='\t')
        codes = {id: code for id, code in zip(codes['ID'], codes['Name'])}
        codings['Code'] = codings['CodeID'].map(codes)
        codings.drop(['CodeID'], axis=1)

        # Datei-IDs auf Dateinamen abbilden:
        texts = pd.read_csv('{}{}_Texts.csv'.format(annotation_directory, coder), sep='\t')
        texts = {id: code for id, code in zip(texts['ID'], texts['Name'])}
        codings['Text'] = codings['TextID'].map(texts)
        codings.drop(['TextID'], axis=1)

        # Korrektur der Form des Dateinamens für Übereinstimmung mit dem corpus-Ordner:
        codings['Text_korr'] = correct_file_names(codings['Text'])

        if coder == 'annotator1':
            codings = fix_annotator1(codings)
        elif coder == 'annotator2':
            codings = fix_annotator2(codings)

        # Einzigartigen Index aus Textname und Startzeichen erstellen:
        codings['index_intermediate'] = np.where(codings['StartChar-PDF'].str.match('.*:.*'),
                                                 codings['StartChar-PDF'],
                                                 codings['StartChar'])
        codings['Index'] = codings['Text'] + '+' + codings['index_intermediate'].astype(str)
        codings = codings.set_index('Index')
        codings.drop(['index_intermediate'], axis=1)

        # Bei Duplikaten nur den ersten Eintrag behalten:
        items_with_duplicates = codings.shape[0]
        codings = codings.loc[~codings.index.duplicated(keep='first')]
        items_without_duplicates = codings.shape[0]
        print('{} Duplikat(e) bei {} gelöscht.'.format(items_with_duplicates - items_without_duplicates, coder))

        # Spalten umsortieren:
        codings = codings[['ID', 'Text', 'Text_korr', 'Span', 'StartChar', 'EndChar', 'Code']]

        coder_data[coder] = codings

    return coder_data


def merge_datasets(data_table):

    data_table = pd.concat(data_table, axis=1, join='outer')
    data_table.columns = pd.Series(data_table.columns.tolist()).apply(pd.Series).sum(axis=1)  # collapse multi index

    # Zusammenführen analoger Informationen der vier Datensätze in den Spalten von annotator1
    for column in ['Text', 'Text_korr', 'ID', 'StartChar', 'EndChar']:
        data_table['annotator1{}'.format(column)].update(data_table['annotator2{}'.format(column)])
        data_table['annotator1{}'.format(column)].update(data_table['annotator4{}'.format(column)])
        data_table['annotator1{}'.format(column)].update(data_table['annotator3{}'.format(column)])

    # Datentypen korrigieren
    data_table['annotator1StartChar'] = data_table['annotator1StartChar'].astype(int)
    data_table['annotator1EndChar'] = data_table['annotator1EndChar'].astype(int)

    # Reduktion der Tabelle auf die relevanten Spalten, Umbenennungen
    data_table_clean = data_table.loc[:, 'annotator1ID': 'annotator1Code']
    data_table_clean = data_table_clean.rename(columns={'annotator1ID': 'ID',
                                                        'annotator1Text': 'Text',
                                                        'annotator1Text_korr': 'Text_korr',
                                                        'annotator1Span': 'Span',
                                                        'annotator1StartChar': 'StartChar',
                                                        'annotator1EndChar': 'EndChar',
                                                        'annotator1Code': 'Code-annotator1'})
    for coder in ['annotator2', 'annotator3', 'annotator4']:
        data_table_clean['Code-{}'.format(coder)] = data_table['{}Code'.format(coder)]

    # Sortieren, leere Felder mit 'None' füllen
    data_table_clean = data_table_clean.sort_index()
    data_table_clean.fillna('None', inplace=True)

    return data_table_clean


annotation_directory = 'data/annotation-data/'
coders = ['annotator2', 'annotator1', 'annotator3', 'annotator4']

coder_data = get_coder_data(annotation_directory, coders)
result = merge_datasets(coder_data)

result.to_csv('results/01_mapping.txt', sep='\t', index=True)
