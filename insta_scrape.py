import time
import re
from selenium.webdriver import Chrome


def recent_25_posts(username, post_count=25):
    """
    With the input of an account page, scrape the 25 most recent posts urls

    Args:
    username: Instagram username
    post_count: default of 25, set as many or as few as you want

    Returns:
    A list with the unique url links for the 25 most recent posts for the provided user
    """
    url = "https://www.instagram.com/" + username + "/"
    browser = Chrome().get(url)
    post = 'https://www.instagram.com/p/'
    post_links = []
    while len(post_links) < post_count:
        links = [a.get_attribute('href')
                 for a in browser.find_elements_by_tag_name('a')]
        for link in links:
            if post in link and link not in post_links:
                post_links.append(link)
        scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
        browser.execute_script(scroll_down)
        time.sleep(10)
    else:
        return post_links[:post_count]


def insta_details(urls):
    """
    Take a post url and return post details

    Args:
    urls: a list of urls for Instagram posts 

    Returns:
    A list of dictionaries with details for each Instagram post, including link,
    like/view count, age (when posted), and initial comment
    """
    browser = Chrome()
    post_details = []
    for link in urls:
        browser.get(link)
        try:
            # This captures the standard like count.
            likes = browser.find_element_by_partial_link_text(' likes').text
        except:
            # This captures the like count for videos which is stored
            view_id = '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/span'
            likes = browser.find_element_by_xpath(view_id).text
        age = browser.find_element_by_css_selector('a time').text
        xpath_c = '//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/li[1]/div/div/div'
        comment = browser.find_element_by_xpath(xpath_c).text
        post_details.append(
            {'link': link, 'likes/views': likes, 'age': age, 'comment': comment})
        time.sleep(10)
    return post_details


def find_hashtags(comment):
    """
    Find hastags used in comment and return them

    Args:
    comment: Instagram comment text

    Returns:
    a list of all hashtags found in the given comment
    """
    hashtags = re.findall('#[A-Za-z]+', comment)
    return hashtags
