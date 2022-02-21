import requests


def get_lines(url):
    response = requests.get(url)
    assert response.status_code == 200, 'Wrong status code'
    # print response.content

    lines = [x.decode() for x in response.content.splitlines()[1:]]

    return lines
