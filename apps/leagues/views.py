from django.shortcuts import render, redirect
from django.db.models import Avg, Count
from .models import League, Team, Player

from . import team_maker

def index(request):
	context = {
		"one": Team.objects.filter(league_id=League.objects.get(name="Atlantic Soccer Conference").id),
		"two": Player.objects.filter(curr_team_id=Team.objects.get(location="Boston", team_name="Penguins").id),
		"three": Player.objects.filter(curr_team_id__in=Team.objects.filter(league_id=League.objects.get(name="International Collegiate Baseball Conference").id)),
		"four": Player.objects.filter(curr_team_id__in=Team.objects.filter(league_id=League.objects.get(name="American Conference of Amateur Football").id), last_name="Lopez"),
		"five": Player.objects.filter(curr_team_id__in=Team.objects.filter(league_id__in=League.objects.filter(sport="Football"))),
		"six": Team.objects.filter(curr_players__first_name="Sophia"),
		"seven": League.objects.filter(teams__curr_players__first_name="Sophia"),
		"eight": Player.objects.filter(last_name="Flores").exclude(curr_team=Team.objects.get(location="Washington", team_name="Roughriders")),
		"nine": Team.objects.filter(all_players__first_name="Samuel", all_players__last_name="Evans"),
		"ten": Player.objects.filter(all_teams__location="Manitoba", all_teams__team_name="Tiger-Cats"),
		"eleven": Player.objects.filter(all_teams__location="Manitoba", all_teams__team_name="Tiger-Cats").exclude(curr_team__location="Manitoba", curr_team__team_name="Tiger-Cats"),
		"twelve": Team.objects.filter(all_players__first_name="Jacob", all_players__last_name="Gray").exclude(curr_players__first_name="Jacob", curr_players__last_name="Gray"),
		"thirteen": Player.objects.filter(first_name="Joshua", all_teams__league__name="Atlantic Federation of Amateur Baseball Players"),
		"fourteen": Team.objects.annotate(num_players=Count("all_players")).filter(num_players__gte=12).values("location","team_name"),
		"fifteen": Player.objects.annotate(num_teams=Count("all_teams")).order_by("-num_teams")
	}
	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")