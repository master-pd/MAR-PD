import asyncio
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Callable, Any
import time

class Scheduler:
    def __init__(self):
        self.tasks: Dict[str, Dict] = {}
        self.running = False
        self.thread = None
    
    def add_task(self, name: str, interval: int, callback: Callable, *args, **kwargs):
        """টাস্ক যোগ"""
        self.tasks[name] = {
            'interval': interval,
            'callback': callback,
            'args': args,
            'kwargs': kwargs,
            'last_run': None
        }
    
    def remove_task(self, name: str):
        """টাস্ক রিমুভ"""
        if name in self.tasks:
            del self.tasks[name]
    
    def start(self):
        """শিডিউলার শুরু"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
    
    def stop(self):
        """শিডিউলার বন্ধ"""
        self.running = False
        if self.thread:
            self.thread.join()
    
    def _run_scheduler(self):
        """শিডিউলার রান"""
        while self.running:
            current_time = datetime.now()
            
            for name, task in self.tasks.items():
                if task['last_run'] is None:
                    # প্রথমবার রান
                    task['last_run'] = current_time
                    self._execute_task(name, task)
                else:
                    # ইন্টারভাল চেক
                    time_diff = (current_time - task['last_run']).total_seconds()
                    if time_diff >= task['interval']:
                        task['last_run'] = current_time
                        self._execute_task(name, task)
            
            time.sleep(1)  # প্রতি সেকেন্ডে চেক
    
    def _execute_task(self, name: str, task: Dict):
        """টাস্ক এক্সিকিউট"""
        try:
            task['callback'](*task['args'], **task['kwargs'])
        except Exception as e:
            print(f"Error executing task {name}: {e}")
    
    def add_daily_task(self, name: str, hour: int, minute: int, callback: Callable, *args, **kwargs):
        """ডেইলি টাস্ক যোগ"""
        def daily_wrapper():
            now = datetime.now()
            if now.hour == hour and now.minute == minute:
                callback(*args, **kwargs)
        
        self.add_task(name, 60, daily_wrapper)  # প্রতি মিনিটে চেক
    
    async def async_add_task(self, name: str, interval: int, callback: Callable, *args, **kwargs):
        """এসিংক্রোনাস টাস্ক যোগ"""
        async def async_wrapper():
            while self.running:
                await asyncio.sleep(interval)
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(*args, **kwargs)
                    else:
                        callback(*args, **kwargs)
                except Exception as e:
                    print(f"Error in async task {name}: {e}")
        
        asyncio.create_task(async_wrapper())

# গ্লোবাল শিডিউলার
scheduler = Scheduler()