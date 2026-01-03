from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List
from .tools.push_tool import PushNotificationTool
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage

# ----------------------------
# Structured outputs (Pydantic)
# ----------------------------

class MarketDynamicsReport(BaseModel):
    industry: str
    sector: str
    geography: str
    time_horizon: str
    opportunity_zones: List[str] = Field(default_factory=list, description="List of opportunity zones / themes")
    risk_areas: List[str] = Field(default_factory=list, description="List of risks or vulnerabilities")
    timing_windows: Optional[str] = Field(None, description="Recommended timing or cadence")
    implications_for_target_definition: Optional[str] = Field(None, description="How market dynamics should shape ICP/TSS")

class HPTCriteria(BaseModel):
    industry: str
    sector: str
    icp_description: str = Field(description="Human-readable Ideal Customer Profile")
    qualification_criteria: Dict[str, str] = Field(default_factory=dict, description="Named criteria and short descriptions")
    scoring_weights: Dict[str, float] = Field(default_factory=dict, description="Weights for scoring prospects (0-1)")
    rationale: Optional[str] = Field(None, description="Rationale tying criteria to market analysis")

class Prospect(BaseModel):
    name: str
    domain: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    primary_industry: Optional[str] = None
    reason_matched: Optional[str] = None
    match_score: Optional[float] = None
    notes: Optional[str] = None

class ProspectList(BaseModel):
    industry: str
    sector: str
    prospects: List[Prospect] = Field(default_factory=list)


