from typing import List, Tuple, Dict, Optional
import os
import warnings
from glob import glob
import numpy as np
import pandas as pd
import argparse
from IPython.display import display

parser = argparse.ArgumentParser()
parser.add_argument("--dir-path", type=str,
                    help="example --dir-path ./leaderboard_score")
parser.add_argument("--weight-list", type=float, nargs='*',
                    help="example --weight-list 0.7 0.3")
parser.add_argument("--show-info", action="store_true",
                    help="increase output verbosity")
parser.add_argument("-o", "--csv-output", type=str, default=None,
                    help="example --csv-output output.csv, Default: None")

args = parser.parse_args()

def get_final_score(*csv: List[pd.DataFrame | str], weight_list: List[float], show_info: bool = False, dir_path: Optional[str] = None) -> pd.DataFrame:
    """Calculate the scores from each hackathon using the specified weights (30%, 70%), and display the results for each team by id_team.

    Args:
        weight_list (List[float]): A list of weights corresponding to each hackathon's contribution to the final score. The sum must equal 1.0.
        show_info (bool, optional): If True, includes detailed breakdowns (weight, raw_score, weighted_score) for each hackathon in the output. Defaults to False.
        dir_path (Optional[str], optional): If provided, reads score data from CSV files located in this directory using pandas. Defaults to None.

    Returns:
        pandas.DataFrame:
        Returns a table mapping each id_team to their final weighted score.
    """

    if dir_path is not None:
        if not os.path.exists(dir_path):
            raise FileExistsError("No such directory.")
        warnings.warn("Files are sorted by name, please check all of your filenames before.")
        csv = []
        for fp in sorted(glob(os.path.join(dir_path, "*.csv"))):
            csv.append(pd.read_csv(fp))

    if len(csv) != len(weight_list):
        raise ValueError(f"CSV should equal weight_list, but {len(csv)} != {len(weight_list)}.")
    
    final_score = {}
    info_score = {}
    df_dict = {}
    for w, tab in zip(weight_list, csv):
        one_csv: pd.DataFrame = tab
        for _, row in one_csv.iterrows():
            id_team: str = ''
            if len(row["TeamName"].split('-')) >= 2:
                id_team = row["TeamName"].split('-')[0].strip()
                id_team = str(int(id_team))
            elif len(row["TeamName"].split('_')) >= 2:
                id_team = row["TeamName"].split('_')[0].strip()
                id_team = str(int(id_team))
            else:
                id_team = row["TeamName"].strip()
            info_score[id_team] = info_score.get(id_team, []) + [(w, round(row["Score"], 4), round(w * row["Score"], 4))]
            final_score[id_team] = round(final_score.get(id_team, 0) + (w * row["Score"]), 4)

    id_teams = []        
    final_score_list = []        
    w_rs_ws = []        
    for k, v in final_score.items():
       id_teams.append(k)
       final_score_list.append(v)
       w_rs_ws.append(str(info_score[k]))
    output = pd.DataFrame({
        "id_team": id_teams,
        "final_score": final_score_list,
        "info": w_rs_ws if show_info else [""] * len(w_rs_ws),
    })

    # final_score = dict(sorted(final_score.items(), key=lambda x: x[1], reverse=True))
    # info_score = {k: info_score[k] for k in final_score.keys()}
    # return (info_score, final_score) if show_info else final_score

    output.sort_values(["final_score", "id_team"], ignore_index=True, ascending=False, inplace=True)
    return output

def main():
    df_score: pd.DataFrame = get_final_score(dir_path=args.dir_path, show_info=args.show_info, weight_list=args.weight_list)
    final_score = df_score['final_score'].unique().tolist()
    (winner, runner_up_1, runner_up_2) = final_score[:3]
    df_score["rank"] = pd.NA
    df_score.loc[df_score["final_score"]==winner, 'rank'] = "🥇"
    df_score.loc[df_score["final_score"]==runner_up_1, 'rank'] = "🥈"
    df_score.loc[df_score["final_score"]==runner_up_2, 'rank'] = "🥉"
    for rank, score in enumerate(final_score[3:], start=4):
        df_score.loc[df_score["final_score"]==score, 'rank'] = rank

    display(df_score)
    if args.csv_output is not None:
        df_score.to_csv(args.csv_output, index=False)

if __name__ == "__main__":
    main()