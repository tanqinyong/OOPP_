from scaledrone import ScaleDrone
import json

drone = ScaleDrone('SNazg8KrKdwSphWf', 'fCw1xxKBLoYBFZuif4vRKgK3ibIdH6mk')
room = 'observable-room'
message = {'foo': 'bar'}
response = drone.publish(room, json.dumps(message))
print(response)