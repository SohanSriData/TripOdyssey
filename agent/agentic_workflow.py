from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT, REVIEW_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool


PLANNING_PROMPT = SystemMessage(
    content="""Use a step-by-step planning process for every travel request.
First summarize travel goals and assumptions.
Then gather facts using tools where appropriate.
Create a day-by-day itinerary, lodging, dining, transport, and cost sections.
Finally, provide a short review of feasibility and budget accuracy.
If you need weather, place details, currencies, or calculations, use the available tools explicitly.
Return the answer in clean Markdown with fixed sections."""
)


class GraphBuilder():
    def __init__(self, model_provider: str = "groq"):
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()
        
        self.tools = []
        
        self.weather_tools = WeatherInfoTool()
        self.place_search_tools = PlaceSearchTool()
        self.calculator_tools = CalculatorTool()
        self.currency_converter_tools = CurrencyConverterTool()
        
        self.tools.extend([
            *self.weather_tools.weather_tool_list,
            *self.place_search_tools.place_search_tool_list,
            *self.calculator_tools.calculator_tool_list,
            *self.currency_converter_tools.currency_converter_tool_list,
        ])
        
        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        
        self.graph = None
        
        self.system_prompt = SYSTEM_PROMPT
        self.planning_prompt = PLANNING_PROMPT
        self.review_prompt = REVIEW_PROMPT

    def agent_function(self, state: MessagesState):
        user_question = state["messages"]
        input_question = [self.system_prompt, self.planning_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        return {"messages": [response]}

    def review_plan(self, plan_text: str) -> str:
        review_input = [self.system_prompt, self.review_prompt, HumanMessage(content=plan_text)]
        review_response = self.llm.invoke(review_input)
        if hasattr(review_response, 'content'):
            return review_response.content
        return str(review_response)

    def build_graph(self):
        graph_builder = StateGraph(MessagesState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge("agent", END)

        self.graph = graph_builder.compile()
        return self.graph

    def __call__(self):
        return self.build_graph()