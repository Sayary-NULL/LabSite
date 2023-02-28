import json
import psycopg2

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def open_bd():
    conn = psycopg2.connect(dbname='postgres', user='postgres',
                            password='postgres', host='localhost')
    return conn, conn.cursor()


def index(request):
    return render(request, "index.html")


def assets(request, file: str):
    test_file = open(rf'C:\Users\shlia\PycharmProjects\LabSite\templates\assets\{file}', 'rb')
    response = HttpResponse(content=test_file)
    response['Content-Type'] = f'text/{ "css" if file.find("css") != -1 else "javascript"}'
    response['Content-Disposition'] = f'attachment; filename="%s.{ "css" if file.find("css") != -1 else "js"}"' \
                                      % 'whatever'
    return response


def test(request, test: int):
    print('test:', test)
    return JsonResponse({'test': test})


@csrf_exempt
def createStudent(request):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    print('create Student: ', body_data)
    # данные приведены тут только для того чтобы выложить их в git

    conn, cursor = open_bd()

    user_id = body_data['ID']
    cursor.execute("""SELECT count(1) FROM students WHERE id_student = %s""", (user_id, ))
    count_user = cursor.fetchone()
    if count_user != 0:
        return HttpResponseBadRequest('User exists')

    cursor.execute("SELECT id_type_education FROM type_education WHERE type_educ = %s", (body_data['Degree'], ))
    degree_id = cursor.fetchone()
    if degree_id:
        return HttpResponseBadRequest('Degree is not exists')

    degree_id = degree_id[0]

    cursor.execute("SELECT id_faculty FROM faculty WHERE name_fac = %s", (body_data['Faculty'],))
    faculty_id = cursor.fetchone()
    if faculty_id:
        return HttpResponseBadRequest('Faculty is not exists')

    faculty_id = faculty_id[0]

    sql = """
    INSEasdRT INTO id_student
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql,
                   (user_id, body_data['FullName'], user_id, body_data['Finished'], degree_id, faculty_id))

    conn.commit()

    return HttpResponse()


@csrf_exempt
def getStudents(request):
    conn, cursor = open_bd()

    sql = """
SELECT stud.fio, stud.number_stud, type_ed.type_educ, stud.end_education
FROM students stud LEFT JOIN type_education type_ed 
ON stud.id_type_education = type_ed.id_type_education"""

    cursor.execute(sql)

    students = []
    for stud in cursor.fetchall():
        _stud = {'FullName': stud[0], 'ID': stud[1], 'Degree': stud[2], 'Finished': stud[3]}
        students.append(_stud)

    return JsonResponse({'value': students})


@csrf_exempt
def getStudentInfoByStudentID(request, user_id: int):
    conn, cursor = open_bd()

    sql = """
        SELECT stud.fio, stud.number_stud, stud.year_add, type_ed.type_educ, fac.name, stud.end_education
    FROM students stud LEFT JOIN type_education type_ed 
    ON stud.id_type_education = type_ed.id_type_education 
    LEFT JOIN faculty fac ON stud.id_faculty = fac.id_faculty
    where stud.number_stud = %s"""

    cursor.execute(sql, (user_id, ))

    user_info = cursor.fetchone()
    if not user_info:
        return HttpResponseBadRequest('Usser not found')

    sql_works = """
    SELECT * 
from public.work LEFT JOIN public.scientific_supervisor sup 
ON work.id_scientific_supervisor = sup.id_scientific_visor
WHERE work.id_author = %s
    """

    cursor.execute(sql_works)
    works = []

    for work in cursor.fetchall():
        _work = {
            'Advisor': {
                'FullName': 'Имя',
                'Department': 'Матмод',
                'Degree': 'phd'
            },
            'Caption': 'Название',
            'Type': 'Курсовая',
            'Mark': 5
        }

    result = {
        'FullName': user_info[0],
        'ID': user_info[1],
        'Year': user_info[2],
        'Degree': user_info[3],
        'Faculty': user_info[4],
        'Finished': user_info[5],
        'Works': []
    }
    return JsonResponse({'value': result})

