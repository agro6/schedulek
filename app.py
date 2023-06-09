import csv
from flask import Flask, request, jsonify
from flask_cors import CORS
from json import loads, dumps
import pandas as pd

app = Flask(__name__)
CORS(app)

# Define the CSV file path
USERS_FILE_PATH = 'csvs/users.csv'
GROUPS_FILE_PATH = 'csvs/groups.csv'
LESSONS_FILE_PATH = 'csvs/lessons.csv'
GRADES_FILE_PATH = 'csvs/grades.csv'
HOMEWORK_FILE_PATH = 'csvs/homework.csv'
HOURS_FILE_PATH = 'csvs/hours.csv'
MESSAGES_FILE_PATH = 'csvs/messages.csv'

def read_csv(file):
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]
    return rows
# Define the user model
class User:
    def __init__(self, id, name, last_name, type, email):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.type = type
        self.email = email

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'last_name': self.last_name, 'type': self.type, 'email': self.email}

# Helper function for reading the user data from the CSV file
def read_groups_from_csv():
    with open(GROUPS_FILE_PATH, 'r') as f:
        lines = f.readlines()
        headers = lines[0][1:].strip().split(',')
        groups = []
        for line in lines[1:]:
            values = line.strip().split(',')[1:]
            group = Group(*values)
            groups.append(group)
        return groups

class Group:
    def __init__(self, group_name, user_id):
        self.group_name = group_name
        self.user_id = user_id


    def to_dict(self):
        return {'group_name': self.group_name, 'user_id': self.user_id}

# Helper function for reading the user data from the CSV file
def read_users_from_csv():
    with open(USERS_FILE_PATH, 'r') as f:
        lines = f.readlines()
        headers = lines[0].strip().split(',')
        users = []
        for line in lines[1:]:
            values = line.strip().split(',')
            user = User(*values)
            users.append(user)
        return users

@app.route('/groups', methods=['GET'])
def get_groups():
    groups = read_groups_from_csv()
    groups_list = [user.to_dict() for user in groups]
    return jsonify(groups_list)


@app.route('/', methods=['GET'])
def homepage():
    return '/users - get - list all users\n /students - get - list all students /groups - lista klas'

@app.route('/users', methods=['GET'])
def get_users():
    users = read_users_from_csv()
    user_dicts = [user.to_dict() for user in users]
    return jsonify(user_dicts)

@app.route('/students', methods=['GET'])
def get_students():
    users = read_users_from_csv()
    user_dicts = [user.to_dict() for user in users if user.type=='student']
    return jsonify(user_dicts)

@app.route('/groups/<group_name>/users', methods=['GET'])
def get_users_by_group(group_name):
    users = []
    with open('users.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = row['id']
            user_name = row['name']
            user_last_name = row['last_name']
            with open('groups.csv', 'r') as groups_file:
                groups_reader = csv.DictReader(groups_file)
                for group_row in groups_reader:
                    if group_row['group_name'] == group_name and group_row['user_id'] == user_id:
                        users.append({'name': user_name, 'last_name': user_last_name})
                        break

    return jsonify(users)


@app.route('/lessons')
def get_lessons():
# http://localhost:5000/lessons?start_date=2022-01-03&end_date=2022-01-05&user_id=11
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    user_id = request.args.get('user_id')
    lessons = read_csv(LESSONS_FILE_PATH)
    users = read_csv(USERS_FILE_PATH)

    filtered_lessons = [lesson for lesson in lessons if lesson['date'] >= start_date and lesson['date'] <= end_date and lesson['user_id'] == user_id]
    teacher_name = next((user['name'] + ' ' + user['last_name'] for user in users if user['id'] == user_id), '')

    return jsonify(filtered_lessons)

@app.route('/grades/<int:student_id>')
def get_student_grades(student_id):
    # Open the CSV file and read in the rows
    users = pd.read_csv(USERS_FILE_PATH)
    grades = pd.read_csv(GRADES_FILE_PATH)
    STUDENT_ID = 11
    sub_user = users.loc[users['id'] == STUDENT_ID]
    sub_grades = grades.loc[grades['student_id'] == STUDENT_ID]
    ccc = pd.merge(sub_grades, users, left_on='teacher_id', right_on='id')
    ccc = ccc.reset_index()
    out = []
    for index, row in ccc.iterrows():
        out.append({'teacher': ' '.join([row['name'],row['last_name']]), 'grade': row['grade'], 'wage': row['wage'], 'subject': row['subject'], 'id': row['id_x']})
    return {'grades': out}

@app.route('/teacher_subjects/<int:user_id>')
def get_teacher_subjects(user_id):
    lessons = pd.read_csv(LESSONS_FILE_PATH)
    groups = pd.read_csv(GROUPS_FILE_PATH)
    USER_ID = 1
    sub_lessons = lessons.loc[lessons['user_id'] == USER_ID]
    ccc = pd.merge(sub_lessons, groups, left_on='group_name', right_on='group_name')
    c = ccc[['subject','group_name']].drop_duplicates().reset_index()
    out = c.groupby('subject')['group_name'].apply(list).to_dict()
    return {'subjects': out}

@app.route('/students_from_group/<group_name>')
def get_students_from_group(group_name):
    users = pd.read_csv(USERS_FILE_PATH)
    groups = pd.read_csv(GROUPS_FILE_PATH)
    GROUP_NAME = '1A'
    sub_groups = groups.loc[groups['group_name'] == GROUP_NAME]
    ccc = pd.merge(sub_groups, users, left_on='user_id', right_on='id')
    ccc = ccc.reset_index()

    out = []
    for index, row in ccc.iterrows():
        out.append({'student': ' '.join([row['name'],row['last_name']]), 'group_name': row['group_name'],
         'user_id': row['user_id'], 'id': row['id_x']})
    return {'students': out}


def get_next_id(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next_id = sum(1 for _ in reader)
    return next_id


@app.route('/grades', methods=['POST'])
def add_grade():
    try:
        TEACHER_ID = 1
        data = request.get_json()
        student_id = data.get('studentId')
        wage = data.get('wage')
        grade = data.get('grade')
        subject = data.get('subject')
        if not student_id or not wage or not grade or not subject:
            return jsonify({'error': 'Missing required fields'}), 400
        next_id = get_next_id(GRADES_FILE_PATH)
        new_grade = [str(next_id), student_id, wage, TEACHER_ID, grade, subject]
        with open(GRADES_FILE_PATH, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_grade)
        return jsonify({'message': 'Grade added successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/homework', methods=['POST'])
def add_homework():
    try:
        TEACHER_ID = 1
        data = request.get_json()
        print(data)
        student_id = data.get('studentId')
        lesson_number = data.get('lesson_number')
        is_to_upload = data.get('is_to_upload')
        deadline_date = data.get('deadline_date')
        summary = data.get('summary')
        subject = data.get('subject')
        if not student_id or not summary or not subject or not subject:
            return jsonify({'error': 'Missing required fields'}), 400
        next_id = get_next_id(HOMEWORK_FILE_PATH)
        new_homework = [str(next_id), subject,lesson_number,summary,TEACHER_ID,student_id,0,int(is_to_upload),'None','None',deadline_date]
        print(new_homework)
        with open(HOMEWORK_FILE_PATH, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_homework)
        return jsonify({'message': 'Homework added successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/grades_avg/<int:student_id>')
def get_student_grades_average(student_id):
    # Open the CSV file and read in the rows
    users = pd.read_csv(USERS_FILE_PATH)
    grades = pd.read_csv(GRADES_FILE_PATH)
    STUDENT_ID = 11
    sub_user = users.loc[users['id'] == STUDENT_ID]
    sub_grades = grades.loc[grades['student_id'] == STUDENT_ID]
    ccc = pd.merge(sub_grades, users, left_on='teacher_id', right_on='id')
    ccc = ccc.reset_index()

    def weighted_avg(group):
        weights = group['wage']
        grades = group['grade']
        return (weights * grades).sum() / weights.sum()

    result = ccc.groupby('subject').apply(weighted_avg).reset_index(name='weighted_avg')
    result = result.reset_index()
    out = []
    for index, row in result.iterrows():
        out.append({'avg': row['weighted_avg'], 'subject': row['subject'], 'id': row['index']})
    return {'grades_avg': out}

@app.route('/lessons/<int:student_id>')
def get_student_lessons(student_id):
    # Open the CSV file and read in the rows
    lessons = pd.read_csv(LESSONS_FILE_PATH)
    groups = pd.read_csv(GROUPS_FILE_PATH)
    STUDENT_ID = 11
    sub_user = groups.loc[groups['user_id'] == STUDENT_ID]
    sub_lessons = lessons.loc[lessons['group_name'] == sub_user['group_name'][0]]
    sub_lessons = sub_lessons.sort_values(by=['date','lesson_number'])
    sub_lessons = sub_lessons.reset_index()
    out = []
    for index, row in sub_lessons.iterrows():
        out.append({'id': row['id'], 'date': row['date'], 'lesson_number': row['lesson_number'], 'subject': row['subject']})
    return {'lessons': out}


@app.route('/homework/<int:student_id>')
def get_student_homework(student_id):
    homework = pd.read_csv(HOMEWORK_FILE_PATH)
    users = pd.read_csv(USERS_FILE_PATH)
    STUDENT_ID = 11
    sub_homework = homework.loc[homework['student_id'] == STUDENT_ID]
    ccc = pd.merge(sub_homework, users, left_on='teacher_id', right_on='id')
    ccc = ccc.reset_index()
    out = []
    for index, row in ccc.iterrows():
        out.append({'id': row['index'], 'subject': row['subject'], 'lesson_number': row['lesson_number'], 'summary': row['summary'],
        'is_done': row['is_done'], 'is_to_upload': row['is_to_upload'], 'deadline_date': row['deadline_date'], 'date_of_solution': row['date_of_solution'],
        'teacher': ' '.join([row['name'],row['last_name']])})

    return {'homework': out}

@app.route('/homework_teacher/<int:teacher_id>')
def get_teacher_homework(teacher_id):
    homework = pd.read_csv(HOMEWORK_FILE_PATH)
    TEACHER_ID = 1
    sub_homework = homework.loc[homework['teacher_id'] == TEACHER_ID]
    groups = pd.read_csv(GROUPS_FILE_PATH)
    ccc = pd.merge(sub_homework, groups, left_on='student_id', right_on='user_id')
    ccc = ccc.drop('user_id', axis=1)
    ccc = ccc.drop('id_x', axis=1)
    ccc = ccc.drop('id_y', axis=1)
    ccc = ccc.drop('student_id', axis=1).drop_duplicates()
    ccc = ccc.reset_index()
    out = []
    for index, row in ccc.iterrows():
        out.append({'id': row['index'], 'subject': row['subject'], 'lesson_number': row['lesson_number'], 'summary': row['summary'], 'group_name': row['group_name'],
        'deadline_date': row['deadline_date'], 'date_of_solution': row['date_of_solution']})
    return {'homework': out}

@app.route('/lessons_table/<int:student_id>')
def get_student_timetable(student_id):
    lessons = pd.read_csv(LESSONS_FILE_PATH)
    groups = pd.read_csv(GROUPS_FILE_PATH)
    STUDENT_ID = 11
    sub_user = groups.loc[groups['user_id'] == STUDENT_ID]
    sub_lessons = lessons.loc[lessons['group_name'] == sub_user['group_name'][0]]
    sub_lessons = sub_lessons.reset_index()
    c = sub_lessons
    c = c.sort_values(by=['lesson_number','date'])
    pivot_df = c.pivot_table(index='lesson_number', columns='date', values='subject', aggfunc='first', fill_value='')
    result = pivot_df.to_json(orient="index")
    parsed = loads(result)
    dumps(parsed, indent=4)

    return {'timetable': parsed}

@app.route('/teacher_lessons_table/<int:user_id>')
def get_teacher_timetable(user_id):
    lessons = pd.read_csv(LESSONS_FILE_PATH)
    groups = pd.read_csv(GROUPS_FILE_PATH)
    USER_ID = 1
    sub_lessons = lessons.loc[lessons['user_id'] == USER_ID]
    ccc = pd.merge(sub_lessons, groups, left_on='group_name', right_on='group_name')
    ccc = ccc.reset_index()
    c = ccc
    c = c.sort_values(by=['lesson_number','date'])
    c['group_name_subject'] = c.apply(lambda row: row['group_name'] + ' - ' + row['subject'], axis=1)
    pivot_df = c.pivot_table(index='lesson_number', columns='date', values='group_name_subject', aggfunc='first', fill_value='')
    result = pivot_df.to_json(orient="index")
    parsed = loads(result)
    dumps(parsed, indent=4)
    return {'timetable': parsed}

@app.route('/lessons_hours')
def get_lessons_hours():
    mapped = pd.read_csv(HOURS_FILE_PATH)
    array = mapped.to_numpy().tolist()
    print(array)
    return {'hours': array}

@app.route('/user_info',methods=['GET'])
def user_info():
    users_retrieved = pd.read_csv(USERS_FILE_PATH)
    email = request.args.get('email')
    user_info = {}
    print(email)
    
    for index, user in users_retrieved.iterrows():
        if user["email"] == email:
            user_info["last_name"] = user["last_name"]
            user_info["name"] = user["name"]
            user_info["type"] = user["type"]
            
            return user_info
        
    return jsonify(result ='not found')


@app.route('/grades/<group>/<subject>', methods=['GET'])
def get_grades(group, subject):
    grades_data = pd.read_csv(GRADES_FILE_PATH)
    groups_data = pd.read_csv(GROUPS_FILE_PATH)

    joined_data = pd.merge(grades_data, groups_data, left_on='student_id', right_on='user_id')
    filtered_grades = joined_data.loc[(joined_data['subject'] == subject) & (joined_data['group_name'] == group)]
    filtered_grades = filtered_grades[['student_id', 'wage', 'grade']].to_dict('records')
    return jsonify({'grades': filtered_grades})

@app.route('/messages/<int:student_id>')
def get_user_messages(student_id):
        # Open the CSV file and read in the rows
    users = pd.read_csv(USERS_FILE_PATH)
    messages = pd.read_csv(MESSAGES_FILE_PATH)
    STUDENT_ID = 11
    sub_mess = messages.loc[messages['from_user_id'] == STUDENT_ID]
    sub_mess2 = messages.loc[messages['to_user_id'] == STUDENT_ID]

    ccc = pd.merge(sub_mess, users, left_on='to_user_id', right_on='id')
    ccc = ccc.reset_index()

    ccc2 = pd.merge(sub_mess2, users, left_on='from_user_id', right_on='id')
    ccc2 = ccc2.reset_index()

    out1 = []
    out2 = []

    for index, row in ccc.iterrows():
        out1.append({'id': row['index'], 'date': row['date_sent'], 'from': ' '.join([row['name'],row['last_name']]), 'title': row['title'], 'message': row['message']})

    for index, row in ccc2.iterrows():
        out2.append({'id': row['index'], 'date': row['date_sent'], 'from': ' '.join([row['name'],row['last_name']]), 'title': row['title'], 'message': row['message']})


    return {'received': out2, 'sent': out1}

    

if __name__ == '__main__':
    app.run(debug=True)
