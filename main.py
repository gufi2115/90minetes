from db.models import ClubsNamesM, TimetableM
from django.db.models import Count
import json
from types import NoneType
from scraped_league import scraping


#testm.objects.create(nazwa="dupa2", dupa=2)
#test = testm(nazwa="dupa23", dupa=23)
#test.save()



def save_sql(scraping):
    scraping = scraping.replace("/", "_").replace(" ", "_").replace(",", "").replace(":", "").lower()
    with open(f"league/{scraping}.json", "r", encoding="utf-8") as f:
           table_json = json.load(f)
    return table_json


var_table = save_sql(scraping)
def league_name(json_table):
    for k, v in json_table["Tabela"][-1].items():
        return k


def teams_name(json_table):

    teams_names_list = []

    list_with_data_for_table = []

    for v in list(json_table["Tabela"][-1].values()):
        for i in v:
          list_with_data_for_table.append(i)

    for i in list_with_data_for_table:
        for k, v in i.items():
            if k == "Nazwa":
                teams_names_list.append(v)

    return sorted(teams_names_list)


def rounds(json_table):

    list_with_round_dict = []

    list_with_round = []

    for k, v in json_table["Tabela"][-1].items():
        for i in v:
            if list(i.keys())[0] == "Terminarz":
                list_with_round_dict.append(list(i.values())[0])

    for i in list_with_round_dict:
        for k, v in i.items():
            list_with_round.append(k)

    return list_with_round


def insert_clubs(teams_names, league_name):

    league_count = ClubsNamesM.objects.filter(league_name=league_name).count()
    if league_count < len(teams_names):
        for data_teams in teams_names:
            ClubsNamesM.objects.create(league_name=league_name, club_name=data_teams)


def full_timetable(league_name, teams_names, json_table):
    timetable = []
    for league in json_table["Tabela"]:
        for k, v in league.items():
            if k == league_name:
                timetable = league[league_name][len(teams_names):][0]
    return timetable


def results(rounds, full_timetable, teams_names):

    results_list = []
    all_months = ['lipca', 'sierpnia', 'września', 'października', 'listopada', 'grudnia', 'stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca']

    for r in range(len(rounds)):
        for i in full_timetable["Terminarz"][rounds[r]]:
            if ":" in i:
                i = i.split()[:-3]
                for i1 in i:
                    if i1 not in " ".join(teams_names) or i1 == '-' or i1[1] == '-':
                        if i1 == '-' or i1[1] == '-' and " ".join(i[:i.index(i1)]) in " ".join(teams_names) and " ".join(i[i.index(i1) + 1:]) in " ".join(teams_names):
                            results_list.append({rounds[r]:" ".join(i).replace(f"{i1} ", f"~{i1}~").split("~")})

            else:

                if '-' in i.split():
                    results_list.append({rounds[r]: [" ".join(i.split()[:i.split().index("-")]), '-', " ".join(i.split()[i.split().index("-") + 1:])]})

                else:

                    try:
                        if not i.split()[-1] in all_months:
                            for i1 in i.split():
                                if i1[1] == "-" or i1[0] == "-" :
                                    results_list.append({rounds[r]:i.replace(f"{i1} ", f"~{i1}~").split("~")})

                        else:
                            match_day = " ".join(i.split()[-2:])
                            print(match_day)
                            for i1 in i.split():
                                if i1[1] == "-" or i1[0] == "-" :
                                    results_list.append({rounds[r]:i.replace(f"{i1} ", f"~{i1}~").replace(match_day, "").split("~")})

                    except IndexError:
                        pass
    return results_list


def insert_timetable(results, rounds, league_name):
    for r in range(len(rounds)):
        for i in results:
            try:
                team_one_goals = int(i[rounds[r]][1].split("-")[0]) if i[rounds[r]][1].split("-")[0] != '' else None
                team_two_goals = int(i[rounds[r]][1].split("-")[1]) if i[rounds[r]][1].split("-")[1] != '' else None
                date_round = rounds[r].split()[3:]
                home_team = ClubsNamesM.objects.filter(club_name=f"{i[rounds[r]][0].strip()}", league_name=f"{league_name}").values_list('id', flat=True).first()
                away_team = ClubsNamesM.objects.filter(club_name=f"{i[rounds[r]][2].strip()}", league_name=f"{league_name}").values_list('id', flat=True).first()
                count_of_results_in_sql = TimetableM.objects.filter(league_name=league_name).count()
                count_of_results = len(results)
                round_number = rounds[r].split()[1]
                home_team_win = (True if team_one_goals > team_two_goals else False) if not isinstance(team_one_goals, type(None)) and not isinstance(team_two_goals, type(None)) else False
                draw = ((True if team_one_goals == team_two_goals else False)
                        if not isinstance(team_one_goals, str) and not isinstance(team_two_goals, str)
                        else False) if not isinstance(team_one_goals, type(None)) and not isinstance(team_two_goals, type(None)) else False
                away_team_win = (True if team_one_goals < team_two_goals else False) if not isinstance(team_one_goals, type(None)) and not isinstance(team_two_goals, type(None)) else False
                if count_of_results > count_of_results_in_sql:
                    TimetableM.objects.create(league_name=league_name, round_number=round_number, date_round=date_round,
                                              home_team_goals=team_one_goals, away_team_goals=team_two_goals, home_team_win=home_team_win,
                                              draw=draw, away_team_win=away_team_win, away_team_id=away_team, home_team_id=home_team)
            except KeyError:
                continue


def main():
    var_league_name = league_name(var_table)
    var_teams_names = teams_name(var_table)
    var_rounds = rounds(var_table)
    var_full_timetable = full_timetable(var_league_name, var_teams_names, var_table)
    var_results = results(var_rounds, var_full_timetable, var_teams_names)
    insert_clubs(teams_name(var_table), league_name(var_table))
    insert_timetable(var_results, var_rounds, var_league_name)

main()