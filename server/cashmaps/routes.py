from cashmaps import queue, utils
from flask import render_template, request, current_app

"""
These register all the pages with Flask. They all point to the compiled
React file, and React Router takes care of routing to the right page.
A catchall wasn't working here, because it was also intercepting static files.
"""
@current_app.route('/')
def index():
    return render_template('static/index.html')

@current_app.route('/parser')
def parser():
    return render_template('static/index.html')

@current_app.route('/files')
def files():
    return render_template('static/index.html')

@current_app.route('/map')
def map():
    return render_template('static/index.html')

@current_app.route('/upload')
def upload():
    return render_template('static/index.html')

@current_app.route('/gallery')
def gallery():
    return render_template('static/index.html')

@current_app.route('/tools')
def tools():
    return render_template('static/index.html')





@current_app.route('/_clear_rq', methods=['POST'])
def clear_rq():
    """
    Removes all jobs from the Redis Queue. This is used for development:
    sometimes there will be stale jobs created by testing or debugging.
    Also removes temp files associated with these jobs.
    """
    queue.empty()
    # Any stale parsing jobs will have temp files associated with them,
    # remove those. This works because nothing but parsing jobs use the
    # temp file directory. If that changes, this will need to change.
    utils.remove_temp_files()
    return {}


@current_app.route('/_upload_photo', methods=['POST'])
def upload_photo():
    filepath = request.form.get('filepath')
    for i in range(0, len(request.files)):
        f = request.files.get(str(i))
        fullpath = os.path.join(os.path.join(current_app.config['UPLOAD_FOLDER_PHOTOS'], filepath), f.filename)
        os.makedirs(fullpath)
        print(fullpath)
    return {}


@current_app.after_request
def after_request(response):
    """
    A method called after every url request is processed. Disables caching
    if not a production build, so that changes to the pages are immediately
    seen.
    """
    if current_app.config['DEBUG']:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"

    return response
