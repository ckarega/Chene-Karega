from flask import render_template, request, session, redirect, url_for, g
from app import app
from schedule_api import *
from map_api import *

class Misched:
    posts = []
    id = 0
    


app.secret_key = 'This is a secreajiofeoiew'


@app.route('/', methods=['GET', 'POST'])
def index():
    options = {}
    options['terms'] = get_terms()
    if request.method == 'POST':
            session['logged_in']= True
            session['username'] = request.form['username']
            options['logged_in'] = True

    else:
        session.pop('logged_in', None)
        session.pop('username', None)
        del Misched.posts[:]
    return render_template('index.html', **options)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['logged_in']= True
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html', **session)


@app.route('/logout')
def logout():

    session.pop('username', None)
    session.pop('logged_in', None)
    Misched.posts = []
    return redirect(url_for('index'))



@app.route('/<termcode>')
def school( termcode):
    options = {}
    options['schools'] = get_schools(termcode)
    options['classterms'] = termcode
    return render_template( 'schools.html', **options)


@app.route('/<termcode>/<subjectschool>')
def subjects(termcode, subjectschool):
    options = {}
    options['subjects'] = get_subjects(termcode,subjectschool)
    options['classterms'] = termcode
    options['classsubschool'] = subjectschool
    return render_template('subjects.html', **options)


@app.route('/<termcode>/<subjectschool>/<subject>')
def courses(termcode,subjectschool,subject):
    options = {}
    options['catalogs'] = get_catalog_numbers(termcode,subjectschool, subject)
    options['classterms'] = termcode
   
    options['classsubschool'] = subjectschool
    
    options['classsubject'] = subject
   
    return render_template ('courses.html', **options)


@app.route('/<termcode>/<subjectschool>/<subject>/<catalog>/<id>')
def coursedesc(termcode,subjectschool,subject,catalog,id):
    options = {}
    options['catalogs'] = get_catalog_numbers(termcode,subjectschool, subject)
    options['text'] = get_catalog_numbers(termcode,subjectschool, subject)

    Misched.id = int(id)


    options['courseinfo'] = get_course_description(termcode, subjectschool, subject,catalog)
    options['sections'] = get_sections(termcode, subjectschool, subject,catalog)

    options['classterms'] = termcode
    options['classsubschool'] = subjectschool
    options['classsubject'] = subject
    options['classcatalog'] = catalog
    return render_template('specificCourse.html', **options)


@app.route('/<termcode>/<subjectschool>/<subject>/<catalog>/<section>/<id>', methods=['GET', 'POST'])
def sections(termcode,subjectschool,subject,catalog, section,id):
    options = {}
    posts= []
    options['sections'] = get_sections(termcode, subjectschool, subject,catalog)
    options['catalogs'] = get_catalog_numbers(termcode,subjectschool, subject)
    
    
    if request.method == 'POST':

        if request.form['action'] == 'Select':
            if options['catalogs'][Misched.id]['CourseDescr'] and options['catalogs'][Misched.id]['CatalogNumber'] in Misched.posts:
                return redirect(url_for('backpack'))
            else:
                posts.append(options['catalogs'][Misched.id]['CourseDescr'])
                posts.append(options['catalogs'][Misched.id]['CatalogNumber'])
                posts.append(options['sections'][int(id)]['SectionType'])
                posts.append(options['sections'][int(id)]['SectionNumber'])
                posts.append(options['sections'][int(id)]['CreditHours'])
                Misched.posts.append(posts)
                return redirect(url_for('backpack'))
    
    options['sectDesc'] = get_section_details(termcode, subjectschool,subject,catalog,section)
    options['meetings'] = get_meetings(termcode, subjectschool, subject, catalog,section)
    options['textbooks'] = get_textbooks(termcode, subjectschool, subject, catalog,section)
    options['instructor'] = get_instructors(termcode, subjectschool, subject, catalog,section)
    options['classterms'] = termcode
    options['classlocation'] = get_building(termcode, subjectschool, subject, catalog,section)
   
    options['classsubschool'] = subjectschool
    options['classsubject'] = subject
    options['classcatalog'] = catalog
    options['classsection']= section
    return render_template('section.html', **options)



@app.route('/mibackpack',methods=['GET', 'POST'])
def backpack():
    options = {}

    options['catalogs'] = Misched.posts
    return render_template('backpack.html', **options)
    
@app.route('/<id>/mibackpack',methods=['GET', 'POST'])
def remove(id):
    options = {}
    
    if request.method == 'POST':
        
        if request.form['action'] == 'Remove':
            del Misched.posts[int(id)]
            return redirect(url_for('backpack'))
   
