from tracker.models import Challenge

challenges = [
    # Machine Learning & AI
    ("50 Days of ML", 50), ("60 Days of AI", 60), ("45 Days of Deep Learning", 45),
    ("20 Days of NLP", 20), ("14 Days of OpenCV", 14), ("30 Days of Computer Vision", 30),
    ("9 Days of TensorFlow", 9), ("12 Days of PyTorch", 12), ("15 Days of Scikit-Learn", 15),
    ("20 Days of Reinforcement Learning", 20), ("25 Days of AI Ethics", 25),
    
    # Programming Languages
    ("30 Days of JavaScript", 30), ("20 Days of Python", 20), ("10 Days of HTML", 10),
    ("15 Days of CSS", 15), ("30 Days of TypeScript", 30), ("25 Days of C++", 25),
    ("21 Days of Java", 21), ("14 Days of C#", 14), ("18 Days of Rust", 18),
    ("12 Days of Go", 12), ("16 Days of Kotlin", 16), ("22 Days of Swift", 22),
    
    # Frontend Development
    ("50 Days of Frontend", 50), ("7 Days of React", 7), ("20 Days of Vue.js", 20),
    ("15 Days of Svelte", 15), ("40 Days of Bootstrap", 40), ("10 Days of Tailwind CSS", 10),
    ("35 Days of Web Animation", 35), ("25 Days of UI/UX Design", 25),
    
    # Backend Development
    ("50 Days of Backend", 50), ("6 Days of Node.js", 6), ("25 Days of Express.js", 25),
    ("30 Days of Django", 30), ("20 Days of FastAPI", 20), ("12 Days of GraphQL", 12),
    ("14 Days of REST APIs", 14), ("21 Days of PostgreSQL", 21), ("18 Days of MongoDB", 18),
    
    # Cloud & DevOps
    ("30 Days of DevOps", 30), ("8 Days of Docker", 8), ("8 Days of Kubernetes", 8),
    ("7 Days of Terraform", 7), ("15 Days of AWS", 15), ("12 Days of Azure", 12),
    ("10 Days of Google Cloud", 10), ("14 Days of CI/CD", 14), ("9 Days of Ansible", 9),
    
    # Security & Blockchain
    ("20 Days of Cybersecurity", 20), ("15 Days of Ethical Hacking", 15),
    ("12 Days of Blockchain", 12), ("10 Days of Solidity", 10), ("8 Days of Smart Contracts", 8),
    
    # Databases
    ("12 Days of SQL", 12), ("21 Days of PostgreSQL", 21), ("18 Days of MongoDB", 18),
    ("9 Days of Redis", 9), ("7 Days of Firebase", 7),
    
    # Mobile Development
    ("15 Days of Flutter", 15), ("12 Days of React Native", 12), ("18 Days of Swift", 18),
    ("16 Days of Kotlin", 16),
    
    # Software Engineering Concepts
    ("25 Days of System Design", 25), ("30 Days of Data Structures", 30),
    ("25 Days of Algorithms", 25), ("15 Days of Design Patterns", 15),
    ("20 Days of Clean Code", 20), ("12 Days of OOP", 12),
    
    # Game Development
    ("20 Days of Unity", 20), ("18 Days of Unreal Engine", 18),
    ("10 Days of Game Physics", 10), ("15 Days of Game AI", 15),
    
    # Other Tech Skills
    ("15 Days of Figma", 15), ("12 Days of Adobe XD", 12), ("20 Days of Illustrator", 20),
    ("18 Days of Photoshop", 18), ("10 Days of Git & GitHub", 10),
    ("14 Days of Web Scraping", 14), ("7 Days of Web3", 7),
    ("8 Days of Raspberry Pi", 8), ("10 Days of Arduino", 10)
]

for name, total_days in challenges:
    Challenge.objects.get_or_create(name=name, total_days=total_days)

from tracker.models import FieldOfInterest

fields_of_interest = [
    "Artificial Intelligence", "Machine Learning", "Deep Learning",
    "Data Science", "Cybersecurity", "Cloud Computing", "Blockchain",
    "Internet of Things (IoT)", "Computer Vision", "Natural Language Processing",
    "Web Development", "Mobile App Development", "Game Development",
    "Database Management", "Software Engineering", "DevOps", "Embedded Systems",
    "UI/UX Design", "Frontend Development", "Backend Development",
    "Full Stack Development", "Ethical Hacking"
]


for field in fields_of_interest:
    FieldOfInterest.objects.get_or_create(name=field)