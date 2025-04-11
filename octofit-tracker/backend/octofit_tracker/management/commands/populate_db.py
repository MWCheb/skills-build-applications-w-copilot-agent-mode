from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId


class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data
        db = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])[settings.DATABASES['default']['NAME']]
        db.leaderboard.drop()
        db.workouts.drop()
        db.teams.drop()

        # Insert teams
        teams = [
            {"_id": ObjectId(), "name": "Blue Team"},
            {"_id": ObjectId(), "name": "Gold Team"}
        ]
        db.teams.insert_many(teams)

        # Insert leaderboard entries
        leaderboard_entries = [
            {"_id": ObjectId(), "team": teams[0]["_id"], "points": 100},
            {"_id": ObjectId(), "team": teams[1]["_id"], "points": 90}
        ]
        db.leaderboard.insert_many(leaderboard_entries)

        # Insert workouts
        workouts = [
            {"_id": ObjectId(), "name": "Cycling Training", "description": "Training for a road cycling event", "duration": 60},
            {"_id": ObjectId(), "name": "Crossfit", "description": "Training for a crossfit competition", "duration": 45}
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('Database populated successfully with MongoDB!'))
