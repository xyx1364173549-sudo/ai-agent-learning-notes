from functools import wraps
import json
def log_action(func):
    @wraps(func)
    def wrapper(self,*args, **kwargs):
        result = func(self, *args, **kwargs)  # 先执行原方法
        action = func.__name__  # 方法名（add_task/mark_done...）
        print(f"[日志] {action} -> {'成功' if result else '失败'} (共{len(self._tasks)}个任务)")
        return result

    return wrapper


class Task:
    def __init__(self, title: str, done=False):
        self.title = title.strip()
        self.done = done


    def __call__(self):
        self.done = True
        return self


    def __str__(self):

       return f"[✓] {self.title}" if self.done else f"[○] {self.title}"


    def __repr__(self):
        return f"Task({self.title!r}, done={self.done!r})"

    def to_dict(self)->dict:
        data = {"title": self.title, "done": self.done}
        return data

    @classmethod
    def from_dict(cls, data: dict)->"Task":
        return cls(title=data["title"], done=data.get("done",False))


class TaskManager:
    def __init__(self):
        self._tasks: list[Task] = []
        # 这上下两种写法有什么区别，下面的这个好像写出来没有用，它没有和上面的Task产生连接，像是单独出来的一个列表，我只能这样很浅显的理解，可是我还是不清楚，但是我这样写下面的函数似乎没有收到什么影响
        # self._tasks = []

    @log_action
    def add_task(self, title:str)->Task:
        """添加任务，返回新创建的 Task"""
        task = Task(title)
        self._tasks.append(task)
        return task

    @log_action
    def mark_done(self,index:int)->bool:
        """标记第 index 个任务完成（序号从 1 开始）"""
        if 1<=index<=len(self._tasks):
            self._tasks[index-1]()
            return True
        return False

    @log_action
    def delete_task(self, index:int)->bool:
        """删除第 index 个任务"""
        if 1<=index<=len(self._tasks):
            del self._tasks[index-1]
            return True
        return False


    def pending_tasks(self) -> list[Task]:
        """返回未完成的任务"""
        return [task for task in self._tasks if not task.done]

    
    def completed_tasks(self) -> list[Task]:
        """返回已完成的任务"""
        return [task for task in self._tasks if task.done]

    def __len__(self)->int:
        # 支持 len(manager)
        return len(self._tasks)
    def __iter__(self):
        # 支持 for task in manager 遍历
        return iter(self._tasks)
    def __getitem__(self, index:int):
        # 支持 manager[0] 下标访问
        return self._tasks[index]

    def __str__(self)->str:
        """支持 print(manager)：显示带序号的任务列表"""
        if not self._tasks:
            return "（空，暂无任务）"
        else:
            # 这一部分有点看不懂，解释一下，join()这个函数是干什么的
            lines = [f"  {i}. {task}" for i, task in enumerate(self._tasks, 1)]
            # enumerate(["任务A", "任务B", "任务C"], 1)
            # → (1, "任务A") → (2, "任务B") → (3, "任务C")
            # enumerate(列表, 起始数字) = "带着号码牌的遍历"
            return "\n".join(lines)
            # ↑胶水       ↑要拼的列表

            # 结果: "1. 任务A\n2. 任务B\n3. 任务C"
            # 也就是:
            # 1. 任务A
            # 2. 任务B
            # 3. 任务C
    def save(self,filepath:str = "tasks.json")->bool:
        try:
            data = [task.to_dict() for task in self._tasks]
            with open(filepath, "w",encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except OSError as e:
            print(f"[错误] 保存失败: {e}")
            return False
        # data = [task.to_dict() for task in self._tasks]
        # if filepath:
        #     with open(filepath, "w") as f:
        #         json.dump(data,f,ensure_ascii=False,indent=2)
        #         return True
        # return False

    def load(self,filepath:str = "tasks.json")->bool:
        try:
            with open(filepath, "r",encoding="utf-8") as f:
                data = json.load(f)
                self._tasks = [Task.from_dict(item) for item in data]
                return True
        except FileNotFoundError:
            return False

def main():
    manager = TaskManager()
    manager.load()

    print("=== TODO 任务管理器 ===")
    print("命令: add <标题> | done <序号> | delete <序号> | list | pending | completed | save | load | quit")

    while True:
        cmd = input("\n>").strip()
        parts = cmd.split(" ",1)
        action = parts[0].lower()
        if action == "quit":
            print("再见")
            break
        elif action == "add":
            if len(parts) <2:
                print("用法: add <任务标题>")
            else:
                manager.add_task(parts[1])
                print(manager)
        elif action == "list":
            print(manager)
        elif action == "done":
            try:
                n = int(parts[1])
                print(manager.mark_done(n))
            except (ValueError, IndexError):
                print("用法: done <序号>")
        elif action == "delete":
           try:
               n = int(parts[1])
               print(manager.delete_task(n))
           except(ValueError, IndexError):
               print("用法: delete <序号>")

        elif action == "pending":
            for i in manager.pending_tasks():
                print(i)
        elif action == "completed":
            for i in manager.completed_tasks():
                print(i)
        elif action == "save":
            manager.save()
        elif action == "load":
            manager.load()
        else:
            print(f"未知命令: {action}")

        manager.save()







if __name__ == "__main__":
    main()
    pass
