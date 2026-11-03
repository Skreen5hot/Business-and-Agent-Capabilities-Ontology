"""Phase I-4: synthesize the Candidate Capability Catalog from the inventories.

Directed by the architect on 2026-11-03
(docs/decisions/2026-11-03-bulk-capability-synthesis-directed.md): the I-4
crosswalk and triage, expanded to derive candidate Business Capability types
from every permitted source record. This tool reads the committed inventories
of Phases I-1, I-2b and I-2c, never edits them, and writes four generated
files to docs/catalog/:

  bpo-act-types.yaml  BPO's act types at the I-1 pin, each with its genus and
                      outputs (IRIs only); written by --rebuild-acts
  candidates.yaml     the catalog: one record per candidate
  crosswalk.yaml      one row per source record, with its interpretation
  report.md           the counts and the quality findings

The method, in order (docs/catalog/README.md states it with its limits):

  1. extract    every entry of the five inventories, as a uniform record
  2. normalize  each label into a frame: an ability (verbs, an ability
                family) and an object phrase, folded to a key
  3. generate   a candidate per key that a designating record carries; a
                fine-grained record (PCF levels 4-5, a FIBF business
                capability) designates only when its key is already a
                candidate's or recurs under two parents
  4. crosswalk  every other record to the nearest ancestor that designates:
                a PCF process as realization evidence, a FIBF business
                capability as requirement evidence
  5. relate     broader/narrower from the source hierarchies and from object
                containment; overlaps and synonyms
  6. classify   by stated rules, each with its reason
  7. check      consistency and originality; a hard failure refuses to write

Nothing here is ontology. Candidate ids are inventory identifiers
("BCC-" and eight hex digits of the key's SHA-256), never IRIs; the tool
emits no class, property, subclass axiom or ratification, and the inventory
admission guard runs over every output (scope approval, amendment 4).

  python tools/catalog/synthesize.py                 # offline check
  python tools/catalog/synthesize.py --write         # regenerate the catalog
  python tools/catalog/synthesize.py --rebuild-acts  # re-read BPO's act types
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "inventory"))
import harvest_bpo as hb  # noqa: E402  (the pins, fetch and admission guard)

GENERATOR = "tools/catalog/synthesize.py"
OUT_DIR = "docs/catalog"
DECISION = "docs/decisions/2026-11-03-bulk-capability-synthesis-directed.md"
INVENTORY = "docs/sources/inventory"
INPUTS = {
    "bpo": INVENTORY + "/bpo-entries.yaml",
    "pcf": INVENTORY + "/pcf-7.4-entries.yaml",
    "brm": INVENTORY + "/feaf-brm-entries.yaml",
    "fibf": INVENTORY + "/fibf-entries.yaml",
    "fibf-bc": INVENTORY + "/fibf-business-capabilities.yaml",
}
ACTS = OUT_DIR + "/bpo-act-types.yaml"
CANDIDATES = OUT_DIR + "/candidates.yaml"
CROSSWALK = OUT_DIR + "/crosswalk.yaml"
REPORT = OUT_DIR + "/report.md"

BPO = "https://fandaws.com/ontology/bpo#"
CCO = "https://www.commoncoreontologies.org/"
#: Verified against vendor/cco/cco-bco-extract.ttl: "Organization" and
#: "Organization Capability".
ORGANIZATION = "cco:ont00001180"
ORGANIZATION_CAPABILITY = "cco:ont00000568"
#: CM-01, BPO Act Type: development acts need a recorded reason before they
#: enter a realization index (CAP-06).
DEVELOPMENT_GENERA = tuple(BPO + n for n in (
    "ActOfDevelopment", "ActOfImprovement",
    "ActOfOrganizationalEstablishment", "ActOfAcquisition"))
SOURCE_NAMES = {"bpo": "BPO", "pcf": "APQC PCF 7.4", "brm": "FEAF-II BRM 3.1",
                "fibf": "FIBF", "fibf-bc": "FIBF"}


class Refused(SystemExit):
    """A consistency failure: the catalog is not written."""


# ------------------------------------------------------------- lexicon
#
# The normalizer's linguistic resource. A verb maps to its nominal (used in
# names) and an ability family (used in keys and definitions). The families
# follow BPO's act genera where one fits, so a family is a hypothesis about
# the kind of act the capability is realized in, checked against the act
# types BPO actually asserts (report: family/genus agreement).

V = {
    "manage": ("management", "management"), "develop": ("development", "development"),
    "define": ("definition", "formulation"), "identify": ("identification", "identification"),
    "establish": ("establishment", "implementation"), "determine": ("determination", "analysis"),
    "monitor": ("monitoring", "monitoring"), "evaluate": ("evaluation", "analysis"),
    "assess": ("assessment", "analysis"), "asses": ("assessment", "analysis"),
    "create": ("creation", "development"), "analyze": ("analysis", "analysis"),
    "analyse": ("analysis", "analysis"), "process": ("processing", "administration"),
    "maintain": ("maintenance", "maintenance"), "plan": ("planning", "planning"),
    "review": ("review", "analysis"), "design": ("design", "design"),
    "execute": ("execution", "implementation"), "prepare": ("preparation", "formulation"),
    "implement": ("implementation", "implementation"), "report": ("reporting", "reporting"),
    "communicate": ("communication", "communication"),
    "understand": ("understanding", "analysis"), "measure": ("measurement", "monitoring"),
    "calculate": ("calculation", "analysis"), "select": ("selection", "selection"),
    "confirm": ("confirmation", "verification"), "track": ("tracking", "monitoring"),
    "receive": ("receipt", "administration"), "administer": ("administration", "administration"),
    "schedule": ("scheduling", "scheduling"), "validate": ("validation", "verification"),
    "prioritize": ("prioritization", "analysis"), "generate": ("generation", "development"),
    "record": ("recording", "data"), "deliver": ("delivery", "service"),
    "produce": ("production", "production"), "align": ("alignment", "coordination"),
    "refine": ("refinement", "improvement"), "collect": ("collection", "collection"),
    "negotiate": ("negotiation", "negotiation"), "solicit": ("solicitation", "acquisition"),
    "support": ("support", "service"), "respond": ("response", "resolution"),
    "derive": ("derivation", "analysis"), "collaborate": ("collaboration", "coordination"),
    "test": ("testing", "verification"), "approve": ("approval", "governance"),
    "resolve": ("resolution", "resolution"), "assign": ("assignment", "administration"),
    "build": ("building", "development"), "operate": ("operation", "management"),
    "obtain": ("acquisition", "acquisition"), "investigate": ("investigation", "resolution"),
    "ensure": ("assurance", "compliance"), "coordinate": ("coordination", "coordination"),
    "gather": ("gathering", "collection"), "optimize": ("optimization", "improvement"),
    "close": ("closing", "administration"), "reconcile": ("reconciliation", "accounting"),
    "post": ("posting", "accounting"), "audit": ("audit", "verification"),
    "capture": ("capture", "data"), "formulate": ("formulation", "formulation"),
    "document": ("documentation", "data"), "finalize": ("finalization", "administration"),
    "request": ("request", "administration"), "revise": ("revision", "improvement"),
    "match": ("matching", "verification"), "modify": ("modification", "improvement"),
    "model": ("modeling", "analysis"), "deploy": ("deployment", "deployment"),
    "forecast": ("forecasting", "forecasting"), "reward": ("reward", "remuneration"),
    "relocate": ("relocation", "transportation"), "triage": ("triage", "resolution"),
    "control": ("control", "management"), "promote": ("promotion", "promotion"),
    "verify": ("verification", "verification"), "secure": ("securing", "protection"),
    "accept": ("acceptance", "verification"), "update": ("updating", "maintenance"),
    "specify": ("specification", "formulation"), "apply": ("application", "implementation"),
    "train": ("training", "training"), "quantify": ("quantification", "analysis"),
    "acquire": ("acquisition", "acquisition"), "incorporate": ("incorporation", "implementation"),
    "handle": ("handling", "administration"), "order": ("ordering", "acquisition"),
    "research": ("research", "research"), "release": ("release", "deployment"),
    "set": ("setting", "formulation"), "initiate": ("initiation", "implementation"),
    "complete": ("completion", "administration"), "archive": ("archiving", "data"),
    "authorize": ("authorization", "governance"), "service": ("servicing", "service"),
    "notify": ("notification", "communication"), "screen": ("screening", "verification"),
    "liaise": ("liaison", "coordination"), "appraise": ("appraisal", "analysis"),
    "integrate": ("integration", "coordination"), "consolidate": ("consolidation", "accounting"),
    "correspond": ("correspondence", "communication"),
    "discuss": ("discussion", "communication"), "publish": ("publication", "communication"),
    "adjust": ("adjustment", "improvement"), "compile": ("compilation", "reporting"),
    "scope": ("scoping", "formulation"), "sustain": ("sustainment", "maintenance"),
    "survey": ("survey", "research"), "migrate": ("migration", "data"),
    "assemble": ("assembly", "production"), "adopt": ("adoption", "implementation"),
    "govern": ("governance", "governance"), "introduce": ("introduction", "deployment"),
    "retire": ("retirement", "disposition"), "eliminate": ("elimination", "improvement"),
    "install": ("installation", "deployment"), "market": ("marketing", "selling"),
    "predict": ("prediction", "forecasting"), "orchestrate": ("orchestration", "coordination"),
    "achieve": ("achievement", "implementation"), "de-duplicate": ("deduplication", "data"),
    "submit": ("submission", "administration"), "present": ("presentation", "communication"),
    "retrieve": ("retrieval", "data"), "terminate": ("termination", "disposition"),
    "procure": ("procurement", "acquisition"), "clarify": ("clarification", "communication"),
    "seek": ("seeking", "acquisition"), "certify": ("certification", "verification"),
    "distribute": ("distribution", "transportation"), "expedite": ("expediting", "scheduling"),
    "rerun": ("rerun", "implementation"), "automate": ("automation", "improvement"),
    "calibrate": ("calibration", "maintenance"), "translate": ("translation", "communication"),
    "return": ("return", "transportation"), "pick": ("picking", "transportation"),
    "enable": ("enablement", "service"), "make": ("making", "production"),
    "harvest": ("harvesting", "production"), "agree": ("agreement", "negotiation"),
    "route": ("routing", "transportation"), "register": ("registration", "administration"),
    "organize": ("organization", "coordination"), "recruit": ("recruitment", "staffing"),
    "source": ("sourcing", "acquisition"), "interview": ("interviewing", "selection"),
    "hire": ("hiring", "staffing"), "redeploy": ("redeployment", "staffing"),
    "transform": ("transformation", "improvement"), "outline": ("outlining", "formulation"),
    "facilitate": ("facilitation", "coordination"), "synthesize": ("synthesis", "analysis"),
    "articulate": ("articulation", "communication"), "access": ("access", "data"),
    "bundle": ("bundling", "development"), "balance": ("balancing", "planning"),
    "run": ("running", "management"), "escalate": ("escalation", "resolution"),
    "operationalize": ("operationalization", "implementation"),
    "invoice": ("invoicing", "transaction"), "transmit": ("transmission", "communication"),
    "pay": ("payment", "transaction"), "issue": ("issuance", "administration"),
    "protect": ("protection", "protection"), "enforce": ("enforcement", "compliance"),
    "comply": ("compliance", "compliance"), "inspect": ("inspection", "verification"),
    "store": ("storage", "maintenance"), "reinstate": ("reinstatement", "administration"),
    "inform": ("informing", "communication"), "educate": ("education", "training"),
    "oversee": ("oversight", "governance"), "estimate": ("estimation", "forecasting"),
    "budget": ("budgeting", "planning"), "allocate": ("allocation", "planning"),
    "prevent": ("prevention", "protection"), "detect": ("detection", "monitoring"),
    "mitigate": ("mitigation", "protection"), "recover": ("recovery", "resolution"),
    "restore": ("restoration", "resolution"), "benchmark": ("benchmarking", "analysis"),
    "engage": ("engagement", "relationship"), "upgrade": ("upgrade", "improvement"),
    "configure": ("configuration", "deployment"), "draw": ("drawing", "implementation"),
    "conduct": None, "perform": None, "undertake": None, "carry": None, "take": None,
    "provide": ("provision", "service"), "evaluated": ("evaluation", "analysis"),
    "obtaining": ("acquisition", "acquisition"), "distinguish": ("distinction", "analysis"),
    "cultivate": ("cultivation", "relationship"), "elicit": ("elicitation", "collection"),
    "convene": ("convening", "coordination"), "brief": ("briefing", "communication"),
    "advise": ("advice", "service"), "assist": ("assistance", "service"),
    "recommend": ("recommendation", "analysis"), "store,": ("storage", "maintenance"),
    "use": ("use", "implementation"), "employ": ("employment", "implementation"),
    "explore": ("exploration", "research"), "examine": ("examination", "analysis"),
    "establishes": ("establishment", "implementation"),
    "contact": ("contact", "communication"), "confer": ("conferral", "communication"),
    "anticipate": ("anticipation", "forecasting"),
    "drive": ("driving", "implementation"), "embed": ("embedding", "implementation"),
    "foster": ("fostering", "relationship"), "mature": ("maturation", "improvement"),
    "nurture": ("nurturing", "relationship"), "attract": ("attraction", "staffing"),
    "retain": ("retention", "staffing"), "onboard": ("onboarding", "staffing"),
    "evolve": ("evolution", "improvement"), "realize": ("realization", "implementation"),
    "outsource": ("outsourcing", "acquisition"), "purchase": ("purchasing", "acquisition"),
    "sell": ("selling", "selling"), "price": ("pricing", "analysis"),
    "fulfill": ("fulfillment", "service"), "ship": ("shipping", "transportation"),
    "repair": ("repair", "maintenance"),
    "dispose": ("disposal", "disposition"), "decommission": ("decommissioning", "disposition"),
    "construct": ("construction", "production"), "manufacture": ("manufacturing", "production"),
    "license": ("licensing", "administration"), "file": ("filing", "administration"),
    "settle": ("settlement", "transaction"), "remit": ("remittance", "transaction"),
    "disburse": ("disbursement", "transaction"), "bill": ("billing", "transaction"),
    "invest": ("investment", "transaction"), "hedge": ("hedging", "protection"),
    "insure": ("insurance", "protection"), "advocate": ("advocacy", "promotion"),
    "sponsor": ("sponsorship", "promotion"),
    "advertise": ("advertising", "promotion"),
    "segment": ("segmentation", "analysis"),
    "open": ("opening", "administration"), "enter": ("entry", "data"),
    "cancel": ("cancellation", "administration"), "unwind": ("unwinding", "transaction"),
    "remediate": ("remediation", "resolution"), "account": ("accounting", "accounting"),
    "address": ("addressing", "resolution"), "classify": ("classification", "analysis"),
    "change": ("change", "improvement"), "augment": ("augmentation", "improvement"),
    "renew": ("renewal", "maintenance"), "dismantle": ("dismantling", "disposition"),
    "recycle": ("recycling", "disposition"), "demolish": ("demolition", "disposition"),
    "recognize": ("recognition", "accounting"), "amend": ("amendment", "improvement"),
    "share": ("sharing", "communication"), "appoint": ("appointment", "staffing"),
    "extend": ("extension", "improvement"), "improve": ("improvement", "improvement"),
    "realign": ("realignment", "coordination"), "prove": ("proving", "verification"),
    "summarize": ("summary", "reporting"), "decide": ("decision", "selection"),
    "assure": ("assurance", "verification"), "transfer": ("transfer", "transportation"),
    "form": ("formation", "implementation"), "reengineer": ("reengineering", "improvement"),
    "leverage": ("leveraging", "implementation"), "enhance": ("enhancement", "improvement"),
    "expand": ("expansion", "development"), "compare": ("comparison", "analysis"),
    "search": ("search", "data"), "follow": ("following", "compliance"),
    "reject": ("rejection", "administration"), "aggregate": ("aggregation", "data"),
    "categorize": ("categorization", "analysis"), "add": ("addition", "data"),
    "keep": ("keeping", "data"), "obligate": ("obligation", "accounting"),
    "correlate": ("correlation", "analysis"), "authenticate": ("authentication", "verification"),
    "separate": ("separation", "administration"), "minimize": ("minimization", "improvement"),
    "place": ("placement", "administration"), "export": ("export", "data"),
    "convert": ("conversion", "data"), "sanitize": ("sanitization", "protection"),
    "scan": ("scanning", "monitoring"), "reset": ("reset", "maintenance"),
    "refresh": ("refresh", "maintenance"), "adapt": ("adaptation", "improvement"),
}
#: Words that are verbs and nouns alike: "and test" may continue an object.
AMBIGUOUS = {"test", "support", "control", "design", "plan", "forecast", "report",
             "model", "service", "order", "process", "record", "audit", "release",
             "request", "issue", "match", "return", "update", "survey", "research",
             "budget", "schedule", "document", "file", "bill", "price", "market",
             "source", "set", "use", "access", "post", "transfer", "review", "change",
             "account", "address", "form", "export", "search", "place", "share",
             "reset", "refresh", "scan", "add", "estimate", "draw", "store", "brand"}
ADVERBS = {"internally", "externally", "continuously", "regularly", "periodically",
           "effectively", "efficiently", "annually", "quarterly", "proactively",
           "accordingly", "appropriately", "consistently", "globally", "locally"}
#: A light verb carries no ability of its own: "Perform revenue accounting"
#: is revenue accounting.
LIGHT = {v for v, x in V.items() if x is None}

#: Trailing nominals of noun-phrase labels (FIBF, BRM, BPO class names).
N = {
    "management": "management", "administration": "administration",
    "admin": "administration", "mgmt": "management", "analysis": "analysis",
    "analytics": "analysis", "planning": "planning", "processing": "administration",
    "accounting": "accounting", "development": "development", "evaluation": "analysis",
    "assessment": "analysis", "review": "analysis", "appraisal": "analysis",
    "selection": "selection", "award": "administration", "closeout": "administration",
    "preparation": "formulation", "capture": "data", "creation": "development",
    "validation": "verification", "verification": "verification", "testing": "verification",
    "test": "verification", "retention": "data", "maintenance": "maintenance",
    "migration": "data", "disposal": "disposition", "transfer": "transportation",
    "governance": "governance", "scanning": "monitoring", "collection": "collection",
    "response": "resolution", "emulation": "verification", "exercise": "verification",
    "mitigation": "protection", "monitoring": "monitoring", "authentication": "verification",
    "federation": "coordination", "training": "training", "prevention": "protection",
    "promotion": "promotion", "protection": "protection", "enforcement": "compliance",
    "exploration": "research", "issuance": "administration", "tracking": "monitoring",
    "remediation": "resolution", "stewardship": "management", "exhibition": "service",
    "preservation": "protection", "assistance": "service", "education": "training",
    "production": "production", "transmission": "transportation", "control": "management",
    "support": "service", "service": "service", "relation": "relationship",
    "relationship": "relationship", "engagement": "relationship", "research": "research",
    "intelligence": "analysis", "forecasting": "forecasting", "procurement": "acquisition",
    "acquisition": "acquisition", "recruitment": "staffing", "hiring": "staffing",
    "onboarding": "staffing", "staffing": "staffing", "design": "design",
    "construction": "production", "engineering": "design", "inspection": "verification",
    "investigation": "resolution", "adjudication": "resolution", "litigation": "resolution",
    "oversight": "governance", "reporting": "reporting", "communication": "communication",
    "outreach": "communication", "coordination": "coordination",
    "integration": "coordination", "optimization": "improvement",
    "improvement": "improvement", "innovation": "development", "budgeting": "planning",
    "payment": "transaction", "billing": "transaction", "invoicing": "transaction",
    "reconciliation": "accounting", "audit": "verification", "auditing": "verification",
    "compliance": "compliance", "security": "protection", "safety": "protection",
    "delivery": "service", "fulfillment": "service", "scheduling": "scheduling",
    "dispatch": "scheduling", "registration": "administration", "licensing": "administration",
    "certification": "verification", "accreditation": "verification",
    "surveillance": "monitoring", "detection": "monitoring", "prioritization": "analysis",
    "categorization": "analysis", "classification": "analysis", "determination": "analysis",
    "negotiation": "negotiation", "discussion": "communication", "solicitation": "acquisition",
    "approval": "governance", "action": "implementation", "completion": "administration",
    "extension": "administration", "change": "improvement", "creation,": "development",
    "deployment": "deployment", "implementation": "implementation", "use": "implementation",
    "operation": "management", "provision": "service", "distribution": "transportation",
    "warehousing": "maintenance", "storage": "maintenance", "transportation": "transportation",
    "treatment": "service", "care": "service", "custody": "protection",
    "incarceration": "protection", "regulation": "compliance", "benchmarking": "analysis",
    "branding": "promotion", "marketing": "selling", "sale": "selling", "pricing": "analysis",
    "forecast": "forecasting", "deduplication": "data", "archiving": "data",
    "translation": "communication", "rollout": "deployment", "handling": "administration",
    "aid": "service", "benefit": "service", "insurance": "service", "lending": "transaction",
    "loan": "transaction", "grant": "transaction", "collection,": "collection",
    "evaluation,": "analysis", "deterrence": "protection", "interdiction": "protection",
    "defense": "protection", "response,": "resolution", "recovery": "resolution",
    "preparedness": "protection", "planning,": "planning",
}
#: Heads that name what an activity yields, not an ability. A noun phrase
#: ending in one gets the family the head implies and `action_inferred`.
ARTIFACT = {
    "strategy": "formulation", "plan": "formulation", "policy": "formulation",
    "procedure": "formulation", "package": "formulation", "document": "formulation",
    "estimate": "forecasting", "report": "reporting", "notification": "communication",
    "request": "administration", "record": "data", "hold": "administration",
    "context": "governance", "priority": "governance", "requirement": "formulation",
    "objective": "formulation", "outcome": "formulation", "eligibility": "analysis",
    "profile": "data", "catalog": "data", "inventory": "data",
}
#: An object these head nouns name is planned or defined, so "develop" or
#: "create" or "establish" it is formulation, not development.
PLAN_NOUNS = {
    "strategy", "plan", "policy", "procedure", "vision", "mission", "objective", "goal",
    "requirement", "budget", "roadmap", "standard", "guideline", "framework", "approach",
    "measure", "metric", "criterion", "criteria", "concept", "initiative", "model",
    "specification", "target", "case", "proposal", "position", "priority", "scope",
    "charter", "methodology", "taxonomy", "governance", "principle", "program",
    "agenda", "direction", "statement", "rule", "structure", "level", "planning",
    "design", "architecture", "idea", "activity",
}
#: Objects too general to pick out a type without their broader context.
GENERIC_OBJECTS = {"result", "performance", "information", "data", "issue", "requirement",
                   "need", "opportunity", "measure", "transaction", "plan", "strategy",
                   "program", "process", "policy and procedure", "risk", "change",
                   "initiative", "project", "report", "record", "case", "resource",
                   "activity", "solution", "service", "relationship", "stakeholder",
                   "scope", "objective", "goal", "budget", "cost", "metric"}
#: Heads that name an agent or a person's ability (CM-01: role, skill).
ROLE_HEADS = {"role", "officer", "steward", "champion", "representative", "liaison",
              "owner", "board", "committee", "team"}
SKILL_HEADS = {"skill", "competency", "competence", "proficiency", "literacy"}
#: Verbs whose act is one episode with a definite end.
BOUNDED_VERBS = {
    "approve", "issue", "submit", "receive", "notify", "close", "finalize", "post",
    "record", "request", "award", "calculate", "confirm", "match", "pay", "invoice",
    "transmit", "accept", "initiate", "complete", "release", "terminate", "return",
    "register", "reinstate", "assign", "pick", "route", "rerun", "relocate", "expedite",
}
BOUNDED_NOMINALS = {"award", "closeout", "approval", "completion", "issuance", "action",
                    "extension", "request", "notification", "hold", "eligibility"}
STOP = {"the", "a", "an", "its", "their", "all", "any", "new", "existing", "overall",
        "appropriate", "relevant", "necessary", "organization's", "organizations'",
        "organization", "company's", "enterprise's", "own", "various", "related",
        "applicable", "required", "specific", "key", "other", "current"}
TAIL_GENERIC = {"operation", "activity", "effort", "capability", "function", "area"}
ACRONYMS = {
    "IT": "information technology", "HR": "human resources",
    "EHS": "environmental health and safety", "HRIS": "human resources information system",
    "EQMS": "enterprise quality management system", "KM": "knowledge management",
    "SLA": "service level agreement", "SLAs": "service level agreements",
    "ERM": "enterprise risk management", "BPM": "business process management",
}
SYNONYMS = {"human capital": "human resource", "personnel": "employee", "staff": "employee",
            "client": "customer", "vendor": "supplier", "product and service": "product",
            "products and services": "product", "service and solution": "service",
            "services and solutions": "service"}
KEEP_PLURAL = {"sales", "goods", "logistics", "analytics", "ethics", "economics",
               "series", "status", "basis", "news", "means", "business", "process",
               "access", "address", "class", "loss", "gross", "its", "us", "as", "is",
               "this", "has", "was", "across", "less", "affairs", "arms", "assets'",
               "species", "chassis", "corps", "diagnosis", "operations'", "physics"}

#: Each family's ability phrase, for definitions. `{o}` is the object.
FAMILY = {
    "management": "direct and control {o} on a continuing basis",
    "development": "bring new {o} into being and make it ready for use",
    "formulation": "formulate, set out and keep current {o}",
    "identification": "identify and characterize {o}",
    "implementation": "put {o} into effect and carry it through",
    "analysis": "examine and assess {o} so as to inform decisions",
    "monitoring": "observe and measure {o} over time against expectations",
    "administration": "administer the recurring work of {o}",
    "maintenance": "keep {o} in a working, current and serviceable state",
    "planning": "plan {o} ahead of need",
    "design": "design {o} to stated requirements",
    "reporting": "compile and report on {o} to those who need it",
    "communication": "convey {o} to the intended audiences",
    "selection": "choose among alternatives for {o} against criteria",
    "verification": "check, test and confirm {o} against requirements",
    "scheduling": "schedule and sequence {o}",
    "data": "capture, keep and make available records of {o}",
    "service": "provide {o} to those it serves",
    "production": "produce {o}",
    "coordination": "coordinate {o} across the parties involved",
    "collection": "gather {o} from its sources",
    "negotiation": "negotiate {o} with other parties",
    "acquisition": "obtain {o} from suppliers or other sources",
    "resolution": "investigate and resolve {o}",
    "governance": "govern {o}, setting direction and holding to account",
    "improvement": "improve {o} against stated objectives",
    "compliance": "keep {o} in conformance with applicable obligations",
    "accounting": "account for {o}",
    "deployment": "deploy and introduce {o} into use",
    "transportation": "move and distribute {o}",
    "forecasting": "forecast {o}",
    "remuneration": "reward and remunerate {o}",
    "promotion": "promote {o}",
    "training": "train and develop {o}",
    "research": "research and investigate {o}",
    "protection": "protect {o} against harm, loss or misuse",
    "staffing": "attract, recruit and place {o}",
    "relationship": "build and sustain relationships with {o}",
    "selling": "market and sell {o}",
    "transaction": "carry out financial transactions for {o}",
    "disposition": "dispose of or retire {o}",
    "provision": "carry out {o}",
}
#: The BPO act genera each family expects, by local name, for the
#: family/genus agreement count. A hypothesis, reported, never enforced.
FAMILY_GENERA = {
    "formulation": {"act of formulation", "act of planning"},
    "planning": {"act of formulation", "act of planning", "act of scheduling"},
    "analysis": {"act of analysis", "act of identification", "act of appraisal",
                 "act of forecasting", "act of information processing", "act of measuring"},
    "identification": {"act of identification", "act of analysis"},
    "monitoring": {"act of monitoring", "act of verification", "act of measuring"},
    "accounting": {"act of accounting", "act of financial transaction"},
    "administration": {"act of administration", "act of data management",
                       "act of information processing"},
    "acquisition": {"act of acquisition", "act of selection"},
    "selling": {"act of selling"}, "service": {"act of service provision"},
    "reporting": {"act of reporting"},
    "data": {"act of data management", "act of information processing"},
    "transaction": {"act of financial transaction", "act of payment"},
    "scheduling": {"act of scheduling"},
    "verification": {"act of verification", "act of measuring", "act of appraisal"},
    "implementation": {"act of implementation", "act of deployment"},
    "deployment": {"act of deployment", "act of implementation"},
    "design": {"act of design"}, "development": {"act of development", "act of design"},
    "improvement": {"act of improvement"},
    "forecasting": {"act of forecasting", "act of prediction"},
    "selection": {"act of selection"}, "disposition": {"act of disposition"},
    "transportation": {"act of transportation", "act of cargo transportation",
                       "act of location change"},
    "resolution": {"act of resolution", "act of investigation"},
    "relationship": {"act of relationship management", "act of communication"},
    "negotiation": {"act of negotiation", "act of contract formation"},
    "communication": {"act of communication", "act of representative communication",
                      "act of mass media communication", "act of reporting"},
    "production": {"act of production", "act of construction"},
    "remuneration": {"act of remuneration"}, "training": {"act of training",
                                                          "act of training instruction"},
    "maintenance": {"act of maintenance", "act of artifact modification"},
    "management": {"act of administration", "act of monitoring", "act of process control"},
    "governance": {"act of administration", "act of formulation"},
}


#: Verbs whose act confers or exercises standing (CM-01: Authorization Record).
DEONTIC_VERBS = {"approve", "authorize", "certify", "accredit", "license", "grant",
                 "sign", "endorse", "ratify", "sanction", "delegate"}
DEONTIC = "deontic index member (G1-T question 4: re-index to the non-deontic act)"

#: Families whose acts span every genus (managing a thing includes planning,
#: appraising and monitoring it) and genera too general to agree or disagree
#: with anything: both are left out of the agreement count.
BROAD_FAMILIES = {"management", "governance", "provision"}
UNINFORMATIVE_GENERA = {"planned act", "organization capability"}


# ------------------------------------------------------------ utilities


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(data) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=88,
                          default_flow_style=False)


def text_of(value):
    """The text of an inventory field, or None if absent or withheld."""
    return value if isinstance(value, str) and value.strip() else None


def withheld(value) -> bool:
    return isinstance(value, dict) and "withheld" in value


def singular(word: str) -> str:
    if word in KEEP_PLURAL or len(word) <= 3 or not word.isalpha():
        return word
    if word.endswith("ies"):
        return word[:-3] + "y"
    if word.endswith(("sses", "xes", "ches", "shes")):
        return word[:-2]
    if word.endswith("s") and not word.endswith(("ss", "us", "is", "ics", "ws")):
        return word[:-1]
    return word


def camel_words(name: str) -> str:
    parts = re.findall(r"[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[A-Z]+|\d+", name)
    return " ".join(parts)


def tokens(text: str) -> list[str]:
    """Words, with acronyms expanded and punctuation that joins kept apart."""
    text = text.replace("�", "'").replace("’", "'").replace("‐", "-")
    text = re.sub(r"\([^)]*\)", " ", text)
    text = re.sub(r"(?i)\b(as|where|when|if) (needed|appropriate|required|applicable|"
                  r"necessary)\b", " ", text)
    text = text.replace("&", " and ").replace("/", " and ").replace("+", " and ")
    out = []
    for raw in re.findall(r"[A-Za-z][A-Za-z'\-]*|,", text):
        if raw in ACRONYMS:
            exp = ACRONYMS[raw].split()
            if [singular(w) for w in out[-len(exp):]] != [singular(w) for w in exp]:
                out.extend(exp)
        elif raw == ",":
            out.append(",")
        elif len(raw) >= 2 and raw.isupper():
            out.append(raw)
        elif raw.lower() not in ADVERBS:
            out.append(raw.lower().strip("'-"))
    return [t for t in out if t]


# ------------------------------------------------------------ framing


class Frame:
    """What a label says an organization does: verbs, a family, an object."""

    __slots__ = ("verbs", "family", "nominal", "object", "key", "inferred",
                 "bounded", "form")

    def __init__(self, verbs, family, nominal, obj, inferred, bounded, form):
        self.verbs = verbs
        self.family = family
        self.nominal = nominal
        self.object = obj
        self.inferred = inferred
        self.bounded = bounded
        self.form = form
        self.key = "%s|%s" % (family, object_key(obj)) if obj else None

    def as_dict(self) -> dict:
        return {"form": self.form, "verbs": list(self.verbs), "family": self.family,
                "object": self.object, "key": self.key,
                "action_inferred": self.inferred, "bounded": self.bounded}


def object_key(obj: str) -> str:
    words = [w for w in obj.lower().split() if w not in STOP]
    words = [singular(w) for w in words]
    while len(words) > 1 and words[-1] in TAIL_GENERIC:
        words.pop()
    while words and words[0] in ("and", "of", "for", "to", "with"):
        words.pop(0)
    while words and words[-1] in ("and", "of", "for", "to", "with"):
        words.pop()
    key = " ".join(words)
    for a, b in sorted(SYNONYMS.items(), key=lambda x: -len(x[0])):
        key = re.sub(r"\b%s\b" % re.escape(a), b, key)
    return key


def clean_object(words: list[str]) -> str:
    words = [w for w in words if w != ","]
    if len(words) > 1 and singular(words[-1]) == "capability" and words[-2] != "business":
        words = words[:-1]
    while words and words[0] in ("for", "and", "the", "of", "to", "with", "on", "in",
                                 "a", "an", "all", "any", "its", "their"):
        words.pop(0)
    while words and words[-1] in ("and", "of", "for", "the", "to", "with", "on", "in"):
        words.pop()
    return " ".join(words)


def relation_object(words: list[str]):
    """'relations with X' / 'X relationships' -> X, else None."""
    if not words:
        return None
    heads = {"relation", "relations", "relationship", "relationships"}
    for i, w in enumerate(words):
        if w in heads:
            after = words[i + 1:]
            if after and after[0] == "with":
                return clean_object(after[1:])
            if i == len(words) - 1:
                return clean_object(words[:i])
    return None


def imperative(words: list[str], form: str):
    """'Develop and manage X' -> verbs [develop, manage] and object X."""
    verbs, i, joined = [], 0, True
    while i < len(words):
        w = words[i]
        if w in V and joined:
            verbs.append(w)
            i += 1
            joined = False
            if i < len(words) and words[i] in ("out", "for", "on"):
                i += 1
            continue
        if w in ("and", ",", "or") and verbs and i + 1 < len(words) \
                and words[i + 1] in (V.keys() | {"and", ","}):
            i += 1
            joined = True
            continue
        break
    if not verbs:
        return None
    rest = words[i:]
    content = [v for v in verbs if v not in LIGHT]
    if content and not [w for w in rest if w != ","]:
        noms = [V[v][0] for v in content]
        return Frame(tuple(content), V[content[0]][1], None, " and ".join(noms), False,
                     False, form)
    if not content or (content == ["provide"] and nominal_frame(rest, form)):
        inner = nominal_frame(rest, form)
        if inner:
            return inner
        if not content:
            return None
    for k in range(1, len(rest) - 1):
        if rest[k] == "and" and rest[k + 1] in V and V[rest[k + 1]] \
                and rest[k + 1] not in AMBIGUOUS:
            rest = rest[:k]
            break
    rel = relation_object(rest)
    first = content[0]
    nominal, family = V[first]
    obj = clean_object(rest)
    if rel is not None:
        family, nominal, obj = "relationship", "relationship management", rel
    else:
        head = singular(obj.split()[-1]) if obj else ""
        if first in ("develop", "create", "establish", "build", "generate", "set") \
                and head in PLAN_NOUNS:
            family = "formulation"
        if first in ("establish", "build") and head not in PLAN_NOUNS and family != "formulation":
            family = "implementation"
    bounded = first in BOUNDED_VERBS and len(content) == 1
    return Frame(tuple(content), family, nominal, obj, False, bounded, form)


def nominal_frame(words: list[str], form: str):
    """'Records Disposal Approval' -> family of the trailing nominal."""
    words = [w for w in words if w != ","]
    if not words:
        return None
    rel = relation_object(words)
    if rel:
        return Frame(("manage",), "relationship", "relationship management", rel,
                     False, False, form)
    sing = [singular(w) for w in words]
    if len(sing) > 2 and sing[0] in N and words[1] == "of":
        return Frame((), N[sing[0]], words[0], clean_object(words[2:]), False,
                     sing[0] in BOUNDED_NOMINALS, form)
    if len(sing) == 1 and sing[0] in N:
        return Frame((), N[sing[0]], None, words[0], False, False, form)
    j = None
    for k in range(len(sing) - 1, -1, -1):
        if sing[k] in N and (k > 0 or len(sing) == 1):
            j = k
            break
        if k < len(sing) - 2:
            break
    if j is not None:
        start = j
        while start >= 2 and sing[start - 1] == "and" and sing[start - 2] in N:
            start -= 2
        obj = clean_object(words[:start])
        nominal = " ".join(words[start:j + 1])
        family = N[sing[start]]
        if not obj and start < j:
            run = [w for w in words[start:j + 1] if w != "and"]
            return Frame((), family, None, ", ".join(run[:-1]) + " and " + run[-1],
                         False, False, form)
        head = singular(obj.split()[-1]) if obj else ""
        if family == "development" and head in PLAN_NOUNS:
            family = "formulation"
        if not obj:
            return None
        return Frame((), family, nominal, obj, False, sing[j] in BOUNDED_NOMINALS, form)
    last = sing[-1]
    if last in ARTIFACT and len(words) > 1:
        return Frame((), ARTIFACT[last], None, clean_object(words), True,
                     last in BOUNDED_NOMINALS, form)
    return Frame((), "provision", None, clean_object(words), True, False, form)


def frame_label(label: str, form: str):
    """The frame of a label, or None if it yields no ability and object."""
    if not label:
        return None
    if " - " in label:
        left, right = label.split(" - ", 1)
        lt, rt = tokens(left), tokens(right)
        rf = imperative(rt, form) or nominal_frame(rt, form)
        if rf and not rf.inferred:
            return rf
        if len(lt) == 1 and lt[0] in V and V[lt[0]]:
            return imperative(lt + rt, form)
        return nominal_frame(lt, form) or rf
    words = tokens(label)
    if not words:
        return None
    return imperative(words, form) or nominal_frame(words, form)


def frame_sentence(text: str):
    """The leading clause of a FIBF business capability's description."""
    clause = re.split(r"[.;:]\s|\.$", text.strip(), maxsplit=1)[0]
    words = tokens(clause)
    if not words or words[0] not in V:
        return None
    cut = len(words)
    for i, w in enumerate(words):
        if i >= 1 and w in ("if", "whether", "that", "when", "where", "is", "are", "be",
                            "how", "what", "which", "who"):
            cut = i
            break
        if i > 1 and w in ("in", "to", "with", "for", "by", "consistent", "including",
                           "within", "from", "using", "as", "at", ",", "so", "prior",
                           "through", "via", "against", "into", "between", "under", "per",
                           "across", "upon", "after", "before", "during", "until",
                           "following", "and"):
            cut = i
            break
    if all(w in V or w in ("and", ",") for w in words[:cut]):
        return None      # "Determine if ...": the object is in the clause cut off
    f = imperative(words[:cut], "sentence")
    if f and f.object and len(f.object.split()) <= 6:
        return f
    return None


# ------------------------------------------------------------ extract


#: Parsing is the slow part; libyaml's parser gives the same data. Output is
#: always written by the pure-Python dumper, so its bytes do not depend on
#: whether libyaml is installed.
LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


def load_yaml(base: Path, rel: str):
    return yaml.load((base / rel).read_bytes().decode("utf-8"), Loader=LOADER)


def records(base: Path, docs: dict) -> list[dict]:
    """Every inventory entry, as a uniform record, in inventory order."""
    out = []
    pcf = docs["pcf"]["entries"]
    for e in pcf:
        out.append({
            "id": e["id"], "source": "pcf", "kind": "pcf-element",
            "code": e["pcf_hierarchy_id"], "element": e["pcf_element_id"],
            "level": e["level"],
            "parent": ("INV-PCF74-" + e["parent_pcf_element_id"])
            if e["parent_pcf_element_id"] else None,
            "label": text_of(e["name"]), "withheld": False, "draft": False})
    for e in docs["bpo"]["entries"]:
        local = e["iri"].split("#")[-1]
        label = None
        if e["kind"] == "capability-class":
            for d in e["declarations"]:
                for lab in d.get("label") or []:
                    if isinstance(lab, dict) and text_of(lab.get("text")):
                        label = lab["text"]
                        break
                if label:
                    break
        if not label and not re.fullmatch(r"P\d+", local):
            label = camel_words(local)
        if label:
            label = re.sub(r"\s+Capability$", "", label)
        parents = []
        if e["kind"] == "capability-class":
            for d in e["declarations"]:
                for sup in (d.get("hierarchy") or {}).get("subclass_of") or []:
                    if sup.startswith(BPO):
                        parents.append(sup)
        out.append({
            "id": e["id"], "source": "bpo", "kind": "bpo-" + e["kind"],
            "code": local, "iri": e["iri"], "level": None,
            "parent_iris": parents, "parent": None,
            "pcf_code": e.get("pcf_code"),
            "class_entry": e.get("capability_class_entry"),
            "enables": [x for x in e.get("enables_process") or []],
            "label": label, "withheld": False, "draft": False})
    for e in docs["brm"]["entries"]:
        out.append({
            "id": e["id"], "source": "brm", "kind": e["kind"], "code": e["code"],
            "document": e["document"], "level": e["level"],
            "parent_code": e.get("parent_code"), "parent": None,
            "label": text_of(e["name"]), "withheld": withheld(e["name"]),
            "draft": False})
    for e in docs["fibf"]["entries"]:
        out.append({
            "id": e["id"], "source": "fibf", "kind": e["kind"], "code": e["code"],
            "document": e["document"], "domain": e["domain"], "level": e["level"],
            "parent_code": e.get("parent_code"), "parent": None,
            "label": text_of(e["name"]), "withheld": withheld(e["name"]),
            "draft": bool(e.get("draft"))})
    for e in docs["fibf-bc"]["entries"]:
        out.append({
            "id": e["id"], "source": "fibf-bc", "kind": e["kind"], "code": e["code"],
            "document": e["document"], "domain": e["domain"], "level": e["level"],
            "parent_code": e.get("parent_code"), "function_code": e.get("function_code"),
            "parent": None, "label": text_of(e["name"]),
            "sentence": text_of(e["description"]),
            "withheld": withheld(e["description"]) or withheld(e["name"]),
            "draft": bool(e.get("draft"))})
    resolve_parents(out)
    return out


def norm_code(code: str) -> str:
    """FIBF codes with each numeric component padded to three digits."""
    return ".".join(p.zfill(3) if p.isdigit() else p for p in code.split("."))


def resolve_parents(recs: list[dict]) -> None:
    """Each record's parent record, from the source's own hierarchy."""
    by_doc_code, by_domain_code = {}, {}
    for r in recs:
        if r["source"] in ("brm", "fibf"):
            by_doc_code.setdefault((r["document"], r["code"]), r["id"])
        if r["source"] == "fibf":
            by_domain_code.setdefault((r["domain"], norm_code(r["code"])), r["id"])
    class_by_iri = {r["iri"]: r["id"] for r in recs if r["kind"] == "bpo-capability-class"}
    for r in recs:
        if r["source"] in ("brm", "fibf") and r.get("parent_code"):
            r["parent"] = by_doc_code.get((r["document"], r["parent_code"]))
        elif r["source"] == "fibf-bc":
            r["parent"] = (by_doc_code.get((r["document"], r["parent_code"]))
                           or by_doc_code.get((r["document"], r.get("function_code"))))
            if r["parent"] is None:
                # The same domain's activities may sit in another workbook
                # (Travel), sometimes with an unpadded code (TRT.010.70).
                for code in (r["parent_code"], r.get("function_code")):
                    hit = code and by_domain_code.get((r["domain"], norm_code(code)))
                    if hit:
                        r["parent"], r["parent_across_documents"] = hit, True
                        break
        elif r["kind"] == "bpo-capability-class":
            for iri in r["parent_iris"]:
                if iri in class_by_iri and class_by_iri[iri] != r["id"]:
                    r["parent"] = class_by_iri[iri]
                    break


# ------------------------------------------------------------ synthesis


def designating_level(r: dict) -> str:
    """'coarse' records always designate; 'fine' ones only on recurrence."""
    if r["source"] == "pcf":
        return "coarse" if r["level"] <= 3 else "fine"
    if r["source"] == "fibf-bc":
        return "fine"
    if r["kind"] == "bpo-scope-entry":
        return "scope"
    return "coarse"


def frame_of(r: dict):
    if r["withheld"]:
        return None
    if r["source"] == "fibf-bc":
        if r["label"]:
            return frame_label(r["label"], "label")
        return frame_sentence(r["sentence"]) if r.get("sentence") else None
    if r["kind"] == "bpo-scope-entry":
        return frame_label(r["label"], "class-name") if r["label"] else None
    return frame_label(r["label"], "label") if r["label"] else None


def ancestors(r: dict, by_id: dict):
    seen = set()
    p = r.get("parent")
    while p and p not in seen:
        seen.add(p)
        yield by_id[p]
        p = by_id[p].get("parent")


def synthesize(base: Path, docs: dict, acts_doc: dict) -> dict:
    recs = records(base, docs)
    by_id = {r["id"]: r for r in recs}
    for r in recs:
        f = frame_of(r)
        r["frame"] = f
    # The PCF act type behind each element, from BPO at the I-1 pin.
    act_by_element = {a["pcf_element_id"]: a for a in acts_doc["act_types"]}
    genera = {g["iri"]: g for g in acts_doc["genera"]}

    # --- 3. generate: which records designate a key
    coarse_keys = set()
    for r in recs:
        if r["frame"] and r["frame"].key and designating_level(r) == "coarse":
            coarse_keys.add(r["frame"].key)
    fine_parents = defaultdict(set)
    for r in recs:
        if r["frame"] and r["frame"].key and designating_level(r) == "fine":
            fine_parents[r["frame"].key].add(r.get("parent"))
    recurring = {k for k, ps in fine_parents.items() if len(ps) >= 2}
    keys = coarse_keys | recurring

    designates = {}
    for r in recs:
        f = r["frame"]
        if not f or not f.key:
            continue
        level = designating_level(r)
        if level in ("coarse", "scope") or f.key in keys:
            designates[r["id"]] = f.key
    # A scope entry designates what its class designates; one without a
    # class is BPO's word for a capability and designates on its own frame.
    for r in recs:
        if r["kind"] == "bpo-scope-entry" and r["class_entry"] in designates:
            designates[r["id"]] = designates[r["class_entry"]]
    # BPO capability classes minted from PCF nodes (P<id>, Q-12) carry no
    # label of their own here: they designate their element's candidate.
    pcf_by_element = {r["element"]: r for r in recs if r["source"] == "pcf"}
    for r in recs:
        if r["kind"] == "bpo-capability-class" and re.fullmatch(r"P\d+", r["code"]):
            el = pcf_by_element.get(r["code"][1:])
            if el is not None and el["id"] in designates:
                designates[r["id"]] = designates[el["id"]]
                r["frame_from"] = el["id"]

    cands = {}
    for rid, key in designates.items():
        c = cands.setdefault(key, {"key": key, "designated_by": [], "realized_via": [],
                                   "requirement_evidence": [], "broader": {},
                                   "narrower": {}, "flags": set()})
        c["designated_by"].append(rid)

    # --- 4. crosswalk: every record's interpretation
    links = defaultdict(list)          # record id -> [(candidate key, relation)]
    no_interp = {}
    for rid, key in designates.items():
        links[rid].append((key, "designates"))

    def nearest_designating(r):
        for a in ancestors(r, by_id):
            if a["id"] in designates:
                return a
        return None

    for r in recs:
        if r["source"] == "pcf" and designating_level(r) == "fine":
            a = nearest_designating(r)
            if a is not None:
                key = designates[a["id"]]
                if (key, "designates") not in links[r["id"]]:
                    links[r["id"]].append((key, "realization-evidence"))
                cands[key]["realized_via"].append(r["id"])
        elif r["source"] == "fibf-bc":
            a = nearest_designating(r)
            if a is not None:
                key = designates[a["id"]]
                links[r["id"]].append((key, "requirement-evidence"))
                cands[key]["requirement_evidence"].append(r["id"])
        elif r["id"] not in designates:
            a = nearest_designating(r)
            if a is not None and r["source"] in ("fibf", "brm"):
                key = designates[a["id"]]
                links[r["id"]].append((key, "context"))
        if not links[r["id"]]:
            no_interp[r["id"]] = no_interpretation_reason(r, by_id)
    # BPO's own wiring: what each class or scope entry enables.
    for r in recs:
        if r["source"] == "bpo" and r["id"] in designates:
            cands[designates[r["id"]]].setdefault("enables", []).extend(
                (r["id"], x) for x in r["enables"])

    # --- 5. relate: broader from the source hierarchies
    for rid, key in designates.items():
        r = by_id[rid]
        a = nearest_designating(r)
        if a is not None and designates[a["id"]] != key:
            pkey = designates[a["id"]]
            cands[key]["broader"].setdefault(pkey, set()).add("hierarchy:%s<%s" % (rid, a["id"]))
    # ... and from object containment within a family
    by_family = defaultdict(list)
    for key in cands:
        fam, obj = key.split("|", 1)
        by_family[fam].append((obj, key))
    for fam, items in by_family.items():
        objs = {o: k for o, k in items}
        for obj, key in items:
            words = obj.split()
            for n in range(1, len(words)):
                tail = " ".join(words[n:])
                if tail in objs and objs[tail] != key:
                    cands[key]["broader"].setdefault(objs[tail], set()).add(
                        "object-containment:%s" % tail)
                    break
    cycles = break_cycles(cands)
    for key, c in cands.items():
        for pkey, basis in c["broader"].items():
            cands[pkey]["narrower"].setdefault(key, set()).update(basis)

    return {"recs": recs, "by_id": by_id, "cands": cands, "designates": designates,
            "links": links, "no_interp": no_interp, "cycles": cycles,
            "act_by_element": act_by_element, "genera": genera}


def no_interpretation_reason(r: dict, by_id: dict) -> str:
    if r["withheld"]:
        if r.get("parent") is None:
            return ("text withheld (closure decision of 2026-10-30) and no harvested "
                    "parent to attach it to")
        return "text withheld, and no ancestor designates a candidate"
    if r["source"] == "fibf-bc" and r.get("parent") is None:
        return ("its activity and function are not harvested, and its own text "
                "yields no recurring ability")
    if not r.get("label") and not r.get("sentence"):
        if r["kind"] == "bpo-capability-class":
            return ("a BPO class minted from a PCF node (Q-12) whose element "
                    "designates no candidate")
        return "no label or description to read"
    if r.get("frame") is None:
        return "its label yields no ability and object"
    return "no ancestor designates a candidate, and its key does not recur"


def break_cycles(cands: dict) -> list[str]:
    """Drop the weakest broader edge on each cycle; return what was dropped."""
    dropped = []
    while True:
        color, stack, found = {}, [], None

        def visit(k):
            nonlocal found
            color[k] = 1
            stack.append(k)
            for p in sorted(cands[k]["broader"]):
                if found:
                    return
                if color.get(p) == 1:
                    found = stack[stack.index(p):] + [p]
                    return
                if p not in color:
                    visit(p)
            stack.pop()
            color[k] = 2

        for k in sorted(cands):
            if k not in color:
                visit(k)
            if found:
                break
        if not found:
            return dropped
        edges = [(len(cands[a]["broader"][b]), a, b) for a, b in zip(found, found[1:])]
        _, a, b = min(edges)
        dropped.append("%s broader %s (%s)" % (a, b, ", ".join(sorted(cands[a]["broader"][b]))))
        del cands[a]["broader"][b]


# ------------------------------------------------------------ classify


def classify(s: dict) -> None:
    """Preliminary classification, realization evidence and review status."""
    cands, by_id = s["cands"], s["by_id"]
    for key, c in cands.items():
        recs = [by_id[i] for i in c["designated_by"]]
        frames = [r["frame"] for r in recs if r.get("frame")]
        sources = {r["source"] for r in recs}
        fam, obj = key.split("|", 1)
        head = obj.split()[-1] if obj else ""
        c["sources"] = sorted(sources)
        top_only = all((r["source"] == "pcf" and r["level"] == 1)
                       or r["kind"] in ("brm-mission-sector", "brm-business-function")
                       for r in recs)
        coordinated = obj.count(" and ") >= 2
        bounded = frames and all(f.bounded for f in frames)
        inferred = frames and all(f.inferred for f in frames)
        fine_only = all(designating_level(r) == "fine" for r in recs)
        bc_only = sources == {"fibf-bc"}
        if not obj:
            cls, why = "unresolved", "no object phrase could be read from its labels"
        elif bc_only:
            cls, why = "requirement", (
                "supported only by FIBF business capabilities, which are outcome-based "
                "requirement records (E5 homonym), with no process or function behind it")
        elif singular(head) in ROLE_HEADS and inferred:
            cls, why = "role", ("its label names an agent or organizational body and no "
                                "act: a role or a bearer, not a capability")
        elif singular(head) in SKILL_HEADS and fam not in (
                "training", "development", "staffing", "management", "analysis",
                "monitoring", "identification"):
            cls, why = "skill", ("its object names a person's ability; CM-01 places a "
                                 "person's skill outside Business Capability (CD1)")
        elif top_only or (coordinated and any(r["source"] == "pcf" and r["level"] <= 2
                                              for r in recs)):
            cls, why = "function", (
                "a top-level area of a catalog (PCF category or BRM mission sector or "
                "business function) or a coordination of several abilities: a standing "
                "function whose whole-function type is defined only where one is "
                "(CD16, conditional designation R9); E4 is open")
        elif bounded and (fine_only or not c["realized_via"]):
            cls, why = "process", (
                "names one act episode with a definite end, with no process of its own "
                "beneath it: realization evidence for a broader capability, not a type")
        elif inferred and fam in ("formulation", "data", "administration",
                                  "communication", "reporting") and all(
                r["source"] in ("fibf", "fibf-bc", "brm") for r in recs):
            cls, why = "unresolved", (
                "its labels name an artifact (a plan, document, record or notice), not "
                "an ability; the ability is inferred and needs a reader")
        else:
            cls, why = "capability", (
                "an ability of an organization to act on a stated object, with an "
                "ability family and source support")
        c["classification"] = cls
        c["classification_reason"] = why

    # Process candidates hand their acts up to the broader candidates.
    for key, c in cands.items():
        if c["classification"] == "process":
            for pkey in c["broader"]:
                cands[pkey]["realized_via"].extend(
                    i for i in c["designated_by"] if by_id[i]["source"] == "pcf")
                cands[pkey].setdefault("absorbed", []).append(key)

    for key, c in cands.items():
        realization(s, key, c)
    for key, c in cands.items():
        if not c["realization"] and any(cands[k]["realization"] for k in c["narrower"]):
            c["acts_beneath"] = True
            c["flags"].add("realization evidence only through narrower candidates")
        status(c)


def realization(s: dict, key: str, c: dict) -> None:
    by_id, acts, genera = s["by_id"], s["act_by_element"], s["genera"]
    rows, seen = [], set()
    pcf_ids = [i for i in c["designated_by"] if by_id[i]["source"] == "pcf"]
    for rid, via in [(i, "designating record") for i in pcf_ids] + \
                    [(i, "process beneath it") for i in c["realized_via"]]:
        el = by_id[rid]["element"]
        a = acts.get(el)
        if a is None or a["act_type"] in seen:
            continue
        seen.add(a["act_type"])
        rows.append({"act_type": a["act_type"], "genus": a["genus"], "via": rid,
                     "evidence": via})
    for rid, x in c.get("enables", []):
        if x["target"] in seen:
            continue
        seen.add(x["target"])
        rows.append({"act_type": x["target"], "genus": None, "via": rid,
                     "evidence": "BPO enablesProcess (%s)" % x["target_kind"]})
    flags = c["flags"]
    fam = key.split("|", 1)[0]
    agree = total = 0
    for row in rows:
        gs = row["genus"] or []
        if any(g in DEVELOPMENT_GENERA for g in gs):
            flags.add("development-act-genus (CAP-06: needs a recorded reason)")
        # An approval or authorization grants standing: G1-T question 4 asks
        # that every index member be describable without it.
        f = by_id[row["via"]].get("frame") if row["via"] in by_id else None
        if f and f.verbs and f.verbs[0] in DEONTIC_VERBS:
            flags.add(DEONTIC)
        if any(genera.get(g, {}).get("kind") in ("bpo-capability-class",
                                                 "cco-capability-class") for g in gs):
            flags.add("act type typed under a capability class (Q-12)")
        if row["evidence"].startswith("BPO enablesProcess") and "act)" not in row["evidence"]:
            flags.add("BPO index member is not an act (Q-12)")
        labels_ = {(genera.get(g, {}).get("label") or "").lower() for g in gs}
        if labels_ - UNINFORMATIVE_GENERA and fam not in BROAD_FAMILIES:
            total += 1
            if labels_ & FAMILY_GENERA.get(fam, set()):
                agree += 1
    c["realization"] = rows
    c["genus_agreement"] = (agree, total)
    outputs = Counter()
    for row in rows:
        a = s["act_by_element"].get(by_id[row["via"]].get("element") or "")
        if a and a["act_type"] == row["act_type"]:
            outputs.update(a.get("outputs") or [])
    c["outputs"] = [o for o, _ in outputs.most_common(5)]


def status(c: dict) -> None:
    cls = c["classification"]
    has_acts = bool(c["realization"]) or c.get("acts_beneath", False)
    has_support = has_acts or c["requirement_evidence"] or len(c["designated_by"]) >= 2
    if cls == "capability":
        c["compatibility"] = "likely" if has_acts else ("possible" if has_support
                                                        else "unsupported")
        if not has_acts:
            c["flags"].add("no BPO act type: realization index to be drawn")
        c["flags"].discard("x")
        if c["compatibility"] == "unsupported":
            c["review_status"] = "deferred"
            c["status_reason"] = ("one source record and no realization or requirement "
                                  "evidence: kept, not yet supported")
        elif c["flags"]:
            c["review_status"] = "needs-review"
            c["status_reason"] = "generated; quality flags to clear: " + "; ".join(
                sorted(c["flags"]))
        else:
            c["review_status"] = "generated-draft"
            c["status_reason"] = "generated; passed every automated check"
    elif cls in ("function", "unresolved"):
        c["compatibility"] = "not-assessed"
        c["review_status"] = "deferred"
        c["status_reason"] = c["classification_reason"]
    else:
        c["compatibility"] = "not-a-capability"
        c["review_status"] = "rejected"
        c["status_reason"] = ("not a capability type: " + c["classification_reason"]
                              + "; its records are kept as evidence")


# ------------------------------------------------------------ render


def candidate_id(key: str) -> str:
    return "BCC-" + sha256(key.encode())[:8]


def title(words: str) -> str:
    small = {"and", "or", "of", "for", "with", "to", "the", "in", "on", "a"}
    out = []
    for i, w in enumerate(words.split()):
        out.append(w if (w in small and i) else (w[:1].upper() + w[1:]))
    return " ".join(out)


CIRCULAR = "circular differentia: the label names only the ability; a reader writes it"


def circular(obj: str, family: str) -> bool:
    """Whether the object is only ability nominals, one of them the family's own.

    "Procurement" read through its family gives "obtain procurement": the
    differentia restates the name and says nothing. Such a candidate gets
    the neutral "carry out procurement" and a flag that keeps it from
    passing as a generated draft.
    """
    words = [singular(w) for w in obj.lower().replace(",", " ").split()
             if w not in ("and", "or")]
    return bool(words) and all(w in N for w in words) and any(
        N[w] == family for w in words)


def display_object(c: dict, by_id: dict) -> tuple[str, str | None]:
    """The object and nominal(s) of the best designating record."""
    def rank(rid):
        r = by_id[rid]
        order = {"bpo": 0, "pcf": 1, "fibf": 2, "brm": 3, "fibf-bc": 4}[r["source"]]
        return (order, r.get("level") if isinstance(r.get("level"), int) else 9, rid)
    for rid in sorted(c["designated_by"], key=rank):
        f = by_id[rid].get("frame")
        if f and f.object:
            if len(f.verbs) > 1:
                noms = list(dict.fromkeys(V[v][0] for v in f.verbs))
                nominal = noms[0] if len(noms) == 1 else (
                    ", ".join(noms[:-1]) + " and " + noms[-1])
                return f.object, nominal
            return f.object, f.nominal
    return c["key"].split("|", 1)[1], None


def describe(s: dict) -> list[dict]:
    cands, by_id, genera = s["cands"], s["by_id"], s["genera"]
    ids = {k: candidate_id(k) for k in cands}
    if len(set(ids.values())) != len(ids):
        raise Refused("two candidate keys share an identifier; lengthen the hash")
    names = {}
    for key, c in cands.items():
        fam = key.split("|", 1)[0]
        obj, nominal = display_object(c, by_id)
        if fam == "relationship":
            names[key] = title("%s relationship management capability" % obj)
        elif nominal and fam != "provision":
            names[key] = title("%s %s capability" % (obj, nominal))
        else:
            names[key] = title("%s capability" % obj)
        c["display_object"] = obj
    base = dict(names)
    for key, c in cands.items():
        if key.split("|", 1)[1] in GENERIC_OBJECTS and c["broader"]:
            b = sorted(c["broader"], key=lambda k: base[k].lower())[0]
            names[key] = "%s (in %s)" % (base[key], base[b].replace(" Capability", ""))
            c["flags"].add("generic object: named with its broader candidate")
    dup = Counter(n.lower() for n in names.values())
    for key in cands:
        if dup[names[key].lower()] > 1:
            fam = key.split("|", 1)[0]
            names[key] = "%s (%s)" % (names[key], fam)
    for c in cands.values():
        if circular(c["display_object"], c["key"].split("|", 1)[0]):
            c["flags"].add(CIRCULAR)
        status(c)
    out = []
    for key in sorted(cands, key=lambda k: (names[k].lower(), k)):
        c = cands[key]
        fam, objkey = key.split("|", 1)
        broader = sorted(c["broader"], key=lambda k: names[k].lower())
        template = "carry out {o}" if CIRCULAR in c["flags"] else FAMILY.get(
            fam, "carry out {o}")
        ability = template.format(o=c["display_object"])
        gl = sorted({genera[g]["label"] for row in c["realization"]
                     for g in (row["genus"] or []) if g in genera
                     and genera[g]["kind"] in ("bpo-act-genus", "cco-class")})
        definition = ("A business capability of an organization to %s, grounded in "
                      "the organization's members as organized" % ability)
        if broader:
            definition += ", exercised as part of %s" % names[broader[0]][:-len(" Capability")].lower() \
                if names[broader[0]].endswith(" Capability") else ""
        if gl:
            definition += ", and shown in acts of the kinds %s" % join_or(gl[:4])
        definition += "."
        recs = [by_id[i] for i in c["designated_by"]]
        synonyms = sorted({r["label"] for r in recs if r.get("label")
                           and r["label"].lower() != names[key].lower()})
        out.append({
            "id": ids[key],
            "name": names[key],
            "key": key,
            "definition": {
                "text": definition,
                "genus": "Business Capability (CM-01; preliminary alignment %s "
                         "Organization Capability)" % ORGANIZATION_CAPABILITY,
                "differentia": "the ability to %s" % ability,
            },
            "bearer": {
                "proposed": "%s Organization" % ORGANIZATION,
                "context": bearer_context(recs),
            },
            "distinctive_ability": {"family": fam, "ability": ability,
                                    "object": c["display_object"]},
            "classification": c["classification"],
            "classification_reason": c["classification_reason"],
            "bfo_cco_compatibility": c["compatibility"],
            "review": {"status": c["review_status"], "justification": c["status_reason"],
                       "flags": sorted(c["flags"])},
            "sources": [source_row(by_id[i], s) for i in sorted(c["designated_by"])],
            "source_count": dict(sorted(Counter(r["source"] for r in recs).items())),
            "realization_evidence": {
                "act_types": c["realization"],
                "act_genera": gl,
                "outputs": c["outputs"],
                "processes_beneath": len(c["realized_via"]),
                "requirement_records": sorted(c["requirement_evidence"]),
                "absorbed_process_candidates": sorted(ids[k] for k in c.get("absorbed", [])),
            },
            "broader": [{"id": ids[k], "name": names[k],
                         "basis": sorted(c["broader"][k])} for k in broader],
            "narrower": [{"id": ids[k], "name": names[k]}
                         for k in sorted(c["narrower"], key=lambda k: names[k].lower())],
            "duplicates_merged": len(c["designated_by"]) - 1,
            "synonyms": synonyms,
            "overlaps": c.get("overlaps", []),
        })
    for row in out:
        for o in row["overlaps"]:
            o["id"] = ids[o.pop("key")]
            o["name"] = names[[k for k in cands if ids[k] == o["id"]][0]]
    return out


def join_or(items: list[str]) -> str:
    items = [i.lower() for i in items]
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " or " + items[-1]


def bearer_context(recs: list[dict]) -> str:
    srcs = {r["source"] for r in recs}
    if srcs <= {"brm", "fibf", "fibf-bc"}:
        return "sources are U.S. federal reference models: a government agency as bearer"
    if srcs & {"brm", "fibf", "fibf-bc"}:
        return "cross-sector: commercial (PCF/BPO) and U.S. federal sources"
    return "cross-industry organizations (PCF/BPO)"


def source_row(r: dict, s: dict) -> dict:
    row = {"inventory_id": r["id"], "source": SOURCE_NAMES[r["source"]],
           "kind": r["kind"], "code": r["code"]}
    if r["source"] == "pcf":
        row["pcf_element_id"] = r["element"]
        row["level"] = r["level"]
    if r.get("label"):
        row["label"] = r["label"]
    if r.get("frame_from"):
        row["label_from"] = r["frame_from"]
    if r.get("draft"):
        row["draft"] = True
    return row


def overlaps(s: dict) -> None:
    """Same object under another family; or a near object in the same one."""
    cands = s["cands"]
    by_obj = defaultdict(list)
    index = defaultdict(set)
    for key in cands:
        fam, obj = key.split("|", 1)
        by_obj[obj].append(key)
        for w in set(obj.split()):
            if w not in ("and", "of", "for"):
                index[w].add(key)
    for key, c in cands.items():
        fam, obj = key.split("|", 1)
        found = []
        for other in by_obj[obj]:
            if other != key:
                found.append({"key": other, "relation": "same object, other ability"})
        ws = {w for w in obj.split() if w not in ("and", "of", "for")}
        scores = Counter()
        for w in sorted(ws):
            for other in sorted(index[w]):
                if other != key and other.split("|", 1)[0] == fam:
                    scores[other] += 1
        for other, n in sorted(scores.items(), key=lambda x: (-x[1], x[0])):
            ow = {w for w in other.split("|", 1)[1].split() if w not in ("and", "of", "for")}
            j = n / len(ws | ow)
            if j >= 0.5 and other not in c["broader"] and other not in c["narrower"]:
                found.append({"key": other, "relation": "similar object (Jaccard %.2f)" % j})
        c["overlaps"] = found[:6]


# ------------------------------------------------------------ checks


def checks(s: dict, catalog: list[dict], xwalk: list[dict], docs: dict) -> tuple[list, list]:
    """(hard failures, quality findings). A hard failure refuses to write."""
    hard, soft = [], []
    total = sum(len(d["entries"]) for d in docs.values())
    if len(xwalk) != total:
        hard.append("crosswalk has %d rows for %d source records" % (len(xwalk), total))
    if len({x["inventory_id"] for x in xwalk}) != len(xwalk):
        hard.append("a source record appears twice in the crosswalk")
    ids = {c["id"] for c in catalog}
    if len(ids) != len(catalog):
        hard.append("candidate identifiers are not unique")
    for c in catalog:
        if not re.fullmatch(r"BCC-[0-9a-f]{8}", c["id"]):
            hard.append("%s is not a provisional inventory identifier" % c["id"])
        if not c["sources"]:
            hard.append("%s has no designating source record" % c["id"])
        for b in c["broader"]:
            if b["id"] not in ids or b["id"] == c["id"]:
                hard.append("%s has a broader link to %s" % (c["id"], b["id"]))
        if not c["definition"]["text"].startswith("A business capability of an organization"):
            hard.append("%s: definition does not state the genus" % c["id"])
    for x in xwalk:
        for i in x["interpretations"]:
            if i["candidate"] not in ids:
                hard.append("%s points at %s, which is not a candidate"
                            % (x["inventory_id"], i["candidate"]))
        if not x["interpretations"] and not x.get("no_interpretation"):
            hard.append("%s has neither an interpretation nor a reason" % x["inventory_id"])
    narrower = {(c["id"], n["id"]) for c in catalog for n in c["narrower"]}
    broader = {(b["id"], c["id"]) for c in catalog for b in c["broader"]}
    if narrower != broader:
        hard.append("broader and narrower are not inverse (%d against %d)"
                    % (len(broader), len(narrower)))
    # Originality: no definition may carry eight consecutive words of a
    # source description.
    grams = set()
    for d in docs.values():
        for e in d["entries"]:
            t = text_of(e.get("description"))
            if t:
                ws = re.findall(r"[a-z']+", t.lower())
                grams.update(" ".join(ws[i:i + 8]) for i in range(len(ws) - 7))
    for c in catalog:
        ws = re.findall(r"[a-z']+", c["definition"]["text"].lower())
        for i in range(len(ws) - 7):
            if " ".join(ws[i:i + 8]) in grams:
                soft.append("%s: definition shares eight words with a source description"
                            % c["id"])
                break
    names = Counter(c["name"].lower() for c in catalog)
    soft.extend("name used by %d candidates: %s" % (n, k) for k, n in names.items() if n > 1)
    for line in s["cycles"]:
        soft.append("cycle broken in the broader graph: %s" % line)
    return hard, soft


# ------------------------------------------------------------ documents


def notice(docs: dict) -> tuple[str, dict]:
    pcf = docs["pcf"]
    return pcf["apqc_notice"], pcf["apqc_notice_source"]


HEADER = [
    "GENERATED by tools/catalog/synthesize.py --write. Do not edit: the",
    "offline check regenerates this file from the committed inventories and",
    "requires byte identity.",
    "",
    "Phase I-4, the Candidate Capability Catalog (decision of 2026-11-03).",
    "Candidates, not types: nothing here is admitted (G1-T), ratified or",
    "minted, and an identifier BCC-xxxxxxxx is an inventory identifier, never",
    "an IRI. Classifications are preliminary and rule-based; the reason for",
    "each is stated on it.",
    "",
    "This file is derived in part from the APQC Process Classification",
    "Framework, version 7.4, taken from the Business Process Ontology; APQC's",
    "notice is `apqc_notice` below. That material is not covered by this",
    "repository's MIT licence, and APQC does not endorse this work. See",
    "NOTICE.md at the repository root.",
]


def head_block(docs: dict, base: Path, what: str) -> dict:
    text, src = notice(docs)
    return {
        "format": 1,
        "generator": GENERATOR,
        "phase": "I-4",
        "what": what,
        "decision": DECISION,
        "status": "candidates for review; not vocabulary, not taxonomy, not ontology, "
                  "and not an admission (scope approval amendment 4)",
        "apqc_notice": text,
        "apqc_notice_source": src,
        "licence": "Derived in part from APQC's PCF 7.4 (under APQC's notice, "
                   "`apqc_notice`), from BPO (MIT, docs/sources/inventory/NOTICE.md) and "
                   "from U.S. Government works (FEAF-II BRM, FIBF; "
                   "docs/sources/inventory/NOTICE-federal.md). Not covered by this "
                   "repository's MIT licence as to the PCF material.",
        "inputs": [{"path": p, "sha256": sha256((base / p).read_bytes())}
                   for p in list(INPUTS.values()) + [ACTS]],
    }


def crosswalk_rows(s: dict, ids: dict) -> list[dict]:
    rows = []
    for r in s["recs"]:
        f = r.get("frame")
        row = {"inventory_id": r["id"], "source": SOURCE_NAMES[r["source"]],
               "kind": r["kind"], "code": r["code"]}
        if r["source"] == "pcf":
            row["pcf_element_id"] = r["element"]
        if r.get("parent"):
            row["parent"] = r["parent"]
        row["frame"] = f.as_dict() if f else None
        row["interpretations"] = [{"candidate": ids[k], "relation": rel}
                                  for k, rel in s["links"].get(r["id"], [])]
        if not row["interpretations"]:
            row["no_interpretation"] = s["no_interp"][r["id"]]
        rows.append(row)
    return rows


def counts(s: dict, catalog: list[dict], xwalk: list[dict], docs: dict) -> dict:
    by_source = Counter()
    for r in s["recs"]:
        by_source["%s (%s)" % (SOURCE_NAMES[r["source"]], r["kind"])] += 1
    designating = sum(len(c["sources"]) for c in catalog)
    cls = Counter(c["classification"] for c in catalog)
    status = Counter(c["review"]["status"] for c in catalog)
    compat = Counter(c["bfo_cco_compatibility"] for c in catalog)
    reasons = Counter()
    for c in catalog:
        if c["review"]["status"] in ("rejected", "deferred"):
            reasons["%s: %s" % (c["classification"], c["classification_reason"]
                                if c["classification"] != "capability"
                                else c["review"]["justification"])] += 1
    lacking = Counter()
    lacking_src = Counter()
    for x in xwalk:
        if not x["interpretations"]:
            lacking[x["no_interpretation"]] += 1
            lacking_src[x["source"]] += 1
    rel = Counter()
    for x in xwalk:
        for i in x["interpretations"]:
            rel[i["relation"]] += 1
    # An enablesProcess target BPO does not type as an act is not counted
    # as an act type (Q-12); it stays in the evidence, flagged.
    acts = {a["act_type"] for c in catalog for a in c["realization_evidence"]["act_types"]
            if a["genus"] is not None or a["evidence"].endswith("(act)")}
    act_rows = sum(len(c["realization_evidence"]["act_types"]) for c in catalog)
    likely = [c for c in catalog if c["bfo_cco_compatibility"] == "likely"]
    agree = sum(s["cands"][c["key"]]["genus_agreement"][0] for c in catalog)
    with_genus = sum(s["cands"][c["key"]]["genus_agreement"][1] for c in catalog)
    multi = sum(1 for c in catalog if len(c["source_count"]) >= 2)
    card = Counter(min(len(c["sources"]), 5) for c in catalog)
    return {
        "source_records_processed": {"total": len(s["recs"]),
                                     "by_source": dict(sorted(by_source.items()))},
        "candidates_generated": designating,
        "unique_candidates": len(catalog),
        "duplicates_merged": designating - len(catalog),
        "candidates_from_two_or_more_sources": multi,
        "designating_records_per_candidate": {("5+" if k == 5 else str(k)): v
                                              for k, v in sorted(card.items())},
        "classification": dict(sorted(cls.items())),
        "bfo_cco_compatibility": dict(sorted(compat.items())),
        "likely_bfo_cco_capabilities": len(likely),
        "review_status": dict(sorted(status.items())),
        "rejected_or_deferred": sum(status[k] for k in ("rejected", "deferred")),
        "rejected_or_deferred_by_reason": dict(sorted(reasons.items(), key=lambda x: -x[1])),
        "records_lacking_interpretation": sum(lacking.values()),
        "records_lacking_interpretation_by_source": dict(sorted(lacking_src.items())),
        "records_lacking_interpretation_by_reason": dict(sorted(lacking.items(),
                                                                key=lambda x: -x[1])),
        "crosswalk_links_by_relation": dict(sorted(rel.items())),
        "broader_links": sum(len(c["broader"]) for c in catalog),
        "overlap_links": sum(len(c["overlaps"]) for c in catalog),
        "synonym_labels": sum(len(c["synonyms"]) for c in catalog),
        "realization_evidence_rows": act_rows,
        "distinct_act_types_cited": len(acts),
        "act_type_genus_agrees_with_family": {"agree": agree, "with_genus": with_genus},
        "requirement_evidence_links": sum(len(c["realization_evidence"]["requirement_records"])
                                          for c in catalog),
    }


def report(cnt: dict, catalog: list[dict], soft: list[str]) -> str:
    L = ["<!-- GENERATED by tools/catalog/synthesize.py --write. Do not edit. -->", "",
         "# Candidate Capability Catalog — counts and quality findings", "",
         "Phase I-4, directed on 2026-11-03 (`%s`). Every figure below is computed "
         "from `candidates.yaml` and `crosswalk.yaml` by the generator; none is typed. "
         "Candidates are not admitted types, and identifiers are not IRIs." % DECISION, "",
         "Derived in part from the APQC Process Classification Framework® 7.4 (APQC's "
         "notice is in the YAML files and in `NOTICE.md`); APQC does not endorse this "
         "work.", "", "## The counts", "",
         "| Measure | Count |", "| --- | --- |"]
    L.append("| Source records processed | %d |" % cnt["source_records_processed"]["total"])
    L.append("| Candidate capabilities generated (designating records) | %d |"
             % cnt["candidates_generated"])
    L.append("| Unique candidates after deduplication | %d |" % cnt["unique_candidates"])
    L.append("| Duplicates merged | %d |" % cnt["duplicates_merged"])
    L.append("| Candidates supported by two or more sources | %d |"
             % cnt["candidates_from_two_or_more_sources"])
    L.append("| Classified as likely BFO/CCO-compatible capabilities | %d |"
             % cnt["likely_bfo_cco_capabilities"])
    L.append("| Rejected or deferred | %d |" % cnt["rejected_or_deferred"])
    L.append("| Source records lacking a proposed interpretation | %d |"
             % cnt["records_lacking_interpretation"])
    L.append("| Broader links proposed | %d |" % cnt["broader_links"])
    L.append("| Overlap links | %d |" % cnt["overlap_links"])
    L.append("| Realization evidence rows (act types per candidate) | %d |"
             % cnt["realization_evidence_rows"])
    L.append("| Distinct BPO act types cited | %d |" % cnt["distinct_act_types_cited"])
    L.append("| Requirement-evidence links (FIBF business capabilities) | %d |"
             % cnt["requirement_evidence_links"])
    g = cnt["act_type_genus_agrees_with_family"]
    L.append("| Act types whose BPO genus agrees with the candidate's ability family "
             "(specific families and genera only) | %d of %d |" % (g["agree"], g["with_genus"]))
    L += ["", "## Source records processed, by source", "", "| Source (kind) | Records |",
          "| --- | --- |"]
    L += ["| %s | %d |" % kv for kv in cnt["source_records_processed"]["by_source"].items()]
    L += ["", "## Classification", "", "| Classification | Candidates |", "| --- | --- |"]
    L += ["| %s | %d |" % kv for kv in cnt["classification"].items()]
    L += ["", "| BFO/CCO compatibility | Candidates |", "| --- | --- |"]
    L += ["| %s | %d |" % kv for kv in cnt["bfo_cco_compatibility"].items()]
    L += ["", "| Review status | Candidates |", "| --- | --- |"]
    L += ["| %s | %d |" % kv for kv in cnt["review_status"].items()]
    L += ["", "## Rejected or deferred, by reason", "", "| Reason | Candidates |",
          "| --- | --- |"]
    L += ["| %s | %d |" % (k.replace("|", "/"), v)
          for k, v in cnt["rejected_or_deferred_by_reason"].items()]
    L += ["", "## Source records lacking a proposed interpretation", "",
          "| Source | Records |", "| --- | --- |"]
    L += ["| %s | %d |" % kv for kv in cnt["records_lacking_interpretation_by_source"].items()]
    L += ["", "| Reason | Records |", "| --- | --- |"]
    L += ["| %s | %d |" % kv for kv in cnt["records_lacking_interpretation_by_reason"].items()]
    L += ["", "## Crosswalk links, by relation", "", "| Relation | Links |", "| --- | --- |"]
    L += ["| %s | %d |" % kv for kv in cnt["crosswalk_links_by_relation"].items()]
    flags = Counter(f for c in catalog for f in c["review"]["flags"])
    L += ["", "## Quality findings", "", "Flags raised on candidates (a candidate may "
          "carry several):", "", "| Flag | Candidates |", "| --- | --- |"]
    L += ["| %s | %d |" % kv for kv in sorted(flags.items(), key=lambda x: -x[1])]
    L += ["", "Exceptions found by the consistency checks (%d):" % len(soft), ""]
    L += ["- %s" % x for x in soft[:60]] or ["- none"]
    if len(soft) > 60:
        L.append("- … and %d more, listed by the offline check" % (len(soft) - 60))
    tops = [c for c in catalog if c["classification"] == "function"]
    L += ["", "## The catalog's top level", "",
          "Candidates classified `function` (deferred: whole-function types are defined "
          "only where they are), with how many candidates each has beneath it:", "",
          "| Candidate | Name | Narrower |", "| --- | --- | --- |"]
    L += ["| %s | %s | %d |" % (c["id"], c["name"], len(c["narrower"]))
          for c in sorted(tops, key=lambda c: -len(c["narrower"]))[:40]]
    return "\n".join(L) + "\n"


def build(base: Path) -> dict[str, bytes]:
    docs = {k: load_yaml(base, p) for k, p in INPUTS.items()}
    acts_doc = load_yaml(base, ACTS)
    s = synthesize(base, docs, acts_doc)
    overlaps(s)
    classify(s)
    catalog = describe(s)
    ids = {c["key"]: c["id"] for c in catalog}
    xwalk = crosswalk_rows(s, ids)
    hard, soft = checks(s, catalog, xwalk, docs)
    if hard:
        raise Refused("the catalog fails its consistency checks:\n  "
                      + "\n  ".join(hard[:40]))
    cnt = counts(s, catalog, xwalk, docs)
    head = head_block(docs, base, "the Candidate Capability Catalog")
    cat_doc = dict(head, counts=cnt, candidates=catalog)
    xw_head = head_block(docs, base, "the crosswalk: every source record and its "
                         "interpretation")
    xw_doc = dict(xw_head, counts={k: cnt[k] for k in (
        "source_records_processed", "records_lacking_interpretation",
        "crosswalk_links_by_relation")}, records=xwalk)
    hdr = "".join("# %s\n" % x if x else "#\n" for x in HEADER) + "\n"
    out = {
        CANDIDATES: (hdr + dump(cat_doc)).encode("utf-8"),
        CROSSWALK: (hdr + dump(xw_doc)).encode("utf-8"),
        REPORT: report(cnt, catalog, soft).encode("utf-8"),
    }
    guard = hb.admission_findings(base, OUT_DIR, out)
    if guard:
        raise Refused("the admission guard refuses the catalog:\n  " + "\n  ".join(guard))
    return out


# ------------------------------------------------------------ BPO act types


def rebuild_acts(base: Path, cache: Path) -> bytes:
    """BPO's act types at the I-1 pin: genus and outputs, IRIs only."""
    import rdflib

    p = hb.pins(base)
    items = [i for i in p["inputs_flat"] if i["path"].startswith("ontology/")]
    data = hb.fetch_commit(p, p["commit"], items, cache)
    upstream = hb.fetch_upstream(base, cache)
    full = rdflib.Graph()
    for blob in list(data.values()):
        full.parse(data=blob.decode("utf-8"), format="turtle")
    labels = rdflib.Graph()
    for blob in upstream.values():
        labels.parse(data=blob.decode("utf-8"), format="turtle")
    RDFS, OWL = rdflib.RDFS, rdflib.OWL

    def label(iri):
        for g in (full, labels):
            for o in g.objects(rdflib.URIRef(iri), RDFS.label):
                if getattr(o, "language", None) in (None, "en"):
                    return str(o)
        return None

    has_output = [str(s) for s in labels.subjects(RDFS.label, None)
                  if str(labels.value(s, RDFS.label)) == "has output"]
    acts, genera = [], {}
    for path in sorted(data):
        text = data[path].decode("utf-8")
        g = rdflib.Graph().parse(data=text, format="turtle")
        for s in sorted(set(g.subjects(rdflib.RDF.type, OWL.Class)), key=str):
            iri = str(s)
            local = iri.split("#")[-1]
            if not iri.startswith(BPO) or not re.fullmatch(r"P\d+", local):
                continue
            sups = sorted(str(o) for o in g.objects(s, RDFS.subClassOf)
                          if isinstance(o, rdflib.URIRef))
            outs = set()
            for o in g.objects(s, RDFS.subClassOf):
                if isinstance(o, rdflib.BNode) and str(g.value(o, OWL.onProperty)) in has_output:
                    v = g.value(o, OWL.someValuesFrom)
                    if isinstance(v, rdflib.URIRef):
                        outs.add(str(v))
            m = re.search(r"(?m)^bpo:%s\s+a\s+owl:Class" % local, text)
            line = text[:m.start()].count("\n") + 1 if m else None
            acts.append({"act_type": iri, "pcf_element_id": local[1:], "genus": sups,
                         "outputs": sorted(outs), "module": path, "line": line})
            for gi in sups:
                genera.setdefault(gi, None)
    seen = {}
    for a in acts:
        if a["act_type"] in seen:
            raise Refused("%s is declared in %s and %s" % (a["act_type"],
                                                          seen[a["act_type"]], a["module"]))
        seen[a["act_type"]] = a["module"]
    rows = []
    for gi in sorted(genera):
        local = gi.split("#")[-1] if "#" in gi else gi.rsplit("/", 1)[-1]
        if gi.startswith(BPO) and local.startswith("ActOf"):
            kind = "bpo-act-genus"
        elif gi.startswith(BPO) and local.endswith("Capability"):
            kind = "bpo-capability-class"
        elif gi == CCO + ORGANIZATION_CAPABILITY.split(":")[1]:
            kind = "cco-capability-class"
        elif gi.startswith(CCO):
            kind = "cco-class"
        else:
            kind = "other"
        rows.append({"iri": gi, "label": label(gi), "kind": kind,
                     "development_act": gi in DEVELOPMENT_GENERA})
    pcf = load_yaml(base, INPUTS["pcf"])
    doc = {
        "format": 1, "generator": GENERATOR + " --rebuild-acts", "phase": "I-4",
        "what": "BPO's act types (bpo:P<element id>) at the Phase I-1 pin, with each "
                "one's named superclasses (its genus) and the classes it has as "
                "output. IRIs and identifiers only; no PCF text.",
        "decision": DECISION,
        "apqc_notice": pcf["apqc_notice"],
        "apqc_notice_source": pcf["apqc_notice_source"],
        "source": {"repository": p["repository"], "commit": p["commit"],
                   "pins": "config/inventory-sources.yaml",
                   "modules": [{"path": i["path"], "sha256": i["sha256"]} for i in items],
                   "labels_from": "the BPO modules, then the full CCO and BFO pinned in "
                                  "config/upstream-sources.yaml",
                   "has_output": has_output},
        "counts": {"act_types": len(acts),
                   "by_genus_kind": dict(sorted(Counter(
                       r["kind"] for a in acts for gi in a["genus"]
                       for r in rows if r["iri"] == gi).items())),
                   "genera": len(rows)},
        "genera": rows,
        "act_types": sorted(acts, key=lambda a: int(a["pcf_element_id"])),
    }
    hdr = ["GENERATED by tools/catalog/synthesize.py --rebuild-acts, which reads",
           "BPO's modules at the Phase I-1 pin (digest checked). Do not edit.", "",
           "The act type IRIs embed APQC PCF element IDs; APQC's notice is",
           "`apqc_notice`. Not vocabulary, and not an admission."]
    return ("".join("# %s\n" % x if x else "#\n" for x in hdr) + "\n" + dump(doc)).encode()


# ------------------------------------------------------------ main


def check(base: Path) -> list[str]:
    problems = []
    try:
        built = build(base)
    except Refused as error:
        return [str(error)]
    for rel, data in built.items():
        path = base / rel
        if not path.is_file():
            problems.append("%s is missing; run %s --write" % (rel, GENERATOR))
        elif path.read_bytes() != data:
            problems.append("%s is not what the generator writes from the committed "
                            "inputs; run %s --write (a hand edit is overwritten)"
                            % (rel, GENERATOR))
    acts = (base / ACTS).read_bytes()
    if b"\r\n" in acts:
        problems.append("%s has CRLF line endings" % ACTS)
    problems += hb.admission_findings(base, OUT_DIR, {})
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true", help="regenerate the catalog")
    ap.add_argument("--rebuild-acts", action="store_true",
                    help="re-read BPO's act types at the I-1 pin (network or cache)")
    args = ap.parse_args(argv)
    base = Path(__file__).resolve().parents[2]
    if args.rebuild_acts:
        (base / ACTS).parent.mkdir(parents=True, exist_ok=True)
        (base / ACTS).write_bytes(rebuild_acts(base, base / hb.CACHE))
        print("wrote %s" % ACTS)
    if args.write:
        for rel, data in build(base).items():
            (base / rel).write_bytes(data)
            print("wrote %s" % rel)
        return 0
    if args.rebuild_acts:
        return 0
    problems = check(base)
    for p in problems:
        print("FAIL: %s" % p)
    if not problems:
        print("catalog: generated files match the committed inputs; checks pass")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
