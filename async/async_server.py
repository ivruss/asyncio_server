import asyncio
import random
from pathlib import Path
import time
from datetime import datetime

gl_client_id = 1
answer_num = 0
request_num = 0

async def keepalive(writer):
    while True:
        await asyncio.sleep(5)
        writer.write(b"keepalive\n")
        await writer.drain()


def get_current_timestamp(with_date=True):
    current_time = time.time()
    datetime_object = datetime.fromtimestamp(current_time)
    
    if with_date == True:
        timestamp = datetime_object.strftime("%Y:%m:%d;%H:%M:%S.%f")[:-3]
    else:
        timestamp = datetime_object.strftime("%H:%M:%S.%f")[:-3]
        
    return timestamp


async def handle_client(reader, writer):
    global gl_client_id
    global answer_num
    global request_num
    
    client_id = gl_client_id
    gl_client_id+=1
    
    log_file_path = Path("server_logs.txt")
    
    keepalive_task = asyncio.create_task(keepalive(writer))
    
    with log_file_path.open(mode="a") as logs:
        while True:
            data = await reader.read(100)
            request_num+=1
            
            recieve_timestamp = get_current_timestamp()
            message = data.decode()
            
            if random.random() < 0.1:
                logs_str = f"{recieve_timestamp};{message};IGNORED;IGNORED"
                logs.write(f"{logs_str}\n")
                continue
                
            else:
                response = (f"[{answer_num}] PONG ({client_id})\n").encode()
                answer_num+=1
                writer.write(response)
                await writer.drain()
                
                response_timestamp = get_current_timestamp(with_date=False)
                
                logs_str = f"{recieve_timestamp};{message};{response_timestamp};{response.decode()}"
                logs.write(f"{logs_str}\n")



async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 8888)

    async with server:
        try:
            await asyncio.wait_for(server.serve_forever(), timeout=300)
            
        except:
            print("5 минут прошли. Сервер отключен")
    

if __name__ == '__main__':
    asyncio.run(main())