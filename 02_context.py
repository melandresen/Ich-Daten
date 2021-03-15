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


def extended_search(text, start_index, end_index, tolerance_window):

    span = text[start_index - tolerance_window : end_index + tolerance_window]

    if re.search("Ich| ich|^ich", span):
        status = "rough_match_{}".format(tolerance_window)
        start_id_corr, end_id_corr = correct_ids(start_index, end_index, span, tolerance_window)
        target = text[start_id_corr:end_id_corr]
        context_before = text[start_id_corr - context_size : start_id_corr]
        match = target
        context_after = text[end_id_corr : end_id_corr + context_size]

        return status, context_before, match, context_after

    elif tolerance_window < 25:
        status, context_before, match, context_after = extended_search(
            text, start_index, end_index, tolerance_window + 5
        )

        return status, context_before, match, context_after

    else:
        return "no_match", "None", "None", "None"


def get_context(directory, data_table, context_size):
    """nach den dazugehörigen Textstellen im Korpus suchen und zur Tabelle hinzufügen"""

    context_data = pd.DataFrame(columns=["status", "context_before", "match", "context_after"])

    for start_index, end_index, file_name, index in zip(
        data_table["StartChar"], data_table["EndChar"], data_table["Text_korr"], data_table.index
    ):
        if os.path.isfile(directory + file_name):
            with open(directory + file_name, "r") as in_file:
                text = in_file.read()
            text = re.sub("[\t\n]", " ", text)
            target = text[start_index:end_index]

            if re.fullmatch("[Ii]ch", target):
                context_data.loc[index] = [
                    "fullmatch",
                    text[start_index - context_size : start_index],
                    target,
                    text[end_index : end_index + context_size],
                ]
            else:
                status_, context_before_, match_, context_after_ = extended_search(
                    text, start_index, end_index, 5
                )
                context_data.loc[index] = [status_, context_before_, match_, context_after_]

        else:  # PDFs werden zur Zeit übergangen
            context_data.loc[index] = ["PDF", "PDF", "PDF", "PDF"]

    result = pd.concat([data_table, context_data], axis=1)

    return result


corpus_directory = "data/corpus/"
context_size = 150

data_table = pd.read_csv("results/01_mapping.txt", sep="\t", index_col=0)
data_table = get_context(corpus_directory, data_table, context_size)

data_table.to_csv("results/02_context.txt", sep="\t")
