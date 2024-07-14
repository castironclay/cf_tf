from jinja2 import Environment, FileSystemLoader

types = {
    "cfd_debian_64bit": "cfd_debian_64bit.sh.j2",
    "cfd_debian_arm64bit": "cfd_debian_arm64bit.sh.j2",
    "cfd_docker": "cfd_docker.sh.j2",
    "warp_debian_setup": "warp_setup_debian.sh.j2",
}


def render(type: str, values: dict) -> str:
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template(types.get(type))

    content = template.render(values)

    return content
