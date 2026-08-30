import aiohttp
import asyncio
import time


async def 获取用户(session, uid):
    """获取单个用户"""
    try:
        async with session.get(
                f"https://jsonplaceholder.typicode.com/users/{uid}",  # ✅ 真实 API
                timeout=aiohttp.ClientTimeout(total=10)  # ✅ 加超时
        ) as resp:
            await resp.raise_for_status()  # ✅ 加 await
            return await resp.json()
    except aiohttp.ClientError as e:
        print(f"❌ 用户 {uid} 获取失败: {e}")
        return None


async def main():
    开始 = time.time()
    ids = list(range(1, 11))

    async with aiohttp.ClientSession() as session:
        用户列表 = await asyncio.gather(
            *[获取用户(session, uid) for uid in ids],
            return_exceptions=True  # ✅ 单个失败不影响整体
        )

    # 过滤掉失败的（None）
    成功的用户 = [u for u in 用户列表 if u is not None]

    print(f"获取了 {len(成功的用户)} 个用户（共 {len(ids)} 个）")
    print(f"总耗时: {time.time() - 开始:.1f}s")


asyncio.run(main())
