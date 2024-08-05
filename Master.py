import time
from threading import Thread
from Pod import Pod

class MasterNode:
    def __init__(self):
        self.pods = []
        self.deployment_active = True
    
    def add_pod(self, pod):
        self.pods.append(pod)
        thread = Thread(target=pod.process_requests)
        thread.start()

    def remove_pod(self, pod_name):
        self.pods = [pod for pod in self.pods if pod.name != pod_name]

    def balance_requests(self, request):
        for pod in self.pods:
            if pod.add_request(request):
                print(f"Request {request} assigned to {pod.name}")
                return
        print(f"No available pods to handle request {request}")

    def scale_pods(self, num_pods):
        if num_pods > len(self.pods):
            for i in range(num_pods - len(self.pods)):
                new_pod = Pod(f"pod-{len(self.pods) + 1}")
                self.add_pod(new_pod)
                print(f"Added {new_pod.name}")
        else:
            for i in range(len(self.pods) - num_pods):
                pod_name = self.pods[-1].name
                self.remove_pod(pod_name)
                print(f"Removed {pod_name}")

    def monitor_pods(self):
        while self.deployment_active:
            for pod in self.pods:
                if len(pod.requests) + len(pod.processing) > 8:
                    print(f"High load on {pod.name}. Scaling up...")
                    self.scale_pods(len(self.pods) + 1)
            time.sleep(5)
