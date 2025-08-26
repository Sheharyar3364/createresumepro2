from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SelectField, IntegerField, HiddenField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional
from wtforms.widgets import TextArea

class OrderForm(FlaskForm):
    # Customer Information
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    
    # Service Selection
    service_id = SelectField('Service Type', coerce=int, validators=[DataRequired()])
    service_tier = SelectField('Service Tier', 
                              choices=[('basic', 'Basic'), ('standard', 'Standard'), ('premium', 'Premium')],
                              validators=[DataRequired()])
    
    # Career Information
    current_position = StringField('Current Position', validators=[Optional(), Length(max=100)])
    target_position = StringField('Target Position', validators=[DataRequired(), Length(min=2, max=100)])
    industry = StringField('Industry', validators=[Optional(), Length(max=100)])
    experience_years = IntegerField('Years of Experience', validators=[Optional(), NumberRange(min=0, max=50)])
    career_goals = TextAreaField('Career Goals & Objectives', 
                                validators=[DataRequired(), Length(min=10, max=1000)],
                                widget=TextArea(),
                                render_kw={"rows": 4, "placeholder": "Describe your career goals and what you hope to achieve..."})
    special_requirements = TextAreaField('Special Requirements or Additional Information',
                                       validators=[Optional(), Length(max=1000)],
                                       widget=TextArea(),
                                       render_kw={"rows": 3, "placeholder": "Any special requirements, formatting preferences, or additional information..."})
    
    # File Uploads
    current_resume = FileField('Current Resume (Optional)',
                              validators=[Optional(), FileAllowed(['pdf', 'doc', 'docx'], 'Only PDF and DOC files allowed')])
    cover_letter = FileField('Current Cover Letter (Optional)',
                            validators=[Optional(), FileAllowed(['pdf', 'doc', 'docx'], 'Only PDF and DOC files allowed')])
    job_description = FileField('Target Job Description (Optional)',
                               validators=[Optional(), FileAllowed(['pdf', 'doc', 'docx', 'txt'], 'Only PDF, DOC, and TXT files allowed')])
    
    submit = SubmitField('Proceed to Payment')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[Optional(), Length(max=200)])
    message = TextAreaField('Message', 
                           validators=[DataRequired(), Length(min=10, max=1000)],
                           widget=TextArea(),
                           render_kw={"rows": 5, "placeholder": "Please describe your inquiry..."})
    submit = SubmitField('Send Message')

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class OrderStatusForm(FlaskForm):
    status = SelectField('Order Status',
                        choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), 
                                ('completed', 'Completed'), ('cancelled', 'Cancelled')],
                        validators=[DataRequired()])
    admin_notes = TextAreaField('Admin Notes',
                               validators=[Optional(), Length(max=1000)],
                               widget=TextArea(),
                               render_kw={"rows": 3})
    submit = SubmitField('Update Order')
