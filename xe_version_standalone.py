import sys
import radkit_genie as rkg
from radkit_client.sync import create_context, sso_login
from prettytable import PrettyTable

service_id = input("Service ID: ")

# service_id = input("Service ID: ")


def get_ver_uptime():

    client = sso_login()
    service = client.service(service_id).wait()

    xe_routers = service.inventory.filter("device_type", "IOS_XE")
    versions = xe_routers.exec("show version").wait()
    parsed_versions = rkg.parse(versions, os="iosxe")

    ver_table = PrettyTable(["Hostname", "Version", "Uptime"])

    for name, output in parsed_versions.items():
        if output["show version"].data:
            ver_table.add_row(
                [
                    name,
                    output["show version"].data["version"]["xe_version"],
                    output["show version"].data["version"]["uptime"],
                ]
            )

    print(ver_table)


def main():
    with create_context():
        get_ver_uptime()


if __name__ == "__main__":
    main()
