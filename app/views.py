
from app import app
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory
import os
from app import app, db
from werkzeug.utils import secure_filename
from app.models import Property
from app.forms import PropertyForm


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/property/<propid>')
def get_image(propid):
    prop = db.session.execute(db.select(Property).filter_by(id=propid)).scalar()
    if prop is not None:
       return send_from_directory(os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER']), prop.image)
    else:
       return "Image Not Found."
    
@app.route('/properties/<propertyid>')
def get_property(propertyid):
        prop = db.session.execute(db.select(Property).filter_by(id=propertyid)).scalar()
        if prop is not None:
           return render_template('property.html', property = prop)
        return render_template('property.html')


@app.route('/properties')
def properties():
    properties = db.session.execute(db.select(Property)).scalars()
    #print(properties)
    return render_template('properties.html', properties = properties)

@app.route('/properties/create', methods=['POST', 'GET'])
def add_property():
    # Instantiate your form class
    form = PropertyForm()
    # Validate file upload on submit
    if request.method == 'POST':
       if form.validate_on_submit():
          title = form.title.data 
          description = form.description.data 
          bedrooms = form.bedrooms.data 
          bathrooms = form.bathrooms.data 
          price = form.price.data 
          type = form.type.data 
          location = form.location.data 
          photo = form.photo.data 
          filename = secure_filename(photo.filename)
          photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
          prop = Property(title=title,description=description,bedrooms=bedrooms,bathrooms=bathrooms,price=price,type=type,location=location,image=filename)
          db.session.add(prop)
          db.session.commit()
          flash('New Property Added', 'success')
          return redirect(url_for('home'))
       else:
          flash_errors(form)
    return render_template('form.html', form = form)

###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def get_uploaded_images():
    rootdir = os.getcwd()
    for subdir, dirs, files in os.walk(rootdir + '/uploads'):
        for file in files:
            print (os.path.join(subdir, file))
    return files[1:]

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


