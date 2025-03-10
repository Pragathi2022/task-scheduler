
class TaskScheduler:
    def _init_(self, tasks, dependencies, durations):
        self.tasks = tasks
        self.dependencies = dependencies
        self.durations = durations
        self.graph = defaultdict(list)
        self.indegree = {task: 0 for task in tasks}
        self.est = {task: 0 for task in tasks}
        self.eft = {task: 0 for task in tasks}
        self.lst = {task: float('inf') for task in tasks}
        self.lft = {task: float('inf') for task in tasks}
        
        self._build_graph()
        
    def _build_graph(self):
        for dep in self.dependencies:
            prereq, task = dep
            self.graph[prereq].append(task)
            self.indegree[task] += 1
    
    def _topological_sort(self):
        topo_order = []
        q = deque([task for task in self.tasks if self.indegree[task] == 0])
        
        while q:
            task = q.popleft()
            topo_order.append(task)
            
            for neighbor in self.graph[task]:
                self.indegree[neighbor] -= 1
                if self.indegree[neighbor] == 0:
                    q.append(neighbor)
        
        return topo_order
    
    def _forward_pass(self, topo_order):
        for task in topo_order:
            self.eft[task] = self.est[task] + self.durations[task]
            for neighbor in self.graph[task]:
                self.est[neighbor] = max(self.est[neighbor], self.eft[task])
    
    def _backward_pass(self, topo_order):
        project_completion_time = max(self.eft.values())
        
        for task in self.tasks:
            self.lst[task] = project_completion_time - self.durations[task]
            self.lft[task] = project_completion_time
        
        for task in reversed(topo_order):
            for neighbor in self.graph[task]:
                self.lft[task] = min(self.lft[task], self.lst[neighbor])
                self.lst[task] = self.lft[task] - self.durations[task]
    
    def schedule(self):
        topo_order = self._topological_sort()
        self._forward_pass(topo_order)
        self._backward_pass(topo_order)
        
        earliest_completion = max(self.eft.values())
        latest_completion = max(self.lft.values())
        
        return earliest_completion, latest_completion

# Example Usage:
tasks = ['A', 'B', 'C', 'D', 'E']
dependencies = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('D', 'E')]
durations = {'A': 3, 'B': 2, 'C': 4, 'D': 2, 'E': 3}

scheduler = TaskScheduler(tasks, dependencies, durations)
earliest_completion, latest_completion = scheduler.schedule()

print(f"Earliest time all tasks will be completed: {earliest_completion}")
print(f"Latest time all tasks will be completed: {latest_completion}")
