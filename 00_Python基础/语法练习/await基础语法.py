import asyncio
import time


async def 任务(名字, 耗时):
    print(f"[{名字}] 开始")
    await asyncio.sleep(耗时)  # 异步等待
    print(f"[{名字}] 完成（耗时 {耗时}s）")
    return f"{名字}的结果"


async def main():
    开始 = time.time()

    # 三个任务同时跑，总耗时 = 最长的那个
    结果 = await asyncio.gather(
        任务("A", 2),
        任务("B", 1),
        任务("C", 3)
    )
    # main() 里遇到 asyncio.gather(...)→ 把三个 任务() 协程同时注册到事件循环
    print(f"全部完成，总耗时: {time.time() - 开始:.1f}s")
    print(f"结果: {结果}")


asyncio.run(main())
