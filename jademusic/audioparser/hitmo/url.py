from requests_html import HTMLSession


def get_hitmo_url():
    session = HTMLSession()
    response = session.get('https://gde-hitmo.org/')
    hitmo_url_html = response.html.find('a.link.link--with-badge', first=True)
    return hitmo_url_html.attrs.get('href')