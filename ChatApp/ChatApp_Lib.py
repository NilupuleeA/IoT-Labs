from paho.mqtt import client as mqtt_client
import tkinter as tk
import time

# Global variable for MQTT client
client = None

def on_send():
    global client
    # Get the name and message from the entry widgets
    name = entry1.get()
    msg = entry3.get()
    
    # Format the message to include the sender's name
    formatted_message = f"{name}: {msg}"

    # Publish the formatted message
    if client and client.is_connected():
        topic = entry2.get()
        client.publish(topic, formatted_message)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        topic = entry2.get()
        if topic:
            client.subscribe(topic)  # Subscribe to the receive topic
    else:
        print(f"Connection failed with code {rc}")

def on_receive(client, userdata, msg):
    # Decode the received message
    message = str(msg.payload.decode("utf-8"))
    
    # Split the message into name and body
    if ':' in message:
        name, body = message.split(':', 1)
        text_area.insert(tk.END, f"{name.strip()} \t>>\t{body.strip()}\n")
    else:
        # Handle cases where the message format is incorrect
        text_area.insert(tk.END, f"Anonymous\t>>\t{message}\n")

def connect_mqtt():
    global client
    client = mqtt_client.Client()  # Use default constructor

    # Set the callback functions
    client.on_connect = on_connect
    client.on_message = on_receive

    # Connect to the MQTT broker
    broker_address = "test.mosquitto.org"  # broker's address
    broker_port = 1883
    keepalive = 5
    client.connect(broker_address, broker_port, keepalive)
    client.loop_start()

app = tk.Tk()
app.title("Chat App")
app.geometry("600x400")

bar_frame = tk.Frame(app)
bar_frame.pack(pady=20)
bottom_frame = tk.Frame(app)
bottom_frame.pack(pady=10, fill=tk.X, side=tk.BOTTOM)

# Place labels, entries and button in the top frame
label1 = tk.Label(bar_frame, text="Name:")
label1.grid(row=0, column=0, padx=5)
entry1 = tk.Entry(bar_frame)
entry1.grid(row=0, column=1, padx=5)

label2 = tk.Label(bar_frame, text="Topic:")
label2.grid(row=0, column=2, padx=5)
entry2 = tk.Entry(bar_frame)
entry2.grid(row=0, column=3, padx=5)

button = tk.Button(bar_frame, text="Connect", command=connect_mqtt)
button.grid(row=0, column=4, padx=5)

# Place an entry and button in the bottom frame
entry3 = tk.Entry(bottom_frame)
entry3.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

button_send = tk.Button(bottom_frame, text="Send", command=on_send)
button_send.pack(side=tk.LEFT, padx=5, pady=5)

# Text area
text_area = tk.Text(app, height=10, font=("Arial", 10))
text_area.pack(pady=20, fill=tk.BOTH, expand=True)

# Run the application
def on_closing():
    global client
    if client:
        client.loop_stop()
        client.disconnect()
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
