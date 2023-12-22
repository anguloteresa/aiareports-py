from flask import Blueprint
from controllers.apiController import loadApi, uploadFile, generateQuestions, generateReport, generateCode
from controllers.userController import userLogin, getUsers, getUser, getUserQuestions, getUserByEmail, createUser, editUser, deleteUser
from controllers.reportController import getReportGroup, getUserReport, createReport, deleteReport, getReportsAll, editReport
from controllers.questionController import createQuestionGroup, createQuestion, getQuestionGroups, getQuestionsInGroup, deleteQuestion, deleteQuestionGroup, editQuestionGroup, editQuestion, createTest
from controllers.questionController import getQuestions

api = Blueprint('api', __name__)
userbp = Blueprint('user', __name__)
reportbp = Blueprint('report', __name__)
questionbp = Blueprint('question_group', __name__)

# Main Api (login, auth, openai)
api.route('/')(loadApi)
api.route('/login', methods=['GET', 'POST'])(userLogin)
api.route('/upload', methods=['GET', 'POST'])(uploadFile)
api.route('/generate-text', methods=['POST'])(generateReport)
api.route('/generate-questions', methods=['POST'])(generateQuestions)
api.route('/generate-answers', methods=['POST'])(generateCode)
# api.route('/generate-graph', methods = ["POST"])(generateGraph)

# User
userbp.route('/', methods=['GET'])(getUsers)
userbp.route('/create', methods=['POST'])(createUser)
# userbp.route('/<user_id>/', methods=['GET'])(getUser)
userbp.route('/email', methods=['GET'])(getUserByEmail)
userbp.route('/questions', methods=['GET'])(getUserQuestions)
userbp.route('/<user_id>/edit', methods=['POST'])(editUser)
userbp.route('/<user_id>/delete', methods=['DELETE'])(deleteUser)

# Question Routes
questionbp.route('/', methods=['GET'])(getQuestions)
questionbp.route('/create', methods=['POST'])(createTest)
questionbp.route('/update/<question_id>', methods=['POST'])(createTest)
questionbp.route('/delete', methods=['POST'])(createTest)
questionbp.route('/groups', methods=['GET'])(getQuestionGroups)
questionbp.route('/groups/create', methods=['POST'])(createQuestionGroup)
questionbp.route('/groups/<group_id>', methods=['GET'])(getQuestionsInGroup)
questionbp.route('/groups/<group_id>/edit', methods=['POST'])(editQuestionGroup)
questionbp.route('/<question_id>/edit', methods=['POST'])(editQuestion)
# userbp.route('/', methods=['GET'])(getUsers)

# Question Group Routes
# qgroup.route('/', methods = ['GET'])(getQuestions)

# Report Routes
reportbp.route('/', methods=['GET'])(getReportsAll)
reportbp.route('/create', methods=['POST'])(createReport)
reportbp.route('/<user_id>', methods=['GET'])(getReportGroup)
reportbp.route('/<user_id>/<report_id>', methods=['GET'])(getUserReport)
reportbp.route('/<user_id>/<report_id>/delete', methods=['DELETE'])(deleteReport)
reportbp.route('/<user_id>/<report_id>/edit', methods=['GET', 'POST'])(editReport)
