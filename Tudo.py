import time
import random
from threading import Thread



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



class Pod:
    def __init__(self, name):
        self.name = name
        self.requests = []
        self.processing = []
        self.capacity = 10  # número máximo de processos para rodar
        self.status = 'Rodando'

    # Pod recebe um request e se possuir capacidade aceita
    def add_request(self, request):
        if len(self.requests) < self.capacity:
            self.requests.append(request)
            return True
        else:
            return False

    def process_requests(self):
        while True:
            if (self.requests) and (len(self.processing) < self.capacity):
                request = self.requests.pop(0)
                self.processing.append(request)
                print(f"{self.name} processando a requisicao {request}")
                time.sleep(15)  # Simula o tempo de processamento
                self.processing.remove(request)
                print(f"{self.name} completou a requisicao {request}")
            time.sleep(5)



class LoadGenerator:
    def __init__(self, master):
        self.master = master

    def send_requests(self):
        request_id = 0
        while True:
            self.master.balance_requests(request_id)
            request_id += 1
            time.sleep(random.randint(1, 3))



if __name__ == "__main__":
    master = MasterNode()
    master.scale_pods(3)

    load_generator = LoadGenerator(master)

    monitor_thread = Thread(target=master.monitor_pods)
    monitor_thread.start()

    load_thread = Thread(target=load_generator.send_requests)
    load_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        master.deployment_active = False
        print("Shutting down...")