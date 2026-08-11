from .crm import CRMConnector
from .sheets import SheetsConnector
from .email import EmailConnector
from .chatbot import ChatbotConnector
from .ai import AIConnector
from .transform import TransformConnector

CONNECTORS = {
    "crm": CRMConnector(),
    "sheets": SheetsConnector(),
    "email": EmailConnector(),
    "chatbot": ChatbotConnector(),
    "ai": AIConnector(),
    "transform": TransformConnector(),
}
