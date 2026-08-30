from typing import Callable, Dict, List, Optional

# TODO 1: 参数是 {str: function} 的工具注册表
def register_tools(tool_dict :dict[str, Callable[[str],str]])->None:
    # → Dict[str, Callable[[str], str]]
    pass

# TODO 2: 过滤消息列表，返回过滤后的列表
def filter_messages(messages :list[dict[str,str]], role:str)->list[dict[str,str]]:
    # messages: List[Dict[str, str]]，role: str
    # 返回: List[Dict[str, str]]
    return [m for m in messages if m["role"] == role]


# TODO 3: 执行一个工具函数，传入输入数据
def execute_tool(tool_func : Callable[[str],str], input_data:str)->str:
    # tool_func: Callable[[str], str]，input_data: str
    # 返回: str
    return tool_func(input_data)
