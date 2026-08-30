import asyncio




async def fetch_data(name: str, delay: float) -> str:
    """模拟异步获取数据（比如调 API）"""
    print(f"开始获取 {name}...")
    await asyncio.sleep(delay)      # 模拟网络延迟（不阻塞！）
    print(f"完成获取 {name}")
    return f"{name} 的数据"


async def main():
    # TODO 1: 串行调用（await 一个等一个）
    # 计算一下：串行跑 3 个 delay=1 的任务，大约要几秒？
    r1 = await fetch_data("A",1)
    r2 = await fetch_data("B",1)
    r3 = await fetch_data("C",1)
    print("串行结果：",[r1,r2,r3])

    # TODO 2: 用 asyncio.gather 并发调用同样 3 个任务
    result = await asyncio.gather(
        fetch_data("D",1),
        fetch_data("E",1),
        fetch_data("F",1),
    )
    print("并发结果",result)


    # 这些语法知识当时学习的时候一笔带过了，现在忘记了，这些是我看笔记写的，等等你再帮我复习一下这方面的知识吧
    # 计算一下：并发跑 3 个 delay=1 的任务，大约要几秒？
    pass


# 运行
asyncio.run(main())
