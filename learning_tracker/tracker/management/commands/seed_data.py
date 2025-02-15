import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learning_tracker.settings')
django.setup()

from tracker.models import FieldOfInterest, Challenge

def seed_mappings():
    # Define fields of interest
    fields_of_interest = [
        "Artificial Intelligence", "Machine Learning", "Deep Learning",
        "Data Science", "Cybersecurity", "Cloud Computing", "Blockchain",
        "Internet of Things (IoT)", "Computer Vision", "Natural Language Processing",
        "Web Development", "Mobile App Development", "Game Development",
        "Database Management", "Software Engineering", "DevOps", "Embedded Systems",
        "UI/UX Design", "Frontend Development", "Backend Development",
        "Full Stack Development", "Ethical Hacking"
    ]

    # Create fields of interest and store them in a dictionary
    fields_of_interest_map = {}
    for field_name in fields_of_interest:
        field, _ = FieldOfInterest.objects.get_or_create(name=field_name)
        fields_of_interest_map[field_name] = field

    challenge_to_field_mapping = {
    # Machine Learning & AI
    "50 Days of ML": ["Machine Learning", "Artificial Intelligence"],
    "60 Days of AI": ["Artificial Intelligence"],
    "45 Days of Deep Learning": ["Deep Learning", "Machine Learning"],
    "20 Days of NLP": ["Natural Language Processing", "Machine Learning"],
    "14 Days of OpenCV": ["Computer Vision"],
    "30 Days of Computer Vision": ["Computer Vision"],
    "9 Days of TensorFlow": ["Machine Learning", "Deep Learning"],
    "12 Days of PyTorch": ["Machine Learning", "Deep Learning"],
    "15 Days of Scikit-Learn": ["Machine Learning"],
    "20 Days of Reinforcement Learning": ["Machine Learning", "Artificial Intelligence"],
    "25 Days of AI Ethics": ["Artificial Intelligence", "Ethics"],

    # Programming Languages
    "30 Days of JavaScript": ["Programming", "Web Development"],
    "20 Days of Python": ["Programming", "Scripting", "Backend Development"],
    "10 Days of HTML": ["Frontend Development", "Web Development"],
    "15 Days of CSS": ["Frontend Development", "Web Development"],
    "30 Days of TypeScript": ["Programming", "Web Development"],
    "25 Days of C++": ["Programming", "System Development"],
    "21 Days of Java": ["Programming", "Backend Development"],
    "14 Days of C#": ["Programming", "Game Development"],
    "18 Days of Rust": ["Programming", "System Development"],
    "12 Days of Go": ["Programming", "Backend Development"],
    "16 Days of Kotlin": ["Programming", "Mobile Development"],
    "22 Days of Swift": ["Programming", "Mobile Development"],

    # Frontend Development
    "50 Days of Frontend": ["Frontend Development", "Web Development"],
    "7 Days of React": ["Frontend Development", "Web Development"],
    "20 Days of Vue.js": ["Frontend Development", "Web Development"],
    "15 Days of Svelte": ["Frontend Development", "Web Development"],
    "40 Days of Bootstrap": ["Frontend Development", "Web Development"],
    "10 Days of Tailwind CSS": ["Frontend Development", "Web Development"],
    "35 Days of Web Animation": ["Frontend Development", "UI/UX Design"],
    "25 Days of UI/UX Design": ["UI/UX Design"],

    # Backend Development
    "50 Days of Backend": ["Backend Development", "Web Development"],
    "6 Days of Node.js": ["Backend Development", "Web Development"],
    "25 Days of Express.js": ["Backend Development", "Web Development"],
    "30 Days of Django": ["Backend Development", "Web Development"],
    "20 Days of FastAPI": ["Backend Development", "Web Development"],
    "12 Days of GraphQL": ["Backend Development", "Web Development"],
    "14 Days of REST APIs": ["Backend Development", "Web Development"],
    "21 Days of PostgreSQL": ["Databases", "Backend Development"],
    "18 Days of MongoDB": ["Databases", "Backend Development"],

    # Cloud & DevOps
    "30 Days of DevOps": ["Cloud Computing", "DevOps"],
    "8 Days of Docker": ["DevOps", "Containerization"],
    "8 Days of Kubernetes": ["DevOps", "Container Orchestration"],
    "7 Days of Terraform": ["DevOps", "Infrastructure as Code"],
    "15 Days of AWS": ["Cloud Computing", "AWS"],
    "12 Days of Azure": ["Cloud Computing", "Microsoft Azure"],
    "10 Days of Google Cloud": ["Cloud Computing", "Google Cloud"],
    "14 Days of CI/CD": ["DevOps", "Continuous Integration"],
    "9 Days of Ansible": ["DevOps", "Configuration Management"],

    # Security & Blockchain
    "20 Days of Cybersecurity": ["Cybersecurity"],
    "15 Days of Ethical Hacking": ["Cybersecurity"],
    "12 Days of Blockchain": ["Blockchain", "Decentralized Systems"],
    "10 Days of Solidity": ["Blockchain", "Smart Contracts"],
    "8 Days of Smart Contracts": ["Blockchain", "Decentralized Systems"],

    # Databases
    "12 Days of SQL": ["Databases"],
    "21 Days of PostgreSQL": ["Databases"],
    "18 Days of MongoDB": ["Databases"],
    "9 Days of Redis": ["Databases"],
    "7 Days of Firebase": ["Databases"],

    # Mobile Development
    "15 Days of Flutter": ["Mobile Development"],
    "12 Days of React Native": ["Mobile Development"],
    "18 Days of Swift": ["Mobile Development"],
    "16 Days of Kotlin": ["Mobile Development"],

    # Software Engineering Concepts
    "25 Days of System Design": ["Software Engineering", "System Design"],
    "30 Days of Data Structures": ["Software Engineering", "Data Structures"],
    "25 Days of Algorithms": ["Software Engineering", "Algorithms"],
    "15 Days of Design Patterns": ["Software Engineering", "Design Patterns"],
    "20 Days of Clean Code": ["Software Engineering", "Best Practices"],
    "12 Days of OOP": ["Software Engineering", "Object-Oriented Programming"],

    # Game Development
    "20 Days of Unity": ["Game Development"],
    "18 Days of Unreal Engine": ["Game Development"],
    "10 Days of Game Physics": ["Game Development"],
    "15 Days of Game AI": ["Game Development", "Artificial Intelligence"],

    # Other Tech Skills
    "15 Days of Figma": ["UI/UX Design", "Graphic Design"],
    "12 Days of Adobe XD": ["UI/UX Design", "Graphic Design"],
    "20 Days of Illustrator": ["Graphic Design"],
    "18 Days of Photoshop": ["Graphic Design"],
    "10 Days of Git & GitHub": ["Version Control"],
    "14 Days of Web Scraping": ["Web Scraping", "Data Science"],
    "7 Days of Web3": ["Blockchain", "Web Development"],
    "8 Days of Raspberry Pi": ["Embedded Systems", "IoT"],
    "10 Days of Arduino": ["Embedded Systems", "IoT"]
}


    # Map challenges to fields of interest
    for challenge_name, field_names in challenge_to_field_mapping.items():
        challenge, _ = Challenge.objects.get_or_create(name=challenge_name)
        for field_name in field_names:
            field = fields_of_interest_map.get(field_name)
            if field:
                challenge.fields_of_interest.add(field)

if __name__ == "__main__":
    seed_mappings()
    print("Mappings seeded successfully!")