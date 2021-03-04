import os
import pandas as pd
import re


def correct_ids(start, end, string, window):

    match = re.search("[Ii]ch", string)
    match_start = match.start(0)

    expected_match_start = window
    difference = expected_match_start - match_start

    start_corr = start - difference
    end_corr = end - difference

    return start_corr, end_corr


def get_context(directory, data_table, context_size):
    """nach den dazugehörigen Textstellen im Korpus suchen und zur Tabelle hinzufügen"""

    corpus = os.listdir(directory)

    lines = [
        (startID, endID, file_name)
        for startID, endID, file_name in zip(
            data_table["StartChar"], data_table["EndChar"], data_table["Text_korr"]
        )
    ]

    context_before = []
    match = []
    context_after = []
    status = []

    for start_id, end_id, file_name in lines:
        if file_name in corpus:
            with open(directory + file_name, "r") as in_file:
                text = in_file.read()
            target = text[start_id:end_id]

            if re.fullmatch("[Ii]ch", target):
                status.append("fullmatch")
                context_before.append(text[start_id - context_size : start_id])
                match.append(target)
                context_after.append(text[end_id : end_id + context_size])
            else:
                tolerance_window = 5
                success = 0
                while tolerance_window < 30:
                    span = text[start_id - tolerance_window : end_id + tolerance_window]
                    if re.search("Ich| ich|^ich", span):
                        status.append("rough_match_{}".format(tolerance_window))
                        start_id_corr, end_id_corr = correct_ids(
                            start_id, end_id, span, tolerance_window
                        )
                        target = text[start_id_corr:end_id_corr]
                        context_before.append(text[start_id_corr - context_size : start_id_corr])
                        match.append(target)
                        context_after.append(text[end_id_corr : end_id_corr + context_size])
                        success = 1
                        break
                    else:
                        tolerance_window += 5
                if success == 0:
                    status.append("no_match")
                    context_before.append("None")
                    match.append("None")
                    context_after.append("None")
        else:  # PDFs werden zur Zeit übergangen
            status.append("PDF")
            context_before.append("PDF")
            match.append("PDF")
            context_after.append("PDF")

    # Überflüssigen Whitespace entfernen:
    context_before = [re.sub("[\t\n]", " ", line) for line in context_before]
    context_after = [re.sub("[\t\n]", " ", line) for line in context_after]
    match = [re.sub("[\t\n]", " ", line) for line in match]

    data_table["status"] = status
    data_table["context_before"] = context_before
    data_table["match"] = match
    data_table["context_after"] = context_after

    return data_table


corpus_directory = "data/corpus/"
context_size = 150

data_table = pd.read_csv("results/01_mapping.txt", sep="\t", index_col=0)
data_table = get_context(corpus_directory, data_table, context_size)

data_table.to_csv("results/02_context.txt", sep="\t")
