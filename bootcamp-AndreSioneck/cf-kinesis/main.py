import boto3
import json
import random
from datetime import timedelta
from fake_web_events import Simulation

# Monkeypatch Simulation.wait to fix TypeError: 'float' object cannot be interpreted as an integer in Python 3.12
def patched_wait(self):
    offset = int(self.batch_size * 0.3)
    random_offset = random.randrange(-offset, offset) if offset > 0 else 0
    self.cur_time += timedelta(seconds=self.batch_size + random_offset)
    self.rate = self.get_rate_per_step()

Simulation.wait = patched_wait

client =  boto3.client('firehose', region_name='us-east-1')

def put_record(event):
    data = json.dumps(event) + '\n'
    response = client.put_record(
        DeliveryStreamName='kinesis-firehose-fake-web-events',
        Record={'Data': data}
    )
    print(event)
    return response

simulation = Simulation(user_pool_size=100, sessions_per_day=10000)
events = simulation.run(duration_seconds=300)

for event in events:
    put_record(event)