import asyncio


async def fetch_one(i: int) -> str:
    await asyncio.sleep(1)  # 模拟每个请求 1 秒
    return f"任务{i}完成"


async def bounded_fetch(total: int, max_concurrent: int = 3) -> list:
    """
    TODO: 同时最多 max_concurrent 个并发请求
    - 用 asyncio.Semaphore 限制并发数
    - 返回所有结果的列表

    使用方式:
        semaphore = asyncio.Semaphore(max_concurrent)
        async with semaphore:      # 占用一个"名额"
            result = await fetch_one(i)
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def worker(i: int) -> str:
        async with semaphore:  # ← 拿名额，满了就排队等
            return await fetch_one(i)

     # TODO: 用 asyncio.gather 并发跑 total 个 worker

    tasks = [worker(i) for i in range(total)]
    result = await asyncio.gather(*tasks)
    return result
    pass


async def main():
    results = await bounded_fetch(6, max_concurrent=3)
    for r in results:
        print(r)


asyncio.run(main())
