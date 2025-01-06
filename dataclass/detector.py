from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class YoutubeSponsorshipDetector():
    """YoutubeSponsorshipDetector crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def sponsorship_detector(self) -> Agent:
        return Agent(
            config=self.agents_config['sponsorship_detector'],
            verbose=True, 
        )
    
    @task
    def sponsorship_detecting_task(self) -> Task:
        return Task(
            config=self.tasks_config['sponsorship_detecting_task'],
            verbose=True
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  
            tasks=self.tasks,    
            process=Process.sequential,
            verbose=True,
        )