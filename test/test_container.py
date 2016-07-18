import helper               as hlpr
import biobox_cli.container as ctn
import biobox.util          as docker

def test_create_container_with_no_volumes():
    container = ctn.create("bioboxes/velvet", command="default")
    attr = docker.client().inspect_container(container)
    assert attr["Config"]["Volumes"] == None
    hlpr.remove_container(container)

def test_create_container_with_volumes():
    container = ctn.create("bioboxes/velvet", command="default", volumes=["/host:/cont:ro"])
    attr = docker.client().inspect_container(container)
    assert "/host" in attr["Config"]["Volumes"]
    hlpr.remove_container(container)
