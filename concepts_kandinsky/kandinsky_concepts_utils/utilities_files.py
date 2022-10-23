"""
    Files utilities

    :author: Anna Saranti
    :copyright: © 2021 HCI-KDD (ex-AI) group
    :date: 2022-02-10
"""

from datetime import datetime
import os
import shutil


def cleanup_files_output(kandinksy_pattern_name: str, concept_name: str, nodes_nr: int):
    """
    Cleanup the files from the previous run

    :param kandinksy_pattern_name: Kandinsky pattern name
    :param concept_name: Name of the concept
    :param nodes_nr: Number of nodes
    """

    # Delete the files in a folder -------------------------------------------------------------------------------------
    files_output_nodes_nr_folder = os.path.join("data",
                                                "output",
                                                concept_name,
                                                f"{concept_name}_nodes_nr_{nodes_nr}",
                                                kandinksy_pattern_name)
    if os.path.exists(files_output_nodes_nr_folder):
        for file_output_nodes_nr in os.listdir(files_output_nodes_nr_folder):
            if os.path.isfile(os.path.join(files_output_nodes_nr_folder, file_output_nodes_nr)):
                os.remove(os.path.join(files_output_nodes_nr_folder, file_output_nodes_nr))
            else:
                shutil.rmtree(os.path.join(files_output_nodes_nr_folder, file_output_nodes_nr))

    if not os.path.exists(files_output_nodes_nr_folder):
        os.mkdir(files_output_nodes_nr_folder)
    print("\n=======================================================================================================\n")


def zip_generated_files(concept_name: str):
    """
    Zip all generated files in the concept

    :param concept_name: Name of the concept
    """

    files_output_nodes_nr_folder = os.path.join("data",
                                                "output",
                                                concept_name)

    now = datetime.now()
    date_time = now.strftime("%Y%m%d_%H%M")
    print("date and time:", date_time)

    shutil.make_archive(
        os.path.join("data", "output", date_time + "_" + concept_name),
        'zip',
        files_output_nodes_nr_folder
    )

