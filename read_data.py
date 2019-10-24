import app

reader = app.OpenBCI(chunk_size=50,createSession=False)

while True:
	data = reader.read_chunk()
	print(data.mean())
