import json

FILENAME = "sample-data.json"

def print_table(rows):
    print("Interface Status")
    print("=" * 80)
    print(f'{"DN":50}  {"Description":20}  {"Speed":6}  {"MTU":5}')
    print(f'{"-"*50}  {"-"*20}  {"-"*6}  {"-"*5}')

    for dn, descr, speed, mtu in rows:
        print(f"{dn:50}  {descr:20}  {speed:6}  {mtu:5}")

def main():
    with open(FILENAME, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for item in data.get("imdata", []):
        attrs = item.get("l1PhysIf", {}).get("attributes", {})
        dn = attrs.get("dn", "")
        descr = attrs.get("descr", "")
        speed = attrs.get("speed", "")
        mtu = attrs.get("mtu", "")
        rows.append((dn, descr, speed, mtu))

    print_table(rows)

if __name__ == "__main__":
    main()