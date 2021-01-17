import json
from multiprocessing.pool import ThreadPool
import os
from rich.console import Console

console = Console()

def estrai_json(common_ports):
    with open(common_ports, "r") as file:
        data = json.load(file)
    return data

def multithread(funzione, iterabile, lunghezza):
    number_of_workers = os.cpu_count() # numero di cpu nel PC
    print(f"Scannerizzo con {number_of_workers} workers...")
    with  ThreadPool(number_of_workers) as pool:
        try:
            for indice_loop, _ in enumerate(pool.imap(funzione, iterabile)):
                progress = (indice_loop / lunghezza) * 100
                console.print(f"Scan in corso: [bold green]{progress:.2f}%[/bold green]", end="\r")
        except KeyboardInterrupt:
            console.print("\nexiting...", style="italic red")
