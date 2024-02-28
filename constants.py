import os
from dotenv import load_dotenv
load_dotenv()

OPEN_AI_KEY = os.getenv("OPEN_AI_API")

AGENTS = {
    "MasterAgent": "Responsible for managing the other agents and providing the final output to the user",
    "TaskMinerAgent": "Responsible for mining useful necessary details from the user inputs",
    "ETAAgent": "Responsible for providing the estimated time to complete the task",
    "ComplianceAgent": "Responsible for ensuring that the inputs are compliant with the company's policies",
    "PayWallAgent": "Responsible for ensuring that the user has the required subscription to access the services",
}

KELLY = {
    "name": "Kelly",
    "role": "Executive Assistant",
    "skills":[
        "create google calendar events",
        "analyze google calendar events",
        "reschedule google calendar events",
        "Delete google calendar events",
        "Edit google calendar events",
        "Draft emails based on given information",
        "Read google calendar events",
        "Organize and modify meetings only on Google"
    ]
}

GARRY = {
    "name": "Garry",
    "role": "Graphics Designer",
    "skills":[
        "Create creatives for Instagram, Facebook, LinkedIn, WhatsApp and Twitter",
        "Create thumbnails for Youtube",
        "Create T-Shirt design",
        "Create Logos",
        "Create blog graphic",
        "Create graphic for email",
        "Create flyer",
        "Create ad creatives",
        "Create Infographics",
        "Create Bookcover",
        "Design presentation deck",
        "Remove background from images",
        "Create collage photos",
        "Image editing according to requirements",
        "Creat brochure",
        "Website landing page design",
        "Poster design",
        "Event invitation design",
        "Menu design",
        "Package design",
        "Product catalogue",
        "Create art and illustrations",
        "Sticker Design",
        "Stationary design",
        "Design Canva Template"
    ]
}

OLIVIA = {
    "name": "Olivia",
    "role": "Sales Development Representative",
    "skills":[
        "You can prospect stores and companies based on the requirements",
        "You can prospect leads based on the ideal customer profile or business requirements",
        "You will include tools and applications that user wants the comapnies must be using.",
        "You will help user find the email and contact details of People for prospecting."
    ]
}

JAKE = {
    "name": "Jake",
    "role": "Market Researcher",
    "skills":[
        "Perform any market research"
    ]
}