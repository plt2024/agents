from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# Optional tools / memory imports (mirror stock_picker pattern).
from crewai_tools import SerperDevTool
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage


#
# Pydantic output models for each task in target_acquisition/config/tasks.yaml
#

class MarketDynamicsReport(BaseModel):
    """Structured analysis of market and industry dynamics"""
    summary: str = Field(description="Concise summary of market dynamics")
    opportunity_zones: List[str] = Field(description="Identifiable opportunity zones")
    risk_areas: List[str] = Field(description="Key risk areas")
    timing_windows: Optional[str] = Field(description="Timing windows and recommended timing")
    implications: Optional[str] = Field(description="Implications for target definition and strategy")
    raw_findings: Optional[Dict[str, Any]] = Field(description="Raw or structured findings")


class HPTCriteria(BaseModel):
    """Ideal customer profile and target selection standards"""
    icp_summary: str = Field(description="High-level Ideal Customer Profile summary")
    qualification_criteria: Dict[str, Any] = Field(description="Structured Target Selection Standards (TSS)")
    must_have_signals: List[str] = Field(description="Must-have signals for qualification")
    nice_to_have_signals: List[str] = Field(description="Nice-to-have signals")
    rationale: Optional[str] = Field(description="Rationale linking criteria to market dynamics")


class ProspectItem(BaseModel):
    name: str = Field(description="Prospect name / company")
    domain: Optional[str] = Field(description="Website or domain")
    industry: Optional[str] = Field(description="Industry classification")
    location: Optional[str] = Field(description="Geography / HQ")
    notes: Optional[str] = Field(description="Short identifying notes / why matched")


class ProspectList(BaseModel):
    prospects: List[ProspectItem] = Field(description="List of discovered prospect candidates")


class ProspectResearch(BaseModel):
    name: str = Field(description="Prospect name")
    decision_makers: List[str] = Field(description="Names / roles of key decision-makers")
    buying_signals: List[str] = Field(description="Observed buying signals")
    risks: List[str] = Field(description="Risks or red flags")
    engagement_indicators: List[str] = Field(description="Indications of engagement readiness")
    profile_summary: Optional[str] = Field(description="Concise intelligence profile summary")
    raw_data: Optional[Dict[str, Any]] = Field(description="Raw research artifacts")


class ProspectResearchList(BaseModel):
    research: List[ProspectResearch] = Field(description="Comprehensive intelligence profiles")


class HPTEntry(BaseModel):
    name: str = Field(description="Prospect name")
    rank: int = Field(description="Rank (1 = highest)")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0")
    rationale: str = Field(description="Justification for ranking")


class HPTList(BaseModel):
    hpts: List[HPTEntry] = Field(description="Prioritized High-Payoff Target List")


class EngagementBrief(BaseModel):
    prospect: str = Field(description="Prospect name")
    recommended_approach: str = Field(description="Recommended engagement approach")
    key_messages: List[str] = Field(description="Key messages to use in outreach")
    handoff_materials: Optional[Dict[str, Any]] = Field(description="Assets or templates for handoff")


class EngagementBriefs(BaseModel):
    briefs: List[EngagementBrief] = Field(description="Engagement briefs for HPTs")


class AssessmentReport(BaseModel):
    metrics: Dict[str, Any] = Field(description="Performance metrics and KPIs")
    insights: str = Field(description="Observed insights about targeting effectiveness")
    recommendations: List[str] = Field(description="Recommended improvements and next steps")
    raw_evidence: Optional[Dict[str, Any]] = Field(description="Raw evidence or data used for assessment")


#
# Crew definition
#
@CrewBase
class TargetAcquisition:
    """Target Acquisition crew"""

    # point to config files (the crew framework will load these)
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    #
    # Agent definitions mapping to keys in agents.yaml
    #
    @agent
    def market_dynamics_agent(self) -> Agent:
        return Agent(config=self.agents_config['market_dynamics_agent'],
                     tools=[SerperDevTool()])

    @agent
    def hpt_definition_agent(self) -> Agent:
        return Agent(config=self.agents_config['hpt_definition_agent'])

    @agent
    def prospect_discovery_agent(self) -> Agent:
        return Agent(config=self.agents_config['prospect_discovery_agent'],
                     tools=[SerperDevTool()], memory=True)

    @agent
    def prospect_intelligence_agent(self) -> Agent:
        return Agent(config=self.agents_config['prospect_intelligence_agent'],
                     tools=[SerperDevTool()])

    @agent
    def hpt_prioritization_agent(self) -> Agent:
        return Agent(config=self.agents_config['hpt_prioritization_agent'])

    @agent
    def engagement_preparation_agent(self) -> Agent:
        return Agent(config=self.agents_config['engagement_preparation_agent'])

    @agent
    def assessment_agent(self) -> Agent:
        return Agent(config=self.agents_config['assessment_agent'])

    @agent
    def targeting_manager(self) -> Agent:
        # Manager can allow delegation and orchestration
        return Agent(config=self.agents_config['targeting_manager'],
                     allow_delegation=True)

    #
    # Task definitions mapping to keys in tasks.yaml
    #
    @task
    def analyze_market_dynamics(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_market_dynamics'],
            output_pydantic=MarketDynamicsReport,
        )

    @task
    def define_hpt_criteria(self) -> Task:
        return Task(
            config=self.tasks_config['define_hpt_criteria'],
            output_pydantic=HPTCriteria,
        )

    @task
    def discover_prospects(self) -> Task:
        return Task(
            config=self.tasks_config['discover_prospects'],
            output_pydantic=ProspectList,
        )

    @task
    def research_prospects(self) -> Task:
        return Task(
            config=self.tasks_config['research_prospects'],
            output_pydantic=ProspectResearchList,
        )

    @task
    def prioritize_hpts(self) -> Task:
        return Task(
            config=self.tasks_config['prioritize_hpts'],
            output_pydantic=HPTList,
        )

    @task
    def prepare_engagement(self) -> Task:
        return Task(
            config=self.tasks_config['prepare_engagement'],
            output_pydantic=EngagementBriefs,
        )

    @task
    def assess_targeting_effectiveness(self) -> Task:
        return Task(
            config=self.tasks_config['assess_targeting_effectiveness'],
            output_pydantic=AssessmentReport,
        )

    #
    # Crew factory
    #
    @crew
    def crew(self) -> Crew:
        """Create and return the Target Acquisition Crew instance"""

        manager = Agent(
            config=self.agents_config['targeting_manager'],
            allow_delegation=True
        )

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
            memory=True,
            # Long-term memory for persistent storage across sessions
            long_term_memory=LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path="./memory/long_term_memory_storage.db"
                )
            ),
            # Short-term memory for current context using RAG
            short_term_memory=ShortTermMemory(
                storage=RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {"model": "text-embedding-3-small"},
                    },
                    type="short_term",
                    path="./memory/"
                )
            ),
            # Entity memory for tracking key information about entities
            entity_memory=EntityMemory(
                storage=RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {"model": "text-embedding-3-small"},
                    },
                    type="short_term",
                    path="./memory/"
                )
            ),
        )
