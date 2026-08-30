import asyncio

async def safe_fetch(name: str, fail: bool = False) -> str | None:
    """
    TODO: 在 async 函数中处理异常
    - 如果 fail 为 True，抛出 asyncio.TimeoutError
    - 用 try-except 捕获并返回 None
    - 成功时返回 f"{name} 的数据"
    """
    # ↓ 在这里写你的代码
    try:
        if fail:
            raise asyncio.TimeoutError
        print(f"{name} 的数据")
        return f"{name} 的数据"
    except Exception:
        print(f"{name} 的数据")
        return None





async def main():
    # TODO: 分别调用 safe_fetch("正常", fail=False) 和 safe_fetch("失败", fail=True)
    # 失败的应该返回 None 而不是崩溃
    r1 = await safe_fetch("正常", fail=False)
    r2 = await safe_fetch("失败", fail=True)
    print("正常结果:",r1)
    print("失败结果:",r2)
    pass


asyncio.run(main())
