from rich.console import Console
from rich.table import Table

import socket
import sys
from utility import estrai_json, multithread


console = Console()


class Pscanner:

    common_ports = "common_ports.json" # file JSON con porte da scannerizare

    def __init__(self):
        self.porte_aperte = []
        self.port_to_check = {}
        self.ip_address = ""

    def chiavi_json_int(self):
        data = estrai_json(Pscanner.common_ports)
        self.port_to_check = { int(k):v for k,v in data.items() } # traformo chiavi del file json estratto in INT per passarle come porte a scan_port


    def get_ip(self, target):
        try:
            self.ip_address = socket.gethostbyname(target) # ottengo IP da Target
        except socket.gaierror as error:
            console.print(f"Errore nel reperire l'indirizzo ip...[italic red]{error}[/italic red]")
            sys.exit()


    def inizializza(self):
        console.print("[cyan]PORT SCANNER TCP MULTITHREAD[/cyan]")
        print()
        target = input("Inserisci Target: ")
        self.get_ip(target)
        self.chiavi_json_int()
        try:
            console.input("\nPort Scanner pronto! Premi ENTER per avviare la scansione...")
        except KeyboardInterrupt:
            console.print("exiting...", style="italic red")
            sys.exit()
        else:
            self.run()


    def run(self):
        multithread(self.scan_port, self.port_to_check.keys(), len(self.port_to_check.keys()))
        self.show_port()


    def scan_port(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creo socket famiglia IPv4, e di tipo TCP
        conn_status = sock.connect_ex((self.ip_address, port)) # AF_INET vuole una tupla
        if conn_status == 0:    # connect_ex torna 0 se la connessione è andata a buon fine
            self.porte_aperte.append(port)
            sock.close()


    def show_port(self):
        if self.porte_aperte:
            table = Table(show_header = True, style="bold blue")
            table.add_column("Porta", style="green")
            table.add_column("Stato", style="green")
            table.add_column("Servizio", style="green")
            console.print("Porte Aperte:", style="bold green")
            for port in self.porte_aperte:
                table.add_row(str(port), "OPEN", self.port_to_check[port] )
            console.print(table)
            input()
        else:
            console.print("Non sono state trovate porte aperte!", style="bold magenta")
            input()


if __name__ == "__main__":
    pscan = Pscanner()
    pscan.inizializza()
