from flask_wtf import FlaskForm
<<<<<<< HEAD
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
=======
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SelectField, IntegerField, HiddenField, PasswordField, SubmitField, FloatField, DateTimeField, BooleanField
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

# Enhanced Forms for New Features
class TestimonialForm(FlaskForm):
    customer_name = StringField('Customer Name', validators=[DataRequired(), Length(min=2, max=100)])
    customer_title = StringField('Job Title', validators=[Optional(), Length(max=100)])
    customer_company = StringField('Company', validators=[Optional(), Length(max=100)])
    rating = SelectField('Rating', choices=[(5, '5 Stars'), (4, '4 Stars'), (3, '3 Stars'), (2, '2 Stars'), (1, '1 Star')], coerce=int, validators=[DataRequired()])
    testimonial_text = TextAreaField('Testimonial', validators=[DataRequired(), Length(min=20, max=1000)], widget=TextArea(), render_kw={"rows": 4})
    industry = StringField('Industry', validators=[Optional(), Length(max=100)])
    service_used = StringField('Service Used', validators=[Optional(), Length(max=100)])
    customer_photo = FileField('Customer Photo (Optional)', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPG and PNG images allowed')])
    featured = BooleanField('Featured Testimonial')
    approved = BooleanField('Approved for Display')
    submit = SubmitField('Save Testimonial')

class FAQForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired(), Length(min=10, max=500)])
    answer = TextAreaField('Answer', validators=[DataRequired(), Length(min=20, max=2000)], widget=TextArea(), render_kw={"rows": 5})
    category = SelectField('Category', choices=[('general', 'General'), ('pricing', 'Pricing'), ('process', 'Process'), ('delivery', 'Delivery'), ('revisions', 'Revisions')], validators=[DataRequired()])
    order_index = IntegerField('Display Order', validators=[Optional(), NumberRange(min=0)], default=0)
    active = BooleanField('Active', default=True)
    submit = SubmitField('Save FAQ')

class DiscountCodeForm(FlaskForm):
    code = StringField('Discount Code', validators=[DataRequired(), Length(min=3, max=50)])
    description = StringField('Description', validators=[Optional(), Length(max=200)])
    discount_type = SelectField('Discount Type', choices=[('percentage', 'Percentage'), ('fixed', 'Fixed Amount')], validators=[DataRequired()])
    discount_value = FloatField('Discount Value', validators=[DataRequired(), NumberRange(min=0)])
    minimum_order = FloatField('Minimum Order Amount', validators=[Optional(), NumberRange(min=0)], default=0)
    maximum_uses = IntegerField('Maximum Uses (Optional)', validators=[Optional(), NumberRange(min=1)])
    active = BooleanField('Active', default=True)
    submit = SubmitField('Save Discount Code')

class ReferralForm(FlaskForm):
    referrer_name = StringField('Your Name', validators=[DataRequired(), Length(min=2, max=100)])
    referrer_email = StringField('Your Email', validators=[DataRequired(), Email()])
    referred_name = StringField('Friend\'s Name', validators=[DataRequired(), Length(min=2, max=100)])
    referred_email = StringField('Friend\'s Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Referral')

class NewsletterForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    name = StringField('Name (Optional)', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Subscribe')

class LiveChatForm(FlaskForm):
    customer_name = StringField('Your Name', validators=[Optional(), Length(max=100)])
    customer_email = StringField('Email (Optional)', validators=[Optional(), Email()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=5, max=500)], widget=TextArea(), render_kw={"rows": 3})
    submit = SubmitField('Send Message')

class AdminResponseForm(FlaskForm):
    admin_response = TextAreaField('Response', validators=[DataRequired(), Length(min=10, max=2000)], widget=TextArea(), render_kw={"rows": 4})
    priority = SelectField('Priority', choices=[('low', 'Low'), ('normal', 'Normal'), ('high', 'High'), ('urgent', 'Urgent')], default='normal')
    responded = BooleanField('Mark as Responded')
    submit = SubmitField('Send Response')

class DiscountApplicationForm(FlaskForm):
    discount_code = StringField('Discount Code', validators=[Optional(), Length(max=50)])
    submit = SubmitField('Apply Discount')
>>>>>>> ded7f2e4447248a018f7dd7d09de9c43eb09fa0d
