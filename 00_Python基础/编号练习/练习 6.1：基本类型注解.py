from typing import Optional
# TODO: 为以下函数添加完整的类型注解（参数 + 返回值）

def greet(name:str)->str:
    return f"Hello, {name}"
    # → 参数: name: str，返回: str

def find_user(users:list[dict], user_id:int)->Optional[dict]:
    # users 是 List[dict]，user_id 是 int
    # 找到返回该 dict，找不到返回 None → Optional[dict] 或 dict | None
    for u in users:
        if u["id"] == user_id:
            return u
    return None

def process_scores(scores:list[int])->dict[str, float]:
    # scores 是 List[int]，返回 Dict[str, float]
    return {"avg": sum(scores) / len(scores), "max": max(scores)}
