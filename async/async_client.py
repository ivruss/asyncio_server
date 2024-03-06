import asyncio
import random
from pathlib import Path
import time
from datetime import datetime

def get_current_timestamp(with_date = True):
    current_time = time.time()
    datetime_object = datetime.fromtimestamp(current_time)
    if with_date == True:
        timestamp = datetime_object.strftime("%Y:%m:%d;%H:%M:%S.%f")[:-3]
    else:
        timestamp = datetime_object.strftime("%H:%M:%S.%f")[:-3]
    
    return timestamp


async def send_requests(reader, writer, client_num):
    number = 0
    log_file_path = Path(f"{client_num}_client_logs.txt")
    
    with log_file_path.open(mode="a") as logs:
        while True:
            message = (f"[{number}] PING\n").encode()
            number+=1
            
            writer.write(message)
            await writer.drain()
            sending_timestamp = get_current_timestamp()
            
            try:
                data = await asyncio.wait_for(reader.read(100), timeout=3)
                response = data.decode()
                
                response_timestamp = get_current_timestamp(with_date=False)
                
                if response != "keepalive":
                    logs_str = f"{sending_timestamp};{message};{response_timestamp};{response}"
                    logs.write(logs_str)
                else:
                    logs_str = f"{response_timestamp};{response}"
                
            except:
                timeout_timestamp = get_current_timestamp(with_date=False)

                logs_str = f"{sending_timestamp};{message.decode()};{timeout_timestamp};TIMEOUT"
                logs.write(logs_str)
                
            await asyncio.sleep(random.uniform(0.3, 3))

    await keepalive_task

async def main():
    reader1, writer1 = await asyncio.open_connection('127.0.0.1', 8888)
    reader2, writer2 = await asyncio.open_connection('127.0.0.1', 8888)
    
    await asyncio.gather(send_requests(reader1, writer1, 1), send_requests(reader2, writer2, 2))

if __name__ == '__main__':
    asyncio.run(main())