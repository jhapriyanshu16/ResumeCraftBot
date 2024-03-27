#importing libraries
import telebot
import json
from telebot import types
import google.generativeai as genai
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_JUSTIFY
import json
import os

#Telebot api token:
bot = telebot.TeleBot("REPLACE YOUR TOKEN HERE")
#Gemini API key:
genai.configure(api_key="REPLACE YOUR TOKEN HERE")


#Set up the gemini model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["Hi"]
  },
  {
    "role": "model",
    "parts": ["Hello! I'm happy to help you. How can I assist you today?"]
  },
  {
    "role": "user",
    "parts": ["how are you"]
  },
  {
    "role": "model",
    "parts": ["Hello! I'm happy to help you. How can I assist you today?"]
  },
  {
    "role": "user",
    "parts": ["hi"]
  },
  {
    "role": "model",
    "parts": ["Hello! I'm happy to help you. How can I assist you today?"]
  },
])




#Format of json file 
resume_data = {
    "education": [],
    "experience": [],
    "skills": [],
    "projects": [],
    "certification": [],
    "language": [],
    "basicdetails": []
}

#Formatting the pdf file and importing fonts for pdf using reportlab
PAGE_WIDTH, PAGE_HEIGHT = A4
FULL_COLUMN_WIDTH = (PAGE_WIDTH - 1 * inch)
GARAMOND_REGULAR_FONT_PATH = './res/fonts/EBGaramond-Regular.ttf'
GARAMOND_REGULAR = 'Garamond_Regular'

GARAMOND_BOLD_FONT_PATH = './res/fonts/EBGaramond-Bold.ttf'
GARAMOND_BOLD = 'Garamond_Bold'

GARAMOND_SEMIBOLD_FONT_PATH = './res/fonts/EBGaramond-SemiBold.ttf'
GARAMOND_SEMIBOLD = 'Garamond_Semibold'

pdfmetrics.registerFont(ttfonts.TTFont(GARAMOND_REGULAR, GARAMOND_REGULAR_FONT_PATH))
pdfmetrics.registerFont(ttfonts.TTFont(GARAMOND_BOLD, GARAMOND_BOLD_FONT_PATH))
pdfmetrics.registerFont(ttfonts.TTFont(GARAMOND_SEMIBOLD, GARAMOND_SEMIBOLD_FONT_PATH))

JOB_DETAILS_PARAGRAPH_STYLE = ParagraphStyle('job_details_paragraph', leftIndent=12, fontName = GARAMOND_REGULAR, fontSize = 12, leading = 14, alignment = TA_JUSTIFY)
NAME_PARAGRAPH_STYLE = ParagraphStyle('name_paragraph', fontName = GARAMOND_SEMIBOLD, fontSize=16)
CONTACT_PARAGRAPH_STYLE = ParagraphStyle('contact_paragraph', fontName = GARAMOND_REGULAR, fontSize=12)
SECTION_PARAGRAPH_STYLE = ParagraphStyle('section_paragraph', fontName = GARAMOND_SEMIBOLD, fontSize=13, textTransform = 'uppercase')
COMPANY_HEADING_PARAGRAPH_STYLE = ParagraphStyle('company_heading_paragraph', fontName = GARAMOND_SEMIBOLD, fontSize=13)
COMPANY_ROLE_PARAGRAPH_STYLE = ParagraphStyle('company_heading_paragraph', fontName = GARAMOND_SEMIBOLD, fontSize=11)
COMPANY_TITLE_PARAGRAPH_STYLE = ParagraphStyle('company_title_paragraph', fontName = GARAMOND_REGULAR, fontSize=12)
COMPANY_CERTIFICATION_PARAGRAPH_STYLE = ParagraphStyle('company_title_paragraph', fontName = GARAMOND_REGULAR, fontSize=10)
COMPANY_DURATION_PARAGRAPH_STYLE = ParagraphStyle('company_duration_paragraph', fontName = GARAMOND_SEMIBOLD, fontSize=13, alignment = TA_RIGHT)
COMPANY_LOCATION_PARAGRAPH_STYLE = ParagraphStyle('company_location_paragraph', fontName = GARAMOND_REGULAR, fontSize=12, alignment = TA_RIGHT)

#File path
OUTPUT_PDF_PATH = f"./resume.pdf"
JSON_PATH = "./resume_data.json"

#Prompt for ai review
with open(JSON_PATH, 'r') as file:
    # Read the contents of the file
    file_contents = file.read()

prompt= f'''ReviewResumeWithAI Prompt:

Task Description:

Your Telegram bot, equipped with the ReviewResumeWithAI feature, is designed to give users a detailed review of their resumes. The resume information is structured in a JSON format, containing sections for education, certification, experience, skills, languages, and projects. The review should encompass the following key aspects:

Overall Score: Assess the overall quality of the resume and assign a score out of 100, considering completeness, relevance, and presentation.
ATS Compatibility: Provide guidance on optimizing the resume for Applicant Tracking Systems (ATS) while maintaining readability and coherence.
Grammatical Errors: Identify and list any grammatical errors found within the resume content, providing necessary corrections.
Potential Rejection Factors: Highlight any potential mistakes or shortcomings in the resume that could lead to rejection by potential employers and offer actionable recommendations for improvement.
Key Skills/Requirements: Analyze the resume data to recommend 2-3 key skills or requirements that the user should emphasize based on their desired job role.
Tone Adjustment: Evaluate the tone of the resume content and suggest adjustments to make it more professional and aligned with the desired position.
Content Clarity and Coherence: Provide feedback on the clarity and coherence of the resume content, suggesting any areas that may require further elaboration or refinement.
User Input (Resume Content - JSON format):

{file_contents}


Prompt :

"Using the provided resume content structured in JSON format, conduct the following tasks:

i)Evaluate the overall quality of the resume and assign a score out of 100, considering completeness, relevance, and presentation.
ii)Evaluating the content in JSON file. Suggest user some improvement in the content of resume based on ATS.
iii)Identify,list and describe all grammatical errors found within the resume content, offering necessary corrections to improve clarity and professionalism.
iv)Highlight factors that could lead to rejection by potential employers based on the content of resume and point out and quote those errors.
v)Analyze the resume data to recommend 2-3 key skills or requirements that the user should emphasize based on their desired job role.
vi)Evaluate the tone of the resume content and propose adjustments to make it more professional and aligned with the desired position.
vii)Provide feedback on the clarity and coherence of the resume content, indicating any areas that may require further elaboration or refinement based on the content of resume.
viii)Please ensure that the feedback provided is detailed, actionable, and tailored to assist the user in optimizing their resume effectively for their desired job role."
ix) Provide Positive in negative of the resume through bullet points
x) Give descriptive summary of improvement that can be done on the resume

Note:
i)Avoid mentioning Gemini or the Telegram bot specifically in the prompt.
ii) avoid mentioning the json file provided
iii) Avoid using markdown as it is not supported in telegram use i) or numbers for listing
iv) Avoid suggesting using different fonts and icons as the resume structured is predefined as it is made using reportlab and user has no control over it.
v) Describe in detail and use the content in json file to give tailored and precise output

'''

#Setting padding and margin for pdf
def appendSectionTableStyle(table_styles, running_row_index):
    table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 5))
    table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 5))
    table_styles.append(('LINEBELOW', (0, running_row_index), (-1, running_row_index), 1, colors.black))

#Reportlab code to generate resume
def generate_resume(file_path, json_file_path):
    doc = SimpleDocTemplate(file_path, pagesize=A4, showBoundary=0, leftMargin = 0.5 * inch, rightMargin= 0.5 * inch, topMargin = 0.2 * inch, bottomMargin = 0.3 * inch, title = "Resume", author = "ResumeCraftBot")
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    #Fetching data from json file and storing in variable
    author = data['basicdetails'][0]['author']
    email =  data['basicdetails'][0]['email']
    address = data['basicdetails'][0]['address']
    phone = data['basicdetails'][0]['email']
    linkedinurl = data['basicdetails'][0]['linkedinurl']
    githuburl = data['basicdetails'][0]['githuburl']
    role = data['basicdetails'][0]['role']
    # data for the table
    table_data = []
    table_styles = []
    running_row_index = 0
    
    table_styles.append(('ALIGN', (0, 0), (0, -1), 'LEFT'))
    table_styles.append(('ALIGN', (1, 0), (1, -1), 'RIGHT'))
    table_styles.append(('LEFTPADDING', (0, 0), (-1, -1), 0))
    table_styles.append(('RIGHTPADDING', (0, 0), (-1, -1), 0))  
    table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 6))
    table_data.append([
        Paragraph(author, NAME_PARAGRAPH_STYLE)
    ])
    running_row_index += 1

    table_data.append([
        Paragraph(role, COMPANY_ROLE_PARAGRAPH_STYLE)
    ])
    running_row_index += 1

    table_data.append([
        Paragraph(f"{email} | {phone} | {linkedinurl}", CONTACT_PARAGRAPH_STYLE),

    ])
    table_data.append([
        Paragraph(f"{githuburl} | {address}", CONTACT_PARAGRAPH_STYLE),

    ])
    table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 1))
    running_row_index += 1

    
    
    # Append education heading
    table_data.append(
        [Paragraph("Education", SECTION_PARAGRAPH_STYLE)]
    )
    appendSectionTableStyle(table_styles, running_row_index)
    running_row_index += 1
    
    # Append education
    for education in data['education']:
        table_data.append([
            Paragraph(education['university'], COMPANY_HEADING_PARAGRAPH_STYLE),
            Paragraph(education['year'], COMPANY_DURATION_PARAGRAPH_STYLE),
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 5))
        running_row_index += 1

        table_data.append([
            Paragraph(education['degree'], COMPANY_TITLE_PARAGRAPH_STYLE),
            Paragraph(education['location'], COMPANY_LOCATION_PARAGRAPH_STYLE),
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        running_row_index += 1

    # Append projects heading
    table_data.append(
        [Paragraph("Projects", SECTION_PARAGRAPH_STYLE)]
    )
    appendSectionTableStyle(table_styles, running_row_index)
    running_row_index += 1

    #Append projects
    for project in data['projects']:
        table_data.append([
            Paragraph(f"<font face='Garamond_Semibold'>{project['title']}: </font>{project['description']} ( {project['link']} )", bulletText='•', style=JOB_DETAILS_PARAGRAPH_STYLE),
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 0))
        table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
        running_row_index += 1

    # Add Training/Internship heading
    table_data.append(
        [Paragraph("Training / Internship", SECTION_PARAGRAPH_STYLE)]
    )
    appendSectionTableStyle(table_styles, running_row_index)
    running_row_index += 1


    # Append Training/Intership
    for job_experience in data['experience']:
        table_data.append([
            Paragraph(job_experience['company'], COMPANY_HEADING_PARAGRAPH_STYLE),
            Paragraph(job_experience['duration'], COMPANY_DURATION_PARAGRAPH_STYLE),
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 5))
        running_row_index += 1

        table_data.append([
            Paragraph(job_experience['title'], COMPANY_TITLE_PARAGRAPH_STYLE),
            Paragraph(job_experience['location'], COMPANY_LOCATION_PARAGRAPH_STYLE),
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        running_row_index += 1

        for line in job_experience['description']:
            table_data.append([
                Paragraph(line, bulletText='•', style=JOB_DETAILS_PARAGRAPH_STYLE)
            ])
            table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
            table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 0))
            table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
            running_row_index += 1


    # Append skills heading
    table_data.append(
        [Paragraph("Skills", SECTION_PARAGRAPH_STYLE)]
    )
    appendSectionTableStyle(table_styles, running_row_index)
    running_row_index += 1

    # Append skills
    for skill in data['skills']:
        table_data.append([
            Paragraph(skill, bulletText='•', style=JOB_DETAILS_PARAGRAPH_STYLE)
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 0))
        table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
        running_row_index += 1
    
    table_style = TableStyle(table_styles)

    # Append certification heading
    table_data.append(
        [Paragraph("CERTIFICATION", SECTION_PARAGRAPH_STYLE)]
    )
    appendSectionTableStyle(table_styles, running_row_index)
    running_row_index += 1
    
    # Append certifications
    for certification in data['certification']:
        table_data.append([
            Paragraph(certification['certificatename'], COMPANY_HEADING_PARAGRAPH_STYLE),
            Paragraph(certification['year'], COMPANY_DURATION_PARAGRAPH_STYLE),
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 5))
        running_row_index += 1

        table_data.append([
            Paragraph(certification['certificatedetail'], COMPANY_CERTIFICATION_PARAGRAPH_STYLE)
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        running_row_index += 1


    # Append Languages heading
    table_data.append(
        [Paragraph("Language", SECTION_PARAGRAPH_STYLE)]
    )
    appendSectionTableStyle(table_styles, running_row_index)
    running_row_index += 1

    # Append Languages
    for language in data['language']:
        table_data.append([
            Paragraph(language, bulletText='•', style=JOB_DETAILS_PARAGRAPH_STYLE)
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 0))
        table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
        running_row_index += 1
    
    table_style = TableStyle(table_styles)

    # Create the table and apply the style
    table = Table(table_data, colWidths=[FULL_COLUMN_WIDTH * 0.7, FULL_COLUMN_WIDTH * 0.3], spaceBefore=0, spaceAfter=0)
    table.setStyle(table_style)

    # Add the table to the elements list
    elements = [table]

    # Build the PDF document
    doc.build(elements)

#Defining command handler for AI review of the resume
@bot.message_handler(commands=['aireviewresume'])
def send_welcome(message):
	bot.reply_to(message, "Reviewing Resume. Please wait...")
	convo.send_message(prompt)
	response = (convo.last.text)
	bot.reply_to(message,response)

# Defining command handler for generating the resume
@bot.message_handler(commands=['getresume'])
def handle_generate_resume(message):
    # Generate the resume using the provided data and JSON file path
    generate_resume(OUTPUT_PDF_PATH, JSON_PATH)
    
    # Send the generated PDF file
    with open(OUTPUT_PDF_PATH, 'rb') as pdf_file:
        bot.send_document(message.chat.id, pdf_file)
    bot.send_message(message.chat.id, "Please access your resume for download. Type /aireviewresume to have AI review it and offer feedback on improvements.")

@bot.message_handler(commands=['start'])
# Function to handle basic details input
def handle_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Welcome to the Resume Bot! Let's start with your basic details.")
    bot.send_message(chat_id, "Enter your name:")
    bot.register_next_step_handler(message, input_name)

def input_name(message):
    chat_id = message.chat.id
    author = message.text
    resume_data["basicdetails"].append({"author": author})
    bot.send_message(chat_id, "Enter your email:")
    bot.register_next_step_handler(message, input_email)  

def input_email(message):
    chat_id = message.chat.id
    email = message.text
    resume_data["basicdetails"][-1]["email"] = email
    bot.send_message(chat_id, "Enter your location (eg. Delhi, India):")
    bot.register_next_step_handler(message, input_address)  

def input_address(message):
    chat_id = message.chat.id
    address = message.text
    resume_data["basicdetails"][-1]["address"] = address
    bot.send_message(chat_id, "Enter your contact number:")
    bot.register_next_step_handler(message, input_contact)  

def input_contact(message):
    chat_id = message.chat.id
    phone = message.text
    resume_data["basicdetails"][-1]["phone"] = phone
    bot.send_message(chat_id, "Enter the link of your LinkedIn profile:")
    bot.register_next_step_handler(message, input_linkedin)  

def input_linkedin(message):
    chat_id = message.chat.id
    linkedinurl = message.text
    resume_data["basicdetails"][-1]["linkedinurl"] = linkedinurl
    bot.send_message(chat_id, "Enter the link of your Github profile:")
    bot.register_next_step_handler(message, input_github)  

def input_github(message):
    chat_id = message.chat.id
    githuburl = message.text
    resume_data["basicdetails"][-1]["githuburl"] = githuburl
    bot.send_message(chat_id, "Enter your desired Job title (eg. Associate Python Developer):")
    bot.register_next_step_handler(message, input_position)  

def input_position(message):
    chat_id = message.chat.id
    role = message.text
    resume_data["basicdetails"][-1]["role"] = role
    bot.send_message(chat_id, "Great ! Now Let's move to your Education details:")
    bot.send_message(chat_id, "Enter the name of highest level of education you have completed or are currently pursuing (eg. BTech Computer Science and Engineering) :")
    bot.register_next_step_handler(message, process_degree_step)  

def process_degree_step(message):
    chat_id = message.chat.id
    degree = message.text

    # Store degree in the resume_data dictionary
    resume_data["education"].append({"degree": degree})

    # Continue with the next input or finish
    bot.send_message(chat_id, "Enter your university:")
    bot.register_next_step_handler(message, process_university_step)

def process_university_step(message):
    chat_id = message.chat.id
    university = message.text

    # Store university in the resume_data dictionary
    resume_data["education"][-1]["university"] = university

    # Continue with the next input or finish
    bot.send_message(chat_id, "Enter the location (eg. Delhi, India):")
    bot.register_next_step_handler(message, process_location_step)

def process_location_step(message):
    chat_id = message.chat.id
    location = message.text

    # Store location in the resume_data dictionary
    resume_data["education"][-1]["location"] = location

    # Continue with the next input or finish
    bot.send_message(chat_id, "Enter the year (eg., August 2017 - July 2021):")
    bot.register_next_step_handler(message, process_year_step)

def process_year_step(message):
    chat_id = message.chat.id
    year = message.text

    # Store year in the resume_data dictionary
    resume_data["education"][-1]["year"] = year

    # Move to the experience section
    bot.send_message(chat_id, "Great! Now let's move on to your work experience.")
    bot.send_message(chat_id, "Enter your job title/position:")
    bot.register_next_step_handler(message, process_experience_title_step)

def process_experience_title_step(message):
    chat_id = message.chat.id
    title = message.text

    # Store job title in the resume_data dictionary
    resume_data["experience"].append({"title": title})

    # Continue with the next input or finish
    bot.send_message(chat_id, "Enter the company name:")
    bot.register_next_step_handler(message, process_experience_company_step)

def process_experience_company_step(message):
    chat_id = message.chat.id
    company = message.text

    # Store company name in the resume_data dictionary
    resume_data["experience"][-1]["company"] = company

    # Continue with the next input or finish
    bot.send_message(chat_id, "Enter the location: (if remote write Remote )")
    bot.register_next_step_handler(message, process_experience_location_step)

def process_experience_location_step(message):
    chat_id = message.chat.id
    location = message.text

    # Store location in the resume_data dictionary
    resume_data["experience"][-1]["location"] = location

    # Continue with the next input or finish
    bot.send_message(chat_id, "Enter the duration (e.g., July 2021 - Present):")
    bot.register_next_step_handler(message, process_experience_duration_step)

def process_experience_duration_step(message):
    chat_id = message.chat.id
    duration = message.text

    # Store duration in the resume_data dictionary
    resume_data["experience"][-1]["duration"] = duration

    # Continue with the next input or finish
    bot.send_message(chat_id, "Enter job description (press Send button after each line, type 'done' and send when finished):")
    bot.register_next_step_handler(message, process_experience_description_step)

def process_experience_description_step(message):
    chat_id = message.chat.id
    description = []

    bot.send_message(chat_id, "Great Job ! Enter next job description (keep pressing Send button after each line, type 'done' when finished):")

    def handle_description_input(msg):
        nonlocal description

        line = msg.text
        if line.lower() == 'done':
            # If the user types 'done', finish the input and proceed
            resume_data["experience"][-1]["description"] = description

            # Move to the next step
            bot.send_message(chat_id, "Great! Now let's move on to your skills.")
            bot.send_message(chat_id, "Enter your skills (press Send button after each skill, type 'done' when finished):")
            bot.register_next_step_handler(msg, process_skills_step)
        else:
            # If the user enters a line of description, add it to the list
            description.append(line)

            # Continue with the next line of input
            bot.register_next_step_handler(msg, handle_description_input)

    # Register the initial input handler
    bot.register_next_step_handler(message, handle_description_input)

def process_skills_step(message):
    chat_id = message.chat.id
    skills = []

    bot.send_message(chat_id, "Nice you have added one skill type to add more skills (press Send button after each skill, type 'done' when finished):")

    def handle_skills_input(msg):
        nonlocal skills

        skill = msg.text
        if skill.lower() == 'done':
            # If the user types 'done', finish the input and proceed
            resume_data["skills"] = skills

            # Move to the next step
            bot.send_message(chat_id, "Great! Now let's move on to your Languages Section.")
            bot.send_message(chat_id, "Enter the name of languages you know (press Send button after each language, type 'done' when finished):")
            bot.register_next_step_handler(msg, process_language_step)
        else:
            # If the user enters a skill, add it to the list
            skills.append(skill)

            # Continue with the next skill input
            bot.register_next_step_handler(msg, handle_skills_input)

    # Register the initial input handler
    bot.register_next_step_handler(message, handle_skills_input)

def process_language_step(message):
    chat_id = message.chat.id
    language = []

    bot.send_message(chat_id, "Good! Enter the name of other languages you know (press Send button after each language, type 'done' when finished):")

    def handle_language_input(msg):
        nonlocal language

        languages = msg.text
        if languages.lower() == 'done':
            # If the user types 'done', finish the input and proceed
            resume_data["language"] = language

            # Move to the next step
            bot.send_message(chat_id, "Great! Now let's move on to your Certificates.")
            bot.send_message(chat_id, "Enter your Certificates (press Send button after each Certificate, type 'done' when finished):")
            bot.register_next_step_handler(msg, handle_certificate_input)
        else:
            # If the user enters a languages, add it to the list
            language.append(languages)

            # Continue with the next language input
            bot.register_next_step_handler(msg, handle_language_input)

    # Register the initial input handler
    bot.register_next_step_handler(message, handle_language_input)


def handle_certificate_input(message):
    chat_id = message.chat.id

    if message.text.lower() == 'done':
        # If the user types 'done', finish the input and proceed
        # Move to the next step
        bot.send_message(chat_id, "Great! Now let's move on to your projects.")
        bot.send_message(chat_id, "Enter your projects (press Send button after each project, type 'done' when finished):")
        bot.register_next_step_handler(message, handle_projects_input)
    else:
        # If the user didn't type 'done', continue with the next lines of input
        title = message.text
        bot.send_message(chat_id, "Kindly provide the source of certification issuance (e.g., Coursera):")
        bot.register_next_step_handler(message, lambda m: handle_certificate_description_input(m, title))

def handle_certificate_description_input(message, title):
    chat_id = message.chat.id
    description = message.text

    bot.send_message(chat_id, "Please input the year of issuance for the certificate :")
    bot.register_next_step_handler(message, lambda m: handle_certificate_year_input(m, title, description))

def handle_certificate_year_input(message, title, description):
    chat_id = message.chat.id
    year = message.text

    # Store the certificate details in the resume_data dictionary
    resume_data["certification"].append({
        "certificatename": title,
        "certificatedetail": description,
        "year": year
    })

    # Continue with the next certificate or finish
    bot.send_message(chat_id, "Enter the next certificate or type 'done' to finish:")
    bot.register_next_step_handler(message, handle_certificate_input)


def handle_projects_input(message):
    chat_id = message.chat.id

    if message.text.lower() == 'done':
        # If the user types 'done', finish the input and proceed
        # Save the collected data to a JSON file
        with open('resume_data.json', 'w') as json_file:
            json.dump(resume_data, json_file, indent=4)

        # Send a confirmation message
        bot.send_message(chat_id, "Thank you! Your Resume is ready. Type /getresume to get your resume.")
    else:
        # If the user didn't type 'done', continue with the next lines of input
        title = message.text
        bot.send_message(chat_id, "Enter project description:")
        bot.register_next_step_handler(message, lambda m: handle_projects_description_input(m, title))

def handle_projects_description_input(message, title):
    chat_id = message.chat.id
    description = message.text

    bot.send_message(chat_id, "Enter project link:")
    bot.register_next_step_handler(message, lambda m: handle_projects_link_input(m, title, description))

def handle_projects_link_input(message, title, description):
    chat_id = message.chat.id
    link = message.text

    # Store the project details in the resume_data dictionary
    resume_data["projects"].append({
        "title": title,
        "description": description,
        "link": link
    })

    # Continue with the next project or finish
    bot.send_message(chat_id, "Enter the next project title or type 'done' to finish:")
    bot.register_next_step_handler(message, handle_projects_input)

    

# Start the bot polling
bot.polling()



