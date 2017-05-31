from lxml import html
import requests

import urllib.request, shutil, os, re, time


def clean_up_name(bird_name: str):
    return re.sub('[^0-9a-zA-Z]+', '_', bird_name)


def download_clip(bird_name, clip_no):
    bird_name = clean_up_name(bird_name)

    if bird_name == 'Western_Wood_Pewee':
        return

    file_name = bird_name + "___" + clip_no + ".mp3"
    url = "http://animalrecordings.org/Audio/Audio1/{}/{}.mp3".format(str(clip_no)[0:2], clip_no)

    print("Downloading ({}) - {}".format(file_name, url))


    if not os.path.isfile(file_name):
        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        print("\tDownloading complete " + os.getcwd() + "/" + file_name)
    else:
        print("Skipping existing version of {}/{}".format(bird_name, file_name))



def get_url(page_no):
    base_url = "https://macaulaylibrary.org/search?&asset_format_id=1000&collection_type_id=1&layout=1&output=1&sort=7&country_name=United+States"
    return base_url + "&page={}".format(page_no)


def download_page(page_no):
    url = get_url(page_no)

    print("Downloading page number {} with {}".format(page_no, url))

    page = requests.get(url)
    # print(page.content)
    tree = html.fromstring(page.content)
    # print(tree)
    _clips = tree.xpath('//a[contains(@href,"audio/")]/text()')
    _names = tree.xpath('//div[contains(@class,"search-row")]/div[contains(@class,"subject")]/h4/text()')
    # _genus = tree.xpath('//div[contains(@class,"search-row")]/div[contains(@class,"subject")]/h4/div/text()')
    audio_clips = [x.strip() for x in _clips if x != "\n"]
    names = [x.strip() for x in _names if x != "\n"]
    # genus = [x.strip() for x in _genus if x != "\n"]

    for i in range(len(audio_clips)):
        clip = audio_clips[i]
        name = names[i]

        try:
            time.sleep(2.7)
            dir_name = name
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

            os.chdir(dir_name)
            download_clip(name, clip)
            os.chdir('..')

        except Exception as e:
            print(e)
            pass


def main():
    os.chdir('downloads')
    for i in range(85, 1000):
        download_page(i)
    os.chdir('..')


main()


# for clip in audio_clips:
