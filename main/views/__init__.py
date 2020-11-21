from .register import register
from .statics import index, Book, BookSuccess, ClassStore
from .account import Settings, Delete, Profile, SaveProfileData,\
	SaveNotificationLevel, selected_emails
from .store import catalog, ViewAllCompetitions, ViewAllQuizzes,\
	ViewAllWorkshops
from .actions import grant_competition_access, grant_quiz_access,\
	grant_workshop_access, give_soromoney
