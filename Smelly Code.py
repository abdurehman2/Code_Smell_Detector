class Applicant:
    # Primitive Obsession (uses primitives for name, email, phone instead of creating dedicated classes)
    def __init__(self, name, age, email, phone, resume, cover_letter, linkedin):
        self.name = name
        self.age = age
        self.email = email
        self.phone = phone
        self.resume = resume
        self.cover_letter = cover_letter
        self.linkedin = linkedin

    def get_contact_details(self):
        return f"Email: {self.email}, Phone: {self.phone}, LinkedIn: {self.linkedin}"

class Job:
    def __init__(self, title, description, requirements, salary, location):
        self.title = title
        self.description = description
        self.requirements = requirements
        self.salary = salary
        self.location = location

    def get_job_details(self):
        return f"Job: {self.title}, Salary: ${self.salary}, Location: {self.location}"

class Interview:
    # Feature Envy (Excessive use of other class data, should be encapsulated within the Applicant and Job)
    def __init__(self, applicant, job, interview_time):
        self.applicant = applicant
        self.job = job
        self.interview_time = interview_time

    def schedule_interview(self):
        # Schedule an interview for the applicant (improper separation of concerns)
        print(f"Scheduling interview for {self.applicant.name} for the job {self.job.title}")
        print(f"Interview Time: {self.interview_time}")

class JobApplicationSystem:
    def __init__(self):
        self.applicants = []
        self.jobs = []
        self.interviews = []
    
    # Long Method (Still handling multiple tasks within a single method)
    def apply_for_job(self, name, age, job_title, experience, resume, email, phone, cover_letter, linkedin):
        print(f"Applying for {job_title}")
        if len(resume) == 0:
            print("Resume cannot be empty")
            return
        if age < 18:
            print("Applicant must be at least 18 years old")
            return
        if len(email) == 0 or "@" not in email:
            print("Invalid email")
            return
        
        # Adding applicant
        applicant = Applicant(name, age, email, phone, resume, cover_letter, linkedin)
        self.applicants.append(applicant)
        print(f"Applicant {name} successfully applied for {job_title}")

        # Hardcoded job matching (God Class handling job assignment instead of a separate handler)
        job = self.find_job(job_title)
        if job is None:
            print(f"No job found for {job_title}")
            return

        # Scheduling interview
        interview = Interview(applicant, job, "2024-10-01 10:00 AM")
        self.interviews.append(interview)
        interview.schedule_interview()

    # Duplicated Code (Still repeating similar code for job listings)
    def list_jobs(self, job_type=None):
        print("Listing Jobs:")
        for job in self.jobs:
            if job_type is None or job_type.lower() in job.title.lower():
                print(job.get_job_details())

    # God Class (Handles too many operations, including job search)
    def find_job(self, job_title):
        for job in self.jobs:
            if job.title == job_title:
                return job
        return None

    # Large Parameter List (Passes many parameters in apply_for_job)
    def add_job(self, title, description, requirements, salary, location):
        job = Job(title, description, requirements, salary, location)
        self.jobs.append(job)
        print(f"Job {title} added successfully.")

    # Duplicated Code (Another example of duplicated listing logic)
    def list_software_jobs(self):
        print("Listing Software Jobs:")
        self.list_jobs(job_type="Software")

    def list_marketing_jobs(self):
        print("Listing Marketing Jobs:")
        self.list_jobs(job_type="Marketing")

    # Comment Abuser (Excessive comments that are unnecessary)
    def process_applications(self):
        # This method processes all applications in the system
        for applicant in self.applicants:
            # Check each applicant
            print(f"Processing application for {applicant.name}...")
            # Simple check for experience
            print(f"Verifying experience for {applicant.name}...")
            if len(applicant.resume) > 0:
                print(f"{applicant.name} has a valid resume.")
            else:
                print(f"{applicant.name} has an invalid resume.")
            
            # Complete processing
            print(f"Processing complete for {applicant.name}.\n")

# Usage example
system = JobApplicationSystem()

# Adding jobs
system.add_job("Software Engineer", "Develop software solutions", "3+ years experience", 80000, "Remote")
system.add_job("Marketing Manager", "Lead marketing campaigns", "5+ years experience", 70000, "New York")
system.add_job("Data Scientist", "Analyze data trends", "2+ years experience", 90000, "California")

# Applying for jobs
system.apply_for_job("Alice Smith", 25, "Software Engineer", 4, "Alice_Smith_Resume.pdf", "alice@example.com", "555-9876", "Cover letter content", "linkedin.com/alicesmith")
system.apply_for_job("Bob Johnson", 22, "Marketing Manager", 3, "Bob_Johnson_Resume.pdf", "bob@example.com", "555-1234", "Cover letter content", "linkedin.com/bobjohnson")

# Listing jobs
system.list_software_jobs()
system.list_marketing_jobs()

# Processing applications
system.process_applications()
