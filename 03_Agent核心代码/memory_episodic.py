"""2.5b 情景记忆：SQLite 结构化存储"""
import sqlite3
from datetime import datetime


DB_PATH = "memory.db"

def init_db(db_path: str = DB_PATH)->sqlite3.Connection:
    """初始化数据库：建 episodes 表，返回连接对象"""
    # TODO 1：五步走 —— connect → cursor → execute → commit → return conn
    #   SQL 我给你（建表语句）
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS episodes (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,  -- 自增主键
                student_id  TEXT NOT NULL,                      -- 学生 ID
                started_at  TEXT NOT NULL,                      -- 会话开始时间
                topic       TEXT,                               -- 学习的知识点
                summary     TEXT,                               -- 本次会话摘要
                difficulty  TEXT,                               -- 遇到的困难
                score       REAL                                -- 练习得分
            )
        """)
    conn.commit()
    return conn

def save_episode(conn,student_id,topic,summary,difficulty,score)->int:
    """写入一条会话摘要，返回自增 id"""
    cur = conn.cursor()
    # TODO 2：执行 INSERT（注意用 ? 占位符，参数放第二个参数的元组里）

    cur.execute(
        "INSERT INTO episodes (student_id, started_at, topic, summary, difficulty, score)"
        " VALUES (?, ?, ?, ?, ?, ?)",
        (student_id, datetime.now().isoformat(), topic, summary, difficulty, score),
    )
    conn.commit()
    return cur.lastrowid# 拿到刚插入那行的自增 id,这个自增ID是什么为什么是9


def query_episodes(conn,student_id,limit: int = 5)->list:
    """查询某学生最近 limit 条会话（按时间倒序）"""
    cur = conn.cursor()
    # TODO 3：执行 SELECT，然后取结果
    cur.execute(
        "SELECT id,started_at,topic,summary,score FROM episodes "
        "WHERE student_id = ? ORDER BY started_at DESC LIMIT ?",#ORDER BY started_at DESC = 按时间倒序
        (student_id,limit),
    )
    return cur.fetchall()#读操作用 fetchall 取结果



# ── 测试 ──
if __name__=="__main__":
    conn = init_db()
    eid1 = save_episode(conn, "stu001", "二次方程",
                        "讲解求根公式，练习 5 题", "判别式符号判断总错", 60.0)
    eid2 = save_episode(conn, "stu001", "因式分解",
                        "复习十字相乘，练习 8 题", "基础薄弱但进步明显", 85.0)
    eid3 = save_episode(conn, "stu002", "勾股定理",
                        "讲解定理证明，练习 3 题", "无", 92.0)

    print(f"已写入 3 条，最后一条 id = {eid3}")

    print("\n--- stu001 的历史会话（按时间倒序）---")
    for row in query_episodes(conn, "stu001"):
        print(f"  id={row[0]} | {row[1][:19]} | {row[2]} | 得分 {row[4]}")# 取字段要用下标 row[0]、row[2]，不是字典的 row["topic"]

    conn.close()
