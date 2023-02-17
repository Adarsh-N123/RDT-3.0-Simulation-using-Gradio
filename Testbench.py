# Simulation Testbench
#
# Author: Neha Karanjkar


import simpy
from Applications import SendingApplication,ReceivingApplication
from Channel import UnreliableChannel
from Protocol_rdt2 import *
import gradio as gr
#from gradio import logs
#gr.config['interface']['theme'] = 'compact'
import matplotlib.pyplot as plt
import numpy as np

def plot_lineplot(x, y):
    # Create data
    x = np.array(x)
    y = np.array(y)
    
    # Create figure and plot
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel('Pc or Pl')
    ax.set_ylabel('T_Avg')
    ax.set_title('Line Plot')

    # Convert plot to image and return
    fig.canvas.draw()
    img = np.array(fig.canvas.renderer.buffer_rgba())
    return img


import logging
import io

# Create a logger with the name of the app
logger = logging.getLogger('Logging App')

# Set the logging level to DEBUG to capture all log messages
logger.setLevel(logging.DEBUG)

# Create a custom formatter to format log messages
formatter = logging.Formatter('%(message)s')

# Create an in-memory buffer to store log messages
log_buffer = io.StringIO()

# Create a custom stream handler to write logs to the in-memory buffer
class LogHandler(logging.StreamHandler):
    def emit(self, record):
        msg = self.format(record)
        log_buffer.write(msg + '\n')

# Create a log handler to write logs to the in-memory buffer
log_handler = LogHandler()

# Set the formatter for the log handler
log_handler.setFormatter(formatter)

# Add the log handler to the logger
logger.addHandler(log_handler)













def function_rdt(one,two,three,four,five,six,seven):
# Create a simulation environment
	env=simpy.Environment()

	# Populate the simulation environment with objects:
	sending_app	  = SendingApplication(env)
	sending_app.logger = logger
	receiving_app = ReceivingApplication(env)
	receiving_app.logger = logger
	rdt_sender	  = rdt_Sender(env)
	rdt_sender.logger = logger
	
	rdt_receiver  = rdt_Receiver(env)
	rdt_receiver.logger = logger
	delayone = two
	channel_for_data  = UnreliableChannel(env=env,Pc=three,Pl=four,delay=delayone,name="DATA_CHANNEL")
	channel_for_data.logger = logger
	channel_for_ack	  = UnreliableChannel(env=env,Pc=five,Pl=six,delay=delayone,name="ACK_CHANNEL")
	channel_for_ack.logger = logger

	rdt_sender.timeout_value = one

	# connect the objects together
	# .....forward path...
	sending_app.rdt_sender = rdt_sender
	rdt_sender.channel = channel_for_data
	channel_for_data.receiver = rdt_receiver
	rdt_receiver.receiving_app = receiving_app
	# ....backward path...for acks
	rdt_receiver.channel = channel_for_ack
	channel_for_ack.receiver = rdt_sender

	# Run simulation
	env.run(until=seven)
	return log_buffer.getvalue()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
def function_rdt_graph(one,two,three,four,five,six,seven,eight,nine,ten):
	L=[]
	L1=[]
	L2=[]
	j=0
	i=0
	while 0<=j<=0.9:
# Create a simulation environment
		env=simpy.Environment()

		# Populate the simulation environment with objects:
		sending_app	  = SendingApplication(env)
		sending_app.logger = logger
		receiving_app = ReceivingApplication(env)
		receiving_app.logger = logger
		rdt_sender	  = rdt_Sender(env)
		rdt_sender.logger = logger
		
		rdt_receiver  = rdt_Receiver(env)
		rdt_receiver.logger = logger
		delayone = two
		channel_for_data  = UnreliableChannel(env=env,Pc=three,Pl=j,delay=delayone,name="DATA_CHANNEL")
		channel_for_data.logger = logger
		channel_for_ack	  = UnreliableChannel(env=env,Pc=five,Pl=j,delay=delayone,name="ACK_CHANNEL")
		channel_for_ack.logger = logger

		rdt_sender.timeout_value = one

		# connect the objects together
		# .....forward path...
		sending_app.rdt_sender = rdt_sender
		rdt_sender.channel = channel_for_data
		channel_for_data.receiver = rdt_receiver
		rdt_receiver.receiving_app = receiving_app
		# ....backward path...for acks
		rdt_receiver.channel = channel_for_ack
		channel_for_ack.receiver = rdt_sender

		L2.append(j)
		while rdt_receiver.receiving_app.total_packets_received<nine:
		# Run simulation
			env.run(until=i+1)
			i = i+1
			L.append(rdt_sender.rtt)
		L1.append(np.array(L).mean())
		j = j+ten
		# Run simulation
		#env.run(until=seven)
	return [L1,L2,log_buffer.getvalue()]
	
	
def run(one,two,three,four,five,six,seven,eight,nine,ten):
	if eight==True:
		answer = function_rdt_graph(one,two,three,four,five,six,seven,eight,nine,ten)
		answerone = plot_lineplot(answer[1],answer[0])
		return [answer[2],np.array(answerone)]
	else:
		return [function_rdt(one,two,three,four,five,six,seven),np.array([255])]
	

	
inputs = [
    gr.inputs.Slider(0,50,label="Timeout"),
    gr.inputs.Slider(0,10,label="Delay"),
    gr.inputs.Slider(0, 1, label="pc"),
    gr.inputs.Slider(0, 1, label="pl"),
    gr.inputs.Slider(0, 1, label="pc-Ack"),
    gr.inputs.Slider(0, 1, label="pl-Ack"),
    gr.inputs.Slider(0,1000,label="Time of simulation"),
    gr.inputs.Checkbox(label="Want to draw a graph for t_avg?(only fill below if yes)"),
    gr.inputs.Slider(0,1000,label="Total no of Packets to be sent"),
    gr.inputs.Slider(0,0.1,label="increment of pc or pl")
]

#outputs = gr.outputs.Logs()
outputs = [
    #gr.outputs.Textbox(),
    gr.outputs.Textbox(label="Logs"),
    gr.outputs.Image(type="numpy",label="graph")
]

#logs.enable()

app = gr.Interface(fn=run, inputs=inputs, outputs=outputs,title = "RDT-3.0 Simulation",description="RDT-3.0 SIMULATOR",article="This app provides a breif idea on how the rdt 3.0 protocol works by simulating the given situation in a simpy environment")
app.launch()


