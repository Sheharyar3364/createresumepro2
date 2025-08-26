from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SelectField, FloatField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    referral_code = StringField('Referral Code (Optional)', validators=[Optional()])

class OrderForm(FlaskForm):
    # Personal Information
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional()])
    
    # Job Information
    target_position = StringField('Target Position', validators=[DataRequired()])
    industry = SelectField('Industry', choices=[
        ('', 'Select Industry'),
        ('technology', 'Technology'),
        ('healthcare', 'Healthcare'),
        ('finance', 'Finance'),
        ('education', 'Education'),
        ('marketing', 'Marketing'),
        ('sales', 'Sales'),
        ('engineering', 'Engineering'),
        ('consulting', 'Consulting'),
        ('retail', 'Retail'),
        ('manufacturing', 'Manufacturing'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    
    experience_level = SelectField('Experience Level', choices=[
        ('', 'Select Experience Level'),
        ('entry', 'Entry Level (0-2 years)'),
        ('mid', 'Mid Level (3-5 years)'),
        ('senior', 'Senior Level (6-10 years)'),
        ('executive', 'Executive Level (10+ years)')
    ], validators=[DataRequired()])
    
    special_requirements = TextAreaField('Special Requirements or Notes', validators=[Optional()])
    
    # File Uploads
    resume_file = FileField('Current Resume (Optional)', 
                          validators=[FileAllowed(['pdf', 'doc', 'docx'], 'Only PDF and Word documents are allowed!')])
    cover_letter_file = FileField('Current Cover Letter (Optional)', 
                                validators=[FileAllowed(['pdf', 'doc', 'docx'], 'Only PDF and Word documents are allowed!')])
    job_description_file = FileField('Job Description (Optional)', 
                                   validators=[FileAllowed(['pdf', 'doc', 'docx', 'txt'], 'Only PDF, Word, and text documents are allowed!')])
    
    # Service and Pricing
    service_type = HiddenField('Service Type')
    referral_code = StringField('Referral Code (Optional)', validators=[Optional()])

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])

class AdminOrderUpdateForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('delivered', 'Delivered')
    ], validators=[DataRequired()])
    
    completed_resume = FileField('Upload Completed Resume', 
                               validators=[FileAllowed(['pdf', 'doc', 'docx'], 'Only PDF and Word documents are allowed!')])
    completed_cover_letter = FileField('Upload Completed Cover Letter', 
                                     validators=[FileAllowed(['pdf', 'doc', 'docx'], 'Only PDF and Word documents are allowed!')])
