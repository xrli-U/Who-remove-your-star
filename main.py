import requests
import re
import os
from datetime import datetime
import time
import argparse

def get_args():
    parser = argparse.ArgumentParser(description='monitor')
    parser.add_argument('--user', type=str, default=None, help='username')
    parser.add_argument('--repo', type=str, default=None, help='repository')
    parser.add_argument('--website', type=str, default=None, help='website')
    args = parser.parse_args()
    return args

def get_date():
    now = datetime.now()
    year = now.year
    month = now.month
    if month < 10:
        month = '0' + str(month)
    day = now.day
    if day < 10:
        day = '0' + str(day)
    hour = now.hour
    if hour < 10:
        hour = '0' + str(hour)
    minute = now.minute
    if minute < 10:
        minute = '0' + str(minute)
    return '{}-{}-{}-{}-{}'.format(year, month, day, hour, minute)

def save_log(removed_Stargazers, added_Stargazers, Stargazers_save):
    date = get_date()
    save_name = os.path.join(Stargazers_save, 'monitor.txt')
    with open(save_name, 'a') as file:
        file.write(date + '\n')
        if len(removed_Stargazers):
            file.write('removed stars: ')
            for item in removed_Stargazers:
                file.write(item + ', ')
            file.write('\n')
        if len(added_Stargazers):
            file.write('giving stars: ')
            for item in added_Stargazers:
                file.write(item + ', ')
            file.write('\n')
        file.write('-'*20 + '\n')

def save_txt(Stargazers, Stargazers_save):
    date = get_date()
    save_name = date + '.txt'
    print('save in {}...'.format(os.path.join(Stargazers_save, save_name)))
    with open(os.path.join(Stargazers_save, save_name), 'w') as file:
        for item in Stargazers:
            file.write(item + '\n')

def load_txt(txt_name):
    with open(txt_name, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines

def main(user, repo):
    Stargazers_save = './stargazers/{}/{}'.format(user, repo)
    os.makedirs(Stargazers_save, exist_ok=True)
    ini_page = 1
    Stargazers = []
    while True:
        url = "https://github.com/{}/{}/stargazers?page={}".format(user, repo, ini_page)
        ini_page += 1
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            # print(html_content)
        else:
            print("Failed to retrieve data:", response.status_code)
        pattern = r'data-hovercard-url="(/users/[^/]+/hovercard)"'
        matches = re.findall(pattern, html_content)
        if len(matches) == 1:
            break
        Stargazers_page = []
        matches = [match.split('/')[-2] for match in matches]
        for match in matches:
            if match not in Stargazers_page and match != user:
                Stargazers_page.append(match)
        Stargazers.extend(Stargazers_page)

    if len(os.listdir(Stargazers_save)) == 0:
        save_txt(Stargazers, Stargazers_save)
    else:
        latest_txt = sorted(os.listdir(Stargazers_save))
        if 'monitor.txt' in latest_txt:
            latest_txt.remove('monitor.txt')
        latest_txt = os.path.join(Stargazers_save, latest_txt[-1])
        latest_Stargazers = load_txt(latest_txt)
        Stargazers_ = set(Stargazers)
        latest_Stargazers_ = set(latest_Stargazers)
        removed_Stargazers = latest_Stargazers_ - Stargazers_
        added_Stargazers = Stargazers_ - latest_Stargazers_
        if len(removed_Stargazers) == 0:
            # print('No one removed the star.')
            pass
        else:
            removed_Stargazers_ = ', '.join(removed_Stargazers)
            print(removed_Stargazers_ + ' removed stars.')
        if len(added_Stargazers) == 0:
            # print('No one gave you star.')
            pass
        else:
            added_Stargazers_ = ', '.join(added_Stargazers)
            print(added_Stargazers_ + ' gave you stars.')
        if len(removed_Stargazers) != 0 or len(added_Stargazers) != 0:
            save_txt(Stargazers, Stargazers_save)
            save_log(removed_Stargazers, added_Stargazers, Stargazers_save)

if __name__ == '__main__':
    args = get_args()
    if args.website is None:
        if args.user is None or args.repo is None:
            assert f"error..."
        else:
            user = args.user
            repo = args.repo
    else:
        user = args.website.split('/')[-2]
        repo = args.website.split('/')[-1]
    while True:
        main(user, repo)
        time.sleep(3600)

# python main.py --user xrli-U --repo MuSc
# python main.py --website https://github.com/xrli-U/MuSc
